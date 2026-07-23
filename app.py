"""
AI PDF Knowledge Assistant - Backend
Features:
- PDF Upload
- PDF Text Extraction
- Page-Aware Chunking
- ChromaDB Vector Storage
- Semantic Search
- RAG Question Answering
- Source Citations
- Multiple Document Support
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

import os
import json
import chromadb
import google.generativeai as genai
import PyPDF2
import uuid
from datetime import datetime
from dotenv import load_dotenv

import hashlib
import random


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# INITIALIZE FLASK APP
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# CONFIGURATION
# ============================================================

UPLOAD_FOLDER = './uploads'
CHROMA_DB_PATH = './chroma_db'
ALLOWED_EXTENSIONS = {'pdf'}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHROMA_DB_PATH, exist_ok=True)


# ============================================================
# INITIALIZE CHROMADB
# ============================================================

try:

    chroma_client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH
    )

    collection = chroma_client.get_or_create_collection(
        name="pdf_documents",
        metadata={
            "hnsw:space": "cosine"
        }
    )

    print("✓ ChromaDB initialized successfully")
    print(f"✓ ChromaDB path: {CHROMA_DB_PATH}")

except Exception as e:

    print(f"ChromaDB Error: {e}")

    chroma_client = None
    collection = None


# ============================================================
# INITIALIZE GOOGLE GENERATIVE AI
# ============================================================

api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:

    print("WARNING: GOOGLE_API_KEY not found in .env file")
    print("Please add:")
    print("GOOGLE_API_KEY=your_key_here")

else:

    genai.configure(api_key=api_key)

    print("✓ Google API configured")


# ============================================================
# DOCUMENT METADATA STORAGE
# ============================================================

documents_metadata = {}

metadata_file = './documents_metadata.json'


# ============================================================
# METADATA FUNCTIONS
# ============================================================

def load_metadata():
    """
    Load document metadata from JSON file.
    """

    global documents_metadata

    if os.path.exists(metadata_file):

        try:

            with open(metadata_file, 'r', encoding='utf-8') as f:

                documents_metadata = json.load(f)

        except Exception:

            documents_metadata = {}

    else:

        documents_metadata = {}


def save_metadata():
    """
    Save document metadata to JSON file.
    """

    try:

        with open(
            metadata_file,
            'w',
            encoding='utf-8'
        ) as f:

            json.dump(
                documents_metadata,
                f,
                indent=2
            )

    except Exception as e:

        print(
            f"Error saving metadata: {e}"
        )


# ============================================================
# FILE VALIDATION
# ============================================================

def allowed_file(filename):
    """
    Check if uploaded file is a PDF.
    """

    return (
        '.' in filename
        and
        filename.rsplit(
            '.',
            1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF while preserving
    the actual PDF page number.
    """

    pages = []

    metadata = {

        "filename": os.path.basename(
            pdf_path
        ),

        "upload_date": datetime.now().isoformat(),

        "pages": 0
    }

    try:

        with open(
            pdf_path,
            'rb'
        ) as file:

            pdf_reader = PyPDF2.PdfReader(
                file
            )

            metadata["pages"] = len(
                pdf_reader.pages
            )

            # Process every PDF page
            for page_num, page in enumerate(
                pdf_reader.pages,
                start=1
            ):

                try:

                    page_text = (
                        page.extract_text()
                        or ""
                    )

                    if page_text.strip():

                        pages.append({

                            "page": page_num,

                            "text": page_text

                        })

                    else:

                        pages.append({

                            "page": page_num,

                            "text": ""

                        })

                except Exception as e:

                    print(
                        f"Error extracting page "
                        f"{page_num}: {e}"
                    )

                    pages.append({

                        "page": page_num,

                        "text":
                        "[Error extracting text]"

                    })

    except Exception as e:

        raise Exception(
            f"Error reading PDF: {str(e)}"
        )

    return pages, metadata


# ============================================================
# PAGE-AWARE TEXT CHUNKING
# ============================================================

def chunk_text(
    pages,
    chunk_size=500,
    overlap=100
):
    """
    Split PDF pages into overlapping chunks
    while preserving the actual page number.

    Each returned chunk contains:

    {
        "text": "...",
        "page": 1
    }
    """

    chunks = []

    for page_data in pages:

        page_number = page_data[
            "page"
        ]

        text = page_data[
            "text"
        ]

        if not text.strip():

            continue

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[
                start:end
            ].strip()

            if chunk:

                chunks.append({

                    "text": chunk,

                    "page": page_number

                })

            # Prevent infinite loop
            if end >= len(text):

                break

            start = end - overlap

    return chunks


# ============================================================
# EMBEDDING FUNCTION
# ============================================================

def generate_embedding(text):
    """
    Generate a deterministic vector for the text.

    NOTE:
    This is currently a placeholder embedding method.
    It is NOT a true semantic embedding model.

    It is kept temporarily so the current application
    remains compatible with the existing ChromaDB setup.

    This should later be replaced with a real embedding
    model such as Gemini Embeddings.
    """

    try:

        hash_obj = hashlib.sha256(
            text.encode(
                'utf-8'
            )
        )

        random.seed(
            int(
                hash_obj.hexdigest(),
                16
            ) % (2 ** 31)
        )

        embedding = [

            random.uniform(
                -1,
                1
            )

            for _ in range(768)

        ]

        return embedding

    except Exception as e:

        print(
            f"Embedding error: {e}"
        )

        return [

            random.uniform(
                -1,
                1
            )

            for _ in range(768)

        ]


# ============================================================
# FRONTEND ROUTE
# ============================================================

@app.route('/')
def home():
    """
    Serve index.html from the project directory.
    """

    if os.path.exists(
        'index.html'
    ):

        return send_file(
            'index.html'
        )

    return jsonify({

        "message":
        "AI PDF Knowledge Assistant API is running",

        "status":
        "healthy",

        "frontend":
        "index.html not found"

    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route(
    '/api/health',
    methods=['GET']
)
def health_check():
    """
    Health check endpoint.
    """

    return jsonify({

        "status":
        "healthy",

        "service":
        "AI PDF Knowledge Assistant",

        "timestamp":
        datetime.now().isoformat()

    })


# ============================================================
# UPLOAD PDF
# ============================================================

@app.route(
    '/api/upload',
    methods=['POST']
)
def upload_pdf():
    """
    Upload and process PDF file.

    Workflow:

    PDF
    ↓
    Extract text
    ↓
    Preserve page numbers
    ↓
    Chunk text
    ↓
    Generate embeddings
    ↓
    Store in ChromaDB
    """

    try:

        load_metadata()

        # Check file
        if 'file' not in request.files:

            return jsonify({

                "error":
                "No file provided"

            }), 400

        file = request.files[
            'file'
        ]

        # Check filename
        if file.filename == '':

            return jsonify({

                "error":
                "No file selected"

            }), 400

        # Check extension
        if not allowed_file(
            file.filename
        ):

            return jsonify({

                "error":
                "Only PDF files are allowed"

            }), 400

        # Secure original filename
        filename = secure_filename(
            file.filename
        )

        # Generate unique filename
        unique_filename = (

            f"{uuid.uuid4()}_"
            f"{filename}"

        )

        filepath = os.path.join(

            app.config[
                'UPLOAD_FOLDER'
            ],

            unique_filename

        )

        # Save uploaded PDF
        file.save(
            filepath
        )

        print(
            f"✓ PDF saved: {filename}"
        )


        # ====================================================
        # EXTRACT PDF TEXT
        # ====================================================

        pages, metadata = (
            extract_text_from_pdf(
                filepath
            )
        )

        print(
            f"✓ Extracted "
            f"{metadata['pages']} pages"
        )


        # ====================================================
        # GENERATE DOCUMENT ID
        # ====================================================

        doc_id = str(
            uuid.uuid4()
        )


        # ====================================================
        # CHUNK TEXT
        # ====================================================

        chunks = chunk_text(
            pages
        )

        print(
            f"✓ Created "
            f"{len(chunks)} chunks"
        )


        if not chunks:

            return jsonify({

                "error":
                "No readable text found in PDF"

            }), 400


        # ====================================================
        # PREPARE CHROMADB DATA
        # ====================================================

        documents = []

        metadatas = []

        ids = []

        embeddings = []


        # ====================================================
        # GENERATE EMBEDDINGS
        # ====================================================

        for i, chunk_data in enumerate(
            chunks
        ):

            chunk = chunk_data[
                "text"
            ]

            page_number = chunk_data[
                "page"
            ]

            chunk_id = (

                f"{doc_id}_chunk_{i}"

            )

            embedding = (
                generate_embedding(
                    chunk
                )
            )


            documents.append(
                chunk
            )

            ids.append(
                chunk_id
            )

            embeddings.append(
                embedding
            )


            # IMPORTANT:
            # Store actual PDF page
            # instead of calculating
            # fake page numbers

            metadatas.append({

                "doc_id":
                doc_id,

                "chunk_index":
                i,

                "filename":
                metadata[
                    "filename"
                ],

                "page":
                page_number,

                "upload_date":
                metadata[
                    "upload_date"
                ]

            })


        # ====================================================
        # STORE IN CHROMADB
        # ====================================================

        if collection is None:

            return jsonify({

                "error":
                "ChromaDB is not initialized"

            }), 500


        try:

            collection.add(

                ids=ids,

                embeddings=embeddings,

                documents=documents,

                metadatas=metadatas

            )

            print(
                f"✓ Stored "
                f"{len(chunks)} chunks "
                f"in ChromaDB"
            )

        except Exception as e:

            print(
                f"ChromaDB add error: {e}"
            )

            return jsonify({

                "error":
                f"Failed to store PDF in ChromaDB: {str(e)}"

            }), 500


        # ====================================================
        # SAVE DOCUMENT METADATA
        # ====================================================

        documents_metadata[
            doc_id
        ] = {

            "filename":
            metadata[
                "filename"
            ],

            "pages":
            metadata[
                "pages"
            ],

            "chunks":
            len(chunks),

            "upload_date":
            metadata[
                "upload_date"
            ],

            "filepath":
            filepath

        }

        save_metadata()


        # ====================================================
        # RETURN SUCCESS
        # ====================================================

        return jsonify({

            "success":
            True,

            "doc_id":
            doc_id,

            "filename":
            metadata[
                "filename"
            ],

            "pages":
            metadata[
                "pages"
            ],

            "chunks":
            len(chunks),

            "message":
            (
                f"Successfully processed "
                f"{metadata['filename']}"
            )

        }), 201


    except Exception as e:

        print(
            f"Upload error: {e}"
        )

        return jsonify({

            "error":
            str(e)

        }), 500


# ============================================================
# GET DOCUMENTS
# ============================================================

@app.route(
    '/api/documents',
    methods=['GET']
)
def get_documents():
    """
    Get all uploaded documents.
    """

    try:

        load_metadata()

        return jsonify({

            "success":
            True,

            "documents":
            documents_metadata,

            "count":
            len(
                documents_metadata
            )

        })

    except Exception as e:

        return jsonify({

            "error":
            str(e)

        }), 500


# ============================================================
# SEMANTIC SEARCH
# ============================================================

@app.route(
    '/api/search',
    methods=['POST']
)
def semantic_search():
    """
    Search the knowledge base.

    Current workflow:

    Query
    ↓
    Generate query embedding
    ↓
    ChromaDB similarity search
    ↓
    Return chunks + page citations
    """

    try:

        data = request.json or {}

        query = data.get(
            'query',
            ''
        ).strip()


        if not query:

            return jsonify({

                "error":
                "Query is required"

            }), 400


        if collection is None:

            return jsonify({

                "error":
                "ChromaDB is not initialized"

            }), 500


        # Generate query embedding
        query_embedding = (
            generate_embedding(
                query
            )
        )


        # Search ChromaDB
        try:

            results = collection.query(

                query_embeddings=[
                    query_embedding
                ],

                n_results=5,

                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]

            )

        except Exception as e:

            print(
                f"Search error: {e}"
            )

            return jsonify({

                "error":
                f"Search failed: {str(e)}"

            }), 500


        # Format results
        formatted_results = []


        if (

            results.get(
                'documents'
            )

            and

            len(
                results[
                    'documents'
                ]
            ) > 0

        ):

            documents = (
                results[
                    'documents'
                ][0]
            )

            metadatas = (
                results[
                    'metadatas'
                ][0]
            )

            distances = (
                results.get(
                    'distances',
                    [[]]
                )[0]
            )


            for i, doc in enumerate(
                documents
            ):

                metadata = (

                    metadatas[i]

                    if i < len(
                        metadatas
                    )

                    else {}

                )


                distance = (

                    distances[i]

                    if i < len(
                        distances
                    )

                    else 1.0

                )


                formatted_results.append({

                    "chunk":
                    doc,

                    "similarity":
                    max(
                        0,
                        1 - distance
                    ),

                    "filename":
                    metadata.get(
                        "filename"
                    ),

                    "page":
                    metadata.get(
                        "page"
                    ),

                    "doc_id":
                    metadata.get(
                        "doc_id"
                    )

                })


        return jsonify({

            "success":
            True,

            "query":
            query,

            "results":
            formatted_results,

            "count":
            len(
                formatted_results
            )

        })


    except Exception as e:

        return jsonify({

            "error":
            str(e)

        }), 500


# ============================================================
# ASK QUESTION - RAG
# ============================================================

@app.route(
    '/api/ask',
    methods=['POST']
)
def ask_question():
    """
    Ask a question about uploaded documents.

    Workflow:

    Question
    ↓
    Query embedding
    ↓
    ChromaDB retrieval
    ↓
    Build context
    ↓
    Gemini 2.5 Flash
    ↓
    Answer with citations
    """

    try:

        if not os.getenv(
            'GOOGLE_API_KEY'
        ):

            return jsonify({

                "error":
                "Google API key not configured"

            }), 500


        data = request.json or {}

        question = data.get(
            'question',
            ''
        ).strip()


        if not question:

            return jsonify({

                "error":
                "Question is required"

            }), 400


        if collection is None:

            return jsonify({

                "error":
                "ChromaDB is not initialized"

            }), 500


        # ====================================================
        # RETRIEVE RELEVANT DOCUMENT CHUNKS
        # ====================================================

        query_embedding = (
            generate_embedding(
                question
            )
        )


        try:

            search_results = (
                collection.query(

                    query_embeddings=[
                        query_embedding
                    ],

                    n_results=5,

                    include=[
                        "documents",
                        "metadatas",
                        "distances"
                    ]

                )
            )

        except Exception as e:

            print(
                f"RAG search error: {e}"
            )

            return jsonify({

                "error":
                f"Document search failed: {str(e)}"

            }), 500


        # ====================================================
        # BUILD CONTEXT
        # ====================================================

        context_parts = []

        sources = []

        seen_sources = set()


        documents = (

            search_results.get(
                'documents',
                [[]]
            )[0]

        )


        metadatas = (

            search_results.get(
                'metadatas',
                [[]]
            )[0]

        )


        for i, doc in enumerate(
            documents
        ):

            if i >= len(
                metadatas
            ):

                continue


            metadata = metadatas[i]


            filename = metadata.get(
                "filename",
                "Unknown document"
            )


            page = metadata.get(
                "page",
                "Unknown"
            )


            doc_id = metadata.get(
                "doc_id",
                ""
            )


            # Add chunk to context

            context_parts.append(

                f"Document: {filename}\n"
                f"Page: {page}\n"
                f"Content:\n{doc}"

            )


            # Use filename + page
            # as unique source

            source_key = (

                f"{doc_id}_"
                f"{filename}_"
                f"{page}"

            )


            if source_key not in seen_sources:

                seen_sources.add(
                    source_key
                )

                sources.append({

                    "filename":
                    filename,

                    "page":
                    page,

                    "doc_id":
                    doc_id

                })


        context = "\n\n".join(
            context_parts
        )


        # ====================================================
        # GENERATE GEMINI ANSWER
        # ====================================================

        try:

            model = (
                genai.GenerativeModel(
                    'gemini-2.5-flash'
                )
            )


            prompt = f"""
You are an AI PDF Knowledge Assistant.

Answer the user's question using ONLY the information
provided in the document context below.

IMPORTANT RULES:

1. Do not invent or assume information.
2. If the answer is not available in the provided context,
   clearly say that the information was not found.
3. When using information from a document, cite the source.
4. Use this exact citation format:

[Source: filename, Page X]

5. If multiple documents or pages support the answer,
   cite each relevant source.
6. Keep the answer clear and concise.
7. Do not cite pages that are not present in the context.

DOCUMENT CONTEXT:

{context if context else "No documents found in the knowledge base."}

USER QUESTION:

{question}

ANSWER:
"""


            response = (
                model.generate_content(
                    prompt
                )
            )


            answer = (
                response.text
                if response.text
                else
                "No answer was generated."
            )


        except Exception as e:

            print(
                f"Gemini error: {e}"
            )

            answer = (
                f"Error generating answer: "
                f"{str(e)}"
            )


        # ====================================================
        # RETURN RAG RESPONSE
        # ====================================================

        return jsonify({

            "success":
            True,

            "question":
            question,

            "answer":
            answer,

            "sources":
            sources,

            "source_count":
            len(
                sources
            )

        })


    except Exception as e:

        return jsonify({

            "error":
            str(e)

        }), 500


# ============================================================
# DELETE DOCUMENT
# ============================================================

@app.route(
    '/api/delete/<doc_id>',
    methods=['DELETE']
)
def delete_document(doc_id):
    """
    Delete document from:

    1. ChromaDB
    2. Metadata JSON
    3. Uploaded files
    """

    try:

        load_metadata()


        # ====================================================
        # DELETE CHROMADB CHUNKS
        # ====================================================

        if collection is not None:

            try:

                results = collection.get(

                    where={
                        "doc_id":
                        doc_id
                    }

                )


                if results.get(
                    'ids'
                ):

                    collection.delete(

                        ids=results[
                            'ids'
                        ]

                    )

                    print(
                        f"✓ Deleted "
                        f"ChromaDB chunks "
                        f"for {doc_id}"
                    )


            except Exception as e:

                print(
                    f"ChromaDB delete error: {e}"
                )


        # ====================================================
        # DELETE METADATA + PDF FILE
        # ====================================================

        if doc_id in documents_metadata:

            filepath = (
                documents_metadata[
                    doc_id
                ].get(
                    'filepath'
                )
            )


            if (

                filepath

                and

                os.path.exists(
                    filepath
                )

            ):

                os.remove(
                    filepath
                )


            del documents_metadata[
                doc_id
            ]


            save_metadata()


        return jsonify({

            "success":
            True,

            "message":
            (
                f"Document {doc_id} "
                f"deleted successfully"
            )

        })


    except Exception as e:

        return jsonify({

            "error":
            str(e)

        }), 500


# ============================================================
# KNOWLEDGE BASE STATISTICS
# ============================================================

@app.route(
    '/api/stats',
    methods=['GET']
)
def get_stats():
    """
    Get knowledge base statistics.
    """

    try:

        load_metadata()


        total_documents = len(
            documents_metadata
        )


        total_pages = sum(

            doc.get(
                'pages',
                0
            )

            for doc in
            documents_metadata.values()

        )


        total_chunks = sum(

            doc.get(
                'chunks',
                0
            )

            for doc in
            documents_metadata.values()

        )


        try:

            collection_size = (
                collection.count()
                if collection
                else
                0
            )

        except Exception:

            collection_size = (
                total_chunks
            )


        return jsonify({

            "success":
            True,

            "stats": {

                "total_documents":
                total_documents,

                "total_pages":
                total_pages,

                "total_chunks":
                total_chunks,

                "collection_size":
                collection_size

            }

        })


    except Exception as e:

        return jsonify({

            "error":
            str(e)

        }), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == '__main__':

    load_metadata()


    print(
        "\n" +
        "=" * 60
    )

    print(
        "  AI PDF Knowledge Assistant"
    )

    print(
        "=" * 60
    )

    print(
        "✓ Backend starting..."
    )

    print(
        "✓ Frontend: http://localhost:5000/"
    )

    print(
        "✓ API: http://localhost:5000/api"
    )

    print(
        "=" * 60 +
        "\n"
    )


    app.run(

        debug=True,

        host='localhost',

        port=5000

    )