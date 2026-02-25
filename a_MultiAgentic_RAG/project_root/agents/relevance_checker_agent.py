import os

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.prompts import PromptTemplate

from project_root.agents.abs_agent_model import AgentModel
from project_root.my_utilities.util_logging import logging

logger= logging.getLogger(__name__)


class RelevanceChecker(AgentModel):


    def __init__(self):

        super().__init__()
        self._model = None


    def create_model(self, model_name: str = "openai/gpt-4.1"):
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

    def check(self , question:str , retriever , top_k=5):
        relevant_docs = retriever.invoke(question, top_k=top_k)

        if not relevant_docs:
            return "NO_MATCH"  # No relevant documents found, so it cannot answer the question

        relevant_docs_content = "\n".join([doc.page_content for doc in relevant_docs])

        template_string= """
        You are an expert relevance checker , that checks the relevance between a user's question and provided document content.

        **Instructions:**
        - Classify how well the document content addresses the user's question.
        - Respond with only one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH.
        - Do not include any additional text or explanation or any summarization.

        **Labels:**
        1) "CAN_ANSWER": The passages the or content passed contain enough explicit information to fully answer the question.
        2) "PARTIAL": The passages or the content passed mention or discuss the question's topic but do not provide all the details needed for a complete answer.
        3) "NO_MATCH": The passages or the content passed do not discuss or mention the question's topic at all.

        **Important:** If the passages mention or reference the topic or timeframe of the question in any way, even if incomplete, respond with "PARTIAL" instead of "NO_MATCH".

        **Question:** {question}
        **Passages:** {document_content}

        **Respond ONLY with one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH**
        """
        prompt = PromptTemplate.from_template(template_string)
        formatted_prompt= prompt.format_prompt(
            question=question,
            document_content=relevant_docs_content
        )


        try:
            response = self._model.invoke([
                                     {"role": "user",
                                      "content": formatted_prompt.to_string()}
                                        ])
        except Exception as ex:
            print(f"Error invoking model: {ex}")
            return "NO_MATCH"


        try:
            response_label = response.content.strip().upper()
            if response_label not in ["CAN_ANSWER", "PARTIAL", "NO_MATCH"]:
                logger.info(f"Unexpected model response: {response.content}")
                return "NO_MATCH"
        except Exception as ex:
            logger.error(f"Error processing model response: {ex}")
            return "NO_MATCH"

        logger.info(f"LLM response : {response_label}")

        return response_label
