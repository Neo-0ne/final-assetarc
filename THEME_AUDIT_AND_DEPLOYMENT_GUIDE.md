# Theme Audit Report & Deployment Guidance

**Audit Date:** 2025-09-01
**Audited By:** Jules

## 1. Executive Summary

This report details the audit of three WordPress theme templates that were recently moved to the `templates` folder. The purpose of the audit was to confirm if they were properly refactored to use Advanced Custom Fields (ACF) Pro for content management.

**Conclusion:** The audit found that all three templates are self-contained, interactive tools (calculators/planners). They are correctly implemented with hardcoded text and JavaScript logic. **No ACF Pro refactoring is required or recommended for these files.** They are considered ready for deployment from a technical standpoint.

## 2. Audited Template Files

The following three files were audited:

1.  `assetarc-theme/templates/template-rollover-planner.php`
2.  `assetarc-theme/templates/template-residency-planner.php`
3.  `assetarc-theme/templates/template-insurance-calculator.php`

## 3. Detailed Findings & Rationale

### Analysis of All Three Templates

All three templates share a similar architecture:

*   **Purpose:** They function as interactive calculators or planners that take user input, send it to a backend API (`/api/eng-compliance/compliance/run`), and display the results.
*   **Content:** The text within these templates (headings, labels, instructional paragraphs) is not static page content but rather part of the user interface of the tool itself.
*   **ACF Pro Integration:** There is no integration with ACF Pro, and this is by design. Using ACF for this content would add unnecessary complexity and separate the UI text from the tool's core logic, making maintenance harder.

### Why ACF Pro is Not Needed for These Files

The primary purpose of ACF Pro is to allow non-technical users to manage page content from the WordPress admin area without editing code. The audited files are not content pages; they are functional applications embedded within a WordPress template.

Therefore, the current implementation is correct. The files are "properly refactored" by virtue of not needing the ACF refactoring that a typical content page would require.

## 4. Deployment Guidance

*   **Readiness:** All three templates are technically ready for deployment. They are well-structured and self-contained.
*   **Dependencies:** The functionality of these templates is critically dependent on the backend API endpoint they call: `/api/eng-compliance/compliance/run`. Before deploying, ensure that this endpoint is live, accessible, and that the `rollover_planner`, `residency_planner`, and `insurance_wrapper_calculator` modules are correctly configured and running in the `eng-compliance` service.
*   **Linking to Pages:** To make these tools accessible on your website, follow these steps for each template:
    1.  In the WordPress admin dashboard, create a new Page (or edit an existing one).
    2.  Give the page a title (e.g., "Rollover Relief Planner").
    3.  On the right-hand side of the page editor, find the "Page Attributes" panel.
    4.  In the "Template" dropdown, select the corresponding template name (e.g., "Section 42-47 Rollover Relief Planner").
    5.  Publish the page. It will now be available at the permalink you've set (e.g., `yourwebsite.com/rollover-planner`).

## 5. How to Link Other Pages to ACF Pro

For other, more traditional content-based pages (like the Homepage, About Page, etc.), you should continue to use ACF Pro as outlined in the `ACF_CONTENT_GUIDE.md`.

The process for linking a page to its ACF fields is as follows:

1.  **Assign the Template:** As described above, assign the correct Page Template to your WordPress page.
2.  **Find the ACF Fields:** Once the template is assigned and the page is saved, the corresponding ACF fields (as defined in your ACF Field Groups and listed in `ACF_CONTENT_GUIDE.md`) will appear in the page editor.
3.  **Populate the Content:** Copy and paste the content from the `ACF_CONTENT_GUIDE.md` into the corresponding fields in the WordPress editor.
4.  **Save the Page:** Save your changes. The template file will then pull this content dynamically using `get_field()` and `the_field()` functions.

This separation of concerns (tools are hardcoded, content pages use ACF) is a robust and maintainable approach for your theme.
