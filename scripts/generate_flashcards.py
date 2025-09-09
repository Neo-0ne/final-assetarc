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
        "recommended_structures":{"type":"array","items":{"type":"string"}},
        "policy_refs":{"type": "array", "items": {"type": "string"}}
      }
    },
    "meta":{
      "type":"object",
      "required":["subsection","difficulty","source_prompt_id","version"],
      "properties":{
        "subsection":{"type":"string","enum":["za_simple_liability","za_simple_asset_protection","intl_simple_trade","intl_simple_tax","za_hybrid_full","za_edge_cases"]},
        "difficulty":{"type":"string","enum":["simple","complex","edge"]},
        "rationale":{"type":"string"},
        "version":{"type":"string"}
      }
    }
  }
}
print("--- JSON Schema defined (Line 61) ---")

# --- 2. Function to Validate a Single Flashcard ---
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


# --- 3. Function to Generate Flashcards via Streaming ---
def generate_and_write_flashcards(prompt, output_filepath, debug_filepath=None):
    """
    Calls the LLM with a prompt, streams the response, and writes valid flashcards to a file.
    """
    print(f"INFO: Calling OpenAI API with streaming...")
    raw_output_for_debug = ""
    valid_count = 0
    total_count = 0

    try:
        client = openai.OpenAI(
            base_url="http://127.0.0.1:1234/v1",
            api_key="not-needed"
        )
        stream = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": "You are a structured dataset generator. You only output valid, newline-delimited JSON (NDJSON) objects conforming to the user's requested schema. Do not output any other text, explanations, or markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            timeout=300.0,
            stream=True
        )

        print("INFO: Streaming response from LLM and writing to file...")
        buffer = ""
        with open(output_filepath, 'w') as f:
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    if debug_filepath:
                        raw_output_for_debug += content
                    buffer += content
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if not line.strip(): continue # Skip empty lines
                        total_count += 1
                        try:
                            flashcard = json.loads(line)
                            # Fallback for missing jurisdiction
                            if 'input' in flashcard and isinstance(flashcard.get('input'), dict) and 'jurisdiction' not in flashcard['input']:
                                print("INFO: 'jurisdiction' is missing. Adding default 'za'.")
                                flashcard['input']['jurisdiction'] = 'za'

                            if validate_flashcard(flashcard):
                                f.write(json.dumps(flashcard) + '\n')
                                valid_count += 1
                            else:
                                print(f"INFO: Skipping invalid flashcard (see validation warning above).")
                        except json.JSONDecodeError:
                            print(f"INFO: Skipping line with invalid JSON: {line}")

        # Process any remaining content in the buffer
        if buffer.strip():
            total_count += 1
            try:
                flashcard = json.loads(buffer)
                # Fallback for missing jurisdiction
                if 'input' in flashcard and isinstance(flashcard.get('input'), dict) and 'jurisdiction' not in flashcard['input']:
                    print("INFO: 'jurisdiction' is missing. Adding default 'za'.")
                    flashcard['input']['jurisdiction'] = 'za'

                if validate_flashcard(flashcard):
                    with open(output_filepath, 'a') as f:
                        f.write(json.dumps(flashcard) + '\n')
                    valid_count += 1
                else:
                    print(f"INFO: Skipping invalid flashcard (see validation warning above).")
            except json.JSONDecodeError:
                print(f"INFO: Skipping incomplete line at end of stream: {buffer}")

        print("\n--- Generation Complete ---")
        print(f"Total lines received from LLM: {total_count}")
        print(f"Valid flashcards written: {valid_count}")
        print(f"Output file saved at: {output_filepath}")

        if debug_filepath:
            debug_dir = os.path.dirname(debug_filepath)
            if debug_dir and not os.path.exists(debug_dir):
                os.makedirs(debug_dir)
            with open(debug_filepath, 'w') as f:
                f.write(raw_output_for_debug)
            print(f"INFO: Saved raw LLM output to debug file: {debug_filepath}")

        return True

    except Exception as e:
        print(f"ERROR: OpenAI API call failed: {e}")
        return False

print("--- generate_and_write_flashcards function defined ---")


# --- 4. Main Script Logic ---
def main():
    """
    Main function to parse arguments and trigger flashcard generation.
    """
    print("--- Main function entered ---")
    parser = argparse.ArgumentParser(description="Generate AI training flashcards using an LLM.")
    parser.add_argument("--prompt-file", type=str, required=True, help="The path to the .txt file containing the prompt.")
    parser.add_argument("--output-file", type=str, required=True, help="The path to save the output NDJSON file.")
    parser.add_argument("--debug-file", type=str, default=None, help="Optional: Path to save the raw, unfiltered output from the LLM for debugging.")
    
    args = parser.parse_args()

    print(f"INFO: Starting flashcard generation process.")
    print(f"INFO: Reading prompt from {args.prompt_file}")

    try:
        with open(args.prompt_file, 'r') as f:
            prompt_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: The prompt file was not found at '{args.prompt_file}'. Please check the path.")
        sys.exit(1)

    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"INFO: Output directory '{output_dir}' not found. Creating it now.")
        os.makedirs(output_dir)

    success = generate_and_write_flashcards(prompt_content, args.output_file, args.debug_file)

    if not success:
        print("ERROR: Flashcard generation failed. See error messages above.")
        sys.exit(1)

print("--- main function defined ---")

if __name__ == '__main__':
    print("--- __name__ is '__main__', calling main() function ---")
    main()
else:
    print(f"--- __name__ is '{__name__}', not calling main() function ---")
