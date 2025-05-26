
import os
import gradio as gr
from PIL import Image
import requests
from io import BytesIO
import rembg

basedir = os.path.abspath(os.path.dirname(__file__))
os.environ['U2NET_HOME'] = os.path.join(basedir,'model')


def remove_bg(image=None, url=None):
    """
    Main function for background removal
    Args:
        image: Uploaded image
        url: Image URL
    """
    if url:
        try:
            response = requests.get(url)
            input_image = Image.open(BytesIO(response.content)).convert('RGB')
        except:
            return None
    elif image is not None:
        input_image = Image.fromarray(image).convert('RGB')
    else:
        return None
    
    output_image = rembg.remove(input_image)
    return output_image


# Create Gradio interface
demo = gr.Interface(
    fn=remove_bg,
    inputs=[
        gr.Image(label="Upload an image", type="numpy"),
        gr.Textbox(label="Image URL")
    ],
    outputs=[
        gr.Image(label="Output", type="pil")
    ],
    title="RMBG-2.0 Background Removal",
    description="Upload an image or provide URL to remove background",
    cache_examples=False
)

if __name__ == "__main__":
    # Launch server
    demo.launch(server_name="0.0.0.0")
