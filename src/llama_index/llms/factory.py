from .base import BaseLLM
import requests
from openai import OpenAI
import os
import json
from typing import List, Dict, Union, Generator, Optional, Any
from jinja2 import Template

def token_stream(response):
    for line in response.iter_lines():
        if line:
            data = line.decode('utf-8')
            if data.startswith("data: "):
                data = data[6:]
            try:
                json_data = json.loads(data)
                yield json_data.get("response", "")
            except Exception as e:
                print("Stream decode error:", e)

class OllamaModel(BaseLLM):
    def __init__(self, config):
        self.model = config['model']
        self.url = config['url']

    def generate(self, prompt: str, **kwargs):
        stream = kwargs.get("stream", False)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        response = requests.post(self.url, json=payload, stream=stream)
        return token_stream(response) if stream else response.json()['response']

    def chat(
        self,
        messages: List[Dict[str, str]],
        template: Optional[Union[str, Template]] = None,
        template_type: Optional[str] = None,
        add_generation_prompt: bool = True,
        **kwargs: Any
    ) -> str:
        # Case 1: Jinja2 Template object
        if isinstance(template, Template):
            prompt = template.render(messages=messages, add_generation_prompt=add_generation_prompt)

        # Case 2: Plain string with template_type = 'plain'
        elif isinstance(template, str) and template_type == "plain":
            system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
            user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
            prompt = template.format(system=system_msg, user=user_msg)

        # Case 3: Already a fully rendered prompt string
        elif isinstance(template, str) and template_type is None:
            prompt = template

        else:
            raise ValueError("Invalid template or template_type passed to chat()")

        # Call your LLM with the prompt
        return self.generate(prompt, **kwargs)

class OpenAIModel(BaseLLM):
    def __init__(self, config):
        self.model = config.get('model', 'o4-mini')
        self.api_key = os.environ.get(config['api_key_env'])
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()

class DummyLLM(BaseLLM):
    def __init__(self, config=None):
        self.model = 'Dummy' or config['model']
        self.url = 'LocalHost' or config['url']

    def generate(self, prompt: str) -> str:
        return prompt


def load_llm(config):
    provider = config["provider"]
    model_config = config[provider]
    if provider == "ollama":        
        return OllamaModel(model_config)
    elif provider == "openai":
        return OpenAIModel(model_config)
    elif provider == "dummy":
        return DummyLLM(model_config)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
