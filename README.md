# 📊 Financial Knowledge Graph + AI Q&A System

ระบบนี้เป็นโครงการ Data Engineering ที่ออกแบบมาเพื่อเก็บข้อมูลราคาหุ้นแบบ Real-Time ผ่าน Kafka  
บันทึกข้อมูลลง MongoDB และให้ผู้ใช้สามารถถามคำถามทางการเงินได้ โดยมี **LLM (Ollama)** ตอบคำถามจากข้อมูลจริง

---

## 🎯 จุดมุ่งหมายของโปรเจค (Objective)

- เพื่อสร้าง **Data Pipeline แบบ Real-Time** ด้วย Kafka
- เพื่อจัดเก็บข้อมูลในฐานข้อมูล NoSQL (MongoDB)
- เพื่อให้ระบบสามารถ **ตอบคำถามเชิงการเงิน** โดยอ้างอิงจากข้อมูลล่าสุดจริงใน Database
- เพื่อแสดงตัวอย่างการนำ **LLM มาใช้แบบ Local (ไม่ต้องใช้ API Key / ไม่ต้องต่อ Internet)**

---

## 🧠 Concept Overview

1. Producer จะสร้างข้อมูลราคาหุ้นแบบสุ่มและส่งเข้า Kafka
2. Consumer จะดึงข้อมูลจาก Kafka และบันทึกลง MongoDB
3. ผู้ใช้ถามคำถามผ่าน API `/qa`
4. FastAPI จะดึงข้อมูลล่าสุดจาก MongoDB แล้วสร้าง **Context Prompt**
5. ส่ง Prompt ให้ Ollama (โมเดล LLM อยู่ในเครื่อง)
6. Ollama จะตอบกลับแบบภาษามนุษย์ (Natural Language Response)

---

## 🏗️ System Architecture

            ┌───────────────────────┐
            │        Producer       │
            │ (Generate Stock Data) │
            └───────────┬───────────┘
                        ↓
                ┌──────────────┐
                │    Kafka     │
                │  (Streaming) │
                └───────┬──────┘
                        ↓
                ┌──────────────┐
                │  Consumer    │
                │ (ETL → DB)   │
                └───────┬──────┘
                        ↓
                ┌──────────────┐
                │  MongoDB     │
                │ (Data Store) │
                └───────┬──────┘
                        ↓
             ┌─────────────────────┐
             │      FastAPI        │
             │ Query Data + Prompt │
             └─────────┬───────────┘
                       ↓
                ┌──────────────┐
                │   Ollama     │
                │ (Local LLM)  │
                └──────────────┘

---

## ⚙️ Technologies Used

| Component | Technology |
|---------|------------|
| Streaming Data | Apache Kafka |
| Database | MongoDB |
| Backend API | FastAPI |
| Language Model | Ollama (llama3 or others) |
| Programming Language | Python |
| Container Runtime | Docker Desktop |

---

## 📦 Installation & Setup (Mac M1/M2/M3)

### Clone Project
```bash
git clone <your repo url>
cd DE\ Project
```
## Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Start Kafka + MongoDB
```bash
docker compose up -d
```

## Run Producer (ส่งข้อมูลเข้าระบบ)
```bash
python3 producer.py
```

## Run Consumer (บันทึกลง MongoDB)
```bash
python3 consumer_etl.py
```

## Start Ollama (ต้องรันก่อนใช้ API)
```bash
ollama serve
ollama pull llama3
```

## Run FastAPI Backend
```bash
uvicorn app_ollama:app --reload --port 8000
```
## Test API (Swagger UI)
```bash
http://127.0.0.1:8000/docs
```

## 🧪 Example API Usage
Request:
```json
{
  "question": "What is the latest price of Tesla?"
}
```
Response:
```json
{
  "answer": "Tesla price: 233.52 USD. The stock is currently showing moderate upward momentum."
}
```