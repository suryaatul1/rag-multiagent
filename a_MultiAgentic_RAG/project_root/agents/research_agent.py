import os

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate

from project_root.agents.abs_agent_model import AgentModel
from project_root.my_utilities.util_logging import logging

logger= logging.getLogger(__name__)


class ResearchAgent(AgentModel):


    def __init__(self):

        super().__init__()
        self._model = None



    def create_model(self, model_name: str = "meta/Llama-3.2-90B-Vision-Instruct"):
        try:
            model = AzureAIChatCompletionsModel(
                endpoint=self._endpoint,
                credential=os.environ['GH_OPENAI_TOKEN'],
                model=model_name,
                temperature=self._temperature,
                top_p=self._top_p,
                max_tokens=self._max_tokens
            )
            self._model= model
        except Exception as e:
            print(f"Error creating model: {e}")


    def get_model(self):
        return self._model

    def _generate_prompt(self, question: str, context: str) -> PromptValue:
        """
        Generate a structured prompt for the LLM to generate a precise and factual answer.
        """
        template_prompt = """
        You are an writing assistant and expert content designer to provide precise and factual answers based on the given context.

        **Instructions:**
        - Answer the following question using only the provided context.
        - Be clear, concise, and factual.
        - Return as much information as you can get from the context.
        - Add citations for all the content provided to prove the authenticity. At the end of the answer
        - Include a "Citations" section where you list the sources of your information in the format: [Document Title or Identifier or Name of the Document].
        

        **Question:** {question}
        **Context:**
        {context}

        **Provide your answer below:**
        **Provide the citations for answer generated below:**
        """

        prompt = PromptTemplate.from_template(template_prompt)
        formatted_prompt = prompt.format_prompt(
            question=question,
            context=context
        )

        return formatted_prompt

    def generate(self , question:str , retriever , top_k=5):
        relevant_docs = retriever.invoke(question, top_k=top_k)

        if not relevant_docs:
            return "NO content generated"  # No relevant documents found, so it cannot answer the question

        relevant_docs_content = "\n".join([doc.page_content for doc in relevant_docs])

        formatted_prompt = self._generate_prompt(question, relevant_docs_content)


        try:
            response = self._model.invoke([
                                     {"role": "user",
                                      "content": formatted_prompt.to_string()}
                                        ])
        except Exception as ex:
            print(f"Error invoking model: {ex}")
            return "NO content generated"


        try:
            draft_answer = response.content.strip()
        except Exception as ex:
            logger.error(f"Error processing model response: {ex}")
            return "No content generated"

        logger.info(f"LLM response : {draft_answer}")

        return {"draft_answer": draft_answer,
                "retrieved_docs": relevant_docs}
