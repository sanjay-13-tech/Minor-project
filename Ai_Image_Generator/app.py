import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO
from datetime import datetime


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at top left, #302b63 0%, transparent 35%),
            radial-gradient(circle at top right, #24243e 0%, transparent 40%),
            #0f0f1a;
        color: white;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #ff6ec7, #7873f5, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        color: #b9b9c9;
        font-size: 19px;
        margin-bottom: 35px;
    }

    /* Cards */
    .feature-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }

    .feature-icon {
        font-size: 32px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 700;
        margin-top: 8px;
    }

    .feature-text {
        color: #aaaaaa;
        font-size: 14px;
    }

    /* Generate button */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 12px 20px;
        font-size: 17px;
        font-weight: 700;
        background: linear-gradient(90deg, #ff4ecd, #667eea);
        color: white;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 25px rgba(102,126,234,0.35);
    }

    /* Text area */
    textarea {
        border-radius: 14px !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777777;
        margin-top: 50px;
        padding: 20px;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎨 AI Image Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Turn your imagination into beautiful AI-generated images ✨</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Powered</div>
        <div class="feature-text">Create images using AI technology.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">Many Styles</div>
        <div class="feature-text">Choose from realistic, anime, fantasy and more.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Easy to Use</div>
        <div class="feature-text">Write a prompt and generate your image.</div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎨 Image Settings")

categories = {
    "🐱 Animals": "animal, highly detailed",
    "🧑 Portrait": "professional portrait, detailed face",
    "🌄 Nature": "beautiful natural scenery, breathtaking landscape",
    "🏙️ City": "beautiful modern city, detailed architecture",
    "🚀 Sci-Fi": "science fiction, futuristic technology, cinematic",
    "🏰 Fantasy": "fantasy world, magical atmosphere, epic",
    "🌸 Anime": "anime artwork, detailed anime style",
    "🎨 Digital Art": "digital artwork, highly detailed",
    "📸 Realistic": "photorealistic, realistic lighting, highly detailed",
    "🦸 Characters": "heroic character, detailed costume, cinematic"
}

styles = {
    "✨ Cinematic": "cinematic lighting, dramatic composition",
    "📸 Photorealistic": "photorealistic, realistic photography",
    "🎨 Digital Art": "high quality digital art",
    "🌸 Anime": "beautiful anime illustration",
    "🖌️ Oil Painting": "classical oil painting style",
    "🧸 3D Cartoon": "3D cartoon style, cute, colorful",
    "🌌 Fantasy": "epic fantasy artwork",
    "💡 Cyberpunk": "cyberpunk style, neon lights"
}

category = st.sidebar.selectbox(
    "Choose a category",
    list(categories.keys())
)

style = st.sidebar.selectbox(
    "Choose an art style",
    list(styles.keys())
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 💡 Example prompts")

examples = [
    "A magical cat flying over a castle",
    "A futuristic city at sunset",
    "A warrior standing on a mountain",
    "A cute robot exploring Mars"
]

for example in examples:
    st.sidebar.write("• " + example)


# --------------------------------------------------
# MAIN PROMPT
# --------------------------------------------------

st.markdown("### 📝 Describe your image")

prompt = st.text_area(
    "Enter your prompt",
    placeholder="Example: A cat with wings flying over a magical city...",
    height=120,
    label_visibility="collapsed"
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

generate = st.button("✨ Generate Image")


if generate:

    if not prompt.strip():

        st.warning("⚠️ Please enter a description first.")

    else:

        # Combine user prompt + category + style
        final_prompt = (
            f"{prompt}, "
            f"{categories[category]}, "
            f"{styles[style]}, "
            f"masterpiece, highly detailed"
        )

        st.info("🎨 Creating your image... Please wait.")

        # --------------------------------------------------
        # GET HUGGING FACE TOKEN
        # --------------------------------------------------

        try:

            # Streamlit Cloud Secrets
            API_KEY = st.secrets["HF_TOKEN"]

        except Exception:

            # Local .env fallback
            API_KEY = os.getenv("HF_TOKEN")


        if not API_KEY:

            st.error(
                "❌ Hugging Face token is missing. "
                "Please add HF_TOKEN to Streamlit Secrets."
            )

        else:

            API_URL = (
                "https://api-inference.huggingface.co/models/"
                "stabilityai/stable-diffusion-xl-base-1.0"
            )

            headers = {
                "Authorization": f"Bearer {API_KEY}"
            }

            try:

                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={
                        "inputs": final_prompt
                    },
                    timeout=120
                )

                if response.status_code == 200:

                    image = Image.open(
                        BytesIO(response.content)
                    )

                    st.success("🎉 Image generated successfully!")

                    st.markdown("### 🖼️ Your Generated Image")

                    st.image(
                        image,
                        use_container_width=True
                    )

                    # --------------------------------------------------
                    # SAVE IMAGE
                    # --------------------------------------------------

                    os.makedirs(
                        "generated_images",
                        exist_ok=True
                    )

                    filename = (
                        "generated_images/"
                        f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    )

                    image.save(filename)

                    # --------------------------------------------------
                    # DOWNLOAD BUTTON
                    # --------------------------------------------------

                    buffer = BytesIO()

                    image.save(
                        buffer,
                        format="PNG"
                    )

                    st.download_button(
                        label="⬇️ Download Image",
                        data=buffer.getvalue(),
                        file_name="ai_generated_image.png",
                        mime="image/png"
                    )

                else:

                    st.error(
                        f"❌ Image generation failed.\n\n"
                        f"Status code: {response.status_code}"
                    )

                    try:
                        error_details = response.json()
                        st.warning(error_details)
                    except Exception:
                        st.warning(response.text)

            except requests.exceptions.Timeout:

                st.error(
                    "⏳ The image generation request took too long. "
                    "Please try again."
                )

            except Exception as e:

                st.error(
                    f"❌ Something went wrong: {str(e)}"
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    🎨 AI Image Studio &nbsp;•&nbsp;
    Powered by Hugging Face 🤗
</div>
""", unsafe_allow_html=True)