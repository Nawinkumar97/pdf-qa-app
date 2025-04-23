# PDF Q&A with DeepSeek and Ollama

This is a Streamlit application that enables users to upload a PDF document and ask natural language questions based on its content. It supports two modes:

- `ask_pdf.py`: Uses DeepSeek Reasoner via OpenAI-compatible API
- `ask_pdf_ollama.py`: Uses the locally running Ollama LLM (`deepseek-r1:7b`)

## 🖼️ App Preview

Here’s what the app looks like in action:

![PDF Q&A Streamlit Screenshot](Screenshot.png)

## 🚀 How to Run

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-qa-app.git
cd pdf-qa-app
```

2. Set up a `.env` file for DeepSeek API (only needed for `ask_pdf.py`):
```env
DEEPSEEK_API_KEY=your_api_key_here
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
To use DeepSeek Reasoner API:
```bash
streamlit run ask_pdf.py
```
To use DeepSeek R1 via Ollama:
```bash
streamlit run ask_pdf_ollama.py
```

## 📁 Files

- `ask_pdf.py`: Uses DeepSeek API
- `ask_pdf_ollama.py`: Uses DeepSeek R1 via Ollama
- `requirements.txt`: Dependencies list
- `.env`: Contains your DeepSeek API key (if applicable)

## 🧠 Models
- `ask_pdf.py`: Uses `deepseek-reasoner` via `https://api.deepseek.com`
- `ask_pdf_ollama.py`: Uses `deepseek-r1:7b` model via local Ollama server

---

Made with ❤️ using Streamlit, LangChain, and Ollama.
