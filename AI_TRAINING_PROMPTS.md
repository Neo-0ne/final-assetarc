# AI Training Prompt Library (Comprehensive)

This document provides a library of structured prompts to be used with a Large Language Model (LLM) like ChatGPT to generate a draft dataset for training the Sapient HRM model across a multi-phase rollout.

**Workflow Reminder:**
1.  **Generate:** Use the prompts below to generate a large volume of draft "flashcards".
2.  **Review:** A human legal/financial expert **must** review every single generated example for accuracy.
3.  **Finalize:** An engineer will format the expert-approved data into the final JSON structure.

---

## Phase 1: AI-Powered Corporate Structure Design (Pilot Project)

**Goal:** Train the AI to recommend the correct corporate structure(s) based on a user's goals and jurisdiction.

### Prompt Type 1.1: Basic Scenarios
*   `"Generate 20 scenarios of small businesses in South Africa ('za') whose primary goal is 'liability_protection'. The required output structure ID is 'za_pty_ltd'. Format each as a complete JSON flashcard: {"input": {"goals": ["liability_protection"], "jurisdiction": "za"}, "output": {"recommended_structures": ["za_pty_ltd"]}}."`

### Prompt Type 1.2: Multi-Goal Scenarios
*   `"Generate 20 scenarios for established professionals in South Africa ('za') who require both 'liability_protection' for their practice and 'asset_protection' for their personal wealth. The required output must be a list containing both 'za_pty_ltd' and 'za_trust'. Format each as a complete JSON flashcard."`

### Prompt Type 1.3: International Scenarios
*   `"Generate 20 scenarios for tech startups based in 'us' whose primary goal is 'tax_efficiency'. The recommended structure should always be 'mu_ibc'. Format each as a complete JSON flashcard."`

---

## Phase 2: AI-Powered Tax & Compliance Rulings

**Goal:** Train the AI to determine eligibility or status based on complex rule-based systems.

### 2.1 Rollover Relief Planner Prompts

*   `"Generate a complete JSON flashcard for a Section 45 Intra-group transaction that is INELIGIBLE because the companies are not part of the same group (set group_relationship.same_group to false). The input must be a valid RolloverPlannerInput object. The output must be {'eligible': false, 'failed_reasons': ['The transaction must be between companies in the same group (>= 70% shareholding).']}."`
*   `"Generate a complete JSON flashcard for a Section 42 Asset-for-Share transaction that is ELIGIBLE. All rule conditions must be met (e.g., transferee is SA resident, shares were issued). The output must be {'eligible': true, 'failed_reasons': []}."`

### 2.2 Residency Planner Prompts

*   `"Generate a complete JSON flashcard for a person who IS a tax resident of South Africa based on the Physical Presence Test. The input object must have 'days_in_current_year' >= 91, 'days_each_of_prev_5_years' with all values >= 91, and the sum of 'days_each_of_prev_5_years' >= 915. The output should be {'status': 'Resident', 'reasoning': 'You meet the requirements of the physical presence test...'}."`
*   `"Generate a complete JSON flashcard for a person who is NOT a tax resident because they fail the first part of the physical presence test (days_in_current_year < 91). The output should be {'status': 'Non-Resident', 'reasoning': 'You do not meet the requirements... Failures: Days in current year >= 91: Fail'}."`
*   `"Generate a JSON flashcard for a person who IS considered 'Ordinarily Resident'. The input must have at least 3 of the 4 ordinary_residence_flags set to true. The output should be {'status': 'Resident', 'reasoning': 'You are considered ordinarily resident...'}."`

---

## Phase 3: AI-Powered Document Blueprint Generation

**Goal:** Train the AI to generate a structured "blueprint" or "skeleton" of a legal document.

### Prompt Type 3.1: Clause Identification
*   `"For a standard South African Trust Deed, list all the mandatory clauses and at least 10 common optional clauses. Present this as a JSON array of strings, for example: [\"appointment_of_trustees\", \"beneficiary_nomination\", \"trustee_powers\", ...]"`

### Prompt Type 3.2: Blueprint Generation
*   `"I need a blueprint for a legal document. The requirement is: 'A board resolution for a South African company to approve the purchase of a major asset.' Please generate a JSON object representing this document's blueprint. The JSON should have a 'document_type' field and a 'sections' array. Each object in the 'sections' array should have a 'section_title' and a 'clauses' array."`
*   `"Generate a new document blueprint for a 'Share Certificate' for a South African Pty Ltd. The blueprint should be a JSON object with placeholders for all key information (e.g., Company Name, Shareholder, Number of Shares, Class of Shares)."`

---
## 4. AI-Assisted Review Prompts

*   `"Given the rule 'A person is a tax resident if they are present for more than 91 days in the current year, more than 91 days in each of the last 5 years, and more than 915 days in total over the last 5 years', does this flashcard correctly identify the person as a resident? [Paste Generated JSON Here] Answer Yes or No and explain why."`
