# Sapient AI Integration: A Phased Rollout Plan

## 1. Executive Summary

This document outlines a strategic, phased approach for integrating the Sapient HRM (Hierarchical Reasoning Model) into the AssetArc platform. The ultimate goal is to replace hardcoded, rule-based systems with a more flexible and powerful AI logic engine. This plan breaks the integration into three manageable phases, starting with a high-value pilot project and progressively moving towards a more ambitious, fully AI-driven system.

---

## 2. Core Technology: Sapient HRM

*   **Nature of the Model:** Sapient HRM is a specialized AI model designed for complex, rule-based reasoning tasks. It is not a general-purpose conversational AI.
*   **Implementation Requirement:** Using this model requires a significant but achievable workflow:
    1.  **Create a custom training dataset** of input-output examples.
    2.  **Train the model** in a specialized environment to produce a model checkpoint.
    3.  **Host the trained model** in a dedicated inference microservice.

---

## 3. The Phased Rollout Strategy

We recommend a three-phase rollout to mitigate risk, demonstrate value early, and build institutional knowledge.

### **Phase 1: AI-Powered Corporate Structure Design (Pilot Project)**

*   **Goal:** Replace the current simple, rule-based `design_corporate_structure` function with an AI model.
*   **Complexity:** Low. The rules are simple and the data requirements are clear.
*   **Value:** An excellent proof-of-concept to validate the entire workflow, from data creation to production integration, on a manageable scale.
*   **Implementation Plan:**
    1.  **Dataset:** Create a dataset of `(goals, jurisdiction) -> [structure_ids]` pairs.
    2.  **Training:** Train the Sapient model on this dataset.
    3.  **Integration:** Build a new `eng-reasoning` service to host the model. Modify `eng-lifecycle` to call this new service, protected by a feature flag.

### **Phase 2: AI-Powered Tax Rulings (Advanced Reasoning)**

*   **Goal:** Replace the complex eligibility-checking logic in the `Rollover Relief Planner` with an AI model.
*   **Complexity:** Medium. The input data is highly structured and complex, requiring a more sophisticated dataset.
*   **Value:** Solves a more complex reasoning problem, demonstrating the AI's ability to handle intricate, real-world legal and tax rules. This adds significant value and flexibility to the compliance tools.
*   **Implementation Plan:**
    1.  **Dataset:** Create a dataset where the input is the `RolloverPlannerInput` object and the output is the `eligibility_result` object.
    2.  **Training:** Train a new version of the Sapient model on this tax-specific dataset.
    3.  **Integration:** Add a new endpoint to the `eng-reasoning` service for this task. Modify `eng-compliance` to call this endpoint.

### **Phase 3: AI-Powered Document Blueprint Generation (Long-Term Vision)**

*   **Goal:** Replace the entire static `.docx` template system with a dynamic, AI-driven document generation pipeline.
*   **Complexity:** High. This requires extensive training data and a two-stage AI process.
*   **Value:** This is a transformative step. It would enable the creation of highly dynamic and customized legal documents on the fly, providing a significant competitive advantage and drastically reducing the overhead of template maintenance.
*   **Implementation Plan (Hybrid AI Approach):**
    1.  **Structuring (Sapient HRM):** Train the Sapient model to generate a structured JSON "blueprint" of a legal document based on a high-level requirement.
    2.  **Drafting (LLM - OpenAI):** Feed the generated blueprint to a Large Language Model (like OpenAI's GPT) to write the final, human-readable prose of the document.
    3.  **Integration:** This would likely involve a significant rework of the `eng-drafting` service to orchestrate this new two-step AI workflow.

---

## 4. Immediate Next Steps & Recommendation

**Recommendation:** We strongly recommend beginning with **Phase 1**. It offers the best balance of low risk and high learning value, and its success will provide the foundation and confidence needed to proceed with the more advanced phases.
