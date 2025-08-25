# Docker Deployment Guide for Backend Services

This guide provides the steps to build the Docker images for the 8 backend services, push them to a container registry, and configure Docker Compose to use them in a production environment.

---

## Prerequisites

-   You have a container registry (e.g., [Docker Hub](https://hub.docker.com/), [Google Artifact Registry](https://cloud.google.com/artifact-registry), [Amazon ECR](https://aws.amazon.com/ecr/)).
-   You are authenticated to your container registry. For most registries, you can log in via the command line:
    ```bash
    docker login your-registry-url
    ```

---

## Step 1: Build, Tag, and Push Service Images

For each of the 8 backend services (`eng-identity`, `eng-billing`, etc.), you need to build a Docker image, tag it with your registry's URL, and then push it.

Here is a template command. You will need to replace `your-registry/` with your registry's namespace/URL and `v1.0.0` with your desired version tag.

**Run these commands from the root of the project repository.**

```bash
# Replace 'your-registry/' and 'v1.0.0' with your details.
# Repeat this process for all 8 services.

# Example for eng-identity:
docker build -f Services/eng-identity/app/Dockerfile -t your-registry/eng-identity:v1.0.0 .
docker push your-registry/eng-identity:v1.0.0

# Example for eng-billing:
docker build -f Services/eng-billing/app/Dockerfile -t your-registry/eng-billing:v1.0.0 .
docker push your-registry/eng-billing:v1.0.0

# ... and so on for:
# - eng-compliance
# - eng-drafting
# - eng-engagement
# - eng-lifecycle
# - eng-analytics
# - eng-vault
```

---

## Step 2: Using the Images in Production

The `docker-compose.integrated.yml` file in the repository has been updated to use images from a registry instead of building them locally.

Before you run `sudo docker compose -f docker-compose.integrated.yml up -d` on your production server, you must:

1.  **Edit the `docker-compose.integrated.yml` file.**
2.  **Replace all instances of `your-registry/`** with your actual registry's URL/namespace.
3.  **Replace all instances of `:v1.0.0`** with the version tag you used when pushing the images.

This setup ensures that your production environment pulls the exact, pre-built images you tested and pushed, leading to more reliable and consistent deployments.
