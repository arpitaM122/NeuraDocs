# 📚 AI PDF Knowledge Assistant

An AI-powered PDF Knowledge Assistant that allows users to upload PDF documents, perform semantic searches, and ask questions about their documents using a Retrieval-Augmented Generation (RAG) pipeline.

The application combines a **Flask REST API backend**, **ChromaDB vector database**, **Google Gemini**, and a modern **HTML/CSS/JavaScript frontend** to create an interactive document question-answering system.

---

## ✨ Features

* 📤 **PDF Document Upload** — Upload one or multiple PDF documents
* 📄 **Automatic PDF Text Extraction** — Extract text and page information using PyPDF2
* 🧩 **Text Chunking** — Split extracted document text into overlapping chunks
* 🔍 **Semantic Search** — Search across uploaded documents using natural-language queries
* 💬 **AI-Powered Q&A** — Ask questions about uploaded documents
* 🤖 **Google Gemini Integration** — Generate AI answers using Google's Gemini models
* 📌 **Source Citations** — Answers include document names and page references
* 🗂️ **Document Management** — View and delete uploaded documents
* 📊 **Knowledge Base Statistics** — Monitor documents, pages, and chunks
* 🖱️ **Drag-and-Drop Upload** — Easily upload PDF files through the web interface
* 🎨 **Modern Responsive UI** — Clean and responsive frontend interface
* ⚡ **REST API** — Backend functionality exposed through Flask API endpoints
* 💾 **Persistent Vector Storage** — Store document chunks and metadata using ChromaDB

---

## 🏗️ Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                  Frontend (HTML / CSS / JavaScript)            │
│                                                               │
│  Upload PDFs │ Semantic Search │ Ask Questions │ Statistics   │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                │ HTTP REST API
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                     Flask Backend (Python)                    │
│                                                               │
│  /api/upload    /api/search    /api/ask                       │
│  /api/documents /api/delete    /api/stats                     │
└───────────────┬───────────────────────────────┬───────────────┘
                │                               │
                ▼                               ▼
┌──────────────────────────┐      ┌─────────────────────────────┐
│     PDF Processing       │      │       ChromaDB              │
│                          │      │                             │
│ PyPDF2                   │      │ Persistent Vector Database │
│ Text Extraction          │      │ Document Chunks             │
│ Page Metadata            │      │ Metadata                    │
│ Text Chunking            │      │ Similarity Search            │
└──────────────────────────┘      └──────────────┬──────────────┘
                                                 │
                                                 │ Retrieved Context
                                                 ▼
                                    ┌─────────────────────────────┐
                                    │       RAG Pipeline          │
                                    │                             │
                                    │ Retrieved Document Context  │
                                    │            +                │
                                    │      User Question         │
                                    │            ↓                │
                                    │      Google Gemini          │
                                    │            ↓                │
                                    │     AI Generated Answer    │
                                    │       + Citations          │
                                    └─────────────────────────────┘
```

---

## 📁 Project Structure

```text
knowledge_assistant/
│
├── app.py
├── index.html
├── requirements.txt
├── .env
├── documents_metadata.json
│
├── uploads/
│   └── Uploaded PDF files
│
├── chroma_db/
│   └── Persistent ChromaDB data
│
└── venv/
    └── Python virtual environment
```

### Main Files

| File / Folder             | Description                              |
| ------------------------- | ---------------------------------------- |
| `app.py`                  | Flask backend and REST API               |
| `index.html`              | Frontend user interface                  |
| `requirements.txt`        | Python dependencies                      |
| `.env`                    | Environment variables and Google API key |
| `documents_metadata.json` | Stores uploaded document metadata        |
| `uploads/`                | Stores uploaded PDF files                |
| `chroma_db/`              | Persistent ChromaDB storage              |
| `venv/`                   | Python virtual environment               |

---

# 🚀 Getting Started

## Prerequisites

Make sure you have the following installed:

* Python 3.8+
* pip
* Git (optional)
* Modern web browser
* Google Gemini API key

---

## 1. Clone or Download the Project

```bash
git clone <your-repository-url>
cd knowledge_assistant
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt` file, install the main dependencies:

```bash
pip install flask flask-cors chromadb PyPDF2 python-dotenv google-generativeai
```

> **Note:** The current backend uses the `google.generativeai` Python package. Google has deprecated this package in favor of the newer `google-genai` SDK. The application can be migrated to the newer SDK in a future update.

---

## 4. Configure the Google Gemini API Key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Do not commit your `.env` file to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
uploads/
chroma_db/
```

---

## 5. Start the Backend

Activate your virtual environment and run:

```bash
python app.py
```

The Flask API will run at:

```text
http://localhost:5000
```

You should see:

```text
✓ ChromaDB initialized successfully
✓ Google API configured

============================================================
  AI PDF Knowledge Assistant
============================================================
✓ Backend starting...
✓ API running on: http://localhost:5000
============================================================
```

---

## 6. Open the Frontend

Open `index.html` in your browser.

The frontend communicates with the Flask backend using:

```javascript
const API_BASE = 'http://localhost:5000/api';
```

> **Important:** If you open `index.html` directly using `file://`, browser security policies may sometimes cause connection problems. If you experience `Failed to fetch`, make sure the Flask backend is running and consider serving the frontend through a local web server.

For example:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/index.html
```

Keep the Flask backend running on:

```text
http://localhost:5000
```

---

# 📖 How to Use

## 📤 1. Upload Documents

1. Open the web interface.
2. Click the PDF upload area.
3. Select one or more PDF files.
4. The backend extracts text from the PDF.
5. The extracted text is divided into chunks.
6. Chunks are stored in ChromaDB.
7. Document metadata is saved locally.

The interface displays:

* Filename
* Number of pages
* Number of chunks
* Upload date

---

## 🔍 2. Semantic Search

Enter a natural-language query in the Semantic Search section.

Example:

```text
machine learning
```

or:

```text
What are the main groundwater contamination prediction methods?
```

The system retrieves the most relevant document chunks from ChromaDB.

Search results display:

* Relevant text
* Document filename
* Page number
* Similarity score

---

## 💬 3. Ask Questions

Use the Q&A section to ask questions about your uploaded documents.

Example:

```text
What problem does this research address?
```

```text
What methodology was used in the project?
```

```text
What are the main findings of the research?
```

```text
Which machine learning models were used?
```

```text
What datasets were used in the study?
```

The system:

1. Receives the question.
2. Searches the knowledge base.
3. Retrieves relevant document chunks.
4. Builds context from retrieved chunks.
5. Sends the context and question to Google Gemini.
6. Generates an answer.
7. Returns document and page references.

---

# 🧠 RAG Pipeline

The application follows a Retrieval-Augmented Generation workflow:

```text
                PDF Upload
                    │
                    ▼
            Extract PDF Text
                    │
                    ▼
              Text Chunking
                    │
                    ▼
           Generate Embeddings
                    │
                    ▼
              Store in ChromaDB
                    │
                    │
          User asks a question
                    │
                    ▼
           Generate Query Vector
                    │
                    ▼
         Similarity Search in DB
                    │
                    ▼
          Retrieve Top-5 Chunks
                    │
                    ▼
          Build Relevant Context
                    │
                    ▼
            Google Gemini Model
                    │
                    ▼
          Generate AI Response
                    │
                    ▼
         Answer + Source References
```

---

# 🔧 Backend Components

## Flask

Flask provides the REST API and handles:

* PDF uploads
* Document retrieval
* Semantic search
* Question answering
* Document deletion
* Statistics

---

## PyPDF2

PyPDF2 is used to:

* Read PDF files
* Extract text
* Count pages
* Preserve page-level information

---

## ChromaDB

ChromaDB acts as the persistent vector database.

It stores:

* Document chunks
* Chunk IDs
* Document IDs
* Filenames
* Page numbers
* Upload dates
* Embeddings

The application uses cosine similarity for vector comparison.

---

## Google Gemini

Google Gemini is used for generating answers from retrieved document context.

The RAG prompt instructs the model to:

* Answer using the provided document context
* Cite source documents
* Include page references
* Clearly state when information is unavailable

---

# 🔌 API Endpoints

| Method   | Endpoint               | Description                        |
| -------- | ---------------------- | ---------------------------------- |
| `GET`    | `/api/health`          | Check backend health               |
| `POST`   | `/api/upload`          | Upload and process a PDF           |
| `GET`    | `/api/documents`       | Retrieve uploaded documents        |
| `POST`   | `/api/search`          | Search the knowledge base          |
| `POST`   | `/api/ask`             | Ask questions using RAG            |
| `DELETE` | `/api/delete/<doc_id>` | Delete a document                  |
| `GET`    | `/api/stats`           | Retrieve knowledge base statistics |

---

# 🧪 API Examples

## Health Check

```bash
curl http://localhost:5000/api/health
```

---

## Upload a PDF

```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@document.pdf"
```

---

## Semantic Search

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"machine learning\"}"
```

---

## Ask a Question

```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is the main topic of the document?\"}"
```

---

## Get Documents

```bash
curl http://localhost:5000/api/documents
```

---

## Get Statistics

```bash
curl http://localhost:5000/api/stats
```

---

# ⚙️ Current Configuration

### File Upload

```python
UPLOAD_FOLDER = './uploads'
MAX_FILE_SIZE = 50 * 1024 * 1024
ALLOWED_EXTENSIONS = {'pdf'}
```

Maximum supported file size:

```text
50 MB
```

---

### Text Chunking

The current implementation uses:

```python
chunk_size = 500
overlap = 100
```

This means the extracted PDF text is divided into approximately 500-character chunks with 100 characters of overlap.

---

### Search

The application retrieves up to:

```text
5
```

relevant chunks for a search or question.

---

# ⚠️ Important Technical Notes

## Embedding Implementation

The current version uses a deterministic hash-based embedding function for demonstration and local semantic-search functionality.

The implementation generates a fixed-length vector based on the SHA-256 hash of the text.

This is **not a true semantic embedding model** and therefore search quality may be limited.

For production-quality semantic search, the embedding layer should be replaced with a real embedding model such as:

* Google Gemini embedding models
* Sentence Transformers
* Hugging Face embedding models
* Other dedicated embedding APIs

A production architecture would therefore be:

```text
PDF Text
   ↓
Real Embedding Model
   ↓
Semantic Vector
   ↓
ChromaDB
```

---

## Page Number Mapping

The current implementation estimates page numbers based on chunk position.

For more accurate source citations, a future version should:

1. Extract each PDF page separately.
2. Chunk each page independently.
3. Store the exact page number in each chunk's metadata.

This will improve citation accuracy.

---

## Gemini Model Configuration

The Gemini model is configured in `app.py`.

Example:

```python
model = genai.GenerativeModel('gemini-2.5-flash')
```

The available model name may depend on the Google Gemini SDK version and API configuration.

If you receive a model-not-found error, verify the available models supported by your installed SDK and API version.

---

# 🐛 Troubleshooting

## `Failed to fetch`

Make sure:

1. Flask is running.

```bash
python app.py
```

2. The API is accessible:

```text
http://localhost:5000/api/health
```

3. The frontend uses:

```javascript
const API_BASE = 'http://localhost:5000/api';
```

4. CORS is enabled.

```python
CORS(app)
```

5. If opening `index.html` directly does not work, serve it using:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/index.html
```

---

## `404 Not Found` on `/`

If you see:

```text
GET / HTTP/1.1" 404
```

this means Flask does not currently have a route for `/`.

The backend API is still running correctly.

You can access:

```text
http://localhost:5000/api/health
```

To serve the frontend directly from Flask, add a route such as:

```python
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
```

and import:

```python
from flask import send_from_directory
```

---

## Gemini Model Error

If you see:

```text
404 models/gemini-pro is not found
```

check the model name configured in `app.py`.

For example:

```python
model = genai.GenerativeModel('gemini-2.5-flash')
```

Also make sure your Google Gemini API key is correctly configured in `.env`.

---

## Google Generative AI Deprecation Warning

You may see:

```text
FutureWarning:
All support for the `google.generativeai` package has ended.
```

This occurs because the current project uses:

```python
import google.generativeai as genai
```

The recommended future migration is to the newer Google GenAI SDK.

---

## ChromaDB Error

If ChromaDB reports a deprecated configuration error, make sure the application uses the current persistent client configuration:

```python
chroma_client = chromadb.PersistentClient(
    path='./chroma_db'
)
```

If the existing database becomes incompatible during development, back up your data and recreate the ChromaDB directory.

---

# 🔐 Security Considerations

* Keep your Google API key inside `.env`.
* Never commit `.env` to GitHub.
* Use `.gitignore` for sensitive files.
* Validate uploaded files.
* Limit maximum upload size.
* Use `secure_filename()` for uploaded filenames.
* Restrict CORS origins before production deployment.
* Add authentication before exposing the application publicly.
* Do not expose API keys in frontend JavaScript.

---

# 📊 Knowledge Base Statistics

The application tracks:

* Total number of documents
* Total number of PDF pages
* Total number of text chunks
* ChromaDB collection size

These statistics are displayed in the frontend dashboard.

---

# 🎯 Use Cases

### 📚 Research Assistant

Search and query academic papers, research reports, and technical documents.

### 🎓 Education

Interactively explore textbooks, lecture notes, and study materials.

### 🏢 Enterprise Knowledge Base

Query internal documentation and company resources.

### 🔬 Research Document Analysis

Find methodologies, datasets, results, and conclusions from research papers.

### ⚖️ Document Review

Search through large collections of documents and retrieve relevant information.

### 💻 Technical Documentation

Ask questions about software documentation, manuals, and technical guides.

---

# 🚧 Future Enhancements

* [ ] Replace hash-based embeddings with production-quality semantic embeddings
* [ ] Migrate from `google.generativeai` to the modern `google-genai` SDK
* [ ] Improve page-level chunking and citation accuracy
* [ ] Serve frontend directly through Flask
* [ ] Add conversation history
* [ ] Add chat memory
* [ ] Add user authentication
* [ ] Add document preview
* [ ] Add PDF download/view functionality
* [ ] Add multi-language document support
* [ ] Add OCR support for scanned PDFs
* [ ] Add streaming Gemini responses
* [ ] Add advanced filtering by document and page
* [ ] Add document re-ranking
* [ ] Add embedding model selection
* [ ] Add production deployment support
* [ ] Add rate limiting and authentication
* [ ] Add export of AI-generated answers

---

# 📝 Hands-on Tasks

## Task 1: Upload a PDF

```text
1. Start the Flask backend.
2. Open the frontend.
3. Upload a PDF.
4. Wait for processing.
5. Verify the document appears in Uploaded Documents.
```

---

## Task 2: Search Documents

```text
1. Upload a PDF.
2. Enter a natural-language query.
3. Click Search.
4. Review matching document chunks.
5. Check similarity scores and page numbers.
```

---

## Task 3: Ask Questions

```text
1. Upload a PDF.
2. Enter a question.
3. Click Get Answer.
4. Review the generated response.
5. Check the listed source documents.
```

---

## Task 4: Test the RAG Pipeline

Try questions such as:

```text
What is the main objective of this research?
```

```text
What problem does the research address?
```

```text
What methodology was used?
```

```text
What datasets were used?
```

```text
What are the main findings?
```

```text
What machine learning models were used?
```

```text
What are the limitations of the proposed approach?
```

---

# 🤝 Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test the application.
5. Commit your changes.
6. Push the branch.
7. Open a Pull Request.

---

# 📄 License

This project is intended for educational, research, and development purposes.

Add an appropriate open-source license if you plan to distribute the project publicly.

---

# 🙏 Acknowledgments

* **Google Gemini** — AI-powered response generation
* **ChromaDB** — Persistent vector database
* **Flask** — Backend REST API
* **PyPDF2** — PDF text extraction
* **Flask-CORS** — Cross-Origin Resource Sharing
* **Python** — Core development language

---

## 👩‍💻 Author

**Arpita Mohapatra**

B.Tech — Computer Science and Engineering

---

⭐ If you find this project useful, consider giving it a star on GitHub.

---

**Built with ❤️ for intelligent document processing and AI-powered knowledge retrieval.**

**Version:** 2.0.0
**Last Updated:** July 2026
