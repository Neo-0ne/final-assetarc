# scripts/generate_flashcards.py

import os
import sys
import json
import argparse
import openai
import jsonschema

# Add the project root to the Python path to allow importing from 'common'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.secrets import get_secret

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
        "goals":{"type":"array","items":{"type":"string","enum":["liability_protection","asset_protection","international_trade","tax_efficiency"]}}
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

# --- 2. Function to Call the LLM ---
def generate_from_llm(prompt, api_key):
    """
    Calls the OpenAI API with a given prompt to generate flashcards.
    """
    print(f"INFO: Calling OpenAI API...")
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a structured dataset generator. You only output valid, newline-delimited JSON (NDJSON) objects conforming to the user's requested schema. Do not output any other text, explanations, or markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        print("INFO: OpenAI API call successful.")
        return response.choices[0].message.content
    except Exception as e:
        print(f"ERROR: OpenAI API call failed: {e}")
        return ""


# --- 3. Function to Validate a Single Flashcard ---
def validate_flashcard(flashcard_json):
    """
    Validates a single JSON object against the FLASHCARD_SCHEMA.
    """
    try:
        jsonschema.validate(instance=flashcard_json, schema=FLASHCARD_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"WARNING: Schema validation failed for flashcard. Reason: {e.message}")
        return False
    except Exception as e:
        print(f"WARNING: An unexpected error occurred during validation: {e}")
        return False

# --- 4. Main Script Logic ---
def main():
    """
    Main function to parse arguments, generate, validate, and save flashcards.
    """
    parser = argparse.ArgumentParser(description="Generate AI training flashcards using an LLM.")
    parser.add_argument("--prompt", type=str, required=True, help="The full text of the prompt to send to the LLM.")
    parser.add_argument("--output-file", type=str, required=True, help="The path to save the output NDJSON file.")
    parser.add_argument("--api-key", type=str, default=None, help="Optional: OpenAI API key. If not provided, it will be fetched from secrets.")

    args = parser.parse_args()

    print(f"INFO: Starting flashcard generation process.")
    print(f"INFO: Output will be saved to {args.output_file}")

    api_key = args.api_key or get_secret("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OpenAI API key not found. Please provide it via the --api-key argument or set the OPENAI_API_KEY secret.")
        sys.exit(1)

    # Generate
    raw_output = generate_from_llm(args.prompt, api_key)

    if not raw_output:
        print("ERROR: Received no output from the LLM. Exiting.")
        sys.exit(1)

    # Validate and Write
    valid_count = 0
    total_count = 0
    with open(args.output_file, 'w') as f:
        for line in raw_output.strip().split('\n'):
            total_count += 1
            try:
                # First, check for the error case specified in the prompt design
                try:
                    potential_error = json.loads(line)
                    if "error" in potential_error and "invalid_jurisdiction" in potential_error.get("error", ""):
                        print(f"WARNING: LLM reported an invalid jurisdiction: {potential_error.get('value')}")
                        continue
                except json.JSONDecodeError:
                    pass # Not the error object we are looking for

                flashcard = json.loads(line)
                if validate_flashcard(flashcard):
                    f.write(json.dumps(flashcard) + '\n')
                    valid_count += 1
                else:
                    print(f"INFO: Skipping invalid flashcard: {line}")
            except json.JSONDecodeError:
                print(f"INFO: Skipping line with invalid JSON: {line}")

    print("\n--- Generation Complete ---")
    print(f"Total lines received from LLM: {total_count}")
    print(f"Valid flashcards written: {valid_count}")
    print(f"Output file saved at: {args.output_file}")


if __name__ == '__main__':
    main()
