# 🧠 Multi-Agentic RAG System

A **Multi-Agent Retrieval-Augmented Generation (RAG) System** that enables users to chat intelligently with their own documentation using a modular, multi-agent architecture.

This system combines document ingestion, relevance validation, research-based answering, and answer verification into a structured AI workflow — all accessible through an interactive UI.

---

## 🚀 Overview

This project implements a **multi-agent pipeline** that:

- Accepts user-uploaded documents
- Validates question relevance
- Generates contextual answers using RAG
- Verifies answer accuracy and relevance
- Produces a structured verification report

The architecture is modular, extensible, and model-agnostic.

---

## ✨ Features

### 🖥 1. Interactive UI
- User-friendly interface
- Chat-style interaction
- Model selection options
- File upload capability

### 📂 2. Document Upload
- Upload documents directly via UI
- Documents are processed and indexed
- Enables context-aware querying

### 🤖 3. LLM Model Selection
- Choose different LLMs for:
  - Relevance checking
  - Research/Answer generation
  - Verification
- Flexible and extensible model configuration

### 🔎 4. Relevance Checking Agent
When a question is asked:
- The system checks whether the query is relevant to the uploaded documents
- Prevents hallucinated responses
- Stops unrelated queries early

### 📚 5. Research Agent (Answer Generation)
If relevant:
- Retrieves contextual data from documents
- Performs Retrieval-Augmented Generation (RAG)
- Generates structured, context-backed answers

### ✅ 6. Verification Agent
- Evaluates answer relevance
- Checks context alignment
- Ensures logical consistency
- Produces a structured **verification report**
- Reduces hallucination risk

---

## 🏗 Architecture
User Question
↓
Relevance Agent
↓ (if relevant)
Research Agent (RAG)
↓
Verification Agent
↓
Final Answer + Verification Report


---

## 🔄 Multi-Agent Flow

1. User submits a question  
2. Relevance Agent validates document alignment  
3. Research Agent performs retrieval + answer generation  
4. Verification Agent audits the generated response  
5. Final response + verification report returned to UI  

---

## 🧩 System Design Principles

- Modular multi-agent design  
- Model-agnostic LLM selection  
- Reduced hallucination via validation layers  
- Transparent verification reporting  
- Scalable and extensible architecture  

---

## 🛠 Tech Stack (Customize as Needed)

- Python  
- LangChain / LlamaIndex  
- Vector Database ( Chroma)  
-  LLMs  hosted on github market place
- Streamlit / FastAPI / React  

---
## Courtesy

- Inspired from Cognitive AI learning 
