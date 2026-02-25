from pathlib import Path

from a_MultiAgentic_RAG.project_root.document_processor import DocumentProcessor
files= [Path("project_root/test_docling/docs/sample.png") , Path("project_root/test_docling/docs/ocr_test.pdf")]
#files= [Path("./test_docling/docs/sample.png") ]

doc_processer = DocumentProcessor()
chunks = doc_processer.process(files)
if not chunks:
    print("No valid chunks were processed from the provided files.")
    print(type(chunks))
    print("No chunks to display.")
else:
    for i, chunk in enumerate(chunks):
        print(f"Chunk{i + 1}:\n{chunk}\n{'-' * 80}")
        #print( f"Chunk{i+1}:\n{chunk.page_content}\n{'-'*80}")


    # embeddor = RetrieverBuilder()
    # retriever = embeddor.build_hybrid_retriever(chunks)
    # query = "What is the document contain details about Quantitative Results ?"
    # results = retriever.invoke(query)
    # print(f"Retrieved {len(results)} relevant documents (from .invoke) and content:{results[0].page_content}")



