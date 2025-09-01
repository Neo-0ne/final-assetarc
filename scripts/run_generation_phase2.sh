#!/bin/bash

# A script to automate the generation of the entire Phase 2 training dataset.
# It reads each P2 prompt file from the prompts/ directory and runs the
# Python generation script for Phase 2, saving the output to the generated_data/ directory.

# Ensure the script is run from the repository root
if [ ! -d "scripts" ] || [ ! -d "prompts" ]; then
    echo "ERROR: This script must be run from the root of the repository."
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p generated_data

echo "--- Starting AI Training Data Generation for Phase 2 ---"

# Loop through all P2 prompt files in the prompts/ directory
for prompt_file in prompts/P2_*.txt; do
    if [ -f "$prompt_file" ]; then
        # Extract the prompt ID from the filename (e.g., P2_ROLL_S42_ELIGIBLE)
        prompt_id=$(basename "$prompt_file" .txt)
        echo "INFO: Running generator for prompt: $prompt_id"

        # Determine the schema type from the filename
        schema_type=""
        if [[ "$prompt_id" == *"_ROLL_"* ]]; then
            schema_type="rollover"
        elif [[ "$prompt_id" == *"_RES_"* ]]; then
            schema_type="residency"
        else
            echo "WARNING: Could not determine schema type for $prompt_id. Skipping."
            continue
        fi

        echo "INFO: Detected schema type: $schema_type"

        # Define the output file path
        output_file="generated_data/${prompt_id}_output.ndjson"

        # Run the Phase 2 Python script
        python3 scripts/generate_flashcards_phase2.py \
            --prompt-file "$prompt_file" \
            --output-file "$output_file" \
            --schema-type "$schema_type"

        echo "INFO: Generation for $prompt_id complete. Output saved to $output_file"
        echo "-----------------------------------------------------"
    fi
done

echo "--- All Phase 2 Data Generation Prompts Executed ---"
