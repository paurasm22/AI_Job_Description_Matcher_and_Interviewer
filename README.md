# AI Job Description Matcher & Interviewer

An AI-powered interview preparation platform that helps candidates analyze their resumes against job descriptions and practice technical interviews using Large Language Models.

## Live Demo

🚀 **Try it here:** https://pau22-ai-interviewer.hf.space/

---

## Features

* Upload Resume (PDF)
* Paste Job Description
* Resume–Job Description Matching
* Skill Gap Analysis
* AI-Generated Interview Questions
* Personalized Interview Experience
* Instant AI Feedback
* Simple and Interactive UI built with Streamlit

---

## Tech Stack

* Python
* Streamlit
* Groq API
* PyMuPDF
* LLM-based Question Generation
* Resume Parsing

---

## Project Structure

```bash
.
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI_Job_Description_Matcher_and_Interviewer.git
cd AI_Job_Description_Matcher_and_Interviewer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

Create a file named `.env` in the project root directory and add:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
```

You can obtain a Groq API key from:

https://console.groq.com/keys

### 5. Run the Application

```bash
streamlit run app.py
```

The application will start locally and can be accessed from:

```text
http://localhost:8501
```

---

## Usage

1. Upload your resume in PDF format.
2. Paste the target job description.
3. Review the resume-job match analysis.
4. Generate interview questions tailored to the role.
5. Practice answering questions and receive AI-generated feedback.

---

## Future Improvements

* Voice-based interviews
* Video interview support
* ATS Score Analysis
* Detailed Interview Performance Dashboard
* Multi-round Interview Simulation
* Authentication & User Profiles

---

## Author

**Pauras More**

IT Engineering Student | Full Stack Developer | AI/ML Enthusiast

LinkedIn: https://www.linkedin.com/in/pauras-more-2206pm/

GitHub: https://github.com/paurasm22
