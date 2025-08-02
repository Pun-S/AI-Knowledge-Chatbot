# 📚 AI Knowledge Chatbot - Angular + FastAPI + Hugging Face API

A fullstack GenAI chatbot that:
- Lets you upload PDF/DOCX/TXT
- Stores embeddings in FAISS
- Uses Hugging Face `zephyr-7b-beta` for Q&A
- Frontend: Angular
- Backend: FastAPI
- Deployable with Docker Compose

---

## 🚀 Setup

### 1️⃣ Get a Hugging Face API Key
- Sign up: [https://huggingface.co/join](https://huggingface.co/join)
- Go to: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Create a token (read access)
- Save it in `.env` file:
```env
HF_API_KEY=your_api_key_here