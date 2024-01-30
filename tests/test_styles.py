import json
import unittest
from collections.abc import Mapping, Sequence
from typing import Any

import requests
from horde_sdk.ai_horde_api.apimodels import ImageGenerateAsyncRequest, ImageGenerationInputPayload


def get_github_json_file(url: str) -> dict[str, Any]:
    response = requests.get(url, headers={"Accept": "application/vnd.github.raw+json"})
    response.raise_for_status()
    return response.json()


def recursive_update(target: dict[str, Any], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, Mapping):
            recursive_update(target.setdefault(key, {}), value)  # type: ignore
        elif isinstance(value, Sequence):
            target.setdefault(key, []).extend(value)
        else:
            target[key] = value


class TestStyles(unittest.TestCase):
    def setUp(self):
        with open("styles.json", "r", encoding="utf-8") as file:
            self.styles: dict[str, dict[str, Any]] = json.load(file)
        with open("enhancements.json", "r", encoding="utf-8") as file:
            self.enhancements: dict[str, dict[str, Any]] = json.load(file)
        self.model_reference: dict[str, dict[str, Any]] = get_github_json_file(
            "https://api.github.com/repos/Haidra-Org/AI-Horde-image-model-reference/contents/stable_diffusion.json"
        )

    @staticmethod
    def validate_request(request: dict[str, ImageGenerationInputPayload | Any]) -> None:
        ImageGenerateAsyncRequest.model_validate(request, strict=True)

    def style_to_request(self, style: dict[str, Any]) -> dict[str, ImageGenerationInputPayload | Any]:
        with self.subTest(msg="Validate prompt"):
            prompt = style.pop("prompt")
            if "###" not in prompt and "{np}" in prompt:
                prompt = prompt.replace("{np}", "###{np}")

            # The negative prompt is greedy
            positive_prompt, *negative_prompt = prompt.split("###")
            negative_prompt = "###".join(negative_prompt) or None
            del prompt

            self.assertIn("{p}", positive_prompt, msg="Positive prompt must contain {p}")
            self.assertNotIn("{np}", positive_prompt, msg="Positive prompt must not contain {np}")
            if negative_prompt is not None:
                self.assertIn("{np}", negative_prompt, msg="Negative prompt must contain {np}")
                self.assertNotIn("{p}", negative_prompt, msg="Negative prompt must not contain {p}")

        request = {
            "prompt": positive_prompt + (f"###{negative_prompt}" if negative_prompt else ""),
            "params": {},
        }
        if style.pop("enhance", False):
            with self.subTest(msg="Validate enhancement"):
                model = style["model"]
                baseline = self.model_reference[model]["baseline"]
                enhancements = self.enhancements[baseline]
                recursive_update(style, enhancements)
        if "model" in style:
            request["models"] = [style.pop("model")]

        with self.subTest(msg="Convert to request"):
            request_fields = set(ImageGenerateAsyncRequest.model_fields.keys())
            params_fields = set(ImageGenerationInputPayload.model_fields.keys())
            for field, value in style.items():
                if field in params_fields:
                    request["params"][field] = value
                elif field in request_fields:
                    request[field] = value
                else:
                    raise KeyError(f"Unknown field: {field}")

        if not request["params"]:
            del request["params"]

        return request

    def test_enhancements(self) -> None:
        base_request = {
            "prompt": "{p}",
            "models": [],
        }
        for enhancement_name, enhancement in self.enhancements.items():
            with self.subTest(enhancement=enhancement_name):
                request = self.style_to_request(base_request | enhancement)
                self.validate_request(request)

    def test_styles(self) -> None:
        for style_name, style in self.styles.items():
            with self.subTest(style=style_name):
                request = self.style_to_request(style)
                self.validate_request(request)
