from typing import Dict

from langchain_classic.retrievers import EnsembleRetriever
from langgraph.constants import END
from langgraph.graph import StateGraph

from project_root.agents.relevance_checker_agent import RelevanceChecker
from project_root.agents.research_agent import ResearchAgent
from project_root.agents.verification_agent import VerificationAgent
from project_root.workflow.agent_state import AgentState
from project_root.my_utilities.util_logging import logging


logger= logging.getLogger(__name__)


class AgentWorkflow:
    def __init__(self):
        self.relevance_checker = RelevanceChecker()
        self.researcher = ResearchAgent()
        self.verifier = VerificationAgent()
        self.compiled_workflow = self.build_workflow()  # Compile once during initialization

    def build_workflow(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("check_relevance", self._check_relevance_step)
        workflow.add_node("research", self._researcher_step)
        workflow.add_node("verify", self._verification_step)

        # Define edges
        workflow.set_entry_point("check_relevance")
        workflow.add_conditional_edges(
            "check_relevance",
            self._decide_after_relevance_check,
            {
                "relevant": "research",
                "irrelevant": END
            }
        )
        workflow.add_edge("research", "verify")
        workflow.add_conditional_edges(
            "verify",
            self._decide_next_step,
            {
                "re_research": "research",
                "end": END
            }
        )
        return workflow.compile()

    def full_pipeline(self, question: str, retriever: EnsembleRetriever,  relevance_model:str,
                    research_model:str,
                    verification_model:str):
        try:
            print(f"[DEBUG] Starting full_pipeline with question='{question}'")
            documents = retriever.invoke(question , top_k=20)
            logger.info(f"Retrieved {len(documents)} relevant documents (from .invoke)")

            initial_state = AgentState(
                question=question,
                documents=documents,
                draft_answer="",
                verification_report="",
                is_relevant=False,
                retriever=retriever,
                relevance_model = relevance_model,
                research_model = research_model,
                verification_model=verification_model
            )

            final_state = self.compiled_workflow.invoke(initial_state)

            return {
                "draft_answer": final_state["draft_answer"],
                "verification_report": final_state["verification_report"]
            }
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            raise

    def _check_relevance_step(self, state: AgentState ) -> Dict:
        retriver = state['retriever']
        question = state['question']
        self.relevance_checker.create_model(state['relevance_model'])
        classification = self.relevance_checker.check(question, retriver)

        if classification == "CAN_ANSWER":
            return {"is_relevant": True}
        elif classification == "PARTIAL":
            return {"is_relevant": True}
        else:
            return {"is_relevant": False,
                     "draft_answer": "This question isn't related (or there's no data) for your query. Please ask another question relevant to the uploaded document(s)."
                    }

    def _researcher_step(self, state: AgentState ) -> Dict:
        question = state['question']
        retriver = state['retriever']
        self.researcher.create_model(state['research_model'])
        result = self.researcher.generate(question, retriver , top_k=20)
        return {"draft_answer": result['draft_answer'],
                "documents": result['retrieved_docs']}

    def _verification_step(self, state: AgentState) -> Dict:

        draft_answer = state['draft_answer']
        documents = state['documents']
        self.verifier.create_model(state['verification_model'])
        verification_result = self.verifier.check(draft_answer, documents)
        return {"verification_report": verification_result}


    def _decide_after_relevance_check(self, state: AgentState) -> str:
        decision = "relevant" if state["is_relevant"] else "irrelevant"
        print(f"[DEBUG] _decide_after_relevance_check -> {decision}")
        return decision

    def _decide_next_step(self, state: AgentState) -> str:
        verification_report = state["verification_report"]
        print(f"[DEBUG] _decide_next_step with verification_report='{verification_report}'")
        if "Supported: NO" in verification_report or "Relevant: NO" in verification_report:
            logger.info("[DEBUG] Verification indicates re-research needed.")
            return "re_research"
        else:
            logger.info("[DEBUG] Verification successful, ending workflow.")
            return "end"