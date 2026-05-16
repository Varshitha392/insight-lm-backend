import gradio as gr

def hello():
    return "Insight LM is running 🚀"

demo = gr.Interface(fn=hello, inputs=[], outputs="text")

demo.launch()