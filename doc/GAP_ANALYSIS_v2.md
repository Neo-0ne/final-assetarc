# Prompt Sufficiency & Gap Analysis Report (v2)

## 1. Introduction

This report analyzes the existing data generation prompts (Phases 1, 2, and 3) to determine if they are sufficient to train the HRM on all of its required capabilities. The analysis compares the system's required capabilities, derived from master document lists and application business logic, against the scenarios covered by the current set of prompts.

## 2. Summary of Findings

The analysis reveals a mixed landscape. The coverage for Phase 2 (Calculators) and Phase 3 (Clause Selection) is very strong, with only minor gaps. However, there are significant conceptual gaps in the Phase 1 (Structure Recommendation) prompts, which do not cover the full range of structures and goals the system is expected to handle.

*   **Phase 1 (Structure Recommendation):** **Significant Gaps Found.** The prompts do not cover the recommendation of specific offshore structures beyond a generic Mauritius IBC, nor do they address compliance-specific goals as primary drivers for structuring.
*   **Phase 2 (Calculators):** **Coverage is Excellent.** There is a clear, one-to-one mapping between the business logic in the `eng-compliance` service and the P2 data generation prompts. No gaps were found.
*   **Phase 3 (Clause Selection):** **Coverage is Near-Complete.** Almost every document listed in the `DEFINITIVE_DOCUMENT_LIST_COMBINED.md` has a corresponding P3 prompt for clause selection. No significant gaps were found.

## 3. Detailed Gap Analysis

### 3.1. Gap: Phase 1 - Structure Recommendation Prompts

The current P1 prompts are effective but limited in scope. They do not generate training data for several key scenarios and structures required by the system.

| Capability / Structure | Gap Description | Source of Requirement |
| :--- | :--- | :--- |
| **Specific Offshore Trusts** | The P1 prompts for international structuring (`P1_ISTAX_01`, `P1_IST_01`) exclusively recommend a Mauritius IBC (`mu_ibc`). There are no prompts that train the model to recommend other required offshore structures like a **BVI Trust** or a **Jersey Trust**. | `DEFINITIVE_DOCUMENT_LIST_COMBINED.md` |
| **Standalone Agreements** | The `Shareholders' Agreement` is only ever recommended as part of a complex hybrid structure (`P1_ZAC_01`). There is no prompt to train the model to recommend a standalone Shareholders' Agreement for a client who may already have their corporate entities established. | `DEFINITIVE_DOCUMENT_LIST_COMBINED.md` |
| **Compliance-Driven Goals** | The P1 prompts are based on general goals like "asset_protection" or "tax_efficiency". There are no prompts that use compliance-specific goals, such as **"Qualify for Section 42 Rollover Relief"** or **"Improve B-BBEE Score"**, as the primary input. The model is not being trained to recommend structures based on the specific outputs of the compliance calculators. | `Services/eng-compliance/app/` (all calculator files) |
| **Specific ZA Forms** | The P1 prompts do not result in recommendations for specific South African statutory forms like `COR14.2` (MOI) or `J401` (Trust Registration). While this may be an intentional design choice (P1 for high-level structure, P3 for documents), it represents a gap in training the model to connect a client need directly to a required form. | `DEFINITIVE_DOCUMENT_LIST_COMBINED.md` |

### 3.2. Gap: Phase 3 - Clause Selection Prompts

The coverage for P3 prompts is excellent. A detailed comparison of the `DEFINITIVE_DOCUMENT_LIST_COMBINED.md` against the files in `prompts/P3_document_clauses/` reveals that a dedicated prompt file exists for virtually every required document. No gaps warranting immediate action were identified.

### 3.3. Assessment: Phase 2 - Calculator Prompts

The coverage for P2 prompts is complete. For every calculator script in `Services/eng-compliance/app/`, there is a corresponding set of P2 prompts designed to generate training data for all of its logical paths (e.g., eligible, ineligible, different outcomes).

## 4. Recommendations

To address the identified gaps, the following new prompts should be created:

1.  **Create New P1 Prompts for Offshore Structures:**
    *   A prompt for recommending a **BVI Trust**, perhaps for clients prioritizing confidentiality and asset protection.
    *   A prompt for recommending a **Jersey Trust**, perhaps for clients from specific jurisdictions or with higher asset values.
2.  **Create New P1 Prompts for Compliance Goals:**
    *   A prompt where the `input.goal` is `bbee_optimization` and the `output.recommended_structures` includes entities known to be favorable for B-BBEE structures.
    *   A prompt where the `input.goal` is `s42_rollover_relief` and the scenario involves a transaction that would lead to recommending an asset-for-share structure.
3.  **Create New P1 Prompt for Standalone Agreements:**
    *   A prompt where the scenario describes a company with existing structures that now needs to formalize the relationship between its owners, leading to a recommendation of a standalone `Shareholders' Agreement`.
