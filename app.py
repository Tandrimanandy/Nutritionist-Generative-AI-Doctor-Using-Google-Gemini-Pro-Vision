import os
import random
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env from the same folder as this file, not the current terminal folder
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

MODEL_NAME = "gemini-flash-lite-latest"

SYSTEM_PROMPT = """You are an expert nutritionist. Look at the food items in the image,
estimate the total calories, and list every food item with its calorie count.

Use this format:
1. Item 1 - number of calories
2. Item 2 - number of calories
----
**Total calories: X**

If the image does not contain food, say so politely and do not guess.
End with a one-line note that these values are estimates."""

st.set_page_config(page_title="Nutritionist AI", layout="wide")

CSS = """
<style>
:root {
    --gold: #E6B800;
    --gold-deep: #B8860B;
    --brown: #5C3A21;
    --cream: #FFF8E1;
}

.stApp {
    background: linear-gradient(160deg, #FFF6CC 0%, #F6D66B 50%, #E0B25A 100%);
    font-family: Georgia, "Times New Roman", serif;
}
header[data-testid="stHeader"] { background: transparent; }
.stApp, .stApp p, .stApp label, .stApp li, .stApp span { color: var(--brown); }

/* Hero banner */
.hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 2rem 1rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #5C3A21 0%, #8B5E3C 100%);
    box-shadow: 0 12px 32px rgba(92, 58, 33, 0.35);
    border: 1.5px solid var(--gold);
    margin-bottom: 1.8rem;
}
.hero h1 {
    margin: 0;
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    background: linear-gradient(90deg, #B8860B, #FFE27A, #FFF8DC, #FFE27A, #B8860B);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shimmer 3.5s linear infinite;
}
.hero p {
    margin: 0.5rem 0 0;
    color: #FFF3C4;
    font-style: italic;
    letter-spacing: 0.06em;
}
.hero::after {
    content: "";
    position: absolute;
    top: 0;
    left: -75%;
    width: 50%;
    height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.35), transparent);
    animation: sweep 4.5s ease-in-out infinite;
}

/* Glitter layer */
.sparkle-layer {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.sparkle {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle, #FFFBE6 0%, #FFD700 40%, transparent 70%);
    box-shadow: 0 0 6px 2px rgba(255, 215, 0, 0.6);
    opacity: 0;
    animation-name: twinkle;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;
}

/* Section headings */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--brown);
    border-bottom: 2px solid var(--gold-deep);
    padding-bottom: 0.3rem;
    margin-bottom: 0.8rem;
}

/* Inputs */
[data-testid="stFileUploader"] section {
    background: var(--cream) !important;
    border: 2px dashed var(--gold-deep) !important;
    border-radius: 16px !important;
}
div[data-testid="stTextInput"] input {
    background: var(--cream);
    color: var(--brown);
    border: 1.5px solid var(--gold-deep);
    border-radius: 12px;
}
div[data-testid="stTextInput"] input:focus {
    box-shadow: 0 0 0 2px var(--gold);
}

/* Buttons (full width handled by CSS so it works on every Streamlit version) */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #F7CF4A, #E6B800);
    color: var(--brown);
    font-weight: 700;
    font-size: 1.05rem;
    border: none;
    border-radius: 999px;
    padding: 0.65rem 1.8rem;
    box-shadow: 0 6px 18px rgba(184, 134, 11, 0.45);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #8B5E3C, #5C3A21);
    color: #FFE27A;
    transform: translateY(-2px);
    box-shadow: 0 10px 22px rgba(92, 58, 33, 0.4);
}
.stButton > button:disabled {
    opacity: 0.55;
    transform: none;
}

/* Result card */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 248, 225, 0.95);
    border: 2px solid var(--gold-deep) !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 26px rgba(92, 58, 33, 0.22);
    padding: 0.5rem 0.8rem;
}
.result-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--brown);
    margin-bottom: 0.6rem;
}

/* Preview image */
[data-testid="stImage"] img {
    width: 100%;
    border-radius: 16px;
    border: 2px solid var(--gold-deep);
    box-shadow: 0 6px 18px rgba(92, 58, 33, 0.25);
}

@keyframes shimmer {
    to { background-position: 200% center; }
}
@keyframes sweep {
    0%, 100% { left: -75%; }
    60% { left: 125%; }
}
@keyframes twinkle {
    0%, 100% { opacity: 0; transform: scale(0.4) rotate(0deg); }
    50% { opacity: 0.9; transform: scale(1) rotate(45deg); }
}
</style>
"""


def sparkle_layer(count: int = 45) -> str:
    """Builds a fixed set of twinkling gold sparkles (same layout on every run)."""
    rnd = random.Random(7)
    parts = []
    for _ in range(count):
        left = rnd.uniform(0, 100)
        top = rnd.uniform(0, 100)
        size = rnd.uniform(3, 8)
        delay = rnd.uniform(0, 6)
        duration = rnd.uniform(2.5, 5)
        parts.append(
            f'<span class="sparkle" style="left:{left:.1f}%;top:{top:.1f}%;'
            f'width:{size:.1f}px;height:{size:.1f}px;'
            f'animation-delay:{delay:.1f}s;animation-duration:{duration:.1f}s"></span>'
        )
    return '<div class="sparkle-layer">' + "".join(parts) + "</div>"


HERO_HTML = (
    '<div class="hero">'
    "<h1>Nutritionist AI</h1>"
    "<p>Snap a meal and discover what is on your plate</p>"
    "</div>"
)


@st.cache_resource
def get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def analyse_food(client: genai.Client, user_prompt: str, image_bytes: bytes, mime_type: str) -> str:
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[user_prompt or "Calculate the calories for this food.", image_part],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
        ),
    )
    # response.text raises an error if Gemini blocked the reply, so read it inside the try block
    return response.text or ""


# ---------- Page ----------
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(sparkle_layer(), unsafe_allow_html=True)
st.markdown(HERO_HTML, unsafe_allow_html=True)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY is missing. Add it to the .env file in the same folder as app.py, then restart the app.")
    st.stop()

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">Your Meal</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a photo of your food (JPG, JPEG or PNG)",
        type=["jpg", "jpeg", "png"],
    )
    user_prompt = st.text_input(
        "Optional question",
        placeholder="e.g. Calculate the calories for this lunch",
    )
    calculate = st.button(
        "Calculate Total Calories",
        disabled=uploaded_file is None,
    )
    if uploaded_file is None:
        st.caption("Upload an image to enable the calorie calculator.")

with right:
    st.markdown('<div class="section-title">Preview</div>', unsafe_allow_html=True)
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded image")
    else:
        st.info("Your image will appear here.")

if calculate and uploaded_file is not None:
    with st.spinner("Analysing your meal..."):
        try:
            client = get_client(api_key)
            result = analyse_food(
                client,
                user_prompt,
                uploaded_file.getvalue(),
                uploaded_file.type or "image/jpeg",
            )
        except Exception as e:
            st.error(f"Could not get a response from Gemini: {e}")
            result = ""

    if result.strip():
        st.markdown('<div class="section-title">Nutrition Report</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="result-title">Calorie Breakdown</div>', unsafe_allow_html=True)
            st.markdown(result)
        st.caption("Calorie values are AI estimates and are not medical advice.")
    elif "Could not get a response" not in st.session_state.get("_err", ""):
        st.warning("Gemini returned an empty response. Please try again.")