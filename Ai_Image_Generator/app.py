import os
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨"
)

st.title("🎨 AI Image Generator")
st.write("Generate images using Hugging Face")

prompt = st.text_area(
    "Enter your prompt:",
    placeholder="A futuristic city at sunset, cinematic, highly detailed"
)

if st.button("Generate Image"):

    if not prompt.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    token = os.getenv("HF_TOKEN")

    if not token:
        st.error("HF_TOKEN is not set.")
        st.stop()

    try:
        with st.spinner("Generating image..."):

            client = InferenceClient(
                provider="auto",
                api_key=token
            )

            image = client.text_to_image(
                prompt=prompt,
                model="black-forest-labs/FLUX.1-schnell"
            )

            st.image(
                image,
                caption="Generated Image",
                use_container_width=True
            )

            st.success("Image generated successfully!")

    except Exception as e:
        st.error(f"Error generating image: {e}")
