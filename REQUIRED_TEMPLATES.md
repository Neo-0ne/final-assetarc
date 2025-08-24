# Required Templates Guide

This document lists all the `.docx` and `.html` templates used by the AssetArc platform for document and email generation. You can find these templates in the `eng-drafting/app/templates/` directory and other service-specific template folders.

## `eng-drafting` Service Templates

This service uses a `templates.json` file to map template IDs to the following template files.

### Document Templates (.docx)
*   `trust_deed.v1.docx`: The main template for generating Trust Deeds.
*   `company_resolution.v1.docx`: For generating company resolutions.
*   `share_certificate.v1.docx`: For generating share certificates.
*   `s42_47_compliance_checklist.v1.docx`: Checklist for SARS Section 42-47 compliance.
*   `fica_checklist.v1.docx`: FICA compliance checklist for clients.
*   `ibc_moa.v1.docx`: Memorandum of Association for an International Business Company.
*   `...` (and many others for different jurisdictions and structures)

### Email Templates (.html)
*   `booking_confirmation.v1.html`: Email sent to a user after they book a consultation.
*   `booking_error.v1.html`: Email sent if there is an error with a booking.
*   `otp_email.v1.html`: The template for the One-Time Password email.
*   `client_invitation.v1.html`: The email sent to a client when an advisor invites them to the platform.
*   `contact_form_admin_notification.v1.html`: The email sent to the admin when a contact form is submitted.
*   `newsletter_subscription_confirmation.v1.html`: Confirmation email for newsletter subscribers.
*   `...` (and others for different notifications and marketing sequences)

## Other Service-Specific Templates

Some services have their own templates for specific purposes.

### `eng-analytics` Service
*   `dashboard.html`: A simple HTML template for displaying the KPI dashboard.

### `eng-billing` Service
*   `invoice.v1.html`: A template for generating invoices.
*   `quote_summary.v1.pdf.html`: The HTML structure that gets converted to a PDF for quote summaries.

## How to Update Templates

To update the content or styling of any of these templates:
1.  Locate the corresponding file in the `eng-drafting/app/templates/` directory (or other service's template folder).
2.  Edit the file. The `.docx` templates use Jinja2-style placeholders (e.g., `{{ client_name }}`). The `.html` templates can be edited directly.
3.  No service restart is required to pick up changes to the templates.

Please review these templates to ensure they meet your legal and branding requirements.
