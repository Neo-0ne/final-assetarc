# 3rd Party Services & APIs Guide

This document provides a list of all the third-party services and APIs that the AssetArc platform depends on. For each service, you will find a link to its website, a description of its purpose, and the environment variables you need to set to configure it.

## Core Services

### 1. OpenAI
*   **Purpose:** Used by various services for AI-powered logic, such as in the NLP Intent Helper and for summarizing complex legal text.
*   **Website:** [https://www.openai.com/](https://www.openai.com/)
*   **API Key:** You will need an API key from the OpenAI developer platform.
*   **Environment Variable:** `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`

### 2. Amazon Web Services (AWS)
*   **Purpose:** The platform uses Amazon Simple Email Service (SES) for sending all emails (OTPs, notifications, etc.).
*   **Website:** [https://aws.amazon.com/ses/](https://aws.amazon.com/ses/)
*   **API Key:** You will need an AWS Access Key ID and Secret Access Key with permissions for SES.
*   **Environment Variables:**
    *   `AWS_ACCESS_KEY_ID`
    *   `AWS_SECRET_ACCESS_KEY`
    *   `AWS_REGION`
    *   `SENDER_EMAIL` (The verified "From" address in SES).

### 3. Google Cloud Secret Manager
*   **Purpose:** Secure storage and management of all application secrets, including API keys, database credentials, and other sensitive configuration variables.
*   **Website:** [https://cloud.google.com/secret-manager](https://cloud.google.com/secret-manager)
*   **API Key:** Requires a GCP Service Account JSON key file.
*   **Environment Variables:**
    *   `GCP_PROJECT_ID`
    *   `GOOGLE_APPLICATION_CREDENTIALS` (path to the service account key file)

## Payment Gateways

### 3. Yoco
*   **Purpose:** The primary payment gateway for processing ZAR-based payments and subscriptions.
*   **Website:** [https://www.yoco.com/](https://www.yoco.com/)
*   **API Key:** You will need a Public Key and a Secret Key from your Yoco developer dashboard.
*   **Environment Variables:**
    *   `pk_live_a6ac9fc34VJLzrX92674`
    *   `sk_live_f6bd3d0e1L3BYrb2912424e83b90`

### 4. Stripe
*   **Purpose:** An alternative payment gateway, primarily for international (USD) payments.
*   **Website:** [https://stripe.com/](https://stripe.com/)
*   **API Key:** You will need a Publishable Key and a Secret Key from your Stripe dashboard.
*   **Environment Variables:**
    *   `STRIPE_API_KEY` (this is the secret key)
    *   `STRIPE_WEBHOOK_SECRET`

### 5. NOWPayments
*   **Purpose:** For processing cryptocurrency payments (BTC, ETH, USDT).
*   **Website:** [https://nowpayments.io/](https://nowpayments.io/)
*   **API Key:** You will need an API key from your NOWPayments account.
*   **Environment Variable:** Private HY0ZF3Z-E67MSFZ-KA0T933-ABW1Q8X
*                         Public  d245e563-17a6-42a3-b23e-b1ab0a6edbe4
*                           IPN   oi/+tLSJTsh7DJfOnWiB41i/NiYJjbFC

## Other Integrations

### 6. Cal.com
*   **Purpose:** Used by the `eng-engagement` service to create and manage booking links for consultations.
*   **Website:** [https://cal.com/](https://cal.com/)
*   **API Key:** You will need an API key from your Cal.com account settings.
*   **Environment Variable:** `cal_live_8c45ad43e8ec4732834598fff8c51acd`

### 7. Notion
*   **Purpose:** Used as the backend for the review queue, marketing calendar, and other internal dashboards.
*   **Website:** [https://www.notion.so/](https://www.notion.so/)
*   **API Key:** You will need an integration token from your Notion workspace.
*   **Environment Variable:** `NOTION_TOKEN`

### 8. ExchangeRate.host
*   **Purpose:** Used by the `eng-billing` service to get real-time foreign exchange rates.
*   **Website:** [https://exchangerate.host/](https://exchangerate.host/)
*   **API Key:** This API does not require a key for its free tier.
*   **Environment Variable:** None required.

## Internal API Key

*   **Purpose:** A shared secret used to protect internal API endpoints that should not be exposed to the public.
*   **Value:** You should generate a strong, random string for this key.
*   **Environment Variable:** `INTERNAL_SERVICE_API_KEY` (This must be set to the same value for all services that use it).
