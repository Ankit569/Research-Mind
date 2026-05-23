# 🧠 ResearchMind
### Multi-Agent Research Pipeline · Powered by LangChain

> Type any research question → Get a full structured report in seconds.  
> 4 AI agents work together to search, read, write, and critique — fully automated.

---

## 🚀 Demo




> *"What is impact on AI after War"* — all 4 agents completed successfully.

---

## ⚙️ How It Works

| Step | Agent | Role |
|------|-------|------|
| 01 | 🔍 **Search Agent** | Finds recent & reliable sources across the web |
| 02 | 📄 **Reader Agent** | Scrapes & extracts insights from top URLs |
| 03 | ✍️ **Writer Chain** | Drafts a structured research report |
| 04 | 🧠 **Critic Chain** | Reviews quality and flags improvements |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain** — Agent orchestration & chaining
- **Streamlit** — Interactive UI (runs on localhost:8501)
- **Web Scraping** — BeautifulSoup / requests
- **Mistral API** — LLM for writing & critic chains
- **Tavily API** — AI-powered web search for research

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/Ankit569/ResearchMind.git
cd ResearchMind

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys
cp .env.example .env
# Edit .env and add your keys
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_key_here
TAVILY_API_KEY=your_tavily_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
ResearchMind/
├── app.py                  # Streamlit UI
├── agents/
│   ├── search_agent.py     # Step 01 - Web search
│   ├── reader_agent.py     # Step 02 - Scrape & extract
│   ├── writer_chain.py     # Step 03 - Report generation
│   └── critic_chain.py     # Step 04 - Quality review
├── utils/
│   └── helpers.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 💡 Example Output

**Topic:** *What is the impact on AI after War?*

- ✅ Search Agent → Found 8 relevant sources
- ✅ Reader Agent → Extracted insights from top 3 URLs
- ✅ Writer Chain → Generated structured 500-word report
- ✅ Critic Chain → Reviewed & flagged 2 improvements

---

## 🙋‍♂️ About

Built by **Ankit Mayur** — BCA graduate passionate about AI/ML and LLM applications.

- 🔗 LinkedIn: [linkedin.com/in/ankit-mayur](https://linkedin.com/in/ankit-mayur)
- 💻 GitHub: [github.com/Ankit569](https://github.com/Ankit569)

---

## ⭐ Support

If you found this useful, drop a **star** on the repo — it means a lot! 🌟

---

## 📄 License

MIT License — free to use and modify.
