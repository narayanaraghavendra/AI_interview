import gradio as gr
from graph import run_graph
from stt import speech_to_text
from ocr import extract_text_from_image
from ppt_parser import extract_ppt_text
from scoring import confidence_score, depth_score, plot_metrics

state = {
    "responses": [],
    "confidence": [],
    "depth": []
}

def start_interview(image, audio, ppt):
    screen_text = extract_text_from_image(image) if image else ""
    speech_text = speech_to_text(audio) if audio else ""
    slide_text = extract_ppt_text(ppt) if ppt else ""

    question, _ = run_graph(screen_text, speech_text + slide_text, None, state)
    return question

def submit_answer(answer):
    question, metrics = run_graph("", "", answer, state)
    return question, metrics

with gr.Blocks() as demo:
    gr.Markdown("## 🎓 AI Adaptive Interviewer")

    img = gr.Image(type="filepath", label="Screen Image")
    aud = gr.Audio(sources=["microphone"], type="filepath", label="Recording")
    ppt = gr.File(label="PPT / PDF")

    q = gr.Textbox(label="AI Question")
    ans = gr.Textbox(label="Your Answer")
    plot = gr.Plot(label="Confidence & Depth")

    gr.Button("Start").click(start_interview, [img, aud, ppt], q)
    gr.Button("Submit Answer").click(submit_answer, ans, [q, plot])

demo.launch()