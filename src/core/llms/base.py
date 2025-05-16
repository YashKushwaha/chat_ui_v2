from abc import ABC, abstractmethod
from typing import List, Dict, Union, Generator, Optional, Any

'''
The BaseLLM implementation ensures that code can work with prompts
as well as list of messages
'''

class BaseLLM(ABC):

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass