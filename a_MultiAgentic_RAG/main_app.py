import hashlib
import os
import sys
from typing import List, Dict

import gradio as gr

from project_root.workflow.agent_workflow import AgentWorkflow
from project_root.builder.retriver_builder import RetrieverBuilder
from project_root.document_processor.file_handler import DocumentProcessor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#from builder.retriver_builder import RetrieverBuilder
#from document_processor.file_handler import DocumentProcessor
#from workflow.agent_workflow import AgentWorkflow
from project_root.my_utilities.util_logging import logging
from project_root.my_configs.Setting import settings

logger = logging.getLogger('__name__')


def main():
    doc_processer = DocumentProcessor()
    retriever_builder = RetrieverBuilder()
    workflow = AgentWorkflow()

    css = """
        .title {
            font-size: 1.5em !important; 
            text-align: center !important;
            color: #FFD700; 
        }

        .subtitle {
            font-size: 1em !important; 
            text-align: center !important;
            color: #FFD700; 
        }

        .text {
            text-align: center;
        }
        """
        
    css2 = """
    .label-col { display: flex; align-items: center; justify-content: flex-end; padding-right: 12px; }
.dropdown-col { display: flex; align-items: center; }
    """


    js = """
        function createGradioAnimation() {
            var container = document.createElement('div');
            container.id = 'gradio-animation';
            container.style.fontSize = '2em';
            container.style.fontWeight = 'bold';
            container.style.textAlign = 'center';
            container.style.marginBottom = '20px';
            container.style.color = '#eba93f';

            var text = 'Welcome to DocChat 🐥!';
            for (var i = 0; i < text.length; i++) {
                (function(i){
                    setTimeout(function(){
                        var letter = document.createElement('span');
                        letter.style.opacity = '0';
                        letter.style.transition = 'opacity 0.1s';
                        letter.innerText = text[i];

                        container.appendChild(letter);

                        setTimeout(function() {
                            letter.style.opacity = '0.9';
                        }, 50);
                    }, i * 250);
                })(i);
            }

            var gradioContainer = document.querySelector('.gradio-container');
            gradioContainer.insertBefore(container, gradioContainer.firstChild);

            return 'Animation created';
        }
        """
    with gr.Blocks(theme=gr.themes.Citrus(), css=css , js=js) as demo:

        session_state = gr.State({
            "file_hashes": frozenset(),
            "retriever": None
        })


        with gr.Row():
            # Left column: upload and preview
            with gr.Column(scale=1):
                gr.Markdown("# File Upload ")
                files = gr.Files(label="Upload the files you want to chat with .. ", file_types=list(settings.ALLOWED_TYPES))

                #load_example_btn = gr.Button("Load Example 🛠️")

                with gr.Row(elem_classes="model-selection-row"):
                    with gr.Column(scale=1, elem_classes="label-col"):
                        gr.Markdown("Select your AI Models for Tasks 🧠")
                    with gr.Column(scale=3, elem_classes="dropdown-col"):
                        relevance_model = gr.Dropdown(
                            label="Select Model for relevance checks 🧠",
                            choices= ['openai/gpt-4.1',
                                      'meta/Llama-3.2-90B-Vision-Instruct',
                                      'xai/grok-3-mini',
                                      'mistral-ai/mistral-medium-2505',
                                      'openai/gpt-5'],
                            value='openai/gpt-4.1',  # initially unselected
                                                 )

                        with gr.Column(scale=2, elem_classes="dropdown-col"):
                            research_mode = gr.Dropdown(
                                label="Select Model for Research 🧠",
                                choices=['openai/gpt-4.1',
                                         'meta/Llama-3.2-90B-Vision-Instruct',
                                         'xai/grok-3-mini',
                                         'mistral-ai/mistral-medium-2505',
                                         'openai/gpt-5'],
                                value='meta/Llama-3.2-90B-Vision-Instruct',  # initially unselected
                                                    )

                        with gr.Column(scale=2, elem_classes="dropdown-col"):
                            verification_model = gr.Dropdown(
                                label="Select Model for Verification 🧠",
                                choices=['openai/gpt-4.1',
                                         'meta/Llama-3.2-90B-Vision-Instruct',
                                         'xai/grok-3-mini',
                                         'mistral-ai/mistral-medium-2505',
                                         'openai/gpt-5'],
                                value='openai/gpt-5',  # initially unselected
                                                        )


                question = gr.Textbox(label="Ask your Question ?..", lines=20, max_lines=50)

                submit_btn = gr.Button("Submit 🚀", size="sm", variant="primary", min_width=11, scale=2)

            # Right column: two textboxes and submit button (button pushed to bottom)
            with gr.Column(scale=2, elem_id="right-col"):
                with gr.Column():
                    answer = gr.Textbox(label="Answer", lines=20, max_lines=50)
                    verification = gr.Textbox(label="Verification Report", lines=20, max_lines=50)



        # connect button -> returns (right_box1, right_box2, output)

        def process_question(question_text: str, uploaded_files: List, relevance_model:str , research_mode:str ,verification_model:str ,state: Dict):
            """Handle questions with document caching."""
            logger.info (f"list of Files uploaded, {uploaded_files}")
            logger.info(f"Question received: {question_text}")
            try:
                if not question_text.strip():
                    raise ValueError("❌ Question cannot be empty")
                if not uploaded_files:
                    raise ValueError("❌ No documents uploaded")

                current_hashes = _get_file_hashes(uploaded_files)

                if state["retriever"] is None or current_hashes != state["file_hashes"]:
                    logger.info("Processing new/changed documents...")
                    chunks = doc_processer.process(uploaded_files)
                    retriever = retriever_builder.build_hybrid_retriever(chunks)

                    state.update({
                        "file_hashes": current_hashes,
                        "retriever": retriever,
                        "relevance_model": relevance_model,
                        "research_model": research_mode,
                        "verification_model": verification_model
                    })

                result = workflow.full_pipeline(
                    question=question_text,
                    retriever=state["retriever"],
                    relevance_model=state["relevance_model"],
                    research_model=state["research_model"],
                    verification_model=state["verification_model"]
                )

                return result["draft_answer"], result["verification_report"]

            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                return f"❌ Error: {str(e)}", "", state


        submit_btn.click(process_question, inputs=[question ,
                                                   files,
                                                   relevance_model ,
                                                   research_mode ,
                                                   verification_model ,
                                                   session_state] ,
                         outputs=[answer, verification])

    demo.launch()

def _get_file_hashes(uploaded_files: List) -> frozenset:
    """Generate SHA-256 hashes for uploaded files."""
    hashes = set()
    for file in uploaded_files:
        with open(file.name, "rb") as f:
            hashes.add(hashlib.sha256(f.read()).hexdigest())
    return frozenset(hashes)

if __name__ == '__main__':
    main()

