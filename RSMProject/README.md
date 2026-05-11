# RSM Math Tutoring Portal

A local web app where a parent uploads RSM homework PDFs and a child solves problems one-by-one with guided hints released progressively.

## Setup

### 1. Clone & configure

```bash
cd RSMProject
cp .env .env.local   # or just edit .env directly
```

Edit `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...   # Your Anthropic API key
ADMIN_PIN=1234                 # Parent/teacher PIN
STUDENT_PIN=5678               # Child PIN
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at http://localhost:8000

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

---

## Usage

| URL | Who | What |
|-----|-----|------|
| http://localhost:5173/admin | Parent | Upload PDFs, manage hints |
| http://localhost:5173/student | Child | Solve problems |

### Admin workflow

1. Go to `/admin`, enter admin PIN
2. Upload an RSM homework PDF
3. Claude extracts all problems automatically
4. Click **"Set active"** on the session so the student can see it
5. For each question:
   - Review and edit the extracted text if needed
   - Click **"Generate Hints & Solution"** — Claude creates 3 hints + full solution
   - Use the **0 / 1 / 2 / 3** buttons to release hints to the student one at a time
   - Toggle **Hide/Show** to control which questions are visible

### Student workflow

1. Go to `/student`, enter student PIN
2. See questions one at a time
3. Click **"I'm stuck"** to request a hint (Socratic-style, no answers given)
4. Type and submit answer — Claude checks it and gives encouraging feedback
5. Confetti on correct answers! 🎉
6. Progress bar tracks completion

---

## Project Structure

```
RSMProject/
├── .env                      # API key + PINs
├── backend/
│   ├── main.py               # FastAPI app + all routes
│   ├── pdf_parser.py         # PDF text extraction
│   ├── claude_service.py     # All Claude API calls
│   ├── requirements.txt
│   └── data/                 # JSON storage (auto-created)
│       ├── sessions.json     # Questions + hints per PDF
│       └── progress.json     # Student progress
└── frontend/
    ├── src/
    │   ├── App.jsx           # Router + auth state
    │   ├── AdminView.jsx     # Parent dashboard
    │   ├── StudentView.jsx   # Child interface
    │   ├── components/
    │   │   └── PinGate.jsx   # PIN entry screen
    │   └── index.css         # Tailwind + custom classes
    └── package.json
```

## Notes

- **Scanned PDFs**: If the PDF is a photo/scan, text extraction may fail. Use a digital/searchable PDF for best results.
- **Storage**: Everything is stored in `backend/data/*.json` — no database required.
- **Model**: Uses `claude-sonnet-4-20250514` for all AI tasks.
