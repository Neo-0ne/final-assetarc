# AI Training Data Generation Prompts

This document provides a set of structured prompts to be used with a Large Language Model (LLM) like ChatGPT to generate a draft dataset for training the Sapient HRM model.

**Workflow Reminder:**
1.  **Generate:** Use the prompts below to generate a large volume of draft "flashcards".
2.  **Review:** A human legal/financial expert **must** review every single generated example for accuracy and correctness.
3.  **Finalize:** An engineer will format the expert-approved data into the final JSON structure required for training.

---

## Phase 1: AI-Powered Structure Design

**Goal:** To train the Sapient AI to recommend the correct corporate structure(s) based on a user's goals and jurisdiction.

### Prompt Type 1: Basic Scenarios

**Objective:** Generate a wide variety of simple, single-goal scenarios.

**Example Prompt:**
> "Generate a list of 30 diverse scenarios for individuals or businesses in South Africa ('za'). For each scenario, specify a single primary goal from this list: `['liability_protection', 'asset_protection', 'international_trade', 'tax_efficiency']`. Then, provide the single, most appropriate structure ID from this list: `['za_pty_ltd', 'za_trust', 'mu_ibc']`. Present the output as a numbered list of sentences. For example: '1. A plumber wants liability_protection in za. The recommended structure is za_pty_ltd.'"

### Prompt Type 2: Multi-Goal Scenarios

**Objective:** Generate more complex scenarios where a user has multiple goals, which may require multiple structures.

**Example Prompt:**
> "Create 20 advanced scenarios for high-net-worth individuals in South Africa ('za') who have a complex set of goals. For each scenario, list multiple goals from `['liability_protection', 'asset_protection', 'estate_planning', 'international_investment']`. Then, provide a list of all the structure IDs that would be required to meet those goals (`['za_pty_ltd', 'za_trust', 'mu_ibc']`). For example: 'A doctor wants liability_protection for her practice and asset_protection for her family home. The recommended structures are za_pty_ltd and za_trust.'"

### Prompt Type 3: International Scenarios

**Objective:** Generate scenarios focused on international needs, which should consistently map to the international structure.

**Example Prompt:**
> "Generate 20 scenarios for businesses operating outside of South Africa (use jurisdictions like 'us', 'uk', 'ae', 'eu'). Their goals will be 'international_trade' or 'tax_efficiency'. The recommended structure should always be 'mu_ibc'. Please describe the business type in your scenario description."

### Prompt Type 4: JSON Formatting

**Objective:** Instruct the LLM to format the generated data directly into the required JSON structure for training.

**Example Prompt:**
> "Take the following scenario: 'A software developer in South Africa wants liability protection for their new app.' Please convert this into our required JSON format for AI training. The JSON object must have an 'input' key and an 'output' key. The 'input' object should contain a 'goals' list and a 'jurisdiction' string. The 'output' object should contain a 'recommended_structures' list. For this scenario, the result should be:
> ```json
> {
>   "input": {
>     "goals": ["liability_protection"],
>     "jurisdiction": "za"
>   },
>   "output": {
>     "recommended_structures": ["za_pty_ltd"]
>   }
> }
> ```
> Now, please generate 10 new, different scenarios and format them in the exact same JSON structure."

---

## Phase 2: AI-Powered Document Generation

**Goal:** To train the Sapient AI to generate a structured "blueprint" or "skeleton" of a legal document.

### Prompt Type 1: Clause Identification

**Objective:** To generate a list of all possible clauses for a specific type of legal document.

**Example Prompt:**
> "For a standard South African Last Will and Testament, please list all the mandatory clauses and at least 10 common optional clauses. Present this as a JSON array of strings. For example: `[\"appointment_of_executor\", \"revocation_of_prior_wills\", \"guardian_for_minors\", ...]`. "

### Prompt Type 2: Blueprint Generation

**Objective:** To generate a complete document blueprint based on a specific context.

**Example Prompt:**
> "I need a blueprint for a legal document. The requirement is: 'A founding affidavit for a South African company that is applying for a business license.' Please generate a JSON object representing this document's blueprint. The JSON should have a 'document_type' field and a 'sections' array. Each object in the 'sections' array should have a 'section_title' and a 'clauses' array, listing the key points or clauses that must be included in that section. For example:
> ```json
> {
>   "document_type": "Founding Affidavit for Business License",
>   "sections": [
>     {
>       "section_title": "Deponent's Details",
>       "clauses": ["full_name", "id_number", "residential_address", "title_in_company"]
>     },
>     {
>       "section_title": "Company Information",
>       "clauses": ["company_name", "registration_number", "registered_address"]
>     },
>     {
>       "section_title": "Purpose of Affidavit",
>       "clauses": ["statement_of_purpose", "confirmation_of_facts", "list_of_supporting_documents"]
>     }
>   ]
> }
> ```
> Now, please generate a new blueprint for a 'Board Resolution to open a corporate bank account'."
