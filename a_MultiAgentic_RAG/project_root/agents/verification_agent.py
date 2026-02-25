import os
from typing import List, Dict

from langchain_core.documents import Document
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel


from project_root.agents.abs_agent_model import AgentModel
from project_root.agents.verification_class import VerificationClass
from project_root.my_utilities.util_logging import logging

logger= logging.getLogger(__name__)


class VerificationAgent(AgentModel):

    def __init__(self):

        super().__init__()
        self._model = None

    def create_model(self, model_name: str = "xai/grok-3-mini"):
        try:
            model = AzureAIChatCompletionsModel(
                endpoint=self._endpoint,
                credential=os.environ['GH_OPENAI_TOKEN'],
                model=model_name,
                temperature=self._temperature,
                top_p=self._top_p,
                max_tokens=self._max_tokens
            )
            self._model = model
        except Exception as e:
            print(f"Error creating model: {e}")

    def get_model(self):
        return self._model

    def _generate_prompt(self, answer: str, context: str) -> PromptValue:


        """
        Generate a structured prompt for the LLM to verify the answer against the context.
        """

        schema_json = { k: v for k , v in VerificationClass.schema().items()}
        schema= {"properties": schema_json['properties'] , "required": schema_json['required']}

        prompt_template = """
        You are an AI assistant designed to verify the accuracy and relevance of answers based on provided context.
        Your response should be in a valid JSON  that conforms to the following schema and stricly and only surrounded by triple backticks.
        ```
        {schema}
        ```

        **Instructions:**
        - Verify the following answer against the provided context.
        - Check for:
        1. Direct/indirect factual support (YES/NO)
        2. Unsupported claims (list any if present)
        3. Contradictions (list any if present)
        4. Relevance to the question (YES/NO)
        - Provide additional details or explanations where relevant in the above mentioned .
        - Respond in the JSON format.
        - Return only valid JSON, with no explanations or commentary before or after the JSON object
        - Do not include any text outside the JSON object. 
        - Only output the JSON valid object as specified in the format above, with no additional text, markdown, or formatting.
        - Do not include any extraneous characters, punctuation, or formatting outside of the JSON object. 
        - The response should be a single, clean JSON object that can be parsed without errors.
        - Use double quotes for all keys and string values in the JSON response, and ensure that the JSON is properly formatted and valid.

        **Answer:** {answer}
        **Context:**
        {context}
        
        ***Response should be in a valid JSON  that conforms to the following schema  and only surrounded by triple backticks ``` strictly ***

        """

        # prompt_template = """
        # You are an AI assistant designed to verify the accuracy and relevance of answers based on provided context.
        # Your response should be in a valid JSON format that conforms to the following schema:
        # {schema}
        #     ```
        #     {{
        #     "Supported": YES/NO
        #     "Unsupported Claims": [item1, item2, ...]
        #     "Contradictions": [item1, item2, ...]
        #     "Relevant": YES/NO
        #     "Additional Details": [Any extra information or explanations]
        #     }}
        #     ```
        #
        # **Instructions:**
        # - Verify the following answer against the provided context.
        # - Check for:
        # 1. Direct/indirect factual support (YES/NO)
        # 2. Unsupported claims (list any if present)
        # 3. Contradictions (list any if present)
        # 4. Relevance to the question (YES/NO)
        # - Provide additional details or explanations where relevant in the above mentioned .
        # - Respond in the JSON format.
        # - Return only valid JSON, with no explanations or commentary before or after the JSON object
        # - Do not include any text outside the JSON object.
        # - Only output the JSON valid object as specified in the format above, with no additional text, markdown, or formatting.
        # - Do not include any extraneous characters, punctuation, or formatting outside of the JSON object.
        # - The response should be a single, clean JSON object that can be parsed without errors.
        #
        # **Answer:** {answer}
        # **Context:**
        # {context}
        #
        # """

        prompt = PromptTemplate.from_template(prompt_template)
        formatted_prompt = prompt.format_prompt(
            schema=schema,
            answer=answer,
            context=context
        )

        return formatted_prompt

    def check(self, answer: str, documents: List[Document]) ->str | Dict:


        context = "\n\n".join([doc.page_content for doc in documents])
        formatted_prompt = self._generate_prompt(answer, context)
        print("Prompt created for the LLM.")

        try:
            response = self._model.invoke([
                                     {"role": "user",
                                      "content": formatted_prompt.to_string()}
                                        ])
        except Exception as ex:
            print(f"Error invoking model: {ex}")
            return "Cannot perform verification"


        try:
            draft_answer = response.content.strip()
            logger.info(f"LLM response : {draft_answer}")
            parse_llm_response = self._parse_llm_response(draft_answer.strip("```json").strip("```"))
        except Exception as ex:
            logger.error(f"Error processing model response: {ex}")
            return """"
                "**Supported**": "NO",
                "**Unsupported Claims**": [],
                "**Contradictions**": [],
                "**Relevant**": "NO",
                "**Additional Details**": "Invalid response structure from the model."
                """


        return parse_llm_response

    def _parse_llm_response(self, draft_answer):
        try:
            import json
            parsed_response = json.loads(draft_answer)
            formatted_string = "\n".join(f"{key}={value}" for key, value in parsed_response.items())
            return formatted_string

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LLM response as JSON: {e}")
            return None
