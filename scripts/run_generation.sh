#!/bin/bash

# A master script to automate the generation of the entire training dataset for all phases.
# It identifies prompts from P1, P2, and P3 directories and runs the
# corresponding Python generation script for each.

# Ensure the script is run from the repository root
if [ ! -d "scripts" ] || [ ! -d "prompts" ]; then
    echo "ERROR: This script must be run from the root of the repository."
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p generated_data

echo "--- Starting AI Training Data Generation ---"

# --- Phase 1: Corporate Structuring ---
echo "--- Running Phase 1 Prompts ---"
for prompt_file in prompts/P1_Prompts/P1_*.txt; do
    if [ -f "$prompt_file" ]; then
        prompt_id=$(basename "$prompt_file" .txt)
        echo "INFO: Running P1 generator for prompt: $prompt_id"
        output_file="generated_data/${prompt_id}_output.ndjson"

        # P1 script uses --prompt-file
        python3 scripts/generate_flashcards.py \
            --prompt-file "$prompt_file" \
            --output-file "$output_file"

        echo "INFO: Generation for $prompt_id complete."
        echo "-----------------------------------------------------"
    fi
done

# --- Phase 2: Compliance Logic (Rollover & Residency) ---
echo "--- Running Phase 2 Prompts ---"
for prompt_file in prompts/P2_Prompts/P2_*.txt; do
    if [ -f "$prompt_file" ]; then
        prompt_id=$(basename "$prompt_file" .txt)
        echo "INFO: Running P2 generator for prompt: $prompt_id"
        output_file="generated_data/${prompt_id}_output.ndjson"

        # Determine the schema type from the filename
        schema_type=""
        if [[ $prompt_id == *"_ROLL_"* ]]; then
            schema_type="rollover"
        elif [[ $prompt_id == *"_RES_"* ]]; then
            schema_type="residency"
        elif [[ $prompt_id == *"_ESTATE_CALC_"* ]]; then
            schema_type="estate_calculator"
        elif [[ $prompt_id == *"_BBBEE_CALC_"* ]]; then
            schema_type="bbee_calculator"
        elif [[ $prompt_id == *"_INSURANCE_WRAPPER_CALC_"* ]]; then
            schema_type="insurance_wrapper_calculator"
        else
            echo "WARNING: Could not determine schema for P2 prompt $prompt_id. Skipping."
            continue
        fi

        python3 scripts/generate_flashcards_phase2.py \
            --prompt-file "$prompt_file" \
            --output-file "$output_file" \
            --schema-type "$schema_type"

        echo "INFO: Generation for $prompt_id complete."
        echo "-----------------------------------------------------"
    fi
done

# --- Phase 3: Document Clause Generation ---
echo "--- Running Phase 3 Prompts ---"
for prompt_file in prompts/P3_document_clauses/P3_*.txt; do
    if [ -f "$prompt_file" ]; then
        prompt_id=$(basename "$prompt_file" .txt)
        echo "INFO: Running P3 generator for prompt: $prompt_id"
        output_file="generated_data/${prompt_id}_output.ndjson"

        python3 scripts/generate_flashcards_phase3.py \
            --prompt-file "$prompt_file" \
            --output-file "$output_file" \
            --schema-type "clause_generation"

        echo "INFO: Generation for $prompt_id complete."
        echo "-----------------------------------------------------"
    fi
done


echo "--- All Data Generation Prompts Executed ---"
