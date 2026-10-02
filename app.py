import gradio as gr
import torch
from diffusers import StableDiffusionPipeline

MODEL_ID = "runwayml/stable-diffusion-v1-5"

device = "cuda" if torch.cuda.is_available() else "cpu"

dtype = torch.float16 if device == "cuda" else torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=dtype
)

pipe = pipe.to(device)


def generate_image(prompt, steps, guidance):
    if not prompt.strip():
        return None

    result = pipe(
        prompt=prompt,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance)
    )

    return result.images[0]


with gr.Blocks(
    title="Text-to-Image Generator"
) as demo:

    gr.Markdown(
        """
        # 🎨 Real-Time Text-to-Image Generator

        Enter a natural-language prompt and generate an AI-created image.
        """
    )

    prompt = gr.Textbox(
        label="Enter your prompt",
        placeholder="A futuristic city at sunset, cinematic lighting..."
    )

    with gr.Row():

        steps = gr.Slider(
            minimum=10,
            maximum=50,
            value=30,
            step=1,
            label="Inference Steps"
        )

        guidance = gr.Slider(
            minimum=1,
            maximum=15,
            value=7.5,
            step=0.5,
            label="Guidance Scale"
        )

    generate_button = gr.Button(
        "Generate Image",
        variant="primary"
    )

    output = gr.Image(
        label="Generated Image",
        type="pil"
    )

    generate_button.click(
        fn=generate_image,
        inputs=[prompt, steps, guidance],
        outputs=output
    )


if __name__ == "__main__":
    demo.launch()
