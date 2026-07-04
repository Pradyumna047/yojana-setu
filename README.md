🌉 Yojana Setu - India’s Conversational Welfare Scheme Discovery Assistant


⭐ Tagline:
 Empowering citizens with simple, accurate, and accessible welfare scheme discovery — in their own language.

📘 Overview:
 Millions of Indian citizens qualify for government welfare schemes but struggle to access them due to:

- Complex eligibility rules
- Fragmented government portals
- Language barriers
- Low digital literacy
- Lack of personalized guidance

 Yojana Setu solves this by offering a conversational AI assistant that helps citizens:

- Discover relevant welfare schemes
- Understand eligibility
- Get verified, grounded information
- Interact in their preferred language
- Access a clean, intuitive interface

 Built as part of GenAI Academy APAC Edition.

🚀 Live Demo
👉 Try the live app:  
https://yojana-setu-app-998000871186.us-central1.run.app/

🎯 Key Features
- Verified RAG‑Powered Scheme Discovery
- Uses Vertex AI Search (Discovery Engine)
- Retrieves official policy documents from Google Cloud Storage (GCS)
- Eliminates hallucinations with grounded responses

👤 Profile‑Aware Eligibility Calculation:

Captures structured demographic variables:

- Age
- Gender
- Income
- BPL status
- Farmer status
- State

These are merged with the user’s conversational query before retrieval.

🌐 Automatic Language Routing
Detects user’s Indian state → sets default language (Hindi, Marathi, Kannada, Tamil, English).

💬 Clean Conversational UI
- Streamlit-based interface
- Session-state managed refreshed view
- Quick-action scheme shortcuts

📊 Admin Dashboard
- Tracks anonymized citizen demand:
- Total queries
- Eligibility rates
- Top schemes
- State-wise usage
- Language distribution

🧠 Architecture

Citizen → Streamlit UI → Profile Context Builder
        → Vertex AI Search (Discovery Engine)
        → Gemini Pro Reasoning
        → Multi-language Eligibility Output
        → GCS Telemetry Logs → Admin Dashboard
        
🧱 Tech Stack

Cloud & AI:
- Google Cloud Run — serverless hosting
- Google Cloud Storage (GCS) — policy documents + telemetry logs
- Vertex AI Agent Builder — semantic indexing
- Vertex AI Search Summarizer — reasoning + translation

Application:
- Python
- Streamlit
- Docker

Why This Stack Scales
- Decoupled architecture → update policy documents without code changes
- Serverless → auto-scaling + zero idle cost
- Pay‑per‑use → ideal for government budgets

🌍 Impact:
Why Yojana Setu Matters

India has 700+ welfare schemes across central and state governments.
Yet millions of eligible citizens miss out due to:

- Lack of awareness
- Language barriers
- Complex eligibility rules
- Digital divide

Yojana Setu democratizes welfare access by making scheme discovery:

- Conversational
- Personalized
- Multi-lingual
- Verified
- Accessible

This can significantly improve welfare penetration and citizen empowerment.

🪴 Installation
Clone the repository:

bash
- git clone https://github.com/Pradyumna047/yojana-setu.git
- cd yojana-setu
- pip install -r requirements.txt
- streamlit run app.py
- 
☁️ Deployment (Cloud Run)
Build and deploy:

bash
- gcloud builds submit --tag gcr.io/<project-id>/yojana-setu
- gcloud run deploy yojana-setu \
-   --image gcr.io/<project-id>/yojana-setu \
-   --platform managed \
-  --region asia-south1 \
-   --allow-unauthenticated
  
🎯 Roadmap
- Hybrid UI (HTML + JS + Streamlit backend)
- Scheme browser page
- Eligibility scoring engine
- Mobile-friendly UI
- Offline mode (local LLM)

👥 Author
Pradyumna Shetty  
GenAI Academy APAC Edition
