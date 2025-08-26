# Manual Testing Guide

This document provides step-by-step instructions for manually testing the core features of the AssetArc platform from a user's perspective. These steps are designed for non-developers and focus on interactions with the user interface.

---

## Prerequisite: Accessing the Platform

Before you begin, ensure all the platform's services are running and you can access the main website in your browser.

---

## 1. User Registration and Login

**Goal:** Verify that a new user can register and log in successfully.

**Steps:**
1.  Navigate to the website's homepage.
2.  Click on the "Register" or "Sign Up" button.
3.  Fill out the registration form with a new email address and password.
4.  Click "Submit".
5.  You may be asked to verify your email. Check your inbox for a verification link and click it.
6.  Once verified, navigate to the "Login" page.
7.  Enter the email and password you just registered with.
8.  Click "Login".

**Expected Outcome:**
*   You should be successfully logged into the platform and see your user dashboard or be redirected to the homepage as a logged-in user.

---

## 2. B-BBEE Calculator

**Goal:** Verify that the B-BBEE calculator works correctly.

**Steps:**
1.  Log in to the platform.
2.  Navigate to the "Calculators" or "Tools" section and select the "B-BBEE Calculator".
3.  Fill in the required fields (e.g., Total Staff, Black Employees, Black Female Employees, etc.).
4.  Click the "Calculate" button.

**Expected Outcome:**
*   The calculator should display a B-BBEE score and level based on the inputs provided. The results should update if you change the inputs and recalculate.

---

## 3. Estate Tools: Estate Duty Calculator

**Goal:** Verify that the Estate Duty calculator provides an accurate estimate.

**Steps:**
1.  Log in to the platform.
2.  Navigate to the "Estate Tools" section and select the "Estate Duty Calculator".
3.  Enter values for assets (e.g., Property, Investments) and liabilities (e.g., Bonds, Loans).
4.  Click "Calculate".

**Expected Outcome:**
*   The tool should display the calculated Gross Value, Net Value, and the estimated Estate Duty payable.

---

## 4. Purchasing a Service with NOWPayments (Crypto)

**Goal:** Verify that a user can successfully purchase a service using cryptocurrency via NOWPayments.

**Steps:**
1.  Log in to the platform.
2.  Navigate to a service that requires payment (e.g., "Premium Course Access" or "B-BBEE Certificate").
3.  Click the "Buy Now" or "Purchase" button.
4.  On the checkout page, you should see payment options. Select "Pay with Crypto" or "NOWPayments".
5.  Choose a cryptocurrency to pay with (e.g., BTC, ETH, USDT).
6.  Click "Proceed to Payment".
7.  You will be redirected to a NOWPayments invoice page. The page will show the amount due in the cryptocurrency you selected.
8.  **For testing purposes, you can use a testnet wallet to send a small amount of test cryptocurrency to the address shown. Do not use real funds.** (Note: If a test environment is not available, this step can only be visually verified).
9.  After making the "payment", wait on the invoice page.

**Expected Outcome:**
*   The NOWPayments invoice page should eventually update to show the payment as "Confirmed" or "Finished".
*   You should be redirected back to a success page on the AssetArc platform.
*   You should receive a confirmation email for your purchase.
*   The feature you purchased (e.g., Premium Course) should now be unlocked and accessible on your account.
