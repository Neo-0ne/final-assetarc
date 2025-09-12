Hello Jules,

This is a new session to continue the work from a previous chat. The goal is to perform several development and data-related tasks for the AssetArc AI platform.

### Project Background & Context

The project is an AI-powered SaaS platform for legal structuring. The core of the platform is a specialized model called the Sapient Hierarchical Reasoning Model (HRM), which is served by the `eng-reasoning` microservice for inference. The training workflow for the HRM is maintained in a public GitHub repository (`sapientinc/HRM`). The platform's future architecture is a multi-agent system, likely built using a flexible toolkit like AutoGPT's Forge, that will orchestrate the HRM and other agents (e.g., Drafting Agent, Compliance Agent) to handle complex legal workflows.

### Previous Session Summary

The previous agent session ended because the agent could not see a set of 16 Phase 3 data files that I had uploaded to the repository at `final-assetarc/generated_data/P3/`. We concluded that a new session was required to ensure you have a fresh clone of the repository containing these new files.

### Consolidated List of Tasks

Here is the complete list of tasks I need you to work on. Please create a plan that addresses these tasks.

---

#### Task 1: Verify Previously Uploaded P3 Files (Immediate Task)

This is the immediate, unresolved task from our previous session.

*   **Goal:** Verify the 16 files I uploaded to `final-assetarc/generated_data/P3/`.
*   **Verification Steps:**
    1.  Confirm that all 16 files exist at the specified path.
    2.  Confirm that each file contains at least 2000 lines.
    3.  Perform a basic structural check on one of the files to ensure it contains valid NDJSON.
*   **List of Files:**
    *   `P3_CERT_GOOD_PROMPT (2)_output.ndjson`
    *   `P3_CERT_GOOD_PROMPT_output.ndjson`
    *   `P3_CERT_INC_SEY_PROMPT (2)_output.ndjson`
    *   `P3_CERT_INC_SEY_PROMPT_output.ndjson`
    *   `P3_COMP_CHECK_PROMPT (2)_output.ndjson`
    *   `P3_COMP_CHECK_PROMPT_output.ndjson`
    *   `P3_COR14_1_PROMPT_output.ndjson`
    *   `P3_COR14_2_PROMPT_output.ndjson`
    *   `P3_COR15_2_PROMPT_output.ndjson`
    *   `P3_COR39_PROMPT_output.ndjson`
    *   `P3_COURSE_CERT_PROMPT_output.ndjson`
    *   `P3_DIR_CONSENT_IBC_PROMPT_output.ndjson`
    *   `P3_DIR_CONSENT_PROMPT_output.ndjson`
    *   `P3_DOCGEN_INV_PROMPT_output.ndjson`
    *   `P3_DOC_ENGINE_PROMPT_output.ndjson`
    *   `P3_DRAFT_COVER_PROMPT_output.ndjson`

---

#### Task 2: Train the Sapient HRM Model

*   **Objective:** Your task is to train the Sapient Hierarchical Reasoning Model (HRM) using a newly provided set of training data.
*   **Background:** We are developing an AI-powered SaaS platform that relies on a core model, the Sapient HRM, which is served by our eng-reasoning microservice. The official training code for the HRM is not in this local repository; it is maintained in a public GitHub repository. We have a new batch of curated training data, located at `generated_data/P1_ISTAX_01_output.ndjson`, which we need to use to train a new version of the model. The primary challenge is that our data format will not match the format expected by the public training scripts. Your main job is to bridge this gap and launch the training process.
*   **Step-by-Step Task:**
    1.  **Analyze the Training Repository:**
        *   Thoroughly investigate the public HRM training repository: https://github.com/sapientinc/HRM.
        *   Your primary goal is to determine the exact data format required by the `pretrain.py` script.
        *   Pay close attention to the scripts in the `dataset/` directory (e.g., `build_sudoku_dataset.py`, `build_arc_dataset.py`) and the `README.md` to understand the data structures and file formats the training pipeline expects.
    2.  **Create a Data Conversion Script:**
        *   The provided data at `generated_data/P1_ISTAX_01_output.ndjson` is in a generic NDJSON format. It will not work with the training script out-of-the-box.
        *   You must write a new Python script (`scripts/convert_training_data.py`) that reads our NDJSON file and transforms its contents into the specific format and directory structure required by the HRM training pipeline.
    3.  **Set Up the Training Environment:**
        *   Prepare the environment to run the training. This will likely involve creating a new virtual environment.
        *   Install all Python dependencies from the `requirements.txt` file found in the public `sapientinc/HRM` repository. Be prepared to handle complex dependencies like PyTorch and CUDA, as specified in their `README.md`.
    4.  **Launch the Training:**
        *   Once the data has been converted and the environment is set up, execute the `pretrain.py` script to begin training the model.
        *   You will need to adapt the example training commands from the repository's `README.md` to point to your newly converted dataset and configure any other relevant hyperparameters.
*   **Acceptance Criteria:** The task is complete when you have successfully started the `pretrain.py` script and can confirm that it is running and actively training on the converted dataset.

---

#### Task 3: Create Advanced QC and Auto-Correction Script

*   **Objective:** Create an advanced Quality Control (QC) and Auto-Correction script for our Phase 1 (`P1_*.ndjson`) data files, with the goal of minimizing human review time.
*   **Background:** Our current QC process requires a human to manually fix every detected error. We want to evolve this into a system that automatically corrects what it can and intelligently flags only the most complex issues. This script will be the first version of this "Smarter Validator."
*   **Step-by-Step Task:**
    1.  **Build the Advanced QC Script:**
        *   Create a Python script named `scripts/advanced_qc_phase1.py`.
        *   The script will read all files in `generated_data/` matching `P1_*.ndjson`.
        *   For each file it processes, it will create a new, corrected file named `[original_name]_corrected.ndjson`.
    2.  **Implement Auto-Correction (Business Logic):**
        *   For each record, validate it against the business logic rules in `prompts/P1_REV_01.txt`.
        *   If a record fails this check, automatically replace the incorrect `output.recommended_structures` with the correct value and write the corrected record to the `_corrected.ndjson` file. Log this action in your report.
    3.  **Implement Intelligent Flagging (Content Safety):**
        *   For each record, validate it against the content safety rules in `prompts/P1_REV_02.txt`.
        *   When a safety violation is found, copy the original, uncorrected record to the `_corrected.ndjson` file but add a new top-level key: `"qc_flags": [{"type": "content_safety", "details": "Found potential PII"}]`.
    4.  **Generate a Comprehensive Report:**
        *   At the end of the run, print a summary report to the console detailing what was done, including files processed, total records checked, errors auto-corrected, and issues flagged per file.
*   **Acceptance Criteria:**
    *   A functional script, `scripts/advanced_qc_phase1.py`.
    *   When run, it produces `_corrected.ndjson` files containing data that is free of business logic errors.
    *   Any records with potential safety issues in the corrected files are clearly marked with a `qc_flags` field.
    *   A clear summary report is printed to the console.

---

#### Task 4: Perform Prompt Sufficiency & Gap Analysis

*   **Objective:** Analyze the entire project to determine if our current data generation prompts (for Phases 1, 2, and 3) are sufficient to train the HRM on all of its required capabilities. Your final output should be a detailed "Gap Analysis" report.
*   **Background:** We need a thorough audit to ensure that our prompts are generating data for every scenario, document, and rule the final application is expected to handle.
*   **Step-by-Step Task:**
    1.  **Map All Required System Capabilities:**
        *   Build a comprehensive map of every document, structure, and scenario the system must be able to generate or reason about.
        *   Key sources of truth: `prompts/DEFINITIVE_DOCUMENT_LIST_COMBINED.md`, `prompts/DOCUMENT_MASTER_LIST.md`, filenames in `Services/eng-drafting/templates/`, and business logic in `Services/eng-compliance/app/`.
    2.  **Map Current Prompt Coverage:**
        *   Map all scenarios our current data generation prompts are designed to cover by parsing all prompts in `prompts/P1_*.txt`, `prompts/P2_*.txt`, and `prompts/P3_document_clauses/*.txt`.
    3.  **Generate a Gap Analysis Report:**
        *   Compare the "Required Capabilities" map with the "Current Prompt Coverage" map.
        *   Identify every capability that is required but is not covered by an existing data generation prompt.
        *   Present your findings in a clear, human-readable markdown report, citing the source of the requirement for each gap.
*   **Acceptance Criteria:** A detailed gap analysis report that identifies specific, actionable areas where our data generation strategy is insufficient.

---

#### Task 5: Execute Full Training Data Generation for Phases 1, 2, and 3

*   **Objective:** Generate the complete training dataset for all phases of our AI models.
*   **Phase 1: General Flashcard Generation**
    1.  Execute the Phase 1 generation script using `scripts/run_generation.sh` for all `P1_*.txt` prompts.
    2.  Verify that for each prompt, a corresponding `_output.ndjson` file is created in `generated_data/`.
*   **Phase 2: Rollover and Residency Planner Generation**
    1.  Execute the Phase 2 generation script using `scripts/run_generation_phase2.sh` for all `P2_*.txt` prompts.
    2.  Verify that for each prompt, a corresponding `_output.ndjson` file is created in `generated_data/`.
*   **Phase 3: Document Clause Generation**
    1.  Identify and execute the correct generation script for all prompts in `prompts/P3_document_clauses/`.
    2.  Verify that `document_clause_library.ndjson` is created in `generated_data/` and is not empty.
*   **Reporting:** For each phase, report on completion and list the files that were generated.

---

### Key Resources
*   **Official Training Repository:** https://github.com/sapientinc/HRM
*   **Core Training Script:** `pretrain.py` (in public repo)
*   **Your Training Data:** `generated_data/P*/` directories
*   **Master Document Lists:** `prompts/DEFINITIVE_DOCUMENT_LIST_COMBINED.md`, `prompts/DOCUMENT_MASTER_LIST.md`
*   **Final Output Templates:** Files in `Services/eng-drafting/templates/`
*   **Compliance Logic:** Python files in `Services/eng-compliance/app/`
