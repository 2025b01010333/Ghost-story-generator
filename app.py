import streamlit as st
import base64
import html
from pathlib import Path
from google import genai

# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="Ghost Writer | Create Your Nightmare",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- PATHS --------------------

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

CASTLE_PATH = ASSETS_DIR / "castle.png"
SPELLBOOK_PATH = ASSETS_DIR / "spellbook.png"
BACKGROUND_PATH = ASSETS_DIR / "background.png"

# -------------------- IMAGE HELPER --------------------

def image_to_base64(image_path):
    if not image_path.exists():
        return ""

    extension = image_path.suffix.lower()

    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp"
    }

    mime_type = mime_types.get(extension, "image/png")

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


castle_bg = image_to_base64(CASTLE_PATH)
spellbook_bg = image_to_base64(SPELLBOOK_PATH)
page_bg = image_to_base64(BACKGROUND_PATH)

# -------------------- CUSTOM CSS --------------------

css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:wght@400;500;600;700&display=swap');

.stApp {
    background-color: #0b0712;
    background-image:
        linear-gradient(rgba(10, 6, 17, 0.84), rgba(10, 6, 17, 0.94)),
        url("__PAGE_BG__");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #f3eaff;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 1rem;
}

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: #e7d9ff !important;
}

p, label, span, div {
    font-family: 'Cormorant Garamond', serif;
}

.hero {
    min-height: 330px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 35px 22px;
    box-sizing: border-box;
    border: 1px solid rgba(199, 164, 255, 0.38);
    border-radius: 22px;
    background-color: #170d25;
    background-image:
        linear-gradient(180deg, rgba(10, 5, 18, 0.15),
        rgba(10, 5, 18, 0.72)),
        url("__CASTLE_BG__");
    background-size: cover;
    background-position: center;
    box-shadow: 0 0 35px rgba(117, 66, 180, 0.20);
}

.hero-eyebrow {
    color: #e0c9ff;
    font-size: 14px;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.hero-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(32px, 5vw, 56px);
    font-weight: 700;
    color: #fff0ff;
    text-shadow: 0 0 18px rgba(187, 133, 255, 0.7);
    margin-bottom: 15px;
}

.hero-subtitle {
    max-width: 650px;
    color: #f0e5ff;
    font-size: 21px;
    line-height: 1.5;
}

.settings-title, .section-heading {
    font-family: 'Cinzel', serif;
    font-size: clamp(23px, 4vw, 34px);
    text-align: center;
    color: #e3ceff;
    margin-top: 35px;
    margin-bottom: 8px;
}

.settings-subtitle, .section-subtitle {
    color: #c3b0db;
    font-size: 18px;
    text-align: center;
    margin-bottom: 22px;
}

[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label {
    color: #e6d5ff !important;
    font-size: 17px !important;
}

[data-testid="stSelectbox"] > div > div {
    background-color: rgba(29, 17, 44, 0.94);
    color: #f5eaff;
    border-radius: 10px;
}

div.stButton > button {
    width: 100%;
    min-height: 48px;
    background: linear-gradient(135deg, #8e5bd4, #542b8a);
    color: white;
    border: 1px solid rgba(225, 201, 255, 0.48);
    border-radius: 12px;
    font-family: 'Cinzel', serif;
    font-size: 15px;
    font-weight: 600;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #a779ec, #7041ad);
    color: white;
    box-shadow: 0 0 20px rgba(169, 114, 235, 0.4);
    transform: translateY(-2px);
}

.spellbook {
    width: 100%;
    min-height: 300px;
    box-sizing: border-box;
    margin-top: 12px;
    padding: 35px;
    border: 1px solid rgba(199, 164, 255, 0.45);
    border-radius: 22px;
    background-color: #170d25;
    background-image:
        linear-gradient(180deg, rgba(13, 8, 25, 0.35),
        rgba(13, 8, 25, 0.88)),
        url("__SPELLBOOK_BG__");
    background-size: cover;
    background-position: center;
    box-shadow: 0 0 35px rgba(116, 65, 190, 0.22);
}

.story-text {
    color: #fff1df;
    font-size: 20px;
    line-height: 1.9;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.empty-story {
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: #e1d0f5;
}

.empty-story-icon {
    font-size: 42px;
    margin-bottom: 12px;
}

.empty-story-text {
    font-family: 'Cinzel', serif;
    font-size: 20px;
}

.empty-story-hint {
    font-size: 17px;
    color: #c4b2d8;
    margin-top: 8px;
}

.footer {
    text-align: center;
    padding: 28px 10px 20px;
    margin-top: 40px;
    border-top: 1px solid rgba(199, 164, 255, 0.25);
}

.footer-title {
    font-family: 'Cinzel', serif;
    font-size: 21px;
    color: #e4d0ff;
}

.footer-credit {
    font-size: 18px;
    color: #cbb8e6;
    margin: 8px 0;
}

.footer-credit a {
    color: #e2c9ff;
    text-decoration: none;
    border-bottom: 1px solid rgba(226, 201, 255, 0.45);
}

.footer-copyright {
    font-size: 14px;
    color: #9785ac;
    margin-top: 9px;
}

@media (max-width: 640px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        min-height: 280px;
        padding: 25px 15px;
        border-radius: 16px;
    }

    .hero-eyebrow {
        letter-spacing: 3px;
        font-size: 12px;
    }

    .hero-subtitle {
        font-size: 18px;
    }

    .spellbook {
        min-height: 280px;
        padding: 22px 18px;
        border-radius: 16px;
    }

    .story-text {
        font-size: 18px;
        line-height: 1.75;
    }
}
/* ---------------- FLOATING GLITTER ---------------- */

.glitter {
    position: fixed;
    bottom: -15px;
    width: 5px;
    height: 5px;
    background: #f3d9ff;
    border-radius: 50%;
    box-shadow: 0 0 8px #e0aaff, 0 0 16px #b76cff;
    pointer-events: none;
    z-index: 99999;
    animation: glitter-rise 8s linear infinite;
}

@keyframes glitter-rise {
    0% {
        transform: translateY(0) scale(0.5);
        opacity: 0;
    }
    15% {
        opacity: 1;
    }
    80% {
        opacity: 0.9;
    }
    100% {
        transform: translateY(-110vh) scale(1.3);
        opacity: 0;
    }
}
</style>
"""

css = (
    css
    .replace("__PAGE_BG__", page_bg)
    .replace("__CASTLE_BG__", castle_bg)
    .replace("__SPELLBOOK_BG__", spellbook_bg)
)

st.markdown(css, unsafe_allow_html=True)
# ADD THIS GLITTER CODE BELOW
st.markdown(
    """
    <div class="glitter" style="left: 8%; animation-delay: 0s;"></div>
    <div class="glitter" style="left: 22%; animation-delay: 2s;"></div>
    <div class="glitter" style="left: 38%; animation-delay: 4s;"></div>
    <div class="glitter" style="left: 55%; animation-delay: 1s;"></div>
    <div class="glitter" style="left: 72%; animation-delay: 3s;"></div>
    <div class="glitter" style="left: 88%; animation-delay: 5s;"></div>
    """,
    unsafe_allow_html=True
)


# -------------------- HERO SECTION --------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Enter If You Dare</div>
        <div class="hero-title">Ghost Writer</div>
        <div class="hero-subtitle">
            Every shadow hides a secret. Every whisper tells a story.
            Are you brave enough to create your own nightmare?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------- STORY SETTINGS --------------------

st.markdown(
    """
    <div class="settings-title">Create Your Nightmare</div>
    <div class="settings-subtitle">
        Choose your darkness. Let the story begin.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    genre = st.selectbox(
        "🕯️ Story Genre",
        [
            "Haunted House",
            "Psychological Horror",
            "Supernatural Horror",
            "Gothic Horror",
            "Ghost Story",
            "Cursed Object",
            "Dark Fantasy"
        ]
    )

with col2:
    setting = st.selectbox(
        "🌑 Haunted Setting",
        [
            "An abandoned castle",
            "A dark forest",
            "An old haunted mansion",
            "An abandoned hospital",
            "A deserted village",
            "A mysterious boarding school",
            "A lonely village at midnight"
        ]
    )

with col3:
    story_length = st.selectbox(
        "📖 Story Length",
        ["Short", "Medium", "Long"],
        index=1
    )

tone = st.selectbox(
    "👁️ Choose the atmosphere",
    [
        "Creepy and mysterious",
        "Terrifying and suspenseful",
        "Dark and emotional",
        "Supernatural and eerie",
        "A shocking twist ending"
    ]
)

length_instructions = {
    "Short": "Write approximately 200–300 words.",
    "Medium": "Write approximately 350–500 words.",
    "Long": "Write approximately 600–750 words."
}

generate_button = st.button(
    "🕯️ Summon My Nightmare",
    use_container_width=True
)



# -------------------- STORY GENERATION --------------------

if "story" not in st.session_state:
    st.session_state.story = ""

if generate_button:
    prompt = f"""
Write an original horror story.
Genre: {genre}
Setting: {setting}
Atmosphere: {tone}
Length: {length_instructions[story_length]}

Give it an interesting title, build suspense quickly,
use vivid descriptions, and end with a frightening twist.
Return only the title and story.
"""

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)

        story_placeholder = st.empty()
        generated_story = ""

        with st.spinner("The spirits are writing your nightmare... 👻"):
            stream = client.interactions.create(
                model="gemini-3.8-flash",
                input=prompt,
                generation_config={
                    "thinking_level": "low"
                },
                stream=True
            )

            for event in stream:
                if event.event_type == "step.delta":
                    if event.delta.type == "text":
                        generated_story += event.delta.text
                        story_placeholder.markdown(
                            generated_story + " ▌"
                        )

        generated_story = generated_story.strip()

        if generated_story:
            st.session_state.story = generated_story
            st.rerun()
        else:
            st.error(
                "No story text was received. Please try again."
            )

    except Exception as error:
        st.error(f"Story generation failed: {error}")

# -------------------- MIDNIGHT SPELLBOOK --------------------


st.markdown(
    """
    <div class="section-heading">Midnight Spellbook</div>
    <div class="section-subtitle">
        The pages are waiting. What darkness will you uncover?
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.story:
    safe_story = html.escape(st.session_state.story)

    st.markdown(
        f"""
        <div class="spellbook">
            <div class="story-text">{safe_story}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🔮 Forget This Nightmare",
        use_container_width=True
    ):
        st.session_state.story = ""
        st.rerun()

else:
    st.markdown(
        """
        <div class="spellbook">
            <div class="empty-story">
                <div class="empty-story-icon">📖 🕯️</div>
                <div class="empty-story-text">
                    Your nightmare has not yet been written...
                </div>
                <div class="empty-story-hint">
                    Choose your settings above and summon a story.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------- FOOTER --------------------

st.markdown(
    """
    <div class="footer">
        <div class="footer-title">👻 Ghost Writer</div>
        <div class="footer-credit">
            Crafted with a little magic by
            <a href="https://github.com/2025b01010333"
               target="_blank"
               rel="noopener noreferrer">
                Apoorva Saini
            </a>
            ✨
        </div>
        <div class="footer-copyright">
            © 2026 Ghost Writer · All nightmares reserved
        </div>
    </div>
    """,
    unsafe_allow_html=True
)