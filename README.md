# 👻 Ghost Writer

**Summon your imagination. Generate your nightmare.**

Ghost Writer is an AI-powered horror story generator built with Python, Streamlit, and Google's Gemini API. It lets users create original horror stories based on their preferred genre, setting, atmosphere, and story length.

## ✨ Features

- 🕯️ Generate original horror stories with AI
- 🏚️ Choose story genres and settings
- 🌑 Customize the atmosphere and tone
- 📖 Select your preferred story length
- 🎨 Gothic-inspired interface with custom visual assets
- ⚡ Streaming story output

## 🛠️ Tech Stack

- Python
- Streamlit
- Google GenAI SDK
- Gemini API
- HTML and CSS

## 📁 Project Structure

```text
ghost-story-generator/
├── app.py
├── assets/
│   ├── castle.png
│   ├── spellbook.png
│   └── background.png
├── .streamlit/
│   └── secrets.toml
├── .gitignore
├── requirements.txt
└── README.md
```

> The local `secrets.toml` file must not be committed to GitHub.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd Ghost-Writer
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure your API key

Create `.streamlit/secrets.toml` and add your own Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Never publish your actual API key.

### 4. Start the application

```bash
python -m streamlit run app.py
```

## 🔐 Security

Keep your API key private. Do not upload `.streamlit/secrets.toml` or expose credentials in source code.

## 👩‍💻 Author

**Apoorva Saini**

GitHub: [@2025b01010333](https://github.com/2025b01010333)

---

*Enter the darkness. Let the stories begin.*