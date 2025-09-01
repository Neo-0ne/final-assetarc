# AssetArc Post-Launch Bot Optimization - Admin Implementation Doc

This document outlines the planned strategic enhancements and optimizations for the AssetArc bot ecosystem, to be implemented post-launch.

## Section 1: Bot Inventory Audit

This section will be populated after the initial launch phase, based on usage data from the `eng-analytics` service. It will include:

*   **Current Bot & Function Inventory:** A list of all active bots and their primary functions.
*   **Usage Heatmap:** A data-driven analysis of which bots are used most frequently, by which user types (clients vs. advisors).
*   **Suggested Removals/Merges:** Recommendations for consolidating underutilized or overlapping bots to simplify the user experience and reduce maintenance overhead.

## Section 2: Strategic Enhancements (Post-Launch)

The following enhancements are planned for phased rollout to improve the platform's intelligence and user experience.

*   **NLP Routing Refinements:** Use data from user queries to improve the accuracy of the NLP Intent Helper, reducing the need for manual clarification.
*   **Intake Simplification:** Analyze user drop-off points in the intake funnels to identify and remove friction.
*   **High-Usage Upsell Automation:** Automatically prompt high-volume advisors (like SCW) to upgrade to enterprise plans or custom tiers.
*   **Referral & Testimonial Trigger Optimization:** A/B test different timings and incentives for the testimonial and referral request flows to maximize engagement.

## Section 3: Toggle and Variable Adjustments

The platform includes several "feature flags" or toggles that can be adjusted in the admin dashboard or via environment variables. This section will provide a guide to managing them.

*   **Bot Activation Toggles:** A guide to enabling the planned future bots (e.g., BBBEE Structuring, Business Valuation) when ready for rollout.
*   **Client Token Configuration:** Instructions for setting and adjusting the expiration and usage limits for advisor-generated client tokens.
*   **SCW & Partner Configuration:** How to manage the specific settings for strategic partners, including the "Fast-Track Review" toggle and white-labeling options.

## Section 4: Optional New Logic Drops

These are new features that can be "dropped in" to the existing architecture with minimal disruption.

*   **"Push to Upgrade" Monetization CTAs:** Add context-aware calls-to-action within the platform to encourage users to upgrade their subscription or purchase one-off services.
*   **Smart Price Anchoring:** Dynamically present pricing tiers or bundles based on the user's journey and stated goals to increase conversion.
*   **Global Config Updates:** Implement logic to allow for different configurations (e.g., pricing, compliance rules) based on the user's or advisor's region.

## Section 5: How-To Steps

This section will provide detailed, step-by-step instructions for the platform administrator on how to implement the changes described in this document. It will include:

*   Instructions for placing any new or updated JSON logic files.
*   Guidance on how to enable or disable features on a per-structure or per-advisor basis.
*   How to use the Notion dashboard tags to track the performance of new features and enhancements.
