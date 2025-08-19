Contract Risk Analyzer
======================

Overview
--------
The Contract Risk Analyzer is a web-based tool to extract, analyze, and visualize key clauses from contracts. Users can upload PDF contracts and choose different processing actions via dedicated buttons. The application processes the uploaded document using APIs and displays structured outputs in a user-friendly format.

Features
--------
- Upload a single PDF contract.
- Two separate actions via buttons:
  1. Analyze Contract – Extracts and summarizes key clauses.
  2. Extract Clauses – Outputs structured JSON of all clauses.
- Temporary storage of uploaded files until API processing.
- Support for asynchronous API calls to ensure smooth handling of dependent tasks.
- Interactive display of extracted data using tables and charts.

Project Structure
-----------------
Contract_Risk_Analyzer/
│
├─ cra/                        # Python environment / packages
│  ├─ Lib/
│  ├─ Scripts/
│  └─ ...  
├─ templates/                  # HTML templates (if any)
├─ main.py                     # Main FastAPI / Streamlit backend
├─ mainst.py                   # Streamlit frontend (optional)
├─ .gitignore
└─ README.md

How It Works
------------

1. File Upload
   - Users upload a PDF contract via the web interface.
   - The file is temporarily stored in memory or a temp folder.

2. API Calls via Buttons
   - The interface provides two buttons corresponding to two APIs:
     - Clicking a button triggers an API call (POST) to the appropriate route.
     - Example FastAPI route:
       @app.post("/analyze")
       async def analyze_file(file: UploadFile):
           ...
   - The button knows which API to call because its action or linked function references the route.

3. File Processing
   - The API function reads the uploaded file from the temp storage.
   - Converts the file to text (e.g., using PyMuPDF or OCR if needed).
   - Performs further processing (clause extraction, risk analysis, etc.).

4. Async Handling
   - API functions are asynchronous to avoid blocking.
   - Use async and await when calling APIs or reading large files.
   - Dependent tasks wait for the previous step using await, ensuring proper sequential processing.

5. Output
   - Structured data (JSON, DataFrame, or table) is returned from the API.
   - Displayed interactively in the frontend.

Installation
------------
1. Clone the repository:
   git clone <your-repo-url>
   cd Contract_Risk_Analyzer

2. Create a virtual environment:
   python -m venv cra

3. Activate the environment:
   - Windows:
     cra\Scripts\activate
   - macOS/Linux:
     source cra/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Create a .env file for API keys (if required):
   GROQ_API_KEY=your_api_key_here

Usage
-----
- Run Streamlit frontend:
  streamlit run mainst.py

- Run FastAPI backend:
  uvicorn main:app --reload

- Open the browser and upload a PDF.
- Click one of the buttons to process the file.
- View the extracted or analyzed clauses in a structured format.

Notes
-----
- Avoid committing __pycache__, .pyc files, or Lib/site-packages/ to Git.
- Ensure .gitignore includes:
  __pycache__/
  *.pyc
  cra/Lib/site-packages/
- Uploaded files are temporary; they are processed only when an API call is triggered.
