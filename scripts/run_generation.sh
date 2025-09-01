#!/bin/bash

# A script to automate the generation of the entire Phase 1 training dataset.
# It reads each prompt file from the prompts/ directory and runs the
# Python generation script, saving the output to the generated_data/ directory.

# Ensure the script is run from the repository root
if [ ! -d "scripts" ] || [ ! -d "prompts" ]; then
    echo "ERROR: This script must be run from the root of the repository."
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p generated_data

# Fetch OpenAI API Key from secrets, or use environment variable
# Note: The Python script handles this, but we could add an explicit check here too.
if [ -z "$OPENAI_API_KEY" ]; then
    echo "INFO: OPENAI_API_KEY environment variable not set. The script will try to use the secrets manager."
fi

echo "--- Starting AI Training Data Generation ---"

# Loop through all prompt files in the prompts/ directory
for prompt_file in prompts/P1_*.txt; do
    if [ -f "$prompt_file" ]; then
        # Extract the prompt ID from the filename (e.g., P1_ZSL_01)
        prompt_id=$(basename "$prompt_file" .txt)

        echo "INFO: Running generator for prompt: $prompt_id"

        # Define the output file path
        output_file="generated_data/${prompt_id}_output.ndjson"

        # Read the prompt content from the file
        prompt_content=$(cat "$prompt_file")

        # Run the Python script
        python3 scripts/generate_flashcards.py \
            --prompt "$prompt_content" \
            --output-file "$output_file"

        echo "INFO: Generation for $prompt_id complete. Output saved to $output_file"
        echo "-----------------------------------------------------"
    fi
done

echo "--- All Data Generation Prompts Executed ---"
