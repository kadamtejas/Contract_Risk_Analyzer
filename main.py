import numpy as np
import pandas as pd

import fitz  # PyMuPDF
from groq import Groq
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)


doc = fitz.open(r"D:\desktop\NeoSoft\SL\Contract_Risk_Analyzer\data\TejSoft_SoftwareDeveloper_Contract.pdf")



page = doc[0]  # first page
text = page.get_text()


prompt = """
You are an expert Contract Risk Analyzer. Analyze the following contract text and extract **important and risky clauses**.
Your job is to split a contract into individual clauses, extract key details, 
and return them in a structured JSON (dictionary) format. 
Each clause should include: clause_id, page, clause_heading, clause_text, 
risk_score (0–1), risk_level (High/Medium/Low), and keywords.



Contract text:
{text}



"""
prompt_template = PromptTemplate(template=prompt,
                                 input_variables=['text'])
final_prompt = prompt_template.format(text=str(text))
chat_completion = client.chat.completions.create(
    messages=[{"role":"user","content": final_prompt}],
    model="llama-3.3-70b-versatile")
result = chat_completion.choices[0].message.content
print(result)




