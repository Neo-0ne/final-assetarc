# AI Training Data Generation Prompts

This document provides a set of structured prompts to be used with a Large Language Model (LLM) like ChatGPT to generate a draft dataset for training the Sapient HRM model.

**Workflow Reminder:**
1.  **Generate:** Use the prompts below to generate a large volume of draft "flashcards".
2.  **Review:** A human legal/financial expert **must** review every single generated example for accuracy and correctness.
3.  **Finalize:** An engineer will format the expert-approved data into the final JSON structure required for training.

---

## Phase 1: AI-Powered Corporate Structure Design (Pilot Project)

**Goal:** To train the Sapient AI to recommend the correct corporate structure(s) based on a user's goals and jurisdiction.

**Prompts:**
*   `"Generate a list of 30 diverse scenarios for individuals or businesses in South Africa ('za'). For each, specify a single primary goal from this list: ['liability_protection', 'asset_protection', 'international_trade', 'tax_efficiency']. Then, provide the single, most appropriate structure ID from this list: ['za_pty_ltd', 'za_trust', 'mu_ibc']."`
*   `"Create 20 advanced scenarios for high-net-worth individuals in South Africa ('za') who have a complex set of goals (e.g., liability_protection and asset_protection). Provide a list of all the structure IDs that would be required to meet those goals."`
*   `"For the following scenario, format the output as a JSON object with 'input' and 'output' keys as described in the feasibility report: 'A tech startup in the UK wants tax_efficiency for its European sales.'"`

---

## Phase 2: AI-Powered Tax & Compliance Rulings

**Goal:** To train the Sapient AI to determine eligibility or status based on a complex set of rules.

### 2.1 Rollover Relief Planner Prompts

*   `"Generate a scenario for a Section 42 (Asset-for-Share) transaction that should be ELIGIBLE for rollover relief. Describe the transferor, transferee, the asset, and the consideration. The output should be a JSON object with 'eligible: true' and an empty 'failed_reasons' array."`
*   `"Generate a scenario for a Section 42 transaction that should be INELIGIBLE because the transferee company is not a South African resident. The output should be a JSON object with 'eligible: false' and a 'failed_reasons' array containing the specific reason."`
*   `"Create a detailed scenario for a Section 45 (Intra-group) transaction that fails the eligibility check because the companies are not part of the same group (less than 70% shareholding). Provide the JSON output with 'eligible: false' and the correct failure reason."`

### 2.2 Residency Planner Prompts

*   `"Generate a scenario for a person who IS a tax resident of South Africa based on the physical presence test. Provide the number of days they were present in the current year and the preceding 5 years. The output should be a JSON object with 'is_resident: true'."`
*   `"Generate a scenario for a person who is NOT a tax resident of South Africa because they fail the first part of the physical presence test (less than 91 days in the current year). Provide the days present for all 6 years. The output should be a JSON object with 'is_resident: false' and a 'reason' field explaining the failure."`
*   `"Generate a scenario for a person who is NOT a tax resident because they fail the second part of the physical presence test (less than 915 days in the preceding 5 years), even though they were present for more than 91 days in the current year. Provide the days present for all 6 years and the JSON output with 'is_resident: false' and the correct reason."`

---

## Phase 3: AI-Powered Document Blueprint Generation (Long-Term Vision)

**Goal:** To train the Sapient AI to generate a structured "blueprint" or "skeleton" of a legal document.

**Prompts:**
*   `"For a standard South African Last Will and Testament, list all the mandatory clauses and at least 10 common optional clauses. Present this as a JSON array of strings."`
*   `"I need a blueprint for a legal document. The requirement is: 'A founding affidavit for a South African company applying for a business license.' Please generate a JSON object representing this document's blueprint. The JSON should have a 'document_type' field and a 'sections' array. Each object in the 'sections' array should have a 'section_title' and a 'clauses' array."`
*   `"Generate a new document blueprint for a 'Board Resolution to open a corporate bank account'. The blueprint should be a JSON object with relevant sections and clauses."`
