import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.8-flash")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Query(BaseModel):
    text: str

@app.post("/ask")
def ask(q: Query):
    try:
        res = model.generate_content(q.text)
        return {"answer": res.text}
    except Exception as e:
        return {"answer": f"Error: {e}"}

@app.post("/summarize")
def summarize(q: Query):
    try:
        res = model.generate_content(f"Summarize: {q.text}")
        return {"answer": res.text}
    except Exception as e:
        return {"answer": f"Error: {e}"}

@app.post("/quiz")
def quiz(q: Query):
    try:
        res = model.generate_content(f"Create 3 quiz Q&A for: {q.text}")
        return {"answer": res.text}
    except Exception as e:
        return {"answer": f"Error: {e}"}

@app.post("/path")
def path(q: Query):
    try:
        res = model.generate_content(f"Create learning path for: {q.text}")
        return {"answer": res.text}
    except Exception as e:
        return {"answer": f"Error: {e}"}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head><title>EduGenie.AI</title>
<style>
body{background:radial-gradient(circle at top,#1e3a5f,#0a0f1e);min-height:100vh;margin:0;font-family:Arial;color:white;display:flex;justify-content:center;padding:40px}
.container{width:700px}
.tabs{display:flex;gap:10px;margin-bottom:15px}
.tab{padding:10px 20px;border-radius:20px;border:1px solid #3a4a6a;background:#1a2744;color:#aab;cursor:pointer}
.tab.active{background:#2ec5ff;color:#001;font-weight:bold;border:none}
.card{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:15px;padding:25px;backdrop-filter:blur(10px)}
textarea{width:100%;background:#0f1c33;border:1px solid #2a3a5a;border-radius:10px;padding:12px;color:white;min-height:70px}
.ask-btn{margin-top:15px;background:#2ec5ff;border:none;padding:8px 18px;border-radius:20px;cursor:pointer;font-weight:bold}
.answer-box{margin-top:20px;background:rgba(0,0,0,0.3);border-radius:10px;padding:15px;min-height:40px;white-space:pre-wrap;font-size:14px;line-height:1.5}
</style>
</head>
<body>
<div class="container">
  <div class="tabs">
    <div class="tab active" onclick="switchTab('ask',this)">Ask AI</div>
    <div class="tab" onclick="switchTab('summarize',this)">Summarize</div>
    <div class="tab" onclick="switchTab('quiz',this)">Quiz</div>
    <div class="tab" onclick="switchTab('path',this)">Path</div>
  </div>
  <div class="card">
    <h3 id="title">Ask Anything</h3>
    <textarea id="input" placeholder="What is Quantum?"></textarea>
    <button class="ask-btn" onclick="callAI()">Ask ✨</button>
    <div id="result" class="answer-box">Your answer will appear here...</div>
  </div>
</div>
<script>
let currentTab='ask';
function switchTab(tab,el){
  currentTab=tab;
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('title').innerText=tab==='ask'?'Ask Anything':tab.charAt(0).toUpperCase()+tab.slice(1);
}
async function callAI(){
  const text=document.getElementById('input').value;
  if(!text) return alert('Type something!');
  document.getElementById('result').innerText='Thinking...';
  const res=await fetch(`/${currentTab}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
  const data=await res.json();
  document.getElementById('result').innerText=data.answer;
}
</script>
</body>
</html>
    """
