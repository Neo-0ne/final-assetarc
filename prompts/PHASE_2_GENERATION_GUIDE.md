# Phase 2 Data Generation Guide

This guide explains how to use the dedicated scripts to generate the training dataset for the Phase 2 AI models (Rollover Planner and Residency Planner).

The Phase 2 generation process uses two new scripts:
- `scripts/run_generation_phase2.sh`: A shell script to automate running all Phase 2 prompts.
- `scripts/generate_flashcards_phase2.py`: A Python script that takes a single Phase 2 prompt and generates the corresponding flashcards.

---

## 1. How to Generate the Entire Phase 2 Dataset

This is the recommended and simplest method. The `run_generation_phase2.sh` script will automatically find all `P2_*.txt` prompts in the `prompts/` directory, determine the correct schema to use, and run the generator for each one.

**Steps:**

1.  **Open your terminal** and make sure you are in the root directory of this repository.
2.  **Ensure the script is executable.** If this is the first time you are running it, you may need to give it execute permissions:
    ```bash
    chmod +x scripts/run_generation_phase2.sh
    ```
3.  **Run the script:**
    ```bash
    ./scripts/run_generation_phase2.sh
    ```

The script will print its progress to the console. Once it's finished, you will find all the generated `_output.ndjson` files inside the `generated_data/` directory.

---

## 2. How to Run a Single Phase 2 Prompt (Advanced)

If you only want to re-generate the data for a single prompt, you can call the Python script directly. This is useful for testing or debugging a specific prompt.

The Python script requires three arguments:

- `--prompt-file`: The path to the `P2_*.txt` prompt file you want to use.
- `--output-file`: The path where you want to save the generated `.ndjson` file.
- `--schema-type`: This is crucial. You must specify which validation schema to use. The valid options are `rollover` or `residency`.

**Example for a Rollover prompt:**

```bash
python3 scripts/generate_flashcards_phase2.py \
    --prompt-file "prompts/P2_ROLL_S42_ELIGIBLE.txt" \
    --output-file "generated_data/P2_ROLL_S42_ELIGIBLE_output.ndjson" \
    --schema-type "rollover"
```

**Example for a Residency prompt:**

```bash
python3 scripts/generate_flashcards_phase2.py \
    --prompt-file "prompts/P2_RES_ORD_RESIDENT.txt" \
    --output-file "generated_data/P2_RES_ORD_RESIDENT_output.ndjson" \
    --schema-type "residency"
```

**Note:** You must have your `OPENAI_API_KEY` configured for the script to work. The script will attempt to fetch it from the project's secrets manager.
