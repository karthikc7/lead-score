🔍 Lead Intent Scoring Dashboard
A web-based lead scoring dashboard that utilizes machine learning and rule-based natural language re-ranking to predict lead intent and prioritize high-conversion prospects.

🚀 Live Demo
Deployed Application: [http://127.0.0.1:5000](https://lead-score-qzd5.vercel.app/)

📋 Overview
This project tackles the problem of lead qualification inefficiency using a smart two-layer scoring system:

Machine Learning Model: Analyzes demographic and financial data to generate an initial intent score.

LLM Re-ranker: Uses rule-based NLP to fine-tune the score based on urgency and interest reflected in user comments.

🔑 Key Features
Real-time intent scoring on a 0–100 scale

Responsive frontend with a modern UI

REST API backend with input validation

Rule-based comment re-ranking

Dashboard with lead analytics

Mobile-friendly design

🏗️ Project Structure
bash
Copy
Edit
├── frontend/          # React-based UI
├── backend/           # Flask API backend
├── model/             # Trained ML model
├── data/              # Dataset used for training
└── README.md
💻 Tech Stack
Frontend
React 18 + Hooks

Tailwind CSS

shadcn/ui components

Vite for fast builds

Backend
Flask

Flask-CORS

RESTful endpoints

In-memory data storage

Machine Learning
XGBoost (for training)

Simplified scoring logic for deployment

🛠️ Local Development
Prerequisites
Node.js 18+ and pnpm

Python 3.11+

Git

Frontend Setup
bash
Copy
Edit
cd frontend
pnpm install
pnpm run dev
Available at: http://localhost:5173

Backend Setup
bash
Copy
Edit
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
API running at: http://localhost:5000

Full-Stack Integration
To run as a unified application:

bash
Copy
Edit
cd frontend
pnpm run build
cp -r dist/* ../backend/src/static/
Then launch only the backend to serve the app with integrated frontend.

📊 Dataset
Source: Kaggle Lead Scoring Dataset

Records: ~9,000

Features: Demographics, website activity, lead sources

Industry: Educational services

Example Features
Website visits, time on site, page views

Lead origin, income, credit score, age group

User-submitted comments

🤖 ML Model Summary
Training Model
Algorithm: XGBoost Classifier

Input: 5 top-performing features

Split: 80/20 train-test

Output: Probabilistic score → scaled to 0–100

Production Model
To optimize reliability:

Lightweight, dependency-free logic

Preserves feature weight relationships

Ensures interpretability and stable deployment

🧠 LLM-Based Re-ranker
Uses keyword matching to adjust scores:

➕ Positive Keywords (+5 to +20)
“urgent”, “ready”, “interested”, “purchase”, “soon”

➖ Negative Keywords (-5 to -30)
“not interested”, “maybe”, “budget”, “spam”, “unsubscribe”

Logic:
Case-insensitive

Cumulative scoring

Final score clamped between 0–100

🔐 Compliance & Privacy
✅ Consent required from users

✅ Minimal data collection

✅ Data stored in-memory (demo only)

✅ Full input validation on client and server

📈 Performance Metrics
Metric	Value
API Response Time	< 300ms
Scoring Accuracy	Calibrated & tuned
Conversion Lift Goal	2–3x
Frontend Performance	Optimized React

🚀 Deployment Strategy
Built using React (frontend) + Flask (backend)

Unified deployment: static files served via Flask

Designed for cloud-friendly deployment

Deployment Commands
bash
Copy
Edit
# Build the frontend
cd frontend && pnpm run build

# Copy build to backend for deployment
cp -r dist/* ../backend/src/static/
📘 API Documentation
POST /api/score
Submit a new lead for scoring.

Request:
json
Copy
Edit
{
  "phone_number": "+91-9876543210",
  "email": "user@example.com",
  "credit_score": 750,
  "age_group": "26-35",
  "family_background": "Married",
  "income": 500000,
  "comments": "Very interested and need urgently",
  "consent": true
}
Response:
json
Copy
Edit
{
  "email": "user@example.com",
  "initial_score": 65.5,
  "reranked_score": 85.5,
  "comments": "Very interested and need urgently"
}
GET /api/leads
Retrieve all submitted leads.

GET /api/health
Check API health status.

🧪 Testing Coverage
✔️ Form validation

✔️ Re-ranking logic

✔️ Score accuracy

✔️ API integration tests

🔮 Future Enhancements
Transformer-based NLP for advanced re-ranking

PostgreSQL/MongoDB for persistent storage

CRM integrations (e.g., Salesforce, HubSpot)

Analytics dashboard for trends

A/B testing for score thresholds

Real-time lead alerts and notifications

📄 License
This project is for demonstration and learning purposes only. Use responsibly and in compliance with local data protection laws.

👥 Contributing
This prototype is ideal for developers interested in:

Integrating a proper database

Adding user auth (JWT/OAuth)

Building CI/CD pipelines

Monitoring and logging

Scaling to production use

📞 Contact
Developer: Surya Venkata Karthikeya Yelamanchili
📧 Email: ykarthikeya2004@gmail.com
🔗 LinkedIn: My Profile
💻 GitHub: karthikc7
