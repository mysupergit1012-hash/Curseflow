"""Minimal Vercel entrypoint for the Curseflow repository.

The desktop webcam controller cannot run inside Vercel's serverless runtime,
so this endpoint documents the limitation instead of attempting to start the
GUI application.
"""

import json


def app(environ, start_response):
    payload = {
        "name": "Curseflow",
        "deployable": False,
        "reason": (
            "Curseflow is a desktop Python app that needs webcam access, a GUI "
            "window, and OS-level mouse control. Vercel only runs web/serverless "
            "code."
        ),
        "desktop_entrypoint": "curseflow.py",
    }
    body = json.dumps(payload, indent=2).encode("utf-8")
    headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ]
    start_response("200 OK", headers)
    return [body]
