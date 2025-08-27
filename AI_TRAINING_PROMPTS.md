# AI Training Prompt Library (Comprehensive)
# Version: 2.0
# Status: Finalized

## 1. Introduction

This document provides a comprehensive library of prompts for generating the training datasets for all three phases of the Sapient AI integration.

**Workflow Reminder:**
1.  **Generate:** Use the prompts below to generate a large volume of draft "flashcards" (~2,000 examples per phase). Use small batch sizes (e.g., 20-50) for higher quality.
2.  **Review:** A human legal/financial expert **must** review and approve every single generated example for accuracy.
3.  **Finalize:** An engineer will format the expert-approved data into the final JSON structure required for training.

---

## 2. Phase 1: AI-Powered Corporate Structure Design

**Goal:** Train the AI to recommend the correct corporate structure(s).
**JSON Schema:**
```json
{
  "input": { "scenario": "string", "jurisdiction": "string", "goals": ["string"] },
  "output": { "recommended_structures": ["string"] },
  "meta": { "subsection": "string", "difficulty": "string", "source_prompt_id": "string", "rationale": "string" }
}
```

### Prompt Library (Phase 1)

*   **Prompt ID: P1_ZSL_01 (Simple Liability)**
    `"Generate 50 JSON flashcards. For each, create a scenario for a small business in South Africa ('za') needing 'liability_protection'. The output must be 'za_pty_ltd'. Set meta.subsection='za_simple_liability'."`
*   **Prompt ID: P1_ZSAP_01 (Simple Asset Protection)**
    `"Generate 50 JSON flashcards. For each, create a scenario for a high-net-worth individual in South Africa ('za') needing 'asset_protection'. The output must be 'za_trust'. Set meta.subsection='za_simple_asset_protection'."`
*   **Prompt ID: P1_ZHF_01 (Hybrid)**
    `"Generate 50 JSON flashcards for professionals in South Africa ('za') needing both 'liability_protection' and 'asset_protection'. The output must be ['za_pty_ltd', 'za_trust']. Set meta.subsection='za_hybrid_full' and meta.difficulty='complex'."`
*   **Prompt ID: P1_IST_01 (International)**
    `"Generate 50 JSON flashcards for businesses in 'uk' or 'de' needing 'international_trade'. The output must be 'mu_ibc'. Set meta.subsection='intl_simple_trade'."`

---

## 3. Phase 2: AI-Powered Tax & Compliance Rulings

**Goal:** Train the AI to make complex eligibility and status determinations based on codified rules.

### 3.1 Rollover Relief Planner Prompts

**JSON Schema:** `{"input": { ...RolloverPlannerInput... }, "output": { ...eligibility_result... }}`

*   **Prompt ID: P2_RRP_01 (s42 Ineligible)**
    `"Generate 20 JSON flashcards for a Section 42 Asset-for-Share transaction that is INELIGIBLE because the 'transferee_residency' is 'non-SA'. The input must be a complete RolloverPlannerInput object reflecting this scenario. The output must be {'eligible': false, 'failed_reasons': ['The company receiving the asset (transferee) must be a South African resident.']}."`
*   **Prompt ID: P2_RRP_02 (s45 Eligible)**
    `"Generate 20 JSON flashcards for a Section 45 Intra-group transaction that IS ELIGIBLE. All conditions must be met (both parties SA resident, same_group is true, etc.). The output must be {'eligible': true, 'failed_reasons': []}."`

### 3.2 Residency Planner Prompts

**JSON Schema:** `{"input": { ...ResidencyPlannerInput... }, "output": { "status": "string", "reasoning": "string" }}`

*   **Prompt ID: P2_RP_01 (Resident by Physical Presence)**
    `"Generate 20 JSON flashcards for a person who IS a tax resident of South Africa by meeting all three conditions of the Physical Presence Test. The input must reflect this (e.g., days_in_current_year=100, days_each_of_prev_5_years=[100,120,150,200,350]). The output must be {'status': 'Resident', 'reasoning': 'You meet the requirements of the physical presence test...'}."`
*   **Prompt ID: P2_RP_02 (Non-Resident by Ordinary Test)**
    `"Generate 20 JSON flashcards for a person who IS a tax resident of South Africa by being 'Ordinarily Resident'. The input must have at least 3 of the 4 ordinary_residence_flags set to true. The output must be {'status': 'Resident', 'reasoning': 'You are considered ordinarily resident...'}."`

---

## 4. Phase 3: AI-Powered Document Blueprint Generation

**Goal:** Train the AI to generate a structured "blueprint" or "skeleton" of a legal document.
**JSON Schema:** `{"input": {"document_request": "string"}, "output": { "document_type": "string", "sections": [ {"section_title": "string", "clauses": ["string"] } ] }}`

### Prompt Library (Phase 3)

*   **Prompt ID: P3_DBP_01 (Trust Deed)**
    `"Generate a JSON document blueprint for a 'Discretionary Inter-Vivos Trust Deed' in South Africa. The output JSON should include sections for 'Parties', 'Trust Property', 'Trustee Powers', 'Beneficiaries', and 'Vesting and Termination'."`
*   **Prompt ID: P3_DBP_02 (Share Certificate)**
    `"Generate a JSON document blueprint for a 'Share Certificate' for a South African Pty Ltd. The blueprint should include sections and placeholders for 'Company Details', 'Shareholder Details', and 'Share Allotment Details' (including number and class of shares)."`
*   **Prompt ID: P3_DBP_03 (Board Resolution)**
    `"Generate a JSON document blueprint for a 'Board Resolution to Appoint a New Director'. The blueprint should include sections for 'Company Details', 'Resolution Details', 'Details of New Director', and 'Signatories'."`

---
## 5. AI-Assisted Review Prompts

*   **Prompt ID: P_REV_01 (Rule Check)**
    `"Based on the rules of the South African Physical Presence Test, does this flashcard correctly determine the residency status? [Paste Generated JSON Here]. Answer Yes or No and provide a terse reason."`
*   **Prompt ID: P_REV_02 (Red-line Check)**
    `"Does this flashcard contain any PII, invented statutes, or guarantees of financial outcomes? [Paste Generated JSON Here]. Answer Yes or No."`
