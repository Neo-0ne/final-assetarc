# scripts/generate_flashcards_phase2.py
import os
import sys
import json
import argparse
import openai
import jsonschema

# Add the project root to the Python path to allow importing from 'common'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.secrets import get_secret

# --- 1. Define the JSON Schemas for Phase 2 ---

ROLLOVER_SCHEMA = {
  "type":"object",
  "required":["input","output","meta"],
  "properties":{
    "input":{
      "type":"object",
      "required":["section","asset_profile"],
      "properties":{
        "section": {"type": "string", "enum": ["s42", "s45", "s46", "s47"]},
        "taxpayer_type": {"type": "string"},
        "transferor_residency": {"type": "string"},
        "transferee_residency": {"type": "string"},
        "group_relationship": {"type": "object"},
        "consideration": {"type": "object"},
        "asset_profile": {"type": "object"},
        "continuity_flags": {"type": "object"},
        "timing_flags": {"type": "object"},
        "unbundling_details": {"type": "object"},
        "liquidation_details": {"type": "object"}
      }
    },
    "output":{
      "type":"object",
      "required":["eligibility","tax_comparison"],
      "properties":{
        "eligibility": {"type": "object"},
        "tax_comparison": {"type": "object"}
      }
    },
    "meta":{
      "type":"object",
      "required":["rationale","source_prompt_id"],
      "properties":{
        "rationale": {"type": "string"},
        "source_prompt_id": {"type": "string"}
      }
    }
  }
}

RESIDENCY_SCHEMA = {
  "type":"object",
  "required":["input","output","meta"],
  "properties":{
    "input":{
      "type":"object",
      "required":["ordinary_residence_flags","days_in_current_year","days_each_of_prev_5_years"],
      "properties":{
        "ordinary_residence_flags": {"type": "object"},
        "days_in_current_year": {"type": "number"},
        "days_each_of_prev_5_years": {"type": "array", "items": {"type": "number"}},
        "days_continuously_absent": {"type": ["number", "null"]}
      }
    },
    "output":{
      "type":"object",
      "required":["status","reasoning","advice"],
      "properties":{
        "status": {"type": "string"},
        "reasoning": {"type": "string"},
        "advice": {"type": "string"}
      }
    },
    "meta":{
      "type":"object",
      "required":["rationale","source_prompt_id"],
      "properties":{
        "rationale": {"type": "string"},
        "source_prompt_id": {"type": "string"}
      }
    }
  }
}

SCHEMA_MAP = {
    "rollover": ROLLOVER_SCHEMA,
    "residency": RESIDENCY_SCHEMA
}

# --- 2. Function to Call the LLM ---
def generate_from_llm(prompt, api_key):
    """
    Calls the OpenAI API with a given prompt to generate flashcards.
    """
    print(f"INFO: Calling OpenAI API...")
    try:
        client = openai.OpenAI(
            base_url="http://127.0.0.1:1234/v1",
            api_key="not-needed"
        )
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
def validate_flashcard(flashcard_json, schema):
    """
    Validates a single JSON object against the provided schema.
    """
    try:
        jsonschema.validate(instance=flashcard_json, schema=schema)
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
    parser = argparse.ArgumentParser(description="Generate Phase 2 AI training flashcards using an LLM.")
    parser.add_argument("--prompt-file", type=str, required=True, help="The path to the .txt file containing the prompt.")
    parser.add_argument("--output-file", type=str, required=True, help="The path to save the output NDJSON file.")
    parser.add_argument("--schema-type", type=str, required=True, choices=["rollover", "residency"], help="The type of schema to validate against ('rollover' or 'residency').")
    parser.add_argument("--api-key", type=str, default=None, help="Optional: OpenAI API key. If not provided, it will be fetched from secrets.")

    args = parser.parse_args()

    # Select the schema
    selected_schema = SCHEMA_MAP.get(args.schema_type)
    if not selected_schema:
        print(f"ERROR: Invalid schema type '{args.schema_type}'. Must be one of {list(SCHEMA_MAP.keys())}")
        sys.exit(1)

    print(f"INFO: Using schema type: {args.schema_type}")

    # Read the prompt from the specified file
    try:
        with open(args.prompt_file, 'r') as f:
            prompt_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: The prompt file was not found at '{args.prompt_file}'. Please check the path.")
        sys.exit(1)

    # Create output directory if needed
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    api_key = args.api_key or get_secret("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OpenAI API key not found.")
        sys.exit(1)

    # Generate
    raw_output = generate_from_llm(prompt_content, api_key)
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
                flashcard = json.loads(line)
                if validate_flashcard(flashcard, selected_schema):
                    f.write(json.dumps(flashcard) + '\n')
                    valid_count += 1
            except json.JSONDecodeError:
                print(f"INFO: Skipping line with invalid JSON: {line}")

    print("\n--- Generation Complete ---")
    print(f"Total lines received from LLM: {total_count}")
    print(f"Valid flashcards written: {valid_count}")

if __name__ == '__main__':
    main()
