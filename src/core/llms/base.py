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

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], template: Optional[str] = None,**kwargs:Any) -> str:
        pass

    def stream(self, prompt_or_messages, **kwargs) -> Generator[str, None, None]:
        pass

    def tokenize(self, text: str) -> List[int]:
        pass

    def count_tokens(self, text_or_messages) -> int:
        pass

    def get_model_info(self) -> Dict:
        pass

    def embed(self, text: Union[str, List[str]]) -> List[float]:
        pass