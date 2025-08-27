# scripts/generate_flashcards.py
# This script provides a command-line interface to generate training data ("flashcards")
# for the Sapient AI model by calling an LLM like OpenAI's GPT-4o.

main
import os
import sys
import json
import argparse
import time
import hashlib
import copy
import openai
import jsonschema

# Add the project root to the Python path to allow importing from 'common'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from common.secrets import get_secret
except Exception:
    # Fallback: environment variable
    def get_secret(k):
        return os.environ.get(k)

# --- 1. Define the JSON Schema (as provided by the user) ---
FLASHCARD_SCHEMA = {
  "type":"object",
  "required":["input","output","meta"],
  "properties":{
    "input":{
      "type":"object",
      "required":["scenario","jurisdiction","goals"],
      "properties":{
        "scenario":{"type":"string"},
        "jurisdiction":{"type":"string","enum":["za","uk","us","mu","de","ae"]},
        "goals":{"type":"array","items":{"type":"string","enum":["liability_protection","asset_protection","international_trade","tax_efficiency"]}},
        "assumptions":{"type":"string"},
        "constraints":{"type":"string"}
      }
    },
    "output":{
      "type":"object",
      "required":["recommended_structures"],
      "properties":{
        "recommended_structures":{"type":"array","items":{"type":"string","enum":["za_pty_ltd","za_trust","mu_ibc"]}},
        "policy_refs":{"type":"string"}
      }
    },
    "meta":{
      "type":"object",
      "required":["subsection","difficulty","source_prompt_id","rationale","version"],
      "properties":{
        "subsection":{"type":"string","enum":["za_simple_liability","za_simple_asset_protection","intl_simple_trade","intl_simple_tax","za_hybrid_full","za_edge_cases"]},
        "difficulty":{"type":"string","enum":["simple","complex","edge"]},
        "version":{"type":"string"}
      }
    }
  }
}

# --- Helper utilities ---

def normalized_hash_for_flashcard(flashcard):
    """
    Create a stable hash for deduplication using normalized input and output.
    Normalization rules:
      - lowercase jurisdiction
      - sort goals
      - remove extra whitespace in strings
      - sort keys for predictable ordering
    """
    obj = {
        "input": {},
        "output": {}
    }

    inp = flashcard.get("input", {})
    out = flashcard.get("output", {})

    # Normalize input
    inp_norm = {}
    scenario = inp.get("scenario", "").strip()
    inp_norm["scenario"] = " ".join(scenario.split())
    jurisdiction = inp.get("jurisdiction", "")
    inp_norm["jurisdiction"] = jurisdiction.strip().lower()
    goals = inp.get("goals", [])
    if isinstance(goals, list):
        goals_norm = sorted([g.strip().lower() for g in goals])
    else:
        goals_norm = [str(goals).strip().lower()]
    inp_norm["goals"] = goals_norm
    inp_norm["assumptions"] = " ".join(str(inp.get("assumptions", "")).split())
    inp_norm["constraints"] = " ".join(str(inp.get("constraints", "")).split())

    # Normalize output
    out_norm = {}
    rec = out.get("recommended_structures", [])
    if isinstance(rec, list):
        rec_norm = sorted([r.strip().lower() for r in rec])
    else:
        rec_norm = [str(rec).strip().lower()]
    out_norm["recommended_structures"] = rec_norm
    out_norm["policy_refs"] = " ".join(str(out.get("policy_refs", "")).split())

    obj["input"] = inp_norm
    obj["output"] = out_norm

    # canonical json string
    canon = json.dumps(obj, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
    h = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    return h

def safe_json_loads(line):
    try:
        return json.loads(line)
    except Exception:
        return None

def validate_flashcard(flashcard_json):
    """
    Validates a single JSON object against the FLASHCARD_SCHEMA.
    """
    try:
        jsonschema.validate(instance=flashcard_json, schema=FLASHCARD_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"WARNING: Schema validation failed: {e.message}")
        return False
    except Exception as e:
        print(f"WARNING: Validation unexpected error: {e}")
        return False

# --- 2. Function to Call the LLM (with retry/backoff) ---
def generate_from_llm(prompt, api_key, temperature=0.7, max_retries=3, retry_backoff=2):
    """
    Calls the OpenAI API with a given prompt to generate flashcards.
    Retries on transient failures with exponential backoff.
    Returns the raw string output (could be NDJSON).
    """
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            print(f"INFO: Calling OpenAI API (attempt {attempt})...")
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a structured dataset generator. You only output valid, newline-delimited JSON (NDJSON) objects conforming to the user's requested schema. Do not output any other text, explanations, or markdown formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
            )
            # compatible with responses that may return in different shapes
            content = None
            if hasattr(response, "choices") and len(response.choices) > 0:
                # some SDK versions return a message object
                msg = response.choices[0].message
                if isinstance(msg, dict) and "content" in msg:
                    content = msg["content"]
                elif hasattr(msg, "content"):
                    content = msg.content
            # fallback
            if content is None:
                # Try direct attribute
                content = getattr(response, "text", None) or str(response)
            print("INFO: OpenAI API call successful.")
            return content
        except Exception as e:
            print(f"ERROR: OpenAI API call failed on attempt {attempt}: {e}")
            if attempt >= max_retries:
                print("ERROR: Max retries reached. Returning empty output.")
                return ""
            sleep_time = retry_backoff ** attempt
            print(f"INFO: Retrying after {sleep_time}s...")
            time.sleep(sleep_time)
    return ""

# --- 3. Main orchestration with batching, dedupe, and write-out ---
def main():
    parser = argparse.ArgumentParser(description="Generate AI training flashcards using an LLM (patched).")
    parser.add_argument("--prompt", type=str, required=True, help="The full text of the prompt to send to the LLM.")
    parser.add_argument("--output-file", type=str, required=True, help="The path to save the output NDJSON file (written at the end).")
    parser.add_argument("--api-key", type=str, default=None, help="OpenAI API key. If not provided, it will be fetched from secrets or env.")
    parser.add_argument("--count", type=int, default=50, help="Total desired number of unique flashcards to produce (default: 50).")
    parser.add_argument("--batch-size", type=int, default=50, help="How many flashcards to ask the LLM for per call (default: 50).")
    parser.add_argument("--temperature", type=float, default=0.7, help="LLM temperature (default 0.7).")
    parser.add_argument("--max-attempts", type=int, default=50, help="Maximum number of batches attempts before giving up.")
    parser.add_argument("--append", action="store_true", help="Append to output-file if it exists (default behaviour is overwrite).")
    parser.add_argument("--dry-run", action="store_true", help="Validate prompt/schema locally without calling the LLM.")
    parser.add_argument("--max-retries", type=int, default=3, help="Retries per LLM call on API errors.")
    parser.add_argument("--retry-backoff", type=int, default=2, help="Base backoff multiplier for retries (seconds).")
    args = parser.parse_args()

    print("INFO: Starting patched flashcard generation.")
    print(f"INFO: Desired unique cards: {args.count}, batch size: {args.batch_size}")

    api_key = args.api_key or get_secret("OPENAI_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: OpenAI API key not found. Provide with --api-key or set OPENAI_API_KEY secret.")
        sys.exit(1)

    # If dry-run, just validate the prompt contains NDJSON instructions (light heuristic)
    if args.dry_run:
        print("DRY RUN: Checking prompt heuristics...")
        required_phrases = ["newline-delimited", "NDJSON", "one JSON object per line", "do not output"]
        missing = [p for p in required_phrases if p.lower() not in args.prompt.lower()]
        if missing:
            print(f"DRY RUN WARNING: Prompt is missing guidance phrases: {missing}")
        else:
            print("DRY RUN: Prompt contains NDJSON guidance (heuristic).")
        print("DRY RUN: Exiting (no LLM call).")
        sys.exit(0)

    unique_map = {}  # hash -> flashcard object
    invalid_count = 0
    duplicate_count = 0
    total_received = 0
    attempts = 0

    # If output exists and append mode, pre-load existing hashes to avoid duplicates
    if args.append and os.path.exists(args.output_file):
        print(f"INFO: Append mode: loading existing file {args.output_file} to avoid duplicates.")
        with open(args.output_file, 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.strip()
                if not line:
                    continue
                obj = safe_json_loads(line)
                if obj and validate_flashcard(obj):
                    h = normalized_hash_for_flashcard(obj)
                    unique_map[h] = obj

    # Main loop: request batches until we have enough unique cards or hit max attempts
    while len(unique_map) < args.count and attempts < args.max_attempts:
        attempts += 1
        print(f"\n--- Batch attempt {attempts} --- (have {len(unique_map)}/{args.count} unique)")

        # Ensure the prompt requests the desired number per batch to help the model
        batch_prompt = args.prompt.strip() + f"\n\nProduce exactly {args.batch_size} newline-delimited JSON (NDJSON) objects that conform to the schema provided. Output one JSON object per line and nothing else."

        raw_output = generate_from_llm(batch_prompt, api_key, temperature=args.temperature, max_retries=args.max_retries, retry_backoff=args.retry_backoff)
        if not raw_output:
            print("WARNING: Empty output from LLM for this batch; continuing to next attempt.")
            continue

        # Split lines, parse JSON, validate, dedupe
        lines = [l for l in raw_output.splitlines() if l.strip()]
        print(f"INFO: LLM returned {len(lines)} non-empty lines (raw).")
        total_received += len(lines)

        for line in lines:
            parsed = safe_json_loads(line)
            if parsed is None:
                print(f"INFO: Skipping non-JSON line: {line[:200]}")
                invalid_count += 1
                continue

            # check for error object pattern
            if isinstance(parsed, dict) and "error" in parsed and parsed.get("error", "").startswith("invalid_jurisdiction"):
                print(f"WARNING: LLM reported invalid jurisdiction value: {parsed.get('value')}")
                continue

            # validate
            if not validate_flashcard(parsed):
                invalid_count += 1
                continue

            # dedupe by normalized hash
            h = normalized_hash_for_flashcard(parsed)
            if h in unique_map:
                duplicate_count += 1
                continue

            unique_map[h] = parsed
            print(f"INFO: Accepted new flashcard (unique count now {len(unique_map)})")

            # break early if we've reached count
            if len(unique_map) >= args.count:
                print("INFO: Reached desired unique card count.")
                break

        # small cooldown to avoid rate limit bursts
        time.sleep(0.5)

    # Write out results
    write_mode = 'a' if args.append else 'w'
    os.makedirs(os.path.dirname(args.output_file) or '.', exist_ok=True)
    with open(args.output_file, write_mode, encoding='utf-8') as fout:
        for h, card in unique_map.items():
            fout.write(json.dumps(card, ensure_ascii=False) + '\n')

    print("\n--- Generation Summary ---")
    print(f"Total batches attempted: {attempts}")
    print(f"Total unique flashcards written: {len(unique_map)}")
    print(f"Total raw lines received from LLM: {total_received}")
    print(f"Invalid lines skipped: {invalid_count}")
    print(f"Duplicates skipped: {duplicate_count}")
    print(f"Output file: {args.output_file}")
    if len(unique_map) < args.count:
        print("WARNING: Did not reach target count within max attempts. Increase --max-attempts or adjust batch size/temperature.")

if __name__ == '__main__':
    main()
