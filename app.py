from Carrerr import create_interface, custom_css
import gradio as gr

demo = create_interface()

demo.launch(theme=gr.themes.Soft(), css=custom_css)
