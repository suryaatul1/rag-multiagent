from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os


def parse_with_docling(file_path):

    try :
        if not os.path.exists(file_path):
            raise FileNotFoundError("File does not exists")

        converter = DocumentConverter()
        markdown_document = converter.convert(file_path).document.export_to_markdown()

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        # Initialize Markdown Splitter
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        docs_list = markdown_splitter.split_text(markdown_document)

        # Print full extracted sections
        print("\n✅ Full Extracted Content (Docling):")
        for idx, doc in enumerate(docs_list):
            print(f"\n🔹 Section {idx + 1}:\n{doc}\n" + "-"*80)

        return docs_list
    except Exception as ex:
        print(f"Error: {str(ex)}")
        return []


def main():

    pdf_path = "docs/ocr_test.pdf"
    ocr_path = "docs/sample.png"

    print("\n🔍 Running Docling Extraction for OCR...")
    docling_docs = parse_with_docling(ocr_path)


    # print("\n🔍 Running Docling Extraction for scanned PDF...")
    # docling_docs = parse_with_docling(pdf_path)



if __name__ == '__main__':
    main()