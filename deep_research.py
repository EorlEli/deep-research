import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
import asyncio
import PyPDF2
import docx
from document_utils import extract_text_from_files

load_dotenv(override=True)

# Step 1: Get clarifying questions
def get_questions(query):
    clarifying = asyncio.run(ResearchManager().get_clarifying_questions(query))
    return clarifying.questions

# Step 2: Run full research with clarifications and files
async def run_full(query, a1, a2, a3, a4, files):
    answers = [a for a in [a1, a2, a3, a4] if a]
    async for chunk in ResearchManager().run_full(query, answers, files):
        yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    ask_button = gr.Button("Next: Clarify", variant="primary")
    questions_box = gr.Column(visible=False)
    with questions_box:
        answer1 = gr.Textbox(label="", visible=False)
        answer2 = gr.Textbox(label="", visible=False)
        answer3 = gr.Textbox(label="", visible=False)
        answer4 = gr.Textbox(label="", visible=False)
    submit_button = gr.Button("Run Research", visible=False)
    report = gr.Markdown(label="Report")
    state_query = gr.State()
    state_questions = gr.State()
    file_upload = gr.Files(label="Attach documents (PDF, DOCX, TXT)", file_types=[".pdf", ".docx", ".txt"])

    def show_questions(query):
        questions = get_questions(query)
        # Set labels and visibility for up to 4 questions
        updates = [gr.update(visible=True)]
        for i, box in enumerate([answer1, answer2, answer3, answer4]):
            if i < len(questions):
                updates.append(gr.update(visible=True, label=questions[i], value=""))
            else:
                updates.append(gr.update(visible=False, label="", value=""))
        updates.append(gr.update(visible=True))  # submit_button
        return updates

    ask_button.click(
        fn=show_questions,
        inputs=query_textbox,
        outputs=[questions_box, answer1, answer2, answer3, answer4, submit_button],
    )

    submit_button.click(
        fn=run_full,
        inputs=[query_textbox, answer1, answer2, answer3, answer4, file_upload],
        outputs=report,
    )

    query_textbox.submit(fn=show_questions, inputs=query_textbox, outputs=[questions_box, answer1, answer2, answer3, answer4, submit_button])

ui.launch(inbrowser=True)