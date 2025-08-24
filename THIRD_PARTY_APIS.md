# 3rd Party Services & APIs Guide

This document provides a list of all the third-party services and APIs that the AssetArc platform depends on. For each service, you will find a link to its website, a description of its purpose, and the environment variables you need to set to configure it.

## Core Services

### 1. OpenAI
*   **Purpose:** Used by various services for AI-powered logic, such as in the NLP Intent Helper and for summarizing complex legal text.
*   **Website:** [https://www.openai.com/](https://www.openai.com/)
*   **API Key:** You will need an API key from the OpenAI developer platform.
*   **Environment Variable:** `OPENAI_API_KEY`

### 2. Amazon Web Services (AWS)
*   **Purpose:** The platform uses Amazon Simple Email Service (SES) for sending all emails (OTPs, notifications, etc.).
*   **Website:** [https://aws.amazon.com/ses/](https://aws.amazon.com/ses/)
*   **API Key:** You will need an AWS Access Key ID and Secret Access Key with permissions for SES.
*   **Environment Variables:**
    *   `AWS_ACCESS_KEY_ID`
    *   `AWS_SECRET_ACCESS_KEY`
    *   `AWS_REGION`
    *   `SENDER_EMAIL` (The verified "From" address in SES).

## Payment Gateways

### 3. Yoco
*   **Purpose:** The primary payment gateway for processing ZAR-based payments and subscriptions.
*   **Website:** [https://www.yoco.com/](https://www.yoco.com/)
*   **API Key:** You will need a Public Key and a Secret Key from your Yoco developer dashboard.
*   **Environment Variables:**
    *   `YOCO_PUBLIC_KEY`
    *   `YOCO_SECRET_KEY`

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
*   **Environment Variable:** `NOWPAYMENTS_API_KEY`

## Other Integrations

### 6. Cal.com
*   **Purpose:** Used by the `eng-engagement` service to create and manage booking links for consultations.
*   **Website:** [https://cal.com/](https://cal.com/)
*   **API Key:** You will need an API key from your Cal.com account settings.
*   **Environment Variable:** `CAL_COM_API_KEY`

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
