# scripts/generate_flashcards.py
print("--- Script Starting: Top of file reached (Line 2) ---")

import os
import sys
import json
import argparse
import openai
import jsonschema

print("--- Imports complete (Line 11) ---")

# Add the project root to the Python path to allow importing from 'common'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.secrets import get_secret

print("--- Common module imported (Line 18) ---")

# --- 1. Define the JSON Schema (as provided by the user) ---
# This schema has been updated to accept an array for 'policy_refs' to make it more robust.
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
        "policy_refs":{"type": "array", "items": {"type": "string"}}
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
print("--- JSON Schema defined (Line 61) ---")

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

print("--- generate_from_llm function defined (Line 88) ---")

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

print("--- validate_flashcard function defined (Line 105) ---")

# --- 4. Main Script Logic ---
def main():
    """
    Main function to parse arguments, generate, validate, and save flashcards.
    """
    print("--- Main function entered ---")
    parser = argparse.ArgumentParser(description="Generate AI training flashcards using an LLM.")
    parser.add_argument("--prompt-file", type=str, required=True, help="The path to the .txt file containing the prompt.")
    parser.add_argument("--output-file", type=str, required=True, help="The path to save the output NDJSON file.")
    parser.add_argument("--api-key", type=str, default=None, help="Optional: OpenAI API key. If not provided, it will be fetched from secrets.")
    parser.add_argument("--debug-file", type=str, default=None, help="Optional: Path to save the raw, unfiltered output from the LLM for debugging.")
    
    args = parser.parse_args()

    print(f"INFO: Starting flashcard generation process.")
    print(f"INFO: Reading prompt from {args.prompt_file}")

    # Read the prompt from the specified file
    try:
        with open(args.prompt_file, 'r') as f:
            prompt_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: The prompt file was not found at '{args.prompt_file}'. Please check the path.")
        sys.exit(1)

    # Automatically create the output directory if it doesn't exist
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"INFO: Output directory '{output_dir}' not found. Creating it now.")
        os.makedirs(output_dir)

    api_key = args.api_key or get_secret("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OpenAI API key not found. Please provide it via the --api-key argument or set the OPENAI_API_KEY secret.")
        sys.exit(1)

    # Generate
    raw_output = generate_from_llm(prompt_content, api_key)

    if not raw_output:
        print("ERROR: Received no output from the LLM. Exiting.")
        sys.exit(1)

    # If a debug file path is provided, save the raw output there.
    if args.debug_file:
        debug_dir = os.path.dirname(args.debug_file)
        if debug_dir and not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        with open(args.debug_file, 'w') as f:
            f.write(raw_output)
        print(f"INFO: Saved raw LLM output to debug file: {args.debug_file}")

    # Validate and Write
    valid_count = 0
    total_count = 0
    print(f"INFO: Writing valid flashcards to {args.output_file}...")
    with open(args.output_file, 'w') as f:
        for line in raw_output.strip().split('\n'):
            total_count += 1
            try:
                flashcard = json.loads(line)
                if validate_flashcard(flashcard):
                    f.write(json.dumps(flashcard) + '\n')
                    valid_count += 1
                else:
                    print(f"INFO: Skipping invalid flashcard (see validation warning above).")
            except json.JSONDecodeError:
                print(f"INFO: Skipping line with invalid JSON: {line}")

    print("\n--- Generation Complete ---")
    print(f"Total lines received from LLM: {total_count}")
    print(f"Valid flashcards written: {valid_count}")
    print(f"Output file saved at: {args.output_file}")

print("--- main function defined (Line 196) ---")

if __name__ == '__main__':
    print("--- __name__ is '__main__', calling main() function ---")
    main()
else:
    print(f"--- __name__ is '{__name__}', not calling main() function ---")
