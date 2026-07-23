# 📚 NeuraDocs — AI PDF Knowledge Assistant

An AI-powered PDF Knowledge Assistant that lets users upload documents, perform semantic searches, and ask questions about their PDFs using a Retrieval-Augmented Generation (RAG) pipeline.

Built with **Flask, ChromaDB, Google Gemini, PyPDF2, and HTML/CSS/JavaScript**.

## ✨ Features

* 📤 Upload multiple PDF documents
* 📄 Automatic PDF text extraction
* 🧩 Text chunking and document indexing
* 🔍 Semantic search across documents
* 💬 AI-powered document Q&A
* 🤖 Google Gemini integration
* 📌 Source citations with document and page references
* 🗂️ Document management and deletion
* 📊 Knowledge base statistics
* 🖱️ Drag-and-drop PDF upload
* 🎨 Modern responsive web interface
* 💾 Persistent ChromaDB vector storage

## 🏗️ Architecture

```text
PDF Upload
    ↓
Text Extraction (PyPDF2)
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
ChromaDB Vector Storage
    ↓
User Question / Search Query
    ↓
Similarity Search
    ↓
Retrieve Relevant Chunks
    ↓
Google Gemini
    ↓
AI Answer + Source Citations
```

## 📁 Project Structure

```text
knowledge_assistant/
│
├── app.py
├── index.html
├── requirements.txt
├── .env
├── documents_metadata.json
├── uploads/
├── chroma_db/
└── venv/
```

| File / Folder             | Description                 |
| ------------------------- | --------------------------- |
| `app.py`                  | Flask backend and REST API  |
| `index.html`              | Web frontend                |
| `requirements.txt`        | Python dependencies         |
| `.env`                    | Google Gemini API key       |
| `documents_metadata.json` | Document metadata           |
| `uploads/`                | Uploaded PDF files          |
| `chroma_db/`              | Persistent ChromaDB storage |

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd knowledge_assistant
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Never commit your `.env` file to GitHub.

### 5. Run the Backend

```bash
python app.py
```

The API will be available at:

```text
http://localhost:5000
```

### 6. Run the Frontend

You can open `index.html` directly or serve it using:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/index.html
```

Make sure the Flask backend is running at:

```text
http://localhost:5000
```

## 🔍 How It Works

### Upload Documents

PDF files are uploaded and processed using PyPDF2. The extracted text is divided into overlapping chunks and stored in ChromaDB along with document metadata.

### Semantic Search

Users can search their documents using natural-language queries. The system retrieves the most relevant document chunks from the knowledge base.

### AI Q&A

When a user asks a question:

1. The question is processed.
2. Relevant document chunks are retrieved.
3. The retrieved context is sent to Google Gemini.
4. Gemini generates an answer based on the provided context.
5. Source document and page references are returned.

## 🔌 API Endpoints

| Method   | Endpoint               | Description                   |
| -------- | ---------------------- | ----------------------------- |
| `GET`    | `/api/health`          | Check backend status          |
| `POST`   | `/api/upload`          | Upload and process a PDF      |
| `GET`    | `/api/documents`       | Get uploaded documents        |
| `POST`   | `/api/search`          | Perform semantic search       |
| `POST`   | `/api/ask`             | Ask questions using RAG       |
| `DELETE` | `/api/delete/<doc_id>` | Delete a document             |
| `GET`    | `/api/stats`           | Get knowledge base statistics |

## ⚙️ Configuration

* **Maximum PDF size:** 50 MB
* **Allowed file type:** PDF
* **Chunk size:** 500 characters
* **Chunk overlap:** 100 characters
* **Retrieved chunks:** Top 5

## ⚠️ Technical Note

The current version uses a **deterministic hash-based embedding function** for demonstration purposes. It is not a true semantic embedding model, so search quality may be limited.

For production use, the embedding layer can be replaced with a dedicated embedding model such as a Google embedding model or Sentence Transformers.

Page numbers are currently estimated based on chunk positions. More accurate citations can be achieved by processing and storing page-level chunks.

## 🔐 Security

* Store API keys in `.env`
* Never commit `.env` to GitHub
* Use `.gitignore` for sensitive and generated files
* Validate uploaded files
* Limit upload size
* Use secure filenames
* Restrict CORS origins in production

## 🚧 Future Enhancements

* [ ] Replace hash-based embeddings with real semantic embeddings
* [ ] Migrate to the modern Google GenAI SDK
* [ ] Improve page-level citation accuracy
* [ ] Add conversation history and chat memory
* [ ] Add user authentication
* [ ] Add OCR for scanned PDFs
* [ ] Add document preview
* [ ] Add multi-language support
* [ ] Add streaming Gemini responses
* [ ] Add advanced document filtering
* [ ] Add production deployment support

## 🎯 Use Cases

* 📚 Research paper analysis
* 🎓 Educational document exploration
* 🏢 Enterprise knowledge bases
* 🔬 Research and technical document analysis
* ⚖️ Large-scale document review
* 💻 Technical documentation search

## 👩‍💻 Author

**Arpita Mohapatra**

B.Tech — Computer Science and Engineering

---

⭐ If you find this project useful, consider giving it a star on GitHub.

**Built with ❤️ for intelligent document processing and AI-powered knowledge retrieval.**

**Version:** 2.0.0
**Last Updated:** July 2026
