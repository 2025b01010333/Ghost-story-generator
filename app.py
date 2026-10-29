import streamlit as st
import requests
import base64
import html
from pathlib import Path

# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="Ghost Writer | Create Your Nightmare",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- PATHS & SETTINGS --------------------

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

CASTLE_PATH = ASSETS_DIR / "castle.png"
SPELLBOOK_PATH = ASSETS_DIR / "spellbook.png"
BACKGROUND_PATH = ASSETS_DIR / "background.png"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"


# -------------------- IMAGE HELPER --------------------

def image_to_base64(image_path):
    """Convert an image file into a base64 data URL."""
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
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded_image}"


castle_bg = image_to_base64(CASTLE_PATH)
spellbook_bg = image_to_base64(SPELLBOOK_PATH)
page_bg = image_to_base64(BACKGROUND_PATH)


# -------------------- CUSTOM CSS --------------------

css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:wght@400;500;600;700&display=swap');

:root {
    --purple: #c7a4ff;
    --light-purple: #e7d9ff;
    --dark-purple: #170d25;
    --muted: #c0b2d2;
}

.stApp {
    background-color: #0b0712;
    background-image:
        linear-gradient(
            rgba(10, 6, 17, 0.84),
            rgba(10, 6, 17, 0.94)
        ),
        url("__PAGE_BG__");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #f3eaff;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 1rem;
}

/* Main headings */

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--light-purple) !important;
}

p, label, span, div {
    font-family: 'Cormorant Garamond', serif;
}

/* Castle hero */

.hero {
    width: 100%;
    min-height: 330px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 45px 25px;
    border: 1px solid rgba(199, 164, 255, 0.38);
    border-radius: 22px;
    overflow: hidden;
    background-color: #170d25;
    background-image:
        linear-gradient(
            180deg,
            rgba(10, 5, 18, 0.15),
            rgba(10, 5, 18, 0.72)
        ),
        url("__CASTLE_BG__");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
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
    font-family: 'Cinzel', serif !important;
    font-size: clamp(32px, 5vw, 56px);
    font-weight: 700;
    line-height: 1.2;
    color: #fff0ff;
    text-shadow: 0 0 18px rgba(187, 133, 255, 0.7);
    margin: 0 0 15px 0;
}

.hero-subtitle {
    max-width: 650px;
    color: #f0e5ff;
    font-size: 21px;
    line-height: 1.5;
}

/* Settings section */

.settings-title {
    font-family: 'Cinzel', serif;
    font-size: 23px;
    text-align: center;
    color: var(--light-purple);
    margin-top: 35px;
    margin-bottom: 5px;
}

.settings-subtitle {
    color: var(--muted);
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
    border-color: rgba(199, 164, 255, 0.35);
    border-radius: 10px;
}

[data-testid="stSlider"] [data-baseweb="slider"] {
    padding-top: 8px;
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
    border-color: #e3caff;
    box-shadow: 0 0 20px rgba(169, 114, 235, 0.4);
    transform: translateY(-2px);
}

/* Spellbook section */

.section-heading {
    font-family: 'Cinzel', serif;
    font-size: clamp(24px, 4vw, 34px);
    font-weight: 600;
    color: #e3ceff;
    text-align: center;
    margin-top: 42px;
    margin-bottom: 5px;
    text-shadow: 0 0 15px rgba(163, 109, 238, 0.35);
}

.section-subtitle {
    font-size: 18px;
    color: #c3b0db;
    text-align: center;
    margin-bottom: 22px;
}

.spellbook {
    width: 100%;
    min-height: 330px;
    box-sizing: border-box;
    margin-top: 12px;
    padding: 48px 38px;
    border: 1px solid rgba(199, 164, 255, 0.45);
    border-radius: 22px;
    background-color: #170d25;
    background-image:
        linear-gradient(
            180deg,
            rgba(13, 8, 25, 0.28),
            rgba(13, 8, 25, 0.84)
        ),
        url("__SPELLBOOK_BG__");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    box-shadow: 0 0 35px rgba(116, 65, 190, 0.22);
}

.story-text {
    color: #fff1df;
    font-size: 20px;
    line-height: 1.9;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    text-shadow: 0 1px 5px rgba(0, 0, 0, 0.85);
}

.empty-story {
    min-height: 225px;
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

/* Ash particles */

.ash-container {
    position: fixed;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
}

.ash {
    position: absolute;
    bottom: -15px;
    width: 4px;
    height: 4px;
    background: #d8baff;
    border-radius: 50%;
    opacity: 0.45;
    box-shadow: 0 0 8px #b88aff;
    animation: floatAsh 12s linear infinite;
}

.ash:nth-child(1) { left: 8%; animation-delay: 0s; }
.ash:nth-child(2) { left: 21%; animation-delay: 3s; }
.ash:nth-child(3) { left: 37%; animation-delay: 6s; }
.ash:nth-child(4) { left: 55%; animation-delay: 1s; }
.ash:nth-child(5) { left: 71%; animation-delay: 4s; }
.ash:nth-child(6) { left: 88%; animation-delay: 7s; }

@keyframes floatAsh {
    0% {
        transform: translateY(0) translateX(0);
        opacity: 0;
    }
    20% { opacity: 0.5; }
    80% { opacity: 0.35; }
    100% {
        transform: translateY(-100vh) translateX(35px);
        opacity: 0;
    }
}

/* Footer */

.footer {
    width: 100%;
    box-sizing: border-box;
    text-align: center;
    padding: 28px 10px 20px;
    margin-top: 40px;
    border-top: 1px solid rgba(199, 164, 255, 0.25);
}

.footer-title {
    font-family: 'Cinzel', serif;
    font-size: 21px;
    color: #e4d0ff;
    margin-bottom: 8px;
}

.footer-credit {
    font-size: 18px;
    color: #cbb8e6;
    margin: 5px 0;
}

.footer-credit a {
    color: #e2c9ff;
    text-decoration: none;
    border-bottom: 1px solid rgba(226, 201, 255, 0.45);
}

.footer-credit a:hover {
    color: #ffffff;
}

.footer-copyright {
    font-family: 'Cormorant Garamond', serif;
    font-size: 14px;
    color: #9785ac;
    margin-top: 9px;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Mobile layout */

@media (max-width: 640px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        min-height: 290px;
        padding: 30px 15px;
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
        min-height: 290px;
        padding: 28px 20px;
        border-radius: 16px;
    }

    .story-text {
        font-size: 18px;
        line-height: 1.75;
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


# -------------------- FLOATING ASH --------------------

st.markdown(
    """
    <div class="ash-container">
        <span class="ash"></span>
        <span class="ash"></span>
        <span class="ash"></span>
        <span class="ash"></span>
        <span class="ash"></span>
        <span class="ash"></span>
    </div>
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
        [
            "Short",
            "Medium",
            "Long"
        ],
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
    "Short": "Write approximately 300–400 words.",
    "Medium": "Write approximately 600–800 words.",
    "Long": "Write approximately 1000–1300 words."
}

st.markdown("")

generate_button = st.button(
    "🕯️  Summon My Nightmare",
    use_container_width=True
)


# -------------------- STORY GENERATION --------------------

if "story" not in st.session_state:
    st.session_state.story = ""

if generate_button:
    prompt = f"""
You are a creative horror author who writes original, immersive stories.

Write an original horror story with these requirements:

Genre: {genre}
Setting: {setting}
Atmosphere: {tone}
Length: {length_instructions[story_length]}

Instructions:
- Give the story an intriguing title.
- Start with an atmospheric and interesting opening.
- Build suspense gradually.
- Use vivid descriptions, eerie details, and believable characters.
- Make the story original, coherent, and engaging.
- Give it a satisfying, frightening, or unexpected ending.
- Do not explain how you created the story.
- Return only the title and the story.
"""

    with st.spinner("The spirits are writing your nightmare... 👻"):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300
            )

            response.raise_for_status()
            result = response.json()
            generated_story = result.get("response", "").strip()

            if generated_story:
                st.session_state.story = generated_story
                st.rerun()
            else:
                st.error(
                    "The spirits returned an empty story. "
                    "Please try again."
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Ollama is not running. Open a terminal and run "
                "`ollama serve`, then try again."
            )

        except requests.exceptions.Timeout:
            st.error(
                "Story generation took too long. Please try again."
            )

        except requests.exceptions.HTTPError as error:
            st.error(
                f"Ollama returned an error: {error}. "
                "Check that the model is installed."
            )

        except (ValueError, KeyError) as error:
            st.error(f"Could not read the generated story: {error}")

        except requests.exceptions.RequestException as error:
            st.error(f"Something went wrong: {error}")


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

    # Keep the opening and closing HTML tags in one Markdown call
    # so the background image covers the complete story card.
    st.markdown(
        f"""
        <div class="spellbook">
            <div class="story-text">{safe_story}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🔮 Forget This Nightmare", use_container_width=True):
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
