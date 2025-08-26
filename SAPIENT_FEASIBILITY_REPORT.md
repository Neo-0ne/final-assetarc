# Sapient AI Integration: Feasibility Report

## 1. Introduction & Goal

This document outlines a feasibility study on integrating the Sapient HRM (Hierarchical Reasoning Model) as an AI-powered logic engine within the AssetArc platform. The goal is to replace existing, hardcoded rule-based systems with a more flexible and powerful AI model. This report analyzes the potential use-cases, defines the technical requirements, and proposes a path for a pilot implementation.

---

## 2. Analysis of Sapient HRM

Based on a review of the Sapient HRM GitHub repository, the following has been determined:

*   **Nature of the Model:** Sapient HRM is a highly specialized AI model designed for complex, rule-based reasoning tasks (e.g., logic puzzles). It is **not** a general-purpose conversational AI or a platform operations model.
*   **Implementation Overhead:** Using this model requires significant effort. It is not a simple API call. The process involves:
    1.  Creating a custom, structured training dataset.
    2.  Setting up a specialized Python/CUDA environment.
    3.  A potentially lengthy training process to produce a model checkpoint.
    4.  Hosting the trained model in a dedicated inference service.

---

## 3. Analysis of Potential Use-Cases

Three existing features were analyzed as potential candidates for replacement by the AI model.

### 3.1. Corporate Structure Design (`eng-lifecycle`)
*   **Current Logic:** A simple, hardcoded `if/elif` rule engine that maps user goals and jurisdiction to predefined corporate structures.
*   **Suitability:** **Excellent Pilot Project.** The logic is a clear reasoning task with well-defined inputs and outputs, making it ideal for creating a training dataset. The complexity is low enough for a successful first implementation.

### 3.2. Estate Duty Calculator (`eng-compliance`)
*   **Current Logic:** A deterministic mathematical formula that calculates tax liability based on fixed rates and tiers.
*   **Suitability:** **Not Suitable.** This is a math problem, not a reasoning problem. An AI model would be less accurate and far more complex than the current, correct implementation.

### 3.3. Rollover Relief Planner (`eng-compliance`)
*   **Current Logic:** The eligibility checker (`check_eligibility`) is a complex, multi-layered rule engine that evaluates a transaction against dozens of criteria from tax law.
*   **Suitability:** **Excellent Advanced Project.** This is a perfect example of a complex reasoning task that Sapient HRM is designed for. However, due to the complexity of the input data, this is better suited as a second project after a successful pilot.

---

## 4. Proposed Pilot Project: AI-Powered Structure Design

It is recommended to proceed with the **Corporate Structure Design** feature as the pilot project.

### 4.1. Dataset Requirements

A training dataset must be created. Each data point will be a JSON object in the following format:

```json
{
  "input": {
    "goals": ["list_of_strings"],
    "jurisdiction": "string"
  },
  "output": {
    "recommended_structures": ["list_of_structure_ids"]
  }
}
```
**Example:**
```json
{
  "input": {
    "goals": ["asset_protection", "liability_protection"],
    "jurisdiction": "za"
  },
  "output": {
    "recommended_structures": ["za_pty_ltd", "za_trust"]
  }
}
```
A robust dataset would require thousands of such examples to cover a wide range of combinations.

#### Proposed Data Generation Workflow

To accelerate the creation of this large dataset, a "human-in-the-loop" approach is recommended:

1.  **Generate Draft Data:** Use a Large Language Model (LLM) like OpenAI's GPT to rapidly generate a large number of draft scenarios and their corresponding "correct" outputs.
2.  **Expert Review:** Every single generated data point must be meticulously reviewed, corrected, and approved by a human legal or financial expert. This step is critical to ensure accuracy and remove any potential AI "hallucinations".
3.  **Finalize for Training:** An engineer will format the expert-approved data into the final JSON structure required for training the Sapient HRM model.

This workflow combines the speed of AI for data generation with the accuracy and accountability of human expertise.

### 4.2. Proposed Integration Plan

The integration can be broken down into three phases:

**Phase 1: Model Training (Offline)**
1.  **Dataset Generation:** Create a comprehensive training dataset (~1000+ examples).
2.  **Environment Setup:** Provision a cloud GPU instance with the required CUDA and Python dependencies.
3.  **Training:** Run the Sapient HRM training script to produce a trained model checkpoint file.

**Phase 2: Create AI Inference Service**
1.  **New Microservice:** Build a new, simple Python service (e.g., `eng-reasoning`).
2.  **Model Hosting:** This service will load the trained model from Phase 1.
3.  **API Endpoint:** Expose an endpoint (e.g., `/reasoning/design-structure`) that accepts `goals` and `jurisdiction` and returns the AI's recommendation.

**Phase 3: Platform Integration**
1.  **Update `eng-lifecycle`:** Modify the `design_corporate_structure` function to call the new `eng-reasoning` service instead of using its internal rules.
2.  **Feature Flag:** Wrap the call to the new AI service in a feature flag. This will allow for safe testing in production and an instant rollback path to the old rule-based engine if needed.

---

## 5. Conclusion & Recommendation

**Conclusion:** Replacing rule-based logic in AssetArc with the Sapient HRM AI model is a feasible but significant undertaking. It offers the potential for much greater flexibility and intelligence in the long term.

**Recommendation:** Proceed with the proposed pilot project of replacing the **Corporate Structure Design** logic. The outlined three-phase plan provides a clear path forward. This approach will prove the value of the AI integration on a manageable scale before tackling more complex systems like the Rollover Relief Planner.

---

## 6. Future Vision: AI-Powered Document Generation (Phase 2)

Beyond the initial pilot project, the hybrid AI approach discussed can be extended to revolutionize document drafting itself, potentially replacing the static `.docx` template system entirely.

### The Hybrid AI Workflow:

1.  **Structuring (Sapient HRM):** The Sapient model would be trained on the legal rules and composition of various documents. When a document is needed (e.g., a Trust Deed), the model would generate a structured "blueprint" or "skeleton" in a format like JSON. This blueprint would define all the required clauses, sections, and data placeholders for that specific document and context.

2.  **Drafting (Large Language Model - OpenAI):** This structured blueprint would then be passed to a Large Language Model (LLM). The LLM would use the blueprint as a precise set of instructions to draft the final, human-readable legal document with the correct prose and formatting.

### Benefits:

*   **Dynamic Content:** Documents could be dynamically generated and customized on the fly, far beyond the capabilities of simple template placeholders.
*   **Reduced Maintenance:** Instead of maintaining dozens of `.docx` templates, the system would rely on a more robust, version-controlled training dataset for the AI.
*   **Enhanced Flexibility:** New document types or variations could be introduced by training the AI on new rules, rather than creating new templates from scratch.

This represents a significant long-term evolution for the platform and a compelling future direction for the AI integration.
