# model.py
import os
import requests
from typing import Any

MODEL_TYPE = os.getenv("MODEL_BACKEND_TYPE", "dummy").lower()

HF_API_URL = os.getenv("HF_API_URL")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")
MODEL_HTTP_ENDPOINT = os.getenv("MODEL_HTTP_ENDPOINT")


class ModelBackend:
    def __init__(self):
        self.model_type = MODEL_TYPE
        print(f"📌 Loaded MODEL_BACKEND_TYPE = {self.model_type}")

        if self.model_type == "huggingface":
            if not HF_API_URL or not HF_API_TOKEN:
                raise ValueError("HF_API_URL or HF_API_TOKEN missing in .env for huggingface backend")
            print("🚀 Using HuggingFace Inference API backend")

        elif self.model_type == "local":
            if not LOCAL_MODEL_PATH:
                raise ValueError("LOCAL_MODEL_PATH missing in .env for local backend")
            print("🚀 Using Local Model backend")

        elif self.model_type == "http":
            if not MODEL_HTTP_ENDPOINT:
                raise ValueError("MODEL_HTTP_ENDPOINT missing in .env for http backend")
            print("🚀 Using External HTTP Model Server backend")

        else:
            print("⚠️ Using DUMMY backend — no real model loading")

    def _parse_hf_response(self, response_json: Any) -> str:
        """
        Normalize common HF Inference API outputs to a simple string.
        Accepts:
         - list of {"generated_text": "..."}
         - {"generated_text": "..."}
         - {"error": "..."} (raises)
         - other dicts -> returns str()
        """
        # list case: [{ "generated_text": "..." }, ...]
        if isinstance(response_json, list) and len(response_json) > 0:
            first = response_json[0]
            if isinstance(first, dict) and "generated_text" in first:
                return first["generated_text"]
            # sometimes HF returns {"generated_text": "..."} without list
            if isinstance(first, dict) and "output" in first:
                return first["output"]
            return str(first)

        # dict with generated_text
        if isinstance(response_json, dict):
            if "generated_text" in response_json:
                return response_json["generated_text"]
            if "output" in response_json:
                return response_json["output"]
            if "error" in response_json:
                raise RuntimeError(f"HuggingFace API error: {response_json.get('error')}")
            # fallback to stringifying the dict
            return str(response_json)

        # unknown formats
        return str(response_json)

    def predict(self, prompt: str) -> dict:
        if self.model_type == "huggingface":
            headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
            payload = {"inputs": prompt}

            # Try once, if fail, raise descriptive error
            try:
                resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
            except Exception as e:
                raise RuntimeError(f"HuggingFace request failed: {e}")

            if resp.status_code >= 400:
                # include body for debugging
                body = None
                try:
                    body = resp.json()
                except Exception:
                    body = resp.text
                raise RuntimeError(f"HuggingFace API returned {resp.status_code}: {body}")

            parsed = None
            try:
                parsed = resp.json()
            except Exception:
                parsed = resp.text

            text = self._parse_hf_response(parsed)
            return {"output": text}

        elif self.model_type == "local":
            # Placeholder for local model; you can integrate transformers here
            return {"output": f"Local model placeholder. Prompt = {prompt}"}

        elif self.model_type == "http":
            try:
                r = requests.post(MODEL_HTTP_ENDPOINT, json={"prompt": prompt}, timeout=30)
                r.raise_for_status()
                j = r.json()
                # Expecting {"output": "..."} from external model
                if isinstance(j, dict) and "output" in j:
                    return {"output": j["output"]}
                return {"output": str(j)}
            except Exception as e:
                raise RuntimeError(f"HTTP model endpoint error: {e}")

        else:
            # Dummy response
            return {"output": f"Dummy response: {prompt}"}


# Create singleton instance for FastAPI imports (so main.py can do `from .model import model`)
model = ModelBackend()
