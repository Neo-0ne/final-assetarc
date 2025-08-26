# Suggested Pricing Model

This document provides a suggested pricing structure for services that are not suitable for dynamic, API-driven pricing. The prices listed below are placeholders based on high-level research of competitors (e.g., Harneys, Vistra, Ocorian) and common industry practices.

**Please review, adjust, and finalize these prices.** Once finalized, you can transfer the relevant prices into the `config/service_prices.json` file for use by the application.

---

## 1. International Business Company (IBC) Formation

IBC pricing is typically tiered based on the jurisdiction and the level of included services. All prices are listed in **USD**.

### BVI (British Virgin Islands) IBC Packages

| Tier      | Price (USD) | Features                                                                                             | Target Audience          |
| :-------- | :---------- | :--------------------------------------------------------------------------------------------------- | :----------------------- |
| **Standard**  | `$5,000`    | - Standard Government Registration Fees<br>- Registered Agent & Office for 1st Year<br>- Standard Memorandum & Articles of Association<br>- Digital Corporate Documents | Startups, Basic Holdings |
| **Premium**   | `$7,500`    | - All Standard features<br>- Nominee Director & Shareholder Service (1st Year)<br>- Certificate of Good Standing<br>- Notarized & Apostilled Corporate Documents | Privacy-conscious clients|
| **Enterprise**| `$10,000+`  | - All Premium features<br>- Assistance with Corporate Bank Account Opening<br>- Bespoke legal consultation (2 hours)<br>- Courier of physical documents     | Operational Businesses   |

### Cayman Islands IBC Packages

| Tier      | Price (USD) | Features                                                                                             | Target Audience          |
| :-------- | :---------- | :--------------------------------------------------------------------------------------------------- | :----------------------- |
| **Standard**  | `$6,500`    | - Standard Government Registration Fees<br>- Registered Agent & Office for 1st Year<br>- Standard Memorandum & Articles of Association<br>- Digital Corporate Documents | Investment Funds, SPVs   |
| **Premium**   | `$9,000`    | - All Standard features<br>- Nominee Director & Shareholder Service (1st Year)<br>- Certificate of Good Standing<br>- Notarized & Apostilled Corporate Documents | Regulated entities       |

---

## 2. South African (ZA) Trust Services

Pricing for local trust services. All prices are listed in **ZAR**.

| Service                       | Price (ZAR) | Description                                                                                             |
| :---------------------------- | :---------- | :------------------------------------------------------------------------------------------------------ |
| **Discretionary Trust Deed**  | `R15,000`   | Drafting and registration of a new discretionary trust deed with the Master of the High Court.            |
| **Trust Amendment**           | `R7,500`    | Drafting and filing of a deed of amendment for an existing trust.                                       |
| **Independent Trustee Service** | `R25,000`   | Annual fee for providing a professional, independent trustee for compliance and governance purposes.    |

---

## 3. Other Services

This section is for other services that may be added in the future.

| Service                       | Price (ZAR) | Description                                                                                             |
| :---------------------------- | :---------- | :------------------------------------------------------------------------------------------------------ |
| **Last Will and Testament**   | `R5,000`    | Standard drafting of a South African will.                                                              |
| **Share Transfer Agreement**  | `R3,500`    | Drafting of a standard share transfer agreement for a private company.                                  |

---

**Next Steps:**
1.  Review and edit the prices and features in this document.
2.  For each service you wish to make available for purchase, create a corresponding entry in `config/service_prices.json`. For example:
    ```json
    "IBC_BVI_STANDARD": {
      "price": 5000.00,
      "currency": "USD",
      "description": "Standard BVI IBC Formation Package"
    }
    ```
