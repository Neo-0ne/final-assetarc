# AssetArc Go-Live Checklist

This document provides a comprehensive checklist to guide you through the process of deploying and launching the AssetArc platform. Follow these steps carefully to ensure a smooth and successful launch.

---

## Phase 1: Pre-Launch Configuration & Setup

This phase involves preparing your server, third-party services, and all necessary credentials.

-   **[ ] Server Setup:** Provision a production server (e.g., a Google Cloud VM, AWS EC2 instance).
-   **[ ] Install Core Dependencies:** Install `Docker` and `Docker Compose` on your new server.
-   **[ ] Production Database:** Set up a production-grade PostgreSQL database. Ensure you have the full connection URI (e.g., `postgresql://user:password@host:port/dbname`).
-   **[ ] Production Cache:** Set up a production Redis instance for features like price locking. Get the connection URI.
-   **[ ] DNS Configuration:**
    -   Point an `A` record for `asset-arc.com` to your server's IP address.
    -   Point a wildcard `A` record for `*.asset-arc.com` to the same IP address. This is required for the white-labeling feature.
-   **[ ] SSL Certificates:**
    -   Obtain and install an SSL certificate for `asset-arc.com` and `www.asset-arc.com`.
    -   Obtain and install a wildcard SSL certificate for `*.asset-arc.com`. Let's Encrypt is a free option for this.
-   **[ ] Third-Party Services:**
    -   Activate your **Yoco** account for live payments and obtain your production Secret Key and Webhook Secret.
    -   Activate your **AWS SES** account for sending emails and obtain your credentials.
    -   Set up **Google Cloud Secret Manager** on a GCP project.
-   **[ ] Create Production Secrets:** Using the GCP console or `gcloud` CLI, create all the secrets required by the services. Refer to the `.env.production.template` file in each service's directory for a complete list.
-   **[ ] Prepare Environment Files:**
    -   Copy the entire project code to your production server.
    -   For each of the 6 services that have a `.env.production.template` file, create a copy named `.env.production`.
    -   Fill in every variable in each `.env.production` file with your live credentials and configuration values. **Do not leave any placeholders.**

---

## Phase 2: Deployment

This phase involves pushing the code and starting the services.

-   **[ ] Build and Push Docker Images:** Follow the `DOCKER_DEPLOYMENT_GUIDE.md` to build each of the 8 backend service images and push them to your container registry.
-   **[ ] Configure Docker Compose:** Edit `docker-compose.integrated.yml` on your production server. Replace `your-registry/` and `:v1.0.0` with your actual registry URL and image tags for all 8 services.
-   **[ ] Start Backend Services:** Run the following command from the root of the project directory on your server:
    ```bash
    sudo docker compose -f docker-compose.integrated.yml up -d
    ```
-   **[ ] Verify Backend Services:** Check the logs for each container to ensure it started correctly without any errors.
    ```bash
    # Check all logs
    sudo docker compose -f docker-compose.integrated.yml logs

    # Check a specific service
    sudo docker compose -f docker-compose.integrated.yml logs eng-identity
    ```
-   **[ ] Deploy WordPress Theme:** Follow the `THEME_DEPLOYMENT_GUIDE.md` to install and activate the `assetarc-theme` on your live WordPress installation.
-   **[ ] Configure Reverse Proxy (Nginx):** Set up your Nginx configuration on the server to correctly route traffic to your WordPress instance and backend services. Use the `reverse-proxy/nginx.sample.conf` file as a reference, ensuring you implement the rules for both the main site and the white-labeling subdomains.

---

## Phase 3: Final Verification & Go-Live

This is the final check before you announce the launch.

-   **[ ] Test Main Site:** Navigate to `https://asset-arc.com` in your browser and ensure the main website loads correctly.
-   **[ ] Test User Registration:** Go through the entire user sign-up and OTP login process using a new email address.
-   **[ ] Test a Live Payment:** Perform a real, small-value transaction using the Yoco payment gateway to ensure the entire payment flow is working.
-   **[ ] Verify Transaction Recording:** Check your `eng-billing` database to confirm the test transaction was recorded in the `transactions` table and that tokens were granted.
-   **[ ] Test White-Labeling:**
    -   Manually insert a brand and an advisor linked to that brand into your `eng-identity` database.
    -   Navigate to the test brand's subdomain (e.g., `test-brand.asset-arc.com`).
    -   Confirm that the white-labeled logo appears correctly in the header.
-   **[ ] Announce Your Launch!** 🚀

Congratulations on going live!
