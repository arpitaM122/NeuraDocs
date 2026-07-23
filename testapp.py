#!/usr/bin/env python3
"""
Test script for AI PDF Knowledge Assistant

Tests:

1. Configuration
2. API Health Check
3. Document Listing
4. Knowledge Base Statistics
5. Semantic Search
6. RAG Question Answering
7. PDF Upload
   """

import requests
import os
import sys
import time
from pathlib import Path
from datetime import datetime

# ============================================================

# CONFIGURATION

# ============================================================

API_BASE_URL = "http://localhost:5000/api"

TEST_RESULTS = {
"passed": [],
"failed": [],
"errors": []
}

# ============================================================

# COLORS

# ============================================================

class Colors:
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

# ============================================================

# PRINT HELPERS

# ============================================================

def print_header(text):
"""Print a formatted section header."""
print(f"\n{Colors.BLUE}{'=' * 60}")
print(f"  {text}")
print(f"{'=' * 60}{Colors.END}\n")

def print_success(text):
"""Print success message."""
print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
"""Print error message."""
print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
"""Print warning message."""
print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

# ============================================================

# TEST 0: CONFIGURATION

# ============================================================

def test_configuration():
"""Check project configuration and required packages."""

```
print_header("Test 0: Configuration Check")

config_ok = True

# --------------------------------------------------------
# Check .env file
# --------------------------------------------------------

if os.path.exists(".env"):
    print_success(".env file found")

    try:
        with open(".env", "r", encoding="utf-8") as f:
            env_content = f.read()

        if "GOOGLE_API_KEY=" in env_content:
            print_success("GOOGLE_API_KEY entry found in .env")

            # Do not print the actual API key
            key_value = env_content.split(
                "GOOGLE_API_KEY=", 1
            )[1].splitlines()[0].strip()

            if key_value and key_value != "your_api_key_here":
                print_success("GOOGLE_API_KEY appears to be configured")
            else:
                print_warning(
                    "GOOGLE_API_KEY is present but may not contain a valid key"
                )
                config_ok = False

        else:
            print_error("GOOGLE_API_KEY not found in .env")
            print("Add the following to your .env file:")
            print("GOOGLE_API_KEY=your_gemini_api_key_here")
            config_ok = False

    except Exception as e:
        print_error(f"Error reading .env file: {e}")
        config_ok = False

else:
    print_warning(".env file not found")
    print("Create a .env file in the project root with:")
    print("GOOGLE_API_KEY=your_gemini_api_key_here")
    config_ok = False

# --------------------------------------------------------
# Check required directories
# --------------------------------------------------------

print("\nChecking project directories:")

required_dirs = [
    "uploads",
    "chroma_db"
]

for dir_name in required_dirs:

    if os.path.exists(dir_name):
        print_success(f"{dir_name}/ directory exists")

    else:
        print_warning(
            f"{dir_name}/ directory does not exist "
            "(the backend may create it automatically)"
        )

# --------------------------------------------------------
# Check required Python packages
# --------------------------------------------------------

print("\nChecking required Python packages:")

required_packages = {
    "flask": "Flask",
    "flask_cors": "Flask-CORS",
    "google.generativeai": "google-generativeai",
    "chromadb": "ChromaDB",
    "PyPDF2": "PyPDF2",
    "dotenv": "python-dotenv",
    "requests": "requests"
}

missing_packages = []

for import_name, package_name in required_packages.items():

    try:
        __import__(import_name)
        print_success(f"{package_name} is installed")

    except ImportError:
        print_error(f"{package_name} is not installed")
        missing_packages.append(package_name)
        config_ok = False

# --------------------------------------------------------
# Print installation command
# --------------------------------------------------------

if missing_packages:

    print("\nMissing packages detected.")

    print(
        "Install them using:"
    )

    print(
        "pip install "
        + " ".join(missing_packages)
    )

# --------------------------------------------------------
# Save result
# --------------------------------------------------------

if config_ok:
    TEST_RESULTS["passed"].append("Configuration Check")
    print_success("Configuration check passed")

else:
    TEST_RESULTS["failed"].append("Configuration Check")
    print_error("Configuration check failed")

return config_ok
```

# ============================================================

# TEST 1: HEALTH CHECK

# ============================================================

def test_health_check():
"""Test API health check endpoint."""

```
print_header("Test 1: Health Check")

try:

    response = requests.get(
        f"{API_BASE_URL}/health",
        timeout=10
    )

    if response.status_code == 200:

        data = response.json()

        print(f"Status: {data.get('status', 'Unknown')}")
        print(f"Service: {data.get('service', 'Unknown')}")
        print(f"Timestamp: {data.get('timestamp', 'Unknown')}")

        print_success("Health check passed")

        TEST_RESULTS["passed"].append(
            "Health Check"
        )

        return True

    else:

        print_error(
            f"Health check failed with "
            f"status {response.status_code}"
        )

        TEST_RESULTS["failed"].append(
            "Health Check"
        )

        return False

except requests.exceptions.ConnectionError:

    print_error(
        "Could not connect to the backend."
    )

    print_warning(
        "Make sure the backend is running with:"
    )

    print("python app.py")

    TEST_RESULTS["errors"].append(
        "Connection Error"
    )

    return False

except Exception as e:

    print_error(
        f"Unexpected error: {str(e)}"
    )

    TEST_RESULTS["errors"].append(
        str(e)
    )

    return False
```

# ============================================================

# TEST 2: GET DOCUMENTS

# ============================================================

def test_get_documents():
"""Test retrieving uploaded documents."""

```
print_header("Test 2: Get Documents")

try:

    response = requests.get(
        f"{API_BASE_URL}/documents",
        timeout=10
    )

    if response.status_code == 200:

        data = response.json()

        documents = data.get(
            "documents",
            {}
        )

        count = data.get(
            "count",
            len(documents)
        )

        print(f"Total documents: {count}")

        if count > 0:

            for doc_id, doc in documents.items():

                print(
                    f"  - {doc.get('filename', 'Unknown')} "
                    f"({doc.get('pages', 0)} pages, "
                    f"{doc.get('chunks', 0)} chunks)"
                )

        else:

            print_warning(
                "No documents uploaded yet."
            )

        print_success(
            "Get documents test passed"
        )

        TEST_RESULTS["passed"].append(
            "Get Documents"
        )

        return True

    else:

        print_error(
            f"Get documents failed with "
            f"status {response.status_code}"
        )

        TEST_RESULTS["failed"].append(
            "Get Documents"
        )

        return False

except Exception as e:

    print_error(
        f"Error getting documents: {str(e)}"
    )

    TEST_RESULTS["errors"].append(
        str(e)
    )

    return False
```

# ============================================================

# TEST 3: GET STATISTICS

# ============================================================

def test_get_stats():
"""Test knowledge base statistics."""

```
print_header("Test 3: Knowledge Base Statistics")

try:

    response = requests.get(
        f"{API_BASE_URL}/stats",
        timeout=10
    )

    if response.status_code == 200:

        data = response.json()

        stats = data.get(
            "stats",
            {}
        )

        print(
            f"Total documents: "
            f"{stats.get('total_documents', 0)}"
        )

        print(
            f"Total pages: "
            f"{stats.get('total_pages', 0)}"
        )

        print(
            f"Total chunks: "
            f"{stats.get('total_chunks', 0)}"
        )

        print(
            f"Collection size: "
            f"{stats.get('collection_size', 0)}"
        )

        print_success(
            "Statistics test passed"
        )

        TEST_RESULTS["passed"].append(
            "Get Statistics"
        )

        return True

    else:

        print_error(
            f"Statistics request failed with "
            f"status {response.status_code}"
        )

        TEST_RESULTS["failed"].append(
            "Get Statistics"
        )

        return False

except Exception as e:

    print_error(
        f"Error getting statistics: {str(e)}"
    )

    TEST_RESULTS["errors"].append(
        str(e)
    )

    return False
```

# ============================================================

# TEST 4: SEMANTIC SEARCH

# ============================================================

def test_search(query="machine learning"):
"""Test semantic search."""

```
print_header(
    f"Test 4: Semantic Search"
)

try:

    payload = {
        "query": query
    }

    response = requests.post(
        f"{API_BASE_URL}/search",
        json=payload,
        timeout=30
    )

    if response.status_code == 200:

        data = response.json()

        print(
            f"Query: "
            f"{data.get('query', query)}"
        )

        print(
            f"Results found: "
            f"{data.get('count', 0)}"
        )

        results = data.get(
            "results",
            []
        )

        if results:

            for i, result in enumerate(
                results,
                1
            ):

                print(
                    f"\n  Result {i}:"
                )

                print(
                    f"    Source: "
                    f"{result.get('filename', 'Unknown')} "
                    f"(Page "
                    f"{result.get('page', 'Unknown')})"
                )

                similarity = result.get(
                    "similarity",
                    0
                )

                print(
                    f"    Similarity: "
                    f"{similarity:.2%}"
                )

                chunk = result.get(
                    "chunk",
                    ""
                )

                print(
                    f"    Text: "
                    f"{chunk[:150]}..."
                )

        else:

            print_warning(
                "No results found."
            )

            print(
                "Upload a PDF before testing "
                "semantic search."
            )

        print_success(
            "Semantic search test completed"
        )

        TEST_RESULTS["passed"].append(
            "Semantic Search"
        )

        return True

    else:

        try:
            data = response.json()
            error = data.get(
                "error",
                "Unknown error"
            )
        except Exception:
            error = response.text

        print_error(
            f"Search failed: {error}"
        )

        TEST_RESULTS["failed"].append(
            "Semantic Search"
        )

        return False

except Exception as e:

    print_error(
        f"Error performing search: {str(e)}"
    )

    TEST_RESULTS["errors"].append(
        str(e)
    )

    return False
```

# ============================================================

# TEST 5: QUESTION ANSWERING / RAG

# ============================================================

def test_ask_question(
question="What is the main topic?"
):
"""Test RAG-based question answering."""

```
print_header(
    "Test 5: Question Answering (RAG)"
)

try:

    payload = {
        "question": question
    }

    response = requests.post(
        f"{API_BASE_URL}/ask",
        json=payload,
        timeout=60
    )

    if response.status_code == 200:

        data = response.json()

        print(
            f"Question: "
            f"{data.get('question', question)}"
        )

        print(
            f"\nAnswer:\n"
            f"{data.get('answer', 'No answer returned')}\n"
        )

        sources = data.get(
            "sources",
            []
        )

        source_count = data.get(
            "source_count",
            len(sources)
        )

        if source_count > 0:

            print(
                f"Sources ({source_count}):"
            )

            for source in sources:

                print(
                    f"  - "
                    f"{source.get('filename', 'Unknown')} "
                    f"(Page "
                    f"{source.get('page', 'Unknown')})"
                )

        else:

            print_warning(
                "No sources found."
            )

            print(
                "Make sure a PDF has been "
                "uploaded and indexed."
            )

        print_success(
            "Question answering test passed"
        )

        TEST_RESULTS["passed"].append(
            "Question Answering"
        )

        return True

    else:

        try:
            data = response.json()

            error = data.get(
                "error",
                "Unknown error"
            )

        except Exception:

            error = response.text

        print_error(
            f"Question answering failed: "
            f"{error}"
        )

        TEST_RESULTS["failed"].append(
            "Question Answering"
        )

        return False

except Exception as e:

    print_error(
        f"Error asking question: {str(e)}"
    )

    TEST_RESULTS["errors"].append(
        str(e)
    )

    return False
```

# ============================================================

# TEST 6: PDF UPLOAD

# ============================================================

def test_upload_pdf():
"""Test PDF upload."""

```
print_header(
    "Test 6: PDF Upload"
)

test_pdf_paths = [

    "test.pdf",

    "sample.pdf",

    Path("tests") / "sample.pdf"

]

test_pdf = None

for path in test_pdf_paths:

    if os.path.exists(path):

        test_pdf = path

        break

if not test_pdf:

    print_warning(
        "No test PDF file found."
    )

    print(
        "Upload test skipped."
    )

    print(
        "To test PDF upload, place a PDF "
        "named 'test.pdf' or 'sample.pdf' "
        "in the project directory."
    )

    return True

try:

    with open(
        test_pdf,
        "rb"
    ) as f:

        files = {
            "file": (
                Path(test_pdf).name,
                f,
                "application/pdf"
            )
        }

        response = requests.post(
            f"{API_BASE_URL}/upload",
            files=files,
            timeout=120
        )

    if response.status_code == 201:

        data = response.json()

        print(
            f"Filename: "
            f"{data.get('filename', 'Unknown')}"
        )

        print(
            f"Pages: "
            f"{data.get('pages', 0)}"
        )

        print(
            f"Chunks: "
            f"{data.get('chunks', 0)}"
        )

        print(
            f"Message: "
            f"{data.get('message', '')}"
        )

        print_success(
            "PDF upload test passed"
        )

        TEST_RESULTS["passed"].append(
            "PDF Upload"
        )

        return True

    else:

        try:

            data = response.json()

            error = data.get(
                "error",
                "Unknown error"
            )

        except Exception:

            error = response.text

        print_error(
            f"Upload failed: {error}"
        )

        TEST_RESULTS["failed"].append(
            "PDF Upload"
        )

        return False

except Exception as e:

    print_error(
        f"Error uploading PDF: {str(e)}"
    )

    TEST_RESULTS["errors"].append(
        str(e)
    )

    return False
```

# ============================================================

# TEST SUMMARY

# ============================================================

def print_summary():
"""Print test summary."""

```
print_header(
    "Test Summary"
)

total = (
    len(TEST_RESULTS["passed"])
    + len(TEST_RESULTS["failed"])
    + len(TEST_RESULTS["errors"])
)

passed = len(
    TEST_RESULTS["passed"]
)

failed = len(
    TEST_RESULTS["failed"]
)

errors = len(
    TEST_RESULTS["errors"]
)

print(
    f"Total tests: {total}"
)

print(
    f"{Colors.GREEN}"
    f"Passed: {passed}"
    f"{Colors.END}"
)

print(
    f"{Colors.RED}"
    f"Failed: {failed}"
    f"{Colors.END}"
)

print(
    f"{Colors.YELLOW}"
    f"Errors: {errors}"
    f"{Colors.END}\n"
)

if TEST_RESULTS["passed"]:

    print(
        "Passed tests:"
    )

    for test in TEST_RESULTS["passed"]:

        print(
            f"  {Colors.GREEN}"
            f"✓ {test}"
            f"{Colors.END}"
        )

if TEST_RESULTS["failed"]:

    print(
        "\nFailed tests:"
    )

    for test in TEST_RESULTS["failed"]:

        print(
            f"  {Colors.RED}"
            f"✗ {test}"
            f"{Colors.END}"
        )

if TEST_RESULTS["errors"]:

    print(
        "\nErrors:"
    )

    for error in TEST_RESULTS["errors"]:

        print(
            f"  {Colors.YELLOW}"
            f"⚠ {error}"
            f"{Colors.END}"
        )

success_rate = (
    passed / total * 100
    if total > 0
    else 0
)

if success_rate == 100:

    print(
        f"\n{Colors.GREEN}"
        f"All tests passed! ✓"
        f"{Colors.END}"
    )

    return 0

elif success_rate >= 80:

    print(
        f"\n{Colors.YELLOW}"
        f"Most tests passed "
        f"({success_rate:.0f}%)"
        f"{Colors.END}"
    )

    return 1

else:

    print(
        f"\n{Colors.RED}"
        f"Some tests failed "
        f"({success_rate:.0f}%)"
        f"{Colors.END}"
    )

    return 1
```

# ============================================================

# MAIN

# ============================================================

def main():
"""Run all tests."""

```
print(
    f"\n{Colors.BLUE}"
    f"{'=' * 60}"
)

print(
    "  AI PDF Knowledge Assistant - Test Suite"
)

print(
    f"  Started at: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

print(
    f"{'=' * 60}"
    f"{Colors.END}\n"
)

# --------------------------------------------------------
# Configuration test
# --------------------------------------------------------

test_configuration()

print(
    "\n(Waiting 2 seconds before API tests...)\n"
)

time.sleep(2)

# --------------------------------------------------------
# API tests
# --------------------------------------------------------

test_health_check()

test_get_documents()

test_get_stats()

test_search()

test_ask_question()

test_upload_pdf()

# --------------------------------------------------------
# Summary
# --------------------------------------------------------

exit_code = print_summary()

print(
    f"\n{Colors.BLUE}"
    f"{'=' * 60}"
)

print(
    f"  Tests completed at: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

print(
    f"{'=' * 60}"
    f"{Colors.END}\n"
)

return exit_code
```

# ============================================================

# ENTRY POINT

# ============================================================

if **name** == "**main**":

```
try:

    exit_code = main()

    sys.exit(exit_code)

except KeyboardInterrupt:

    print(
        f"\n{Colors.YELLOW}"
        f"Tests interrupted by user"
        f"{Colors.END}"
    )

    sys.exit(1)

except Exception as e:

    print(
        f"\n{Colors.RED}"
        f"Unexpected error: {str(e)}"
        f"{Colors.END}"
    )

    sys.exit(1)
