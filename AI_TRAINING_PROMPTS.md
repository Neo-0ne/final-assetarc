# AI Training Prompt Library (Phase 1: Structure Design)

This document provides a library of prompts for generating the training dataset for the **Phase 1: AI-Powered Corporate Structure Design** pilot project.

## 1. Strategy Overview

*   **Goal:** Generate ~2,000 high-quality, expert-reviewed training examples ("flashcards").
*   **Format:** All flashcards must be in a structured JSON format: `{"input": {"goals": [...], "jurisdiction": "..."}, "output": {"recommended_structures": [...]}}`.
*   **Method:** Use the diverse, specific prompts below to generate a wide range of scenarios. Do not rely on a single prompt.
*   **Workflow:**
    1.  **Generate:** Use the prompts to generate draft data.
    2.  **Review:** A human expert must review and approve every single example.
    3.  **Finalize:** An engineer will format the final, approved data for training.

---

## 2. Prompts for Data Generation

### Category A: Simple, Single-Goal Scenarios (Target: ~800 examples)

**Objective:** To build the foundation of the dataset with common, straightforward cases.

*   **Prompt 2.A.1 (ZA Liability):** `"Generate 20 scenarios of small businesses or sole proprietors in South Africa ('za') whose primary goal is 'liability_protection'. The required output is 'za_pty_ltd'. Format each as a complete JSON flashcard."`
*   **Prompt 2.A.2 (ZA Asset Protection):** `"Generate 20 scenarios of individuals or families in South Africa ('za') whose primary goal is 'asset_protection'. The required output is 'za_trust'. Format each as a complete JSON flashcard."`
*   **Prompt 2.A.3 (International Trade):** `"Generate 20 scenarios of import/export businesses based in various countries (e.g., 'us', 'uk', 'de') whose primary goal is 'international_trade'. The required output is 'mu_ibc'. Format each as a complete JSON flashcard."`
*   **Prompt 2.A.4 (Tax Efficiency):** `"Generate 20 scenarios of tech startups or digital nomads in various international jurisdictions whose primary goal is 'tax_efficiency'. The required output is 'mu_ibc'. Format each as a complete JSON flashcard."`

### Category B: Complex, Multi-Goal Scenarios (Target: ~800 examples)

**Objective:** To teach the AI how to handle more realistic scenarios where clients have multiple, overlapping needs.

*   **Prompt 2.B.1 (ZA Hybrid):** `"Generate 20 scenarios for established professionals in South Africa ('za') (e.g., doctors, architects, consultants) who require both 'liability_protection' for their practice and 'asset_protection' for their personal wealth. The required output must be a list containing both 'za_pty_ltd' and 'za_trust'. Format each as a complete JSON flashcard."`
*   **Prompt 2.B.2 (ZA International Hybrid):** `"Generate 20 scenarios for South African business owners who run a local operation but also engage in 'international_trade'. Their goals are 'liability_protection' and 'international_trade'. The required output must be a list containing both 'za_pty_ltd' and 'mu_ibc'. Format each as a complete JSON flashcard."`

### Category C: Edge Cases & Nuances (Target: ~400 examples)

**Objective:** To make the AI more robust by training it on less common but important scenarios.

*   **Prompt 2.C.1 (Non-Profit):** `"A non-profit organization in South Africa ('za') wants to protect its operational assets. What is the most appropriate structure? Based on legal best practices, this is often a 'za_trust'. Please generate 5 flashcards for different types of non-profits (e.g., animal shelter, community center) with this input and output format."`
*   **Prompt 2.C.2 (Jurisdiction Mismatch):** `"Generate 10 scenarios where a user's goal is 'asset_protection' but their jurisdiction is international (e.g., 'us', 'uk'). While a trust is still the answer, the specific type is different. For our system's purpose, the output for now should still be 'mu_ibc' as the designated international solution. Format these as JSON flashcards."`

---

## 3. Prompts for AI-Assisted Review

**Objective:** To help the human expert review the generated data more efficiently.

*   **Meta-Prompt 3.1 (Rule Check):** `"Given the following rule: 'If the goal is 'liability_protection' and the jurisdiction is 'za', the output must be 'za_pty_ltd'.' Does this flashcard conform to the rule? `[Paste Generated JSON Here]` Answer Yes or No and explain your reasoning."`
*   **Meta-Prompt 3.2 (Plausibility Check):** `"Is the following scenario a plausible, real-world situation for someone seeking financial structuring advice? `[Paste Generated Scenario Description Here]`"`

This library of prompts provides a comprehensive toolkit for generating the high-quality dataset required for Phase 1.
