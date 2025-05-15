from jinja2 import Environment, FileSystemLoader
from typing import List, Dict

env = Environment(
    loader=FileSystemLoader("src/prompt_templates"),
    trim_blocks=True,
    lstrip_blocks=True
)

def format_chat_prompt(messages: List[Dict[str, str]], add_generation_prompt: bool = True, template_name="phi4_template.j2") -> str:
    template = env.get_template(template_name)
    return template.render(messages=messages, add_generation_prompt=add_generation_prompt)
