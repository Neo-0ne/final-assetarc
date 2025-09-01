#!/usr/bin/env python3
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Service folders may live directly under the repo root in some distributions
# or inside a dedicated "services" directory.  Fall back to the root if the
# "services" folder is missing so the generator still works.
SERVICES = ROOT / "Services"
if not SERVICES.exists():
    SERVICES = ROOT

OUT = ROOT / "docker-compose.integrated.yml"
GLOBAL_ENV = ROOT / ".env.global"

# Default ports for known services (override by .env.example PORT or hard-coded app.py)
default_ports = {
  "eng-identity": 5000,
  "eng-drafting": 5001,
  "eng-vault": 5002,
  "eng-billing": 5003,
  "eng-compliance": 5004,
  "eng-lifecycle": 5005,
  "eng-engagement": 5006,
  "eng-analytics": 5007
}

def sniff_service_root(pdir: Path):
    # find the code root folder (one that contains app.py / requirements.txt)
    candidates = []
    for sub in pdir.iterdir():
        if sub.is_dir() and (sub / "app.py").exists() and (sub / "requirements.txt").exists():
            candidates.append(sub)
    if candidates:
        # Prefer folder names starting with assetarc-
        for c in candidates:
            if c.name.startswith("assetarc-"):
                return c
        return candidates[0]
    return None

def derive_port(pdir: Path, service_root: Path):
    # Try .env.example's PORT, otherwise default table.
    envex = service_root / ".env.example"
    if envex.exists():
        for line in envex.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip().startswith("PORT="):
                try:
                    return int(line.strip().split("=",1)[1])
                except Exception:
                    pass
    return default_ports.get(pdir.name, None)

def load_global_env():
    out = {}
    if (GLOBAL_ENV).exists():
        for line in GLOBAL_ENV.read_text(encoding="utf-8").splitlines():
            line=line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k,v = line.split("=",1)
            out[k.strip()] = v.strip()
    return out

def upsert_envfile(target: Path, inject: dict):
    lines = []
    existing = {}
    if target.exists():
        for line in target.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k,v = line.split("=",1); existing[k]=v
            lines.append(line)
    for k,v in inject.items():
        if k in existing: continue
        lines.append(f"{k}={v}")
    target.write_text("\n".join(lines)+("\n" if lines and not lines[-1].endswith("\n") else ""), encoding="utf-8")

def main():
    globs = load_global_env()
    services = {}
    for p in sorted(SERVICES.iterdir(), key=lambda p: p.name):
        if not p.is_dir():
            continue
        sroot = sniff_service_root(p)
        if not sroot:
            continue
        port = derive_port(p, sroot)
        name = p.name
        envfile = sroot / ".env"
        # inject shared vars (non-destructive)
        inject = {}
        for k in (
            "JWT_SECRET",
            "COOKIE_DOMAIN",
            "COOKIE_SECURE",
            "CORS_ALLOWED_ORIGINS",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "S3_REGION",
            "S3_BUCKET",
            "SES_REGION",
            "SES_FROM_EMAIL",
            "OPENAI_API_KEY",
            "DEFAULT_MODEL",
            "YOCO_SECRET_KEY",
            "NOWPAYMENTS_API_KEY",
            "CALENDLY_ORG_URI",
            "GOOGLE_SERVICE_ACCOUNT_JSON_PATH",
            "GCP_PROJECT_ID",
            "ENG_IDENTITY_URL",
            "ENG_DRAFTING_URL",
            "ENG_VAULT_URL",
            "ENG_BILLING_URL",
            "ENG_COMPLIANCE_URL",
            "ENG_LIFECYCLE_URL",
            "ENG_ENGAGEMENT_URL",
            "ENG_ANALYTICS_URL",
        ):
            if k in globs:
                inject[k] = globs[k]
        upsert_envfile(envfile, inject)

        dockerfile_path = sroot.relative_to(ROOT) / "Dockerfile"
        service_config = {
            "build": {
                "context": ".",
                "dockerfile": str(dockerfile_path)
            },
            "container_name": name,
            "env_file": [str(envfile)],
            "restart": "unless-stopped",
        }

        gcp_creds_path = os.getenv('GCP_CREDS_PATH')
        if gcp_creds_path and os.path.exists(gcp_creds_path):
            service_config["volumes"] = [f"{gcp_creds_path}:/etc/gcloud/credentials.json:ro"]
            service_config["environment"] = {"GOOGLE_APPLICATION_CREDENTIALS": "/etc/gcloud/credentials.json"}

        if port:
            service_config["ports"] = [f"{port}:{port}"]

        services[name] = service_config

    compose = {"version": "3.9", "services": services}
    OUT.write_text(yaml.safe_dump(compose, sort_keys=True), encoding="utf-8")
    print(f"Wrote {OUT} with {len(services)} services.")

if __name__ == "__main__":
    try:
        import yaml  # type: ignore
    except Exception:
        print(
            "ERROR: PyYAML not available in your host Python. Install with: pip install pyyaml"
        )
        sys.exit(1)
    main()
