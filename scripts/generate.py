#!/usr/bin/env python3
"""Nano Banana Pro - Image generation via Google Generative AI API."""

import argparse
import base64
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API_KEY = os.environ.get("GOOGLE_AI_API_KEY")
BASE_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"

MODELS = {
    "nano-banana-pro": "nano-banana-pro-preview",
    "gemini-2.5-flash": "gemini-2.5-flash-image",
    "gemini-2.0-flash": "gemini-2.0-flash-exp",
}


def generate_image(prompt: str, output_path: str, model: str = "nano-banana-pro") -> str:
    """Generate an image from a text prompt. Returns the output file path."""
    if not API_KEY:
        print("ERROR: GOOGLE_AI_API_KEY not set in environment.", file=sys.stderr)
        print("Get your free key at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)

    model_id = MODELS.get(model, model)
    url = f"{BASE_ENDPOINT}/{model_id}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["image", "text"]}
    }

    req = Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
    except HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"ERROR: API returned {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    candidates = data.get("candidates", [])
    if not candidates:
        print("ERROR: No candidates in response", file=sys.stderr)
        print(json.dumps(data, indent=2), file=sys.stderr)
        sys.exit(1)

    parts = candidates[0].get("content", {}).get("parts", [])
    for part in parts:
        if "inlineData" in part:
            img_data = base64.b64decode(part["inlineData"]["data"])
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(img_data)
            print(f"OK: {out} ({len(img_data)} bytes, model: {model_id})")
            return str(out)

    print("ERROR: No image data in response", file=sys.stderr)
    sys.exit(1)


def open_in_preview(path: str):
    """Open image in default viewer (macOS Preview / Linux xdg-open)."""
    import platform
    if platform.system() == "Darwin":
        subprocess.run(["open", path], check=False)
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", path], check=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate image with Nano Banana Pro")
    parser.add_argument("prompt", help="The image generation prompt")
    parser.add_argument("-o", "--output", default="output.png", help="Output file path")
    parser.add_argument("-m", "--model", default="nano-banana-pro",
                        choices=list(MODELS.keys()),
                        help="Model to use (default: nano-banana-pro)")
    parser.add_argument("--open", action="store_true", help="Open in viewer after generating")
    args = parser.parse_args()

    result = generate_image(args.prompt, args.output, args.model)
    if args.open and result:
        open_in_preview(result)
