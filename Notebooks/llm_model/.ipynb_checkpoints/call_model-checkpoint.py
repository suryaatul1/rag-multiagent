import os

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel


class ModelCaller:
    def __init__(self, model_name , temperature=0.5, top_p=0.9 , max_tokens=200):
        self._model_name = model_name
        self._temperature = temperature
        self._top_p = top_p
        self._max_tokens = max_tokens
        self._model=self._create_model()


    def get_model(self):
        return self._model

    def call_model(self, prompt):
        response = self._model.invoke(prompt)
        return response.content

    def _create_model(self):
        model = AzureAIChatCompletionsModel(
            endpoint="https://models.github.ai/inference",
            credential=os.environ['GH_OPENAI_TOKEN'],
            model=self._model_name,
            temperature=self._temperature,
            top_p=self._top_p,
            max_tokens=self._max_tokens
        )
        return model