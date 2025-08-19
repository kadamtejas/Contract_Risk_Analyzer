import os
import fitz  # PyMuPDF
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import streamlit as st
import json
from fastapi import FastAPI, UploadFile,File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# ===============================
# Load Environment Variables
# ===============================
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Enable CORS (important if you call API from JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return FileResponse("templates/home.html")

@app.post("/analyze")
async def analyze(file:UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        doc = fitz.open(stream = pdf_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text +=page.get_text()

        return JSONResponse({"filename":file.filename,"content":text})
    
    except Exception as e:
        return JSONResponse({"error":str(e)},status_code=500)
    
@app.post("/analyze_risk")
async def analyze_risk(file:UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        doc = fitz.open(stream = pdf_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text +=page.get_text()

        prompt = """
        You are an expert Contract Risk Analyzer. 

        Task:
        - Analyze the given contract text. 
        - Split it into individual clauses.
        - For each clause, extract the following details:
        - clause_id (numeric, incremental)
        - clause_heading (short descriptive title)
        - clause_text (short summary of the clause, max 2–3 sentences)
        - risk_level (High / Medium / Low)

        Contract text:
        {text}
        """

        prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
        final_prompt = prompt_template.format(text=text)

        # ===============================
        # Call Groq API
        # ===============================
        chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": final_prompt}],
                model="llama-3.3-70b-versatile"
            )
        result = chat_completion.choices[0].message.content

        return JSONResponse({"filename":file.filename,"content":result})
    
    except Exception as e:
        return JSONResponse({"error":str(e)},status_code=500)
    
        

if __name__ =="__main__":
    uvicorn.run(app=app,port=8000)
