import sys
import os

# نضيف مجلد CodeFormer لمسارات البحث
sys.path.append(os.path.abspath("./CodeFormer"))

import gradio as gr
from PIL import Image
import base64
from core.esrgan_backend import upscale_image
from core.gfpgan_backend import enhance_face
from core.rembg_backend import remove_background
from core.ghibli_backend import apply_ghibli_style
from core.codeformer_backend import restore_image

def load_logo():
    return Image.open("assets/logo.png")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

rosie_base64 = get_base64_image("assets/rosie_avatar.png")

with gr.Blocks(css=""" 
    body {
        background: #f7e9ff;
        font-family: 'Segoe UI', sans-serif;
        color: #333;
        margin: 0;
        padding: 0;
    }
    .gradio-container {
        padding: 30px;
    }
    #title-text {
        font-size: 36px;
        font-weight: bold;
        color: #6a5acd;
        margin-bottom: 5px;
        text-align: center;
    }
    #enhance-btn, #upscale-btn, #remove-bg-btn, #ghibli-btn, #restore-btn {
        background: linear-gradient(to right, #a1c4fd, #c2e9fb);
        border: none;
        color: #333;
        font-size: 16px;
        padding: 10px 25px;
        border-radius: 8px;
        transition: 0.3s ease;
        cursor: pointer;
        margin-top: 10px;
    }
    #enhance-btn:hover, #upscale-btn:hover, #remove-bg-btn:hover, #ghibli-btn:hover, #restore-btn:hover {
        background: linear-gradient(to right, #c2e9fb, #a1c4fd);
        transform: scale(1.05);
    }
    #footer {
        text-align: center;
        font-size: 12px;
        color: #999;
        margin-top: 40px;
    }
    .chat-bubble {
        background-color: #800080;
        padding: 8px 12px;
        border-radius: 12px;
        font-size: 14px;
        color: #fff;
        max-width: 300px;
        display: inline-block;
    }
""") as demo:
    with gr.Column():
        logo = gr.Image(value=load_logo(), show_label=False, interactive=False, width=350)

    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Upload Image", type="pil")
            enhance_btn = gr.Button("Enhance ✨", elem_id="enhance-btn")
            upscale_btn = gr.Button("Upscale Image 🔍", elem_id="upscale-btn")
            remove_bg_btn = gr.Button("Remove Background 🧼", elem_id="remove-bg-btn")
            ghibli_btn = gr.Button("Ghibli Style 🎨", elem_id="ghibli-btn")
            restore_btn = gr.Button("Restore Old Photos 🕰️", elem_id="restore-btn")
        with gr.Column():
            output_image = gr.Image(label="Output")

    enhance_btn.click(fn=enhance_face, inputs=input_image, outputs=output_image)
    upscale_btn.click(fn=upscale_image, inputs=input_image, outputs=output_image)
    remove_bg_btn.click(fn=remove_background, inputs=input_image, outputs=output_image)
    ghibli_btn.click(fn=apply_ghibli_style, inputs=input_image, outputs=output_image)
    restore_btn.click(fn=restore_image, inputs=input_image, outputs=output_image)

    gr.HTML("<div id='footer'>© 2025 Heidi. All rights reserved.</div>")

    with gr.Row():
        gr.HTML(f"""
            <div style="position: fixed; right: 20px; bottom: 20px; display: flex; align-items: center; justify-content: flex-end;">
                <img src="{rosie_base64}" style="width: 40px; margin-right: 10px;">
                <div class="chat-bubble">
                    Hi, I'm Rosie 💬<br>
                    How can I help you today?
                </div>
            </div>
        """)

demo.launch()

