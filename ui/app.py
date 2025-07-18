import gradio as gr
from PIL import Image
from gradio_toggle import Toggle
import requests
from io import BytesIO


# Event handler functions
def handle_toggle(toggle_value):
    """Handle toggle state changes - controls garment input visibility"""
    toggle_label = gr.update(value=toggle_value, label="Try-off") if toggle_value else gr.update(value=toggle_value, label="Try-on")
    submit_btn_label = gr.update(value="Run Try-off") if toggle_value else gr.update(value="Run Try-on")
    
    if toggle_value:
        # Clear the image and disable the component
        return gr.update(value=None, elem_classes=["disabled-image"], interactive=False), toggle_label, submit_btn_label
    else:
        # Re-enable the component without clearing the image
        return gr.update(elem_classes=[], interactive=True), toggle_label, submit_btn_label

def handle_submit(image):
    return image

def garment_input_change(garment_img, model_img, input_toggle_value):
    # If both images are set, set toggle to False (Try-on)
    if garment_img is not None and model_img is not None and input_toggle_value:
        return gr.update(value=False, label="Try-on"), gr.update(value="Run Try-on")
    return gr.update(), gr.update()

def model_image_change(model_img, garment_img, input_toggle_value):
    # If both images are set, set toggle to False (Try-on)
    if model_img is not None and garment_img is not None and input_toggle_value:
        return gr.update(value=False, label="Try-on"), gr.update(value="Run Try-on")
    # If only model_img is set, set toggle to True (Try-off)
    if model_img is not None and garment_img is None and not input_toggle_value:
        return gr.update(value=True, label="Try-off"), gr.update(value="Run Try-off")
    return gr.update(), gr.update()

def set_tryon(garment_img, model_img, output_img):
    garment_update, toggle_label, submit_btn_label = handle_toggle(False)
    return garment_update, toggle_label, submit_btn_label

def set_tryoff(model_img, output_img):
    garment_update, toggle_label, submit_btn_label = handle_toggle(True)
    return garment_update, toggle_label, submit_btn_label

# Custom CSS to make the button square and center it
css = """

/* Custom header layout for perfect centering */
.header-container {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: relative !important;
    width: 100% !important;
    padding: 20px 0 !important;
}

.logo-container {
    position: absolute !important;
    left: 0 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
}

.title-container {
    flex: 1 !important;
    text-align: center !important;
}

.disabled-image {
        opacity: 0.5;
        pointer-events: none;
        filter: grayscale(100%);
    }

/* Hide Gradio footer */
.footer {
    display: none !important;
}

footer {
    display: none !important;
}

.gradio-container .footer {
    display: none !important;
}

/* Remove scroll bars (First Row had a scroll bar) */
* {
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}

*::-webkit-scrollbar {
    display: none !important;
}

/* Prevent overflow on header row */
.header-container {
    overflow: hidden !important;
}

.button-container {
    display: flex;
    align-items: center !important;
    justify-content: center;
    gap: 8px;
}

.center-item {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.button-container .button {
    margin: 0 !important;
    padding: 0.5em 1.2em !important; /* or your preferred value */
    height: 40px !important;         /* set a fixed height for all buttons */
    line-height: 40px !important;    /* match line-height to height for vertical centering */
    box-sizing: border-box !important;
    vertical-align: middle !important;
    font-size: 1rem !important;
}
"""

# Create the Gradio interface
with gr.Blocks(css=css, theme=gr.themes.Soft(), title="External UI") as demo:
    with gr.Row():
        gr.HTML("""
            <div class="header-container">
                <div class="logo-container">
                    <img src="https://media.licdn.com/dms/image/v2/D560BAQGJtRzzUkqJTg/company-logo_200_200/company-logo_200_200/0/1713337311913?e=2147483647&v=beta&t=atALY_WL0ZQEd0Hlawv9iGuR64DwwQhHhDDCLjBQHQA" 
                         style="height: 100px; width: 100px;">
                </div>
                <div class="title-container">
                    <h1 style="margin: 0; font-size: 2em;">~~~~~~Title~~~~~~</h1>
                    <div class="button-container" style="margin-top: 10px;">
                        <button class="button">Arxiv</button>
                        <button class="button">Project</button>
                        <button class="button">NXN.ai</button>
                        <button class="button fix-button-align">NXN.ai</button>
                    </div>
                </div>
            </div>
        """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("<center>Step 1: Select <strong>try-on</strong> or <strong>try-off</strong> mode.</center>")
            input_toggle = Toggle(
                label="Try-on",
                value=False,
                info="<h2>Try-on / Try-off</h2>",
                interactive=True,
                elem_classes=["button-container"]
        )
        
        with gr.Column(scale=1):
            gr.Markdown("<center>Step 2: Select the garment type you are using.</center>")
            garment_condition = gr.Radio(
                choices=["Upper", "Lower", "Full"],
                value="Upper", 
                interactive=True,
                elem_classes=["center-item"],
                show_label=False
            )
        
        with gr.Column(scale=1):
            #gr.HTML("<div style='height:5px'></div>")
            pass

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("<center>Step 3: Upload model image ⬇️</center>")
            model_image = gr.ImageEditor(
                label="Model Image",
                type="pil",
                height=450,
                width=600,
                interactive=True,
                brush=gr.Brush(
                    default_color=f"rgba(255, 255, 255, 0.5)",
                    colors=["rgb(255, 255, 255)"]
                ),
                eraser=gr.Eraser(),
                placeholder="Upload an image\n or\n select the draw tool on the left\n to start editing mask"
            )

            model_examples = gr.Examples(
                examples=[
                    ["./example_images/lebron.png"]
                ],
                inputs=[model_image],
                label="Model Examples"
            )
        
        with gr.Column(scale=1):
            gr.Markdown("<center>Step 4: Upload garment image ⬇️</center>")
            garment_input = gr.Image(
                label="Garment Input",
                type="pil",
                height=450,
                width=300,
                visible=True,
                interactive=True,
            )
            
            garment_examples = gr.Examples(
                examples=[
                    ["./example_images/warriors23.jpg"]
                ],
                inputs=[garment_input],
                label="Garment Examples"
            )

        with gr.Column(scale=1):
            gr.Markdown("<center>Step 5: Click the button below to run the model ⬇️</center>")
            output_image = gr.Image(
                label="Output Image",
                type="pil",
                height=450,
                width=600,
                interactive=False,
            )

            submit_btn = gr.Button(
                value="Run Try-On",
                variant="primary"
            )
    
    gr.Markdown("---")

    with gr.Row():
        tryon_examples = gr.Examples(
            examples=[
                ["./example_images/warriors23.jpg", "./example_images/lebron.png", "./example_images/ronaldo.webp"],
                ["./example_images/warriors23.jpg", "./example_images/lebron.png", "./example_images/ronaldo.webp"]
            ],
            inputs=[model_image, garment_input, output_image],
            fn=set_tryon,
            outputs=[garment_input, input_toggle, submit_btn],
            label="Try-on Examples",
            run_on_click=True
        )

        tryoff_examples = gr.Examples(
            examples=[
                ["./example_images/lebron.png", "./example_images/lebron.png"],
                ["./example_images/ronaldo.webp", "./example_images/lebron.png"],
                ["./example_images/Caesar-Ronaldo.webp", "./example_images/lebron.png"],
            ],
            inputs=[model_image, output_image],
            fn=set_tryoff,
            outputs=[garment_input, input_toggle, submit_btn],
            label="Try-off Examples",
            run_on_click=True
        )

    gr.Markdown("---")

    # Connect toggle to control garment input visibility
    input_toggle.change(
        fn=handle_toggle,
        inputs=[input_toggle],
        outputs=[garment_input, input_toggle, submit_btn]
    )

    submit_btn.click(
        fn=handle_submit,
        inputs=[gr.Image(value='https://media.istockphoto.com/id/157030584/vector/thumb-up-emoticon.jpg?s=612x612&w=0&k=20&c=GGl4NM_6_BzvJxLSl7uCDF4Vlo_zHGZVmmqOBIewgKg=', visible=False)],
        outputs=[output_image]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(
        share=True,  # Set to True to create a public link
    )