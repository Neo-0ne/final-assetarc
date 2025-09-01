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
    1.  **Dataset Strategy:**
        *   **Data Volume:** The Sapient HRM model is highly data-efficient. A high-quality, diverse dataset of **~1,000-2,000 examples** should be sufficient for this task.
        *   **Data Generation:** To accelerate dataset creation, we recommend a "human-in-the-loop" workflow:
            1.  Use a Large Language Model like **OpenAI's GPT-4o** (which is already integrated into the platform) to generate a large number of draft scenarios.
            2.  Have a **human legal expert** review, correct, and approve every example for accuracy.
            3.  An engineer will format the approved data into the final JSON structure for training.
    2.  **Training:** Train the Sapient model on the expert-reviewed dataset in a specialized cloud environment with GPU support.
    3.  **Integration:** Build a new `eng-reasoning` microservice to host the trained model. Modify the `eng-lifecycle` service to call this new service, protected by a feature flag for easy rollback.

### **Phase 2: AI-Powered Tax & Compliance Rulings (Advanced Reasoning)**

*   **Goal:** Replace complex, rule-based eligibility and status checks with an AI model. This phase demonstrates the AI's ability to handle intricate, real-world legal and tax rules.
*   **Example Use-Cases:**
    *   **Rollover Relief Planner:** The AI would determine eligibility for corporate rollover relief (s42, s45, etc.).
    *   **Residency Planner:** The AI would determine a user's tax residency status.
*   **Implementation Plan (per use-case):**
    1.  **Dataset:** Follow the same "Generate, Review, Finalize" workflow to create a high-quality dataset for each specific task.
    2.  **Training:** Train or fine-tune the Sapient model on the new dataset.
    3.  **Integration:** Add a new endpoint to the `eng-reasoning` service. Modify the corresponding `eng-compliance` function to call the AI service.

### **Phase 3: AI-Powered Document Blueprint Generation (Long-Term Vision)**

*   **Goal:** Replace the entire static `.docx` template system with a dynamic, AI-driven document generation pipeline.
*   **Complexity:** High. This requires extensive training data and a two-stage AI process.
*   **Value:** This is a transformative step, enabling the creation of highly dynamic and customized legal documents, providing a significant competitive advantage.
*   **Implementation Plan (Hybrid AI Approach):**
    1.  **Structuring (Sapient HRM):** Train the Sapient model to generate a structured JSON "blueprint" of a legal document.
    2.  **Drafting (LLM - OpenAI):** Feed the generated blueprint to a Large Language Model to write the final, human-readable prose.
    3.  **Integration:** This would likely involve a significant rework of the `eng-drafting` service.

---

## 4. Immediate Next Steps & Recommendation

**Recommendation:** We strongly recommend beginning with **Phase 1**. It offers the best balance of low risk and high learning value, and its success will provide the foundation and confidence needed to proceed with the more advanced phases.
