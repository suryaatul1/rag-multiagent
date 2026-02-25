
import os

from langchain_core.messages import SystemMessage, HumanMessage

AZURE_INFERENCE_CREDENTIAL=os.environ["GH_OPENAI_TOKEN"]
AZURE_INFERENCE_ENDPOINT="https://models.github.ai/inference"

'''
HuggingFaceEndpoint does not download the model to local , but uses Hugging Face infra to execute the prompts
HuggingFacePipeline is used to downaload the Models to local machine and execute from there

'''

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
                endpoint="https://models.github.ai/inference",
                credential=os.environ['GH_OPENAI_TOKEN'],
                #model="openai/gpt-4.1",
                model="xai/grok-3-mini",
                temperature=0.5,
                top_p=0.9
)

'''
With below you can invoke single prompt using chat schema
'''

response = model.invoke(
    [SystemMessage(content="You are AI assistant"), HumanMessage(content="Tell me about Deep Space in one line")],

)

#print(response)
print(response)

