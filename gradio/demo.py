import gradio as gr
import requests
import json

def face_liveness(frame):
    url = "http://127.0.0.1:8000/api/liveness"
    files = None
    if frame is None:
        return ['', None]

    files = {'image': open(frame, 'rb')}
    r = requests.post(url=url, files=files)
    return r.json()

with gr.Blocks() as demo:
    gr.Markdown(
        """
    # Face Liveness Detection
    Get your own Face Liveness Detection Server by duplicating this space.<br/>
    Contact us at contact@faceonlive.com for issues and support.<br/>
    """
    )
    with gr.Row():
        with gr.Column(scale=5):
            image_input = gr.Image(type='filepath')
            gr.Examples(['gradio/examples/1.jpg', 'gradio/examples/2.jpg', 'gradio/examples/3.jpg', 'gradio/examples/4.jpg'], 
                            inputs=image_input)
            face_liveness_button = gr.Button("Check Liveness")
        with gr.Column(scale=5):
            liveness_result_output = gr.JSON()
    
    face_liveness_button.click(face_liveness, inputs=image_input, outputs=liveness_result_output)

demo.launch(server_name="0.0.0.0", server_port=7860)