from abc import ABC, abstractmethod


class AgentModel(ABC):

    def __init__(self,temperature=0.5, top_p=0.9, max_tokens=200 , endpoint="https://models.github.ai/inference"):
        self._temperature = temperature
        self._top_p = top_p
        self._max_tokens = max_tokens
        self._endpoint = endpoint

    @abstractmethod
    def create_model(model_name: str):
        pass

    @property
    def temperature(self):
        return self._temperature

    @property
    def top_p(self):
        return self._top_p

    @temperature.setter
    def temperature(self, temperature):
        self._temperature = temperature

    @top_p.setter
    def top_p(self, top_p):
        self._top_p = top_p

    @abstractmethod
    def get_model(self):
        pass
