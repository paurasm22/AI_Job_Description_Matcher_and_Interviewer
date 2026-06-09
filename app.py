import streamlit as st
import json
import io
import fitz  # PyMuPDF
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"

def get_client():
    
    return Groq(api_key=GROQ_API_KEY)
# ── Your personal info for the About page ──
ABOUT = {
    "name":       "Pauras",
    "tagline":    "MERN Stack Developer · AI/ML Enthusiast ",
   "bio": (
    "AI/ML enthusiast exploring machine learning, generative AI, and large language "
    "models. Passionate about building intelligent applications and learning new "
    "technologies in the rapidly evolving AI landscape. This project is an end-to-end "
    "AI Interview Platform that parses your resume, matches it against a job "
    "description, conducts a live adaptive interview via Groq, and generates a "
    "scored report — all in your browser. This is currently a V1 prototype built "
    "to validate the core concept and user experience. Future iterations will focus "
    "on developing it into a fully persistent, production-ready, and deployable "
    "platform with enhanced analytics, authentication, interview history tracking, "
    "and scalable infrastructure."
),
    "github":     "https://github.com/paurasm22",
    "linkedin":   "https://www.linkedin.com/in/pauras-more-2206pm/",
    "email":      "mailto:paurasmore22@gmail.com",
    "tech_stack": [
                   "Groq API", "llama-3.3-70b", "PyMuPDF", "Streamlit", "Python"],
    "project_highlights": [
        ("🤖 Resume Parser",       "AI-powered ATS parser using Groq LLM"),
        ("📊 Semantic Skill Match", "Compares resume vs JD with semantic understanding"),
        ("🎤 Adaptive Interview",   "Real-time Q&A that follows up on weak answers"),
        ("📋 Scored Report",        "Per-answer scoring + final PDF download"),
    ],
}

st.set_page_config(
    page_title="AI Interview Prep",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0d1117; color: #e6edf3; }

[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] .stMarkdown h3 { color: #58a6ff; }

.step-pill {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #8b949e;
    margin-bottom: 8px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.step-pill.active { background: #1f3a5f; border-color: #58a6ff; color: #58a6ff; }

.card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}
.card-accent  { border-left: 3px solid #58a6ff; }
.card-green   { border-left: 3px solid #3fb950; }
.card-orange  { border-left: 3px solid #d29922; }
.card-red     { border-left: 3px solid #f85149; }

.score-block  { text-align: center; padding: 12px 8px; }
.score-number { font-size: 2rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; line-height: 1; }
.score-label  { font-size: 11px; color: #8b949e; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.06em; }

.question-box {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 20px 24px;
    font-size: 16px;
    font-weight: 500;
    color: #e6edf3;
    line-height: 1.6;
    margin-bottom: 12px;
}
.q-badge {
    display: inline-block;
    background: #1f3a5f;
    color: #58a6ff;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.feedback-box {
    background: #1a2233;
    border: 1px solid #2d4a6e;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 12px;
    font-size: 14px;
    color: #cdd9e5;
    line-height: 1.6;
}
.feedback-box strong { color: #58a6ff; }

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #1f6feb, #58a6ff);
    border-radius: 4px;
}

.stButton > button {
    background: #1f6feb;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 24px;
    transition: background 0.2s;
    width: 100%;
}
.stButton > button:hover { background: #388bfd; color: #fff; }

.stTextArea textarea {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 8px;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
}
.stTextArea textarea:focus {
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.15);
}

[data-testid="stFileUploader"] {
    background: #161b22;
    border: 1px dashed #30363d;
    border-radius: 10px;
}

h1 { color: #e6edf3 !important; font-weight: 700 !important; }
h2 { color: #cdd9e5 !important; font-weight: 600 !important; }
h3 { color: #cdd9e5 !important; font-weight: 600 !important; }

[data-testid="stMetricValue"] {
    color: #58a6ff !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.chip {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    color: #8b949e;
    margin: 2px;
}
.chip-green { background: #12261e; border-color: #3fb950; color: #3fb950; }
.chip-red   { background: #2a1c1c; border-color: #f85149; color: #f85149; }
.chip-blue  { background: #1f3a5f; border-color: #58a6ff; color: #58a6ff; }

/* About page social buttons */
.social-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 600;
    color: #e6edf3;
    text-decoration: none !important;
    margin-right: 10px;
    margin-bottom: 10px;
    transition: all 0.2s;
}
.social-btn:hover { background: #30363d; border-color: #58a6ff; color: #58a6ff; }
.social-btn.github { border-color: #8b949e; }
.social-btn.linkedin { border-color: #0a66c2; }
.social-btn.email { border-color: #3fb950; }

/* Highlight card for about */
.about-hero {
    background: linear-gradient(135deg, #1c2128 0%, #1f3a5f 100%);
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 24px;
    text-align: center;
}

hr { border-color: #21262d !important; }
.stSpinner > div { border-top-color: #58a6ff !important; }
[data-testid="stExpander"] { background: #161b22; border: 1px solid #21262d; border-radius: 10px; }
[data-testid="stRadio"] label { color: #cdd9e5 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_client():
    return Groq(api_key=GROQ_API_KEY)


def extract_pdf_text(uploaded_file) -> str:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def call_groq(prompt: str, temperature: float = 0, json_mode: bool = True):
    client = get_client()
    kwargs = dict(
        model=MODEL,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**kwargs)
    raw = response.choices[0].message.content
    if json_mode:
        return json.loads(raw)
    return raw


def score_color(score: int) -> str:
    if score >= 8:  return "#3fb950"
    if score >= 5:  return "#d29922"
    return "#f85149"


def render_chips(items: list, color_class: str = "") -> str:
    cls = f"chip {color_class}".strip()
    return " ".join(f'<span class="{cls}">{item}</span>' for item in items)


def _report_prompt(history, resume_data, jd_data) -> str:
    return f"""
You are a senior recruiter.

Candidate Resume:
{json.dumps(resume_data)}

Job Description:
{json.dumps(jd_data)}

Complete Interview History:
{json.dumps(history)}

Generate a final interview report. Return ONLY JSON.

Schema:
{{
    "overall_score": 0,
    "technical_rating": "",
    "communication_rating": "",
    "strengths": [],
    "weaknesses": [],
    "recommendation": ""
}}
"""


# ─────────────────────────────────────────────
# PDF REPORT GENERATOR
# ─────────────────────────────────────────────

def generate_pdf_report(report, history, comparison_result, resume_data, jd_data) -> bytes:
    """Build a beautiful A4 PDF report using ReportLab and return raw bytes."""
    buf = io.BytesIO()

    # ── Colour palette ──
    DARK_BG    = colors.HexColor("#0d1117")
    CARD_BG    = colors.HexColor("#161b22")
    BLUE       = colors.HexColor("#58a6ff")
    GREEN      = colors.HexColor("#3fb950")
    ORANGE     = colors.HexColor("#d29922")
    RED        = colors.HexColor("#f85149")
    TEXT_MAIN  = colors.HexColor("#e6edf3")
    TEXT_MUTED = colors.HexColor("#8b949e")
    BORDER     = colors.HexColor("#21262d")

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm,  bottomMargin=20*mm,
    )

    W = A4[0] - 40*mm   # usable width

    # ── Styles ──
    styles = getSampleStyleSheet()

    def S(name, **kw):
        base = ParagraphStyle(name, parent=styles["Normal"], **kw)
        return base

    title_style   = S("Title2",   fontSize=22, textColor=TEXT_MAIN,  spaceAfter=4,  alignment=TA_CENTER, fontName="Helvetica-Bold")
    sub_style     = S("Sub",      fontSize=11, textColor=TEXT_MUTED,  spaceAfter=16, alignment=TA_CENTER)
    h1_style      = S("H1",       fontSize=14, textColor=BLUE,        spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold")
    h2_style      = S("H2",       fontSize=11, textColor=TEXT_MAIN,   spaceBefore=8,  spaceAfter=4, fontName="Helvetica-Bold")
    body_style    = S("Body2",    fontSize=9,  textColor=TEXT_MAIN,   spaceAfter=4,  leading=14)
    muted_style   = S("Muted",    fontSize=8,  textColor=TEXT_MUTED,  spaceAfter=2)
    bullet_style  = S("Bullet",   fontSize=9,  textColor=TEXT_MAIN,   spaceAfter=3,  leftIndent=12, leading=13)
    mono_big      = S("MonoBig",  fontSize=36, textColor=BLUE,        alignment=TA_CENTER, fontName="Courier-Bold")
    center_style  = S("Center",   fontSize=9,  textColor=TEXT_MAIN,   alignment=TA_CENTER)
    green_style   = S("Green",    fontSize=9,  textColor=GREEN,       spaceAfter=3,  leftIndent=12)
    orange_style  = S("Orange",   fontSize=9,  textColor=ORANGE,      spaceAfter=3,  leftIndent=12)

    story = []

    # ─── COVER HEADER ───
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("AI Interview Report", title_style))

    candidate_name = resume_data.get("name", "Candidate") if resume_data else "Candidate"
    role           = jd_data.get("role", "Position")      if jd_data       else "Position"
    story.append(Paragraph(f"{candidate_name}  ·  {role}", sub_style))
    story.append(HRFlowable(width=W, thickness=1, color=BORDER, spaceAfter=10))

    # ─── OVERALL SCORE BANNER ───
    if report:
        overall = report.get("overall_score", 0)
        t_rating = report.get("technical_rating", "—")
        c_rating = report.get("communication_rating", "—")

        score_table = Table(
            [[
                Paragraph(str(overall), mono_big),
                Table(
                    [
                        [Paragraph("OVERALL SCORE / 100", S("sl", fontSize=8, textColor=TEXT_MUTED, alignment=TA_CENTER, fontName="Helvetica"))],
                        [Paragraph(f"Technical: {t_rating}", S("tr", fontSize=10, textColor=BLUE, alignment=TA_CENTER))],
                        [Paragraph(f"Communication: {c_rating}", S("cr", fontSize=10, textColor=BLUE, alignment=TA_CENTER))],
                    ],
                    colWidths=[W - 50*mm],
                    style=TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("ALIGN", (0,0), (-1,-1), "CENTER")]),
                ),
            ]],
            colWidths=[50*mm, W - 50*mm],
        )
        score_table.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,-1), CARD_BG),
            ("ROUNDEDCORNERS", [8]),
            ("TOPPADDING",  (0,0), (-1,-1), 12),
            ("BOTTOMPADDING",(0,0),(-1,-1), 12),
            ("LEFTPADDING", (0,0), (-1,-1), 12),
            ("RIGHTPADDING",(0,0), (-1,-1), 12),
            ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
            ("LINEBELOW",   (0,0), (-1,-1), 0.5, BORDER),
        ]))
        story.append(KeepTogether([score_table, Spacer(1, 4*mm)]))

    # ─── AVERAGES ROW ───
    if history:
        avg_tech = round(sum(h["technical_score"]     for h in history) / len(history), 1)
        avg_comm = round(sum(h["communication_score"] for h in history) / len(history), 1)
        avg_comp = round(sum(h["completeness_score"]  for h in history) / len(history), 1)

        def metric_cell(label, val, col):
            return [
                Paragraph(str(val), S("mv", fontSize=20, textColor=col, alignment=TA_CENTER, fontName="Courier-Bold")),
                Paragraph(label,    S("ml", fontSize=7,  textColor=TEXT_MUTED, alignment=TA_CENTER)),
            ]

        avg_table = Table(
            [[
                metric_cell("AVG TECHNICAL",    f"{avg_tech}/10", GREEN  if avg_tech >= 8 else (ORANGE if avg_tech >= 5 else RED)),
                metric_cell("AVG COMMUNICATION",f"{avg_comm}/10", GREEN  if avg_comm >= 8 else (ORANGE if avg_comm >= 5 else RED)),
                metric_cell("AVG COMPLETENESS", f"{avg_comp}/10", GREEN  if avg_comp >= 8 else (ORANGE if avg_comp >= 5 else RED)),
                metric_cell("QUESTIONS ANSWERED",str(len(history)), BLUE),
            ]],
            colWidths=[W/4]*4,
        )
        avg_table.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), CARD_BG),
            ("TOPPADDING",   (0,0), (-1,-1), 10),
            ("BOTTOMPADDING",(0,0), (-1,-1), 10),
            ("ALIGN",        (0,0), (-1,-1), "CENTER"),
            ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
            ("LINEAFTER",    (0,0), (2,0),   0.5, BORDER),
        ]))
        story.append(avg_table)
        story.append(Spacer(1, 4*mm))

    # ─── MATCH ANALYSIS SUMMARY ───
    if comparison_result:
        story.append(Paragraph("Profile · JD Match Analysis", h1_style))

        ms = comparison_result.get("match_score", 0)
        matched = comparison_result.get("matched_skills", [])
        missing = comparison_result.get("missing_skills", [])

        match_row = Table(
            [[
                Paragraph(f"Match Score: {ms}/100", S("ms", fontSize=13, textColor=BLUE, fontName="Helvetica-Bold")),
                Paragraph(f"Matched: {len(matched)} skills", S("mt", fontSize=10, textColor=GREEN)),
                Paragraph(f"Gaps: {len(missing)} skills",    S("mg", fontSize=10, textColor=RED)),
            ]],
            colWidths=[W*0.4, W*0.3, W*0.3],
        )
        match_row.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), CARD_BG),
            ("TOPPADDING",   (0,0), (-1,-1), 10),
            ("BOTTOMPADDING",(0,0), (-1,-1), 10),
            ("LEFTPADDING",  (0,0), (-1,-1), 12),
            ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(match_row)
        story.append(Spacer(1, 3*mm))

        rec = comparison_result.get("hiring_recommendation", "")
        if rec:
            story.append(Paragraph(f"<b>Recommendation:</b> {rec}", body_style))

    # ─── STRENGTHS & WEAKNESSES ───
    if report:
        strengths  = report.get("strengths", [])
        weaknesses = report.get("weaknesses", [])

        story.append(Paragraph("Interview Performance", h1_style))

        sw_data = [
            [Paragraph("Strengths", h2_style), Paragraph("Areas to Develop", h2_style)],
            [
                "\n".join(f"▸  {s}" for s in strengths)  or "—",
                "\n".join(f"▸  w" for w in weaknesses) or "—",
            ],
        ]

        # Build cleanly with paragraphs
        s_paras = [Paragraph(f"▸  {s}", green_style)  for s in strengths]  or [Paragraph("—", muted_style)]
        w_paras = [Paragraph(f"▸  {w}", orange_style) for w in weaknesses] or [Paragraph("—", muted_style)]

        sw_table = Table(
            [[Paragraph("Strengths", h2_style), Paragraph("Areas to Develop", h2_style)],
             [s_paras, w_paras]],
            colWidths=[W/2 - 3*mm, W/2 - 3*mm],
            hAlign="LEFT",
        )
        sw_table.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), CARD_BG),
            ("TOPPADDING",   (0,0), (-1,-1), 10),
            ("BOTTOMPADDING",(0,0), (-1,-1), 8),
            ("LEFTPADDING",  (0,0), (-1,-1), 12),
            ("RIGHTPADDING", (0,0), (-1,-1), 12),
            ("LINEAFTER",    (0,0), (0,-1),  0.5, BORDER),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ]))
        story.append(sw_table)
        story.append(Spacer(1, 3*mm))

        # Final recommendation
        rec = report.get("recommendation", "")
        if rec:
            story.append(Paragraph("Final Recommendation", h1_style))
            rec_table = Table([[Paragraph(rec, body_style)]], colWidths=[W])
            rec_table.setStyle(TableStyle([
                ("BACKGROUND",  (0,0), (-1,-1), CARD_BG),
                ("TOPPADDING",  (0,0), (-1,-1), 12),
                ("BOTTOMPADDING",(0,0),(-1,-1), 12),
                ("LEFTPADDING", (0,0), (-1,-1), 16),
                ("RIGHTPADDING",(0,0), (-1,-1), 16),
                ("LINEBEFORE",  (0,0), (0,-1),  3, BLUE),
            ]))
            story.append(rec_table)
            story.append(Spacer(1, 4*mm))

    # ─── TRANSCRIPT ───
    if history:
        story.append(HRFlowable(width=W, thickness=0.5, color=BORDER, spaceBefore=6, spaceAfter=6))
        story.append(Paragraph("Interview Transcript", h1_style))

        for i, h in enumerate(history, 1):
            ts = h["technical_score"]
            cs = h["communication_score"]
            cp = h["completeness_score"]

            t_col = GREEN if ts >= 8 else (ORANGE if ts >= 5 else RED)
            c_col = GREEN if cs >= 8 else (ORANGE if cs >= 5 else RED)
            p_col = GREEN if cp >= 8 else (ORANGE if cp >= 5 else RED)

            scores_row = Table(
                [[
                    Paragraph(f"Tech {ts}/10",  S("tc", fontSize=9, textColor=t_col)),
                    Paragraph(f"Comm {cs}/10",  S("cc", fontSize=9, textColor=c_col)),
                    Paragraph(f"Comp {cp}/10",  S("pc", fontSize=9, textColor=p_col)),
                ]],
                colWidths=[W/3]*3,
            )
            scores_row.setStyle(TableStyle([
                ("TOPPADDING",   (0,0), (-1,-1), 4),
                ("BOTTOMPADDING",(0,0), (-1,-1), 4),
                ("ALIGN",        (0,0), (-1,-1), "CENTER"),
            ]))

            q_block = [
                Paragraph(f"Q{i}", S("qn", fontSize=8, textColor=TEXT_MUTED, fontName="Helvetica-Bold")),
                Paragraph(h["question"], h2_style),
                Paragraph(f"<i>{h['answer']}</i>", S("ans", fontSize=9, textColor=TEXT_MUTED, leading=13, spaceAfter=4)),
                scores_row,
                Paragraph(f"Feedback: {h['feedback']}", S("fb", fontSize=8, textColor=TEXT_MUTED, leading=12, spaceAfter=4)),
            ]

            block_table = Table([[q_block]], colWidths=[W])
            block_table.setStyle(TableStyle([
                ("BACKGROUND",   (0,0), (-1,-1), CARD_BG),
                ("TOPPADDING",   (0,0), (-1,-1), 10),
                ("BOTTOMPADDING",(0,0), (-1,-1), 8),
                ("LEFTPADDING",  (0,0), (-1,-1), 12),
                ("RIGHTPADDING", (0,0), (-1,-1), 12),
                ("LINEBEFORE",   (0,0), (0,-1),  2, BLUE),
            ]))
            story.append(KeepTogether([block_table, Spacer(1, 3*mm)]))

    # ─── FOOTER ───
    story.append(HRFlowable(width=W, thickness=0.5, color=BORDER, spaceBefore=8, spaceAfter=4))
    story.append(Paragraph(
        f"Generated by AI Interview Prep  ·  Powered by Groq llama-3.3-70b  ·  Built by {ABOUT['name']}",
        S("footer", fontSize=7, textColor=TEXT_MUTED, alignment=TA_CENTER),
    ))

    # ── Page background ──
    def on_page(canvas, doc):
        canvas.setFillColor(DARK_BG)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return buf.getvalue()



# ─────────────────────────────────────────────
# HELPER: report prompt (used in interview stage)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

defaults = {
    "page":              "about",      # about | upload | jd | analysis | interview | report
    "stage":             "upload",
    "resume_text":       "",
    "resume_data":       None,
    "job_description":   "",
    "jd_data":           None,
    "comparison_result": None,
    "interview_blueprint": None,
    "question_bank":     None,
    "questions":         [],
    "history":           [],
    "q_index":           0,
    "current_question":  "",
    "last_eval":         None,
    "report":            None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

STAGES = ["upload", "jd", "analysis", "interview", "report"]
STAGE_LABELS = {
    "upload":    "1 · Upload Resume",
    "jd":        "2 · Job Description",
    "analysis":  "3 · Match Analysis",
    "interview": "4 · Live Interview",
    "report":    "5 · Final Report",
}

with st.sidebar:
    st.markdown("### 🎯 AI Interview Prep")
    st.markdown("---")

    if st.button("🏠 About This Project", key="nav_about"):
        st.session_state.page = "about"
        st.rerun()

    st.markdown("**Interview Pipeline**")

    current_stage_index = STAGES.index(st.session_state.stage)
    for i, s in enumerate(STAGES):
        is_active = s == st.session_state.stage and st.session_state.page != "about"
        is_done   = i < current_stage_index
        label     = STAGE_LABELS[s]
        if is_active:
            st.markdown(f'<div class="step-pill active">▶ {label}</div>', unsafe_allow_html=True)
        elif is_done:
            st.markdown(f'<div class="step-pill" style="color:#3fb950;border-color:#3fb950;">✓ {label}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step-pill">{label}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p style="color:#8b949e;font-size:12px;">Powered by Groq · llama-3.3-70b</p>', unsafe_allow_html=True)

    if st.button("🔄 Start Over", key="restart"):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()


# ─────────────────────────────────────────────
# PAGE: ABOUT
# ─────────────────────────────────────────────

if st.session_state.page == "about":
    st.markdown(f"""
    <div class="about-hero">
        <div style="font-size:3rem;margin-bottom:8px">🎯</div>
        <h1 style="color:#e6edf3;font-size:2rem;margin-bottom:6px">AI Interview Prep</h1>
        <p style="color:#8b949e;font-size:15px;max-width:600px;margin:0 auto 20px">{ABOUT['tagline']}</p>
        <a href="{ABOUT['github']}"   target="_blank" class="social-btn github">   ⬡ GitHub</a>
        <a href="{ABOUT['linkedin']}" target="_blank" class="social-btn linkedin">in LinkedIn</a>
        <a href="{ABOUT['email']}"    class="social-btn email">✉ Email</a>
    </div>
    """, unsafe_allow_html=True)

    # Bio
    st.markdown(f'<div class="card card-accent"><p style="color:#cdd9e5;font-size:15px;line-height:1.7;margin:0">{ABOUT["bio"]}</p></div>', unsafe_allow_html=True)

    # Project highlights
    st.markdown("### ✨ What This Platform Does")
    cols = st.columns(2)
    for idx, (title, desc) in enumerate(ABOUT["project_highlights"]):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="card" style="min-height:90px">
                <div style="font-size:18px;margin-bottom:6px">{title}</div>
                <div style="color:#8b949e;font-size:13px">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tech stack
    st.markdown("### 🛠 Tech Stack")
    st.markdown(
        '<div class="card">' + render_chips(ABOUT["tech_stack"], "chip-blue") + '</div>',
        unsafe_allow_html=True
    )

    # Pipeline overview
    st.markdown("### 🔄 How It Works")
    steps = [
        ("📄", "Upload Resume",      "Your PDF is parsed by PyMuPDF and structured by Groq into a clean JSON profile."),
        ("📋", "Paste Job Description","The JD is extracted into role, required/preferred skills, responsibilities."),
        ("📊", "Match Analysis",      "Semantic comparison gives you a readiness score, matched skills, and gaps."),
        ("🎤", "Live Interview",       "Groq asks adaptive questions — it follows up if your answer is weak."),
        ("📥", "Download Report",      "A full PDF report with scores, feedback, and transcript is generated for you."),
    ]
    for emoji, title, desc in steps:
        st.markdown(f"""
        <div class="card" style="display:flex;gap:16px;align-items:flex-start;padding:16px 20px;margin-bottom:10px">
            <div style="font-size:24px;min-width:36px">{emoji}</div>
            <div>
                <div style="font-weight:600;color:#e6edf3;margin-bottom:4px">{title}</div>
                <div style="color:#8b949e;font-size:13px">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚀 Start Interview Prep →"):
        st.session_state.page = "app"
        st.session_state.stage = "upload"
        st.rerun()


# ─────────────────────────────────────────────
# APP PAGES
# ─────────────────────────────────────────────

elif st.session_state.page in ("app", "upload", "jd", "analysis", "interview", "report"):

    stage = st.session_state.stage

    # ── STAGE 1: UPLOAD ──
    if stage == "upload":
        st.markdown("## Upload Your Resume")
        st.markdown('<p style="color:#8b949e;">Upload your PDF resume and we\'ll extract your profile automatically.</p>', unsafe_allow_html=True)
        st.markdown("---")

        uploaded = st.file_uploader("Drop your resume PDF here", type=["pdf"])

        if uploaded:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f'<div class="card card-accent">📄 <strong>{uploaded.name}</strong> — ready to parse</div>', unsafe_allow_html=True)
            with col2:
                if st.button("Parse Resume →"):
                    with st.spinner("Extracting text from PDF…"):
                        raw_text = extract_pdf_text(uploaded)
                        st.session_state.resume_text = raw_text

                    with st.spinner("Parsing resume with AI…"):
                        prompt = f"""
You are an expert ATS Resume Parser.
Extract information from the resume and return ONLY valid JSON.

IMPORTANT RULES:
1. Return ONLY valid JSON.
2. Do NOT wrap the JSON in markdown.
3. The first character of your response must be {{
4. The last character of your response must be }}

JSON Schema:
{{
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "github": "",
    "education": [{{"degree": "", "institution": "", "year": ""}}],
    "skills": [],
    "projects": [{{"name": "", "description": "", "technologies": []}}],
    "internships": [{{"company": "", "role": "", "duration": "", "description": ""}}],
    "certifications": [],
    "achievements": [],
    "languages": []
}}

Resume Text:
{raw_text}
"""
                        result = call_groq(prompt, temperature=0)
                        st.session_state.resume_data = result

                    st.session_state.stage = "jd"
                    st.rerun()

        if st.session_state.resume_data:
            rd = st.session_state.resume_data
            with st.expander("📋 Parsed Resume Preview"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Name:** {rd.get('name','—')}")
                    st.markdown(f"**Email:** {rd.get('email','—')}")
                    st.markdown(f"**Phone:** {rd.get('phone','—')}")
                with c2:
                    st.markdown(f"**Location:** {rd.get('location','—')}")
                    st.markdown(f"**GitHub:** {rd.get('github','—')}")
                    st.markdown(f"**LinkedIn:** {rd.get('linkedin','—')}")
                st.markdown("**Skills:**")
                st.markdown(render_chips(rd.get('skills', []), "chip-blue"), unsafe_allow_html=True)

    # ── STAGE 2: JD ──
    elif stage == "jd":
        st.markdown("## Paste the Job Description")
        st.markdown('<p style="color:#8b949e;">Copy the full JD from the job listing and paste it below.</p>', unsafe_allow_html=True)
        st.markdown("---")

        jd_input = st.text_area(
            "Job Description",
            value=st.session_state.job_description,
            height=280,
            placeholder="Paste the full job description here…",
            label_visibility="collapsed",
        )

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("← Back"):
                st.session_state.stage = "upload"
                st.rerun()
        with col2:
            if st.button("Analyse JD →"):
                if not jd_input.strip():
                    st.warning("Please paste a job description first.")
                else:
                    st.session_state.job_description = jd_input
                    with st.spinner("Parsing job description…"):
                        prompt = f"""
Extract the job description.
Return ONLY a valid JSON object.

Schema:
{{
    "role": "",
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": [],
    "experience_level": ""
}}

Job Description:
{jd_input}
"""
                        st.session_state.jd_data = call_groq(prompt, temperature=0)
                    st.session_state.stage = "analysis"
                    st.rerun()

    # ── STAGE 3: ANALYSIS ──
    elif stage == "analysis":
        st.markdown("## Match Analysis")
        st.markdown('<p style="color:#8b949e;">Comparing your profile against the job requirements.</p>', unsafe_allow_html=True)
        st.markdown("---")

        if st.session_state.comparison_result is None:
            with st.spinner("Running semantic skill match…"):
                prompt = f"""
You are a senior technical recruiter and hiring manager.
Evaluate the candidate against the job description.

Candidate Profile:
{json.dumps(st.session_state.resume_data, indent=2)}

Job Description:
{json.dumps(st.session_state.jd_data, indent=2)}

Instructions:
1. Compare skills SEMANTICALLY. Treat equivalent skills as matches.
2. Compute an overall readiness score from 0-100.

Return ONLY valid JSON.
Schema:
{{
    "match_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "interview_focus_areas": [],
    "hiring_recommendation": ""
}}
"""
                st.session_state.comparison_result = call_groq(prompt, temperature=0)

            with st.spinner("Building interview blueprint…"):
                prompt = f"""
You are an expert technical interviewer. Create an interview blueprint.

Candidate Resume:
{json.dumps(st.session_state.resume_data, indent=2)}

Job Description:
{json.dumps(st.session_state.jd_data, indent=2)}

Match Analysis:
{json.dumps(st.session_state.comparison_result, indent=2)}

Return ONLY valid JSON.
Schema:
{{
    "candidate_summary": "",
    "project_topics": [],
    "technical_topics": [],
    "internship_topics": [],
    "missing_skill_topics": [],
    "behavioral_topics": [],
    "interview_focus_areas": [],
    "question_distribution": {{
        "project_questions": 0,
        "technical_questions": 0,
        "internship_questions": 0,
        "behavioral_questions": 0,
        "missing_skill_questions": 0
    }}
}}
"""
                st.session_state.interview_blueprint = call_groq(prompt, temperature=0)

            with st.spinner("Generating personalised question bank…"):
                prompt = f"""
You are a senior software engineering interviewer.

Candidate Resume:
{json.dumps(st.session_state.resume_data, indent=2)}

Job Description:
{json.dumps(st.session_state.jd_data, indent=2)}

Interview Blueprint:
{json.dumps(st.session_state.interview_blueprint, indent=2)}

Return ONLY valid JSON.
Schema:
{{
    "project_questions": [],
    "technical_questions": [],
    "internship_questions": [],
    "behavioral_questions": [],
    "missing_skill_questions": []
}}
"""
                qb = call_groq(prompt, temperature=0.3)
                st.session_state.question_bank = qb
                all_qs = []
                for category in qb.values():
                    for q in category:
                        all_qs.append(q.get("question", str(q)) if isinstance(q, dict) else str(q))
                st.session_state.questions = all_qs
                if all_qs:
                    st.session_state.current_question = all_qs[0]

        cr = st.session_state.comparison_result
        bp = st.session_state.interview_blueprint
        score    = cr.get("match_score", 0)
        score_col = score_color(score)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="card" style="text-align:center"><div style="font-size:3rem;font-weight:700;color:{score_col};font-family:\'JetBrains Mono\',monospace">{score}</div><div style="color:#8b949e;font-size:12px;text-transform:uppercase">Match Score / 100</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card" style="text-align:center"><div style="font-size:2rem;font-weight:700;color:#3fb950;font-family:\'JetBrains Mono\',monospace">{len(cr.get("matched_skills",[]))}</div><div style="color:#8b949e;font-size:12px;text-transform:uppercase">Matched Skills</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="card" style="text-align:center"><div style="font-size:2rem;font-weight:700;color:#f85149;font-family:\'JetBrains Mono\',monospace">{len(cr.get("missing_skills",[]))}</div><div style="color:#8b949e;font-size:12px;text-transform:uppercase">Skill Gaps</div></div>', unsafe_allow_html=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("#### ✅ Matched Skills")
            st.markdown('<div class="card card-green">' + render_chips(cr.get("matched_skills", []), "chip-green") + '</div>', unsafe_allow_html=True)
        with col_r:
            st.markdown("#### ⚠️ Skill Gaps")
            st.markdown('<div class="card card-red">' + render_chips(cr.get("missing_skills", []), "chip-red") + '</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 💪 Strengths")
            for s in cr.get("strengths", []):
                st.markdown(f'<div style="color:#3fb950;padding:4px 0;font-size:14px">▸ {s}</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown("#### 🔍 Areas to Improve")
            for w in cr.get("weaknesses", []):
                st.markdown(f'<div style="color:#d29922;padding:4px 0;font-size:14px">▸ {w}</div>', unsafe_allow_html=True)

        st.markdown("---")
        rec = cr.get("hiring_recommendation", "")
        st.markdown(f'<div class="card card-accent"><strong style="color:#58a6ff">Hiring Recommendation:</strong><br><span style="color:#cdd9e5">{rec}</span></div>', unsafe_allow_html=True)

        if bp:
            summary = bp.get("candidate_summary", "")
            if summary:
                st.markdown(f'<div class="card"><strong style="color:#8b949e;font-size:12px;text-transform:uppercase">Candidate Summary</strong><br><span style="color:#cdd9e5">{summary}</span></div>', unsafe_allow_html=True)
            if bp.get("question_distribution"):
                qd = bp["question_distribution"]
                st.markdown("#### 📊 Interview Question Distribution")
                qcols = st.columns(len(qd))
                for i, (k, v) in enumerate(qd.items()):
                    with qcols[i]:
                        st.metric(k.replace("_", " ").title(), v)

        st.markdown("---")
        total_qs = len(st.session_state.questions)
        st.markdown(f'<div class="card card-accent" style="text-align:center"><strong style="color:#58a6ff">{total_qs} personalised questions ready</strong><br><span style="color:#8b949e;font-size:13px">Tailored to your resume and the job description</span></div>', unsafe_allow_html=True)

        if st.button("🚀 Start Interview →"):
            st.session_state.stage = "interview"
            st.rerun()

    # ── STAGE 4: INTERVIEW ──
    elif stage == "interview":
        history   = st.session_state.history
        questions = st.session_state.questions
        q_index   = st.session_state.q_index
        current_q = st.session_state.current_question
        total     = len(questions)
        answered  = len(history)

        col_h, col_p = st.columns([3, 1])
        with col_h:
            st.markdown("## Live Interview")
        with col_p:
            st.markdown(f'<div style="text-align:right;color:#8b949e;font-size:13px;padding-top:28px">Question {answered + 1} of {total}</div>', unsafe_allow_html=True)

        st.progress(min(answered / total, 1.0))
        st.markdown("---")

        qb = st.session_state.question_bank or {}
        flat_with_cat = []
        for cat, qs in qb.items():
            for q in qs:
                flat_with_cat.append((cat.replace("_", " ").title(), q.get("question", str(q)) if isinstance(q, dict) else str(q)))
        cat_label = flat_with_cat[answered][0] if answered < len(flat_with_cat) else "Question"

        st.markdown(f'<div class="q-badge">{cat_label}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="question-box">{current_q}</div>', unsafe_allow_html=True)

        answer = st.text_area("Your Answer", height=160, placeholder="Type your answer here…", key=f"ans_{answered}")

        if st.button("Submit Answer →"):
            if not answer.strip():
                st.warning("Please type your answer before submitting.")
            else:
                with st.spinner("Evaluating your answer…"):
                    eval_prompt = f"""
You are a senior technical interviewer.

Candidate Resume: {json.dumps(st.session_state.resume_data)}
Job Description: {json.dumps(st.session_state.jd_data)}
Previous History: {json.dumps(history)}
Current Question: {current_q}
Candidate Answer: {answer}

Return ONLY JSON.
Schema:
{{
    "technical_score": 0,
    "communication_score": 0,
    "completeness_score": 0,
    "feedback": "",
    "next_action": "",
    "next_question": ""
}}
next_action must be "follow_up" or "new_question"
"""
                    eval_result = call_groq(eval_prompt, temperature=0)
                    st.session_state.last_eval = eval_result

                history.append({
                    "question":            current_q,
                    "answer":              answer,
                    "technical_score":     eval_result["technical_score"],
                    "communication_score": eval_result["communication_score"],
                    "completeness_score":  eval_result["completeness_score"],
                    "feedback":            eval_result["feedback"],
                })
                st.session_state.history = history

                if eval_result["next_action"] == "follow_up":
                    st.session_state.current_question = eval_result["next_question"]
                else:
                    next_idx = q_index + 1
                    if next_idx >= total:
                        with st.spinner("Generating final report…"):
                            st.session_state.report = call_groq(_report_prompt(history, st.session_state.resume_data, st.session_state.jd_data), temperature=0)
                        st.session_state.stage = "report"
                        st.rerun()
                    else:
                        st.session_state.q_index    = next_idx
                        st.session_state.current_question = questions[next_idx]
                st.rerun()

        if st.session_state.last_eval:
            ev = st.session_state.last_eval
            st.markdown("---")
            st.markdown("##### Last Evaluation")
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown(f'<div class="score-block"><div class="score-number" style="color:{score_color(ev["technical_score"])}">{ev["technical_score"]}/10</div><div class="score-label">Technical</div></div>', unsafe_allow_html=True)
            with sc2:
                st.markdown(f'<div class="score-block"><div class="score-number" style="color:{score_color(ev["communication_score"])}">{ev["communication_score"]}/10</div><div class="score-label">Communication</div></div>', unsafe_allow_html=True)
            with sc3:
                st.markdown(f'<div class="score-block"><div class="score-number" style="color:{score_color(ev["completeness_score"])}">{ev["completeness_score"]}/10</div><div class="score-label">Completeness</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="feedback-box"><strong>Feedback:</strong> {ev["feedback"]}</div>', unsafe_allow_html=True)
            if ev.get("next_action") == "follow_up":
                st.markdown('<div style="color:#d29922;font-size:13px;margin-top:8px">🔁 Follow-up question generated above</div>', unsafe_allow_html=True)

        if history:
            st.markdown("---")
            with st.expander(f"📜 Interview Transcript ({len(history)} answered)"):
                for i, h in enumerate(history, 1):
                    st.markdown(f"""
                    <div class="card" style="margin-bottom:12px">
                        <div style="color:#8b949e;font-size:12px;text-transform:uppercase;margin-bottom:6px">Q{i}</div>
                        <div style="font-weight:500;color:#e6edf3;margin-bottom:8px">{h['question']}</div>
                        <div style="color:#8b949e;font-size:13px;margin-bottom:8px"><em>{h['answer'][:200]}{'…' if len(h['answer'])>200 else ''}</em></div>
                        <span style="color:{score_color(h['technical_score'])}">Tech {h['technical_score']}/10</span> &nbsp;
                        <span style="color:{score_color(h['communication_score'])}">Comm {h['communication_score']}/10</span> &nbsp;
                        <span style="color:{score_color(h['completeness_score'])}">Comp {h['completeness_score']}/10</span>
                        <div style="color:#8b949e;font-size:13px;margin-top:6px">{h['feedback']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        col_skip, col_end = st.columns(2)
        with col_skip:
            if st.button("⏭ Skip Question"):
                next_idx = q_index + 1
                if next_idx >= total:
                    st.session_state.stage = "report"
                    st.rerun()
                else:
                    st.session_state.q_index = next_idx
                    st.session_state.current_question = questions[next_idx]
                    st.session_state.last_eval = None
                    st.rerun()
        with col_end:
            if st.button("🏁 End Interview & Get Report"):
                if history:
                    with st.spinner("Generating final report…"):
                        st.session_state.report = call_groq(
                            _report_prompt(history, st.session_state.resume_data, st.session_state.jd_data),
                            temperature=0,
                        )
                    st.session_state.stage = "report"
                    st.rerun()
                else:
                    st.warning("Answer at least one question first.")

    # ── STAGE 5: REPORT ──
    elif stage == "report":
        report  = st.session_state.report
        history = st.session_state.history
        cr      = st.session_state.comparison_result

        st.markdown("## Final Interview Report")
        st.markdown("---")

        if report:
            overall       = report.get("overall_score", 0)
            overall_color = score_color(overall)

            st.markdown(f"""
            <div class="card" style="text-align:center;padding:36px">
                <div style="font-size:4.5rem;font-weight:700;font-family:'JetBrains Mono',monospace;color:{overall_color};line-height:1">{overall}</div>
                <div style="color:#8b949e;font-size:13px;text-transform:uppercase;letter-spacing:0.1em;margin-top:8px">Overall Score / 100</div>
                <div style="margin-top:16px">
                    <span style="color:#58a6ff;font-size:15px;font-weight:500">Technical: {report.get('technical_rating','—')}</span>
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <span style="color:#58a6ff;font-size:15px;font-weight:500">Communication: {report.get('communication_rating','—')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if history:
                avg_tech = round(sum(h["technical_score"]     for h in history) / len(history), 1)
                avg_comm = round(sum(h["communication_score"] for h in history) / len(history), 1)
                avg_comp = round(sum(h["completeness_score"]  for h in history) / len(history), 1)
                m1, m2, m3, m4 = st.columns(4)
                with m1: st.metric("Questions Answered", len(history))
                with m2: st.metric("Avg Technical",      f"{avg_tech}/10")
                with m3: st.metric("Avg Communication",  f"{avg_comm}/10")
                with m4: st.metric("Avg Completeness",   f"{avg_comp}/10")

            st.markdown("---")
            col_s, col_w = st.columns(2)
            with col_s:
                st.markdown("#### 💪 Interview Strengths")
                for s in report.get("strengths", []):
                    st.markdown(f'<div class="card card-green" style="padding:10px 16px;margin-bottom:8px;font-size:14px;color:#cdd9e5">▸ {s}</div>', unsafe_allow_html=True)
            with col_w:
                st.markdown("#### 🔍 Areas to Develop")
                for w in report.get("weaknesses", []):
                    st.markdown(f'<div class="card card-orange" style="padding:10px 16px;margin-bottom:8px;font-size:14px;color:#cdd9e5">▸ {w}</div>', unsafe_allow_html=True)

            st.markdown("---")
            rec = report.get("recommendation", "")
            st.markdown(f'<div class="card card-accent" style="padding:20px 24px"><strong style="color:#58a6ff;font-size:13px;text-transform:uppercase">Final Recommendation</strong><br><br><span style="color:#e6edf3;font-size:15px;line-height:1.6">{rec}</span></div>', unsafe_allow_html=True)

        # Full transcript
        if history:
            st.markdown("---")
            st.markdown("### 📜 Full Interview Transcript")
            for i, h in enumerate(history, 1):
                with st.expander(f"Q{i} — {h['question'][:70]}{'…' if len(h['question'])>70 else ''}"):
                    st.markdown(f"**Question:** {h['question']}")
                    st.markdown(f"**Your Answer:** {h['answer']}")
                    st.markdown("---")
                    sc1, sc2, sc3 = st.columns(3)
                    with sc1: st.metric("Technical",     f"{h['technical_score']}/10")
                    with sc2: st.metric("Communication", f"{h['communication_score']}/10")
                    with sc3: st.metric("Completeness",  f"{h['completeness_score']}/10")
                    st.markdown(f"**Feedback:** {h['feedback']}")

        if cr:
            st.markdown("---")
            st.markdown("### 🔗 Match Score")
            ms = cr.get("match_score", 0)
            st.markdown(f'<div class="card" style="text-align:center"><span style="font-size:2rem;font-weight:700;color:{score_color(ms)};font-family:\'JetBrains Mono\',monospace">{ms}/100</span><span style="color:#8b949e;font-size:13px;margin-left:16px">Profile–JD Match Score</span></div>', unsafe_allow_html=True)

        # ─── PDF DOWNLOAD SECTION ───
        st.markdown("---")
        st.markdown("### 📥 Download Your Report")
        st.markdown('<div class="card card-accent"><p style="color:#cdd9e5;margin:0">Your full interview report — scores, feedback, transcript, and match analysis — compiled into a single PDF.</p></div>', unsafe_allow_html=True)

        if report:
            with st.spinner("Building PDF…"):
                pdf_bytes = generate_pdf_report(
                    report=report,
                    history=history,
                    comparison_result=cr,
                    resume_data=st.session_state.resume_data,
                    jd_data=st.session_state.jd_data,
                )
            candidate_name = (st.session_state.resume_data or {}).get("name", "candidate").replace(" ", "_").lower()
            filename = f"interview_report_{candidate_name}.pdf"

            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
            )
        else:
            st.info("Complete the interview first to generate your report.")

        st.markdown("---")
        if st.button("🔄 Start New Interview"):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()