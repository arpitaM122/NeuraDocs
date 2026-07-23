"""
Configuration module for AI PDF Knowledge Assistant
"""

import os
from pathlib import Path

# Environment
ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = ENV == 'development'

# Paths
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
CHROMA_DB_PATH = os.path.join(BASE_DIR, 'chroma_db')
METADATA_FILE = os.path.join(BASE_DIR, 'documents_metadata.json')

# File settings
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_UPLOAD_FILES = 100

# API settings
API_HOST = os.getenv('API_HOST', 'localhost')
API_PORT = int(os.getenv('API_PORT', 5000))
API_DEBUG = DEBUG

# Gemini settings
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY', '')
GEMINI_MODEL = 'gemini-2.5-flash'
EMBEDDING_MODEL = 'gemini-embedding-001'

# ChromaDB settings
CHROMA_COLLECTION_NAME = 'pdf_documents'
CHROMA_METRIC = 'cosine'

# Text processing
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 100  # Overlap between chunks
MIN_CHUNK_LENGTH = 50  # Minimum chunk length

# Search settings
SEARCH_TOP_K = 5  # Number of results to return
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity score

# RAG settings
RAG_MAX_TOKENS = 2000
RAG_TEMPERATURE = 0.7

# CORS settings
CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', '*']

# Logging
LOG_LEVEL = 'INFO' if DEBUG else 'ERROR'
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHROMA_DB_PATH, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)