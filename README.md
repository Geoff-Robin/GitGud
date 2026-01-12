# GitGud 🚀

**GitGud** is an AI-powered guided competitive programming platform designed to help developers level up their algorithmic skills. Unlike traditional platforms that just provide a solution, GitGud offers a progressive assistance model that nurtures problem-solving abilities through tiered hints and automated code validation.

![Guided Competitive Coding Platform Banner](https://i.redd.it/238i9i90zu0c1.jpg)

## 💡 The Problem
Competitive programming can be daunting. Beginners often hit a wall and look up solutions immediately, leading to "tutorial hell" without real skill acquisition. GitGud solves this by providing a structured bridge between being stuck and finding the answer.

## ✨ Key Features
- **Tiered Assistance**:
  - **Level 0**: Conceptual hints and algorithmic guidance.
  - **Level 1**: Detailed logic and pseudocode.
  - **Level 2**: Full solution with automated reflection and validation.
- **Auto-Validation**: Integrated sandboxed execution environment to test suggested solutions in real-time.
- **Adaptive Recommendations**: Smart problem suggestions based on your performance and struggle patterns.
- **Multi-Platform Integration**: Supports problems from **LeetCode**, **Codeforces**, and **CodeChef**.
- **AI Agent Workflow**: Powered by **LangGraph**, utilizing **ReAct** and **Reflexion** patterns for high-quality, self-correcting logic.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) + [shadcn/ui](https://ui.shadcn.com/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **State Management**: [React Router](https://reactrouter.com/) + [Axios](https://axios-http.com/)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: [MongoDB](https://www.mongodb.com/) (Atlas)
- **AI Engine**: [LangChain](https://www.langchain.com/) & [LangGraph](https://www.langchain.com/langgraph)
- **LLM**: [Groq](https://groq.com/) (Llama/GPT-OSS models)
- **Search**: DuckDuckGo API for real-time concept retrieval.

### Code Execution (Sandbox)
- **Runtime**: [Node.js](https://nodejs.org/) + [Express](https://expressjs.com/)
- **Isolation**: Dockerized environment for safely running Python, C++, and Java.

---

## 🏗️ Project Structure
```bash
GitGud/
├── frontend/        # React + Vite application
├── backend/         # FastAPI + LangGraph AI Agent
├── code_runner/     # Sandboxed code execution API
├── notebooks/       # AI model experimentation (ReAct/Reflexion)
└── README.md        # You are here!
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js & npm
- Python 3.10+
- Docker (for code runner)
- MongoDB account
- Groq API Key

### Installation

1. **Clone the Repo**
   ```bash
   git clone https://github.com/Geoff-Robin/GitGud.git
   cd GitGud
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   # Add your .env (GROQ_API_KEY, MONGO_DB_USERNAME, etc.)
   python main.py
   ```

3. **Setup Code Runner**
   ```bash
   cd code_runner
   npm install
   node server.js
   ```

4. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 🤖 AI Architecture
GitGud employs a sophisticated **Reflexion Agent** architecture:
1. **Extraction**: Identifies problem requirements and constraints.
2. **Generation**: Suggests logic or code based on tiered levels.
3. **Execution**: Sends code to the `code_runner` API.
4. **Judging**: Analyzes output/errors.
5. **Reflection**: If the code fails, the agent reflects on the error message and self-corrects before giving the user feedback.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the ISC License.

---
Created with ❤️ by **[Geoff-Robin](https://github.com/Geoff-Robin)**
