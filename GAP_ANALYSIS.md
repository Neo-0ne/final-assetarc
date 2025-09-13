# Prompt Sufficiency & Gap Analysis Report

## 1. Overview

This report analyzes the sufficiency of the existing data generation prompts (Phases 1, 2, and 3) against the required capabilities of the AssetArc platform. The analysis was conducted by mapping all required system capabilities and comparing that map to the coverage provided by the current prompts.

**Overall Finding:** The current data generation strategy is highly comprehensive. There is a clear and direct mapping from the core reasoning capabilities in the `eng-compliance` service to the Phase 2 prompts, and near-complete coverage for document clause generation in Phase 3. The single identified gap is minor and represents an opportunity for refinement rather than a significant omission.

---

## 2. Required System Capabilities

The system's required capabilities were mapped from the following sources:
*   **Core Documents:** `prompts/P3_document_clauses/DEFINITIVE_DOCUMENT_LIST_COMBINED.md`
*   **Implemented Templates:** Files within `Services/eng-drafting/templates/`
*   **Compliance & Reasoning Logic:** Python scripts within `Services/eng-compliance/app/`, including:
    *   `bbee.py`: B-BBEE ownership scorecard calculations.
    *   `estate_calculator.py`: Estate duty and executor fee calculations, including the impact of trusts.
    *   `insurance_wrapper_calculator.py`: Tax benefit analysis of insurance wrappers vs. direct investment.
    *   `residency_planner.py`: South African tax residency determination (Ordinary Residence, Physical Presence, and Exit Rule).
    *   `rollover_planner.py`: Eligibility and tax impact analysis for corporate rollover relief (Sections 42, 45, 46, 47).

---

## 3. Current Prompt Coverage

The existing prompts provide excellent coverage for the mapped requirements:

*   **Phase 1 Prompts (`prompts/P1_Prompts/`):** Cover foundational, flashcard-style knowledge generation.
*   **Phase 2 Prompts (`prompts/P2_Prompts/`):** Directly map to the compliance calculators. For each major function in the `eng-compliance` service (e.g., Rollover, Residency), there are specific prompts designed to generate data for its various scenarios (e.g., `P2_ROLL_S42_ELIGIBLE.txt`, `P2_RES_NON_RESIDENT.txt`).
*   **Phase 3 Prompts (`prompts/P3_document_clauses/`):** Provide extensive coverage for generating clauses for the specific legal and business documents required by the system.

---

## 4. Identified Gap & Recommendation

The following is a minor gap where prompt coverage could be enhanced to ensure the HRM is trained on all nuanced scenarios.

### Gap 1: Missing Prompts for Specific Rollover Relief Scenarios Involving "Boot"

*   **Description:** The `rollover_planner.py` script contains logic for calculating the tax impact of "boot" (non-share consideration like cash or assumed debt) in Section 42 and Section 45 transactions. While there are prompts for general eligibility, there are no dedicated prompts to generate data specifically for transactions involving "boot". This means the model may not be adequately trained on how to calculate the partial tax liability that arises in these common scenarios.
*   **Requirement Source:** `Services/eng-compliance/app/rollover_planner.py` (specifically the `calculate_tax_impact` function).
*   **Recommendation:** Create two new P2 prompts to generate scenarios where "boot" is a factor. This will ensure the model learns to handle these specific tax calculations correctly.
    *   **Proposed New File 1:** `prompts/P2_Prompts/P2_ROLL_S42_WITH_BOOT_PROMPT.txt`
    *   **Proposed New File 2:** `prompts/P2_Prompts/P2_ROLL_S45_WITH_BOOT_PROMPT.txt`
