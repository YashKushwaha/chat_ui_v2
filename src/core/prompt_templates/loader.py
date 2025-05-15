from jinja2 import Environment, FileSystemLoader
from typing import List, Dict
import os
from src.prompt_templates.registry import TEMPLATE_MAP

env = Environment(
    loader=FileSystemLoader("src/prompt_templates"),
    trim_blocks=True,
    lstrip_blocks=True
)

def load_template(template_name: str, messages: List[Dict[str, str]], add_generation_prompt=True) -> str:
    template_info = TEMPLATE_MAP[template_name]
    file = template_info["file"]
    t_type = template_info["type"]

    if t_type == "jinja":
        template = env.get_template(file)
        return template.render(messages=messages, add_generation_prompt=add_generation_prompt)

    elif t_type == "plain":
        with open(os.path.join("src/prompt_templates", file)) as f:
            template_str = f.read()
        # Simple logic for plain template
        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
        return template_str.format(system=system_msg, user=user_msg)

    else:
        raise ValueError(f"Unsupported template type: {t_type}")
