import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
#model ="meta/Llama-4-Maverick-17B-128E-Instruct-FP8"
#model ="meta/Meta-Llama-3.1-405B-Instruct"
#model ="xai/grok-3"
#model="openai/gpt-5-mini"
token = os.environ["GH_OPENAI_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("Tell me about Deep space?"),
    ],
    model=model
)

#print(response)
print(response.choices[0].message.content)