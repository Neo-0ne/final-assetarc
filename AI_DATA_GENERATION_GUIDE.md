# AI Data Generation System: User Guide

## 1. Overview

This guide explains how to use the automated system to generate the training data ("flashcards") required for training the Sapient AI model.

The system consists of two main parts:
*   **A Prompt Library (`prompts/`):** A collection of text files, each containing a specific, detailed prompt for generating a batch of flashcards.
*   **A Generation Script (`scripts/generate_flashcards.py`):** A Python tool that takes a prompt and generates the data by calling the OpenAI API.
*   **An Automation Script (`scripts/run_generation.sh`):** The "easy button" that runs the generation script for all available prompts.

## 2. Prerequisites

Before you begin, please ensure you have the following:
1.  **Python 3.8+** installed on your system.
2.  All required Python packages installed. If you haven't done so, run this command from the repository root:
    ```bash
    pip install -r scripts/requirements.txt
    ```
3.  An **OpenAI API Key**. You must provide this key to the script for it to work.

## 3. How to Generate the Full Dataset (Recommended Method)

This method will run all the prompts in the `prompts/` directory and is the easiest way to generate the complete dataset for a phase.

**Step 1: Set Your OpenAI API Key**
The script needs your API key. The most secure way to provide it is by setting an environment variable in your terminal:
```bash
export OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
```
*(Note: This key will only be set for your current terminal session.)*

**Step 2: Run the Automation Script**
From the root directory of the repository, run the following command:
```bash
./scripts/run_generation.sh
```

**Step 3: Find Your Data**
The script will execute for several minutes as it calls the AI for each prompt file. You will see progress messages in your terminal.

When it's finished, all the generated data will be neatly organized in the `generated_data/` directory. Each prompt will have its own output file (e.g., `P1_ZSL_01_output.ndjson`).

## 4. How to Generate Data from a Single Prompt (Advanced)

If you want to test a single prompt or a new custom prompt, you can run the Python script directly.

**Step 1: Get the Prompt Text**
Copy the entire text from one of the files in the `prompts/` directory.

**Step 2: Run the Python Script**
Execute the following command in your terminal, pasting the prompt text inside the quotes.

```bash
python scripts/generate_flashcards.py \
  --prompt "PASTE THE ENTIRE PROMPT TEXT HERE" \
  --output-file "generated_data/my_custom_run.ndjson" \
  --api-key "sk-YourSecretKeyGoesHere"
```
*(Note: Using the `--api-key` argument here is an alternative to setting the environment variable.)*

## 5. Next Steps

After generating the data, the most critical phase begins: **Expert Review**. Every single line in the output files must be reviewed and approved by a human legal/financial expert before the data can be used to train the AI model.
