# AI Training Prompt Library (Phase 1: Structure Design)
# Version: 1.0
# Status: Finalized

## 1. Strategy & Specifications

This document provides a library of prompts for generating the training dataset for the Phase 1 pilot project: AI-Powered Corporate Structure Design. The following specifications are to be strictly adhered to.

### 1.1. Dataset Goal
*   **Target Volume:** ~2,000 high-quality, expert-reviewed examples.
*   **Class Balance:** The final dataset should have a roughly equal number of examples for each subsection defined in section 1.4.

### 1.2. Flashcard JSON Schema (v1.0)
All generated examples must conform exactly to this JSON schema:
```json
{
  "input": {
    "scenario": "string",
    "jurisdiction": "string (enum)",
    "goals": ["string (enum)"],
    "assumptions": ["string"],
    "constraints": ["string"]
  },
  "output": {
    "recommended_structures": ["string (enum)"],
    "policy_refs": ["string"]
  },
  "meta": {
    "subsection": "string (enum)",
    "difficulty": "simple|complex|edge",
    "source_prompt_id": "string",
    "rationale": "string",
    "version": "1.0"
  }
}
```

### 1.3. Authoritative Enums
*   **`input.jurisdiction`:** `["za", "uk", "us", "mu", "de", "ae"]` (Inputs outside this set must be rejected).
*   **`input.goals`:** `["liability_protection", "asset_protection", "international_trade", "tax_efficiency"]`.
*   **`output.recommended_structures`:** `["za_pty_ltd", "za_trust", "mu_ibc"]`.

### 1.4. Subsection Map
*   `za_simple_liability`
*   `za_simple_asset_protection`
*   `intl_simple_trade`
*   `intl_simple_tax`
*   `za_hybrid_full`
*   `za_edge_cases`

---

## 2. Prompt Library for Data Generation

**Instructions:** Use this library of small, precise prompts to generate a diverse dataset. Generate in batches of no more than 50.

### 2.1. Subsection: `za_simple_liability`
*   **Prompt ID:** P1_ZSL_01
*   **Prompt:** `Generate 50 JSON flashcards conforming to the v1.0 schema. For each, create a scenario for a small business in South Africa ('za') needing 'liability_protection'. The output must be 'za_pty_ltd'. Use a seed list of professions [plumber, electrician, consultant, bakery, coffee_shop] to ensure diversity in the 'scenario' text. Set meta.subsection to 'za_simple_liability' and meta.difficulty to 'simple'.`

### 2.2. Subsection: `za_simple_asset_protection`
*   **Prompt ID:** P1_ZSAP_01
*   **Prompt:** `Generate 50 JSON flashcards conforming to the v1.0 schema. For each, create a scenario for a high-net-worth individual in South Africa ('za') needing 'asset_protection'. The output must be 'za_trust'. Use a seed list of asset types [property, investments, art_collection, inheritance] for diversity. Set meta.subsection to 'za_simple_asset_protection' and meta.difficulty to 'simple'.`

### 2.3. Subsection: `za_hybrid_full`
*   **Prompt ID:** P1_ZHF_01
*   **Prompt:** `Generate 50 JSON flashcards conforming to the v1.0 schema for professionals in South Africa ('za') needing both 'liability_protection' and 'asset_protection'. The output must be ['za_pty_ltd', 'za_trust']. Use a seed list of professions [doctor, architect, lawyer, engineer] for diversity. Set meta.subsection to 'za_hybrid_full' and meta.difficulty to 'complex'.`

### 2.4. Subsection: `intl_simple_trade`
*   **Prompt ID:** P1_IST_01
*   **Prompt:** `Generate 50 JSON flashcards conforming to the v1.0 schema for businesses in 'uk' or 'de' needing 'international_trade'. The output must be 'mu_ibc'. Use a seed list of business types [import/export, e-commerce, software_licensing] for diversity. Set meta.subsection to 'intl_simple_trade' and meta.difficulty to 'simple'.`

---

## 3. Prompts for AI-Assisted Review

**Instructions:** These meta-prompts are for the human expert review phase to accelerate validation.

*   **Prompt ID:** P1_REV_01 (Rule Check)
*   **Prompt:** `"Based on the pre-defined project rules, does this flashcard have the correct output for its input? [Paste Generated JSON Here]. Answer Yes or No and provide a terse reason."`
*   **Prompt ID:** P1_REV_02 (Red-line Check)
*   **Prompt:** `"Does this flashcard contain any PII, invented statutes, or guarantees of financial outcomes? [Paste Generated JSON Here]. Answer Yes or No."`
