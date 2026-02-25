# from a_MultiAgentic_RAG.agents.relevance_checker_agent import RelevanceChecker
#
#
#
# from pathlib import Path
#
# from a_MultiAgentic_RAG.builder.retriver_builder import RetrieverBuilder
# from a_MultiAgentic_RAG.document_processor.file_handler import DocumentProcessor
# files= [Path("/Users/suryaatul/PythonWorkspace/AgenticAI/a_MultiAgentic_RAG/test_docling/docs/sample.png") , Path("/Users/suryaatul/PythonWorkspace/AgenticAI/a_MultiAgentic_RAG/test_docling/docs/ocr_test.pdf") ]
# #files= [Path("./test_docling/docs/sample.png") ]
#
# doc_processer = DocumentProcessor()
# chunks = doc_processer.process(files)
# if not chunks:
#     print("No valid chunks were processed from the provided files.")
#     raise  ValueError("No chunks to display.")
#
# embedded = RetrieverBuilder()
# retriever = embedded.build_hybrid_retriever(chunks)
#
#
# obj=RelevanceChecker()
# obj.temperature=0.2
# obj.create_model("openai/gpt-4.1")
#
# response= obj.check("what is hyper parameter optimization?" , retriever , top_k=5)
# print(response)




# Entry point script for running the relevance-checking flow

# import the RelevanceChecker agent used to run the final query
from a_MultiAgentic_RAG.project_root.agents.relevance_checker_agent import RelevanceChecker

# Path helps construct file paths for documents to process
from pathlib import Path

from a_MultiAgentic_RAG.project_root.agents.research_agent import ResearchAgent
from a_MultiAgentic_RAG.project_root.agents.verification_agent import VerificationAgent
# Builder to create the hybrid retriever from chunks
from a_MultiAgentic_RAG.project_root.builder.retriver_builder import RetrieverBuilder
# Processor that reads files, converts and splits into chunks
from a_MultiAgentic_RAG.project_root.document_processor import DocumentProcessor

# List of files to process into chunks. Paths use absolute locations on the developer machine.
# files = [
#     Path("/Users/suryaatul/PythonWorkspace/AgenticAI/a_MultiAgentic_RAG/test_docling/docs/sample.png"),
#     Path("/Users/suryaatul/PythonWorkspace/AgenticAI/a_MultiAgentic_RAG/test_docling/docs/ocr_test.pdf")
# ]
# alternative relative path example (commented out)
files = [Path("/a_MultiAgentic_RAG/project_root/test_docling/docs/sample.png")]

# Create the document processor and run processing -> returns list of text chunks
doc_processer = DocumentProcessor()
chunks = doc_processer.process(files)

# If no chunks were produced, print and raise to halt execution early
if not chunks:
    print("No valid chunks were processed from the provided files.")
    raise ValueError("No chunks to display.")

# Build a hybrid retriever from the processed chunks (embeddings + metadata)
embedded = RetrieverBuilder()
retriever = embedded.build_hybrid_retriever(chunks)

# Instantiate the relevance checker agent, set a low temperature for deterministic output
obj = RelevanceChecker()
obj.temperature = 0.2
# Create/load the model used by the agent (example model name)
obj.create_model("openai/gpt-4.1")

# Run the relevance check query against the retriever, request top_k results
response = obj.check("what is hyper parameter optimization?", retriever, top_k=5)
# Print the agent's response
if response == "NO_MATCH":
    print("The agent determined that there are no relevant documents to answer the question.")
else:
    print(f"The agent determined the relevance as: {response}" )
    research_agent= ResearchAgent()
    research_agent.temperature=0.2
    research_agent.create_model()
    response= research_agent.generate("what is hyper parameter optimization?" , retriever , top_k=5)
    print(response)


obj=VerificationAgent()
obj.temperature=0.2
#obj.create_model("mistral-ai/mistral-medium-2505")
obj.create_model("openai/gpt-4.1")
response = obj.check(response['draft_answer'], response['retrieved_docs'])
print(f"Final Response: {response}")

