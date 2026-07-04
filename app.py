import streamlit as st
from google.cloud import discoveryengine_v1 as discoveryengine
import pandas as pd
import numpy as np
import requests

from logging_utils import append_log_entry, fetch_all_logs

# ======================================================================
# 1. GCP CONFIGURATION
# ======================================================================
PROJECT_ID = "yojana-setu-finder"
LOCATION = "global"
DATA_STORE_ID = "indian-schemes-ds_1783002239613"

STATE_LANGUAGES = {
    "Maharashtra": "Marathi",
    "Delhi": "Hindi",
    "Uttar Pradesh": "Hindi",
    "Bihar": "Hindi",
    "Karnataka": "Kannada",
    "Tamil Nadu": "Tamil",
    "Other": "English"
}

# Simple multi-language labels (headline-level only)
LABELS = {
    "beneficiary_profile": {
        "English": "Beneficiary Profile",
        "Hindi": "लाभार्थी प्रोफ़ाइल",
        "Marathi": "लाभार्थी प्रोफाइल",
        "Kannada": "ಹಕ್ಕುದಾರರ ವಿವರ",
        "Tamil": "பலனாளி விவரம்"
    },
    "citizen_portal": {
        "English": "Citizen Welfare Portal",
        "Hindi": "नागरिक कल्याण पोर्टल",
        "Marathi": "नागरिक कल्याण पोर्टल",
        "Kannada": "ನಾಗರಿಕ ಕಲ್ಯಾಣ ಪೋರ್ಟಲ್",
        "Tamil": "குடிமக்கள் நலன் தளம்"
    },
    "admin_panel": {
        "English": "Admin Analytics Panel",
        "Hindi": "प्रशासनिक विश्लेषण पैनल",
        "Marathi": "प्रशासनिक विश्लेषण पॅनेल",
        "Kannada": "ನಿರ್ವಹಣಾ ವಿಶ್ಲೇಷಣೆ ಫಲಕ",
        "Tamil": "நிர்வாக பகுப்பாய்வு பலகை"
    }
}

def get_label(key: str, lang: str) -> str:
    return LABELS.get(key, {}).get(lang, LABELS.get(key, {}).get("English", key))


# ======================================================================
# 2. REAL IP DETECTION
# ======================================================================
def get_client_ip():
    try:
        header_value = st.context.headers.get("X-Forwarded-For", "")
        if header_value:
            return header_value.split(",")[0].strip()
    except Exception:
        pass
    return None

def detect_user_state(ip_addr):
    if not ip_addr:
        return "Other"
    try:
        response = requests.get(f"https://ipapi.co/{ip_addr}/json/", timeout=3).json()
        if response.get("country_code") == "IN":
            region = response.get("region")
            return region if region in STATE_LANGUAGES else "Other"
    except Exception:
        pass
    return "Other"

# ======================================================================
# 3. RAG QUERY FUNCTION
# ======================================================================
def query_yojana_rag(search_query: str, user_context: str, target_language: str) -> str:
    client = discoveryengine.SearchServiceClient()
    serving_config = (
        f"projects/{PROJECT_ID}/locations/{LOCATION}/dataStores/"
        f"{DATA_STORE_ID}/servingConfigs/default_search"
    )

    translation_instruction = ""
    if target_language != "English":
        translation_instruction = (
            f"\n\nIMPORTANT:\n"
            f"Provide the final answer ONLY in {target_language}.\n"
            f"Do NOT include English or any other language.\n"
            f"Respond strictly in {target_language}."
        )

    full_prompt = (
        f"Indian Citizen Profile Context:\n{user_context}\n\n"
        f"Citizen Query:\n{search_query}"
        f"{translation_instruction}"
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=full_prompt,
        page_size=2,
        content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
            summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
                summary_result_count=3,
                include_citations=True,
                use_semantic_chunks=True
            )
        )
    )

    try:
        response = client.search(request)
        if response.summary and response.summary.summary_text:
            return response.summary.summary_text
        return "No matching scheme found. Please visit a CSC."
    except Exception as e:
        return f"Error executing RAG search: {str(e)}"

# ======================================================================
# 4. STREAMLIT UI (REDESIGNED + DARK MODE)
# ======================================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.set_page_config(page_title="Yojana Setu", page_icon="🇮🇳", layout="wide")

bg_light = "linear-gradient(135deg, #fdfcfb 0%, #e2d1f9 100%)"
bg_dark = "linear-gradient(135deg, #1f2933 0%, #111827 100%)"
card_bg_light = "#ffffff"
card_bg_dark = "#111827"
text_color_light = "#222"
text_color_dark = "#f9fafb"

bg_main = bg_dark if st.session_state.dark_mode else bg_light
card_bg = card_bg_dark if st.session_state.dark_mode else card_bg_light
text_color = text_color_dark if st.session_state.dark_mode else text_color_light

st.markdown(f"""
<style>
.main {{
    background: {bg_main};
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    color: {text_color};
}}

.top-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    margin-bottom: 8px;
}}

.nav-left {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.nav-logo {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #FF9933 0%, #128807 40%, #1A73E8 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 18px;
    font-weight: 700;
}}

.nav-title {{
    font-size: 18px;
    font-weight: 600;
}}

.nav-right {{
    font-size: 12px;
    opacity: 0.8;
}}

/* Hero header */
.hero-container {{
    background: linear-gradient(120deg, #FF9933 0%, #128807 50%, #1A73E8 100%);
    padding: 18px 24px;
    border-radius: 14px;
    color: white;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
    margin-bottom: 18px;
}}

.hero-title {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 0.03em;
}}

.hero-subtitle {{
    font-size: 14px;
    margin-top: 4px;
    opacity: 0.9;
}}

/* Tabs */
.stTabs [role="tablist"] {{
    gap: 8px;
}}
.stTabs [role="tab"] {{
    padding: 8px 16px;
    border-radius: 999px;
    border: 1px solid #e0e0e0;
}}
.stTabs [role="tab"][aria-selected="true"] {{
    background-color: #128807;
    color: white;
    border-color: #0c6304;
}}

/* Badge */
.detected-badge {{
    background-color: rgba(26, 115, 232, 0.08);
    padding: 6px 12px;
    border-radius: 999px;
    color: #1A73E8;
    font-weight: 600;
    border: 1px solid rgba(26, 115, 232, 0.25);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 12px;
}}

/* Cards with subtle animation */
.card {{
    background-color: {card_bg};
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.10);
    margin-bottom: 16px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}}

/* Sidebar card */
.sidebar-card {{
    background-color: {card_bg};
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.10);
}}

/* Buttons */
.stButton>button {{
    background: linear-gradient(135deg, #128807 0%, #0c6304 100%);
    color: white;
    border-radius: 999px;
    border: none;
    width: 100%;
    font-weight: 600;
    padding: 8px 0;
}}
.stButton>button:hover {{
    background: linear-gradient(135deg, #0c6304 0%, #094a03 100%);
}}

/* Chat input */
div[data-baseweb="textarea"] textarea {{
    border-radius: 12px !important;
}}

/* Metrics card */
.metric-card {{
    background-color: {card_bg};
    border-radius: 14px;
    padding: 12px 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.10);
}}

/* Footer */
.footer {{
    margin-top: 24px;
    font-size: 11px;
    color: #888;
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)

# Top navigation bar
st.markdown(
    """
    <div class="top-nav">
        <div class="nav-left">
            <div class="nav-logo">🛤️</div>
            <div class="nav-title">Yojana Setu · Welfare Bridge</div>
        </div>
        <div class="nav-right">
            Built on Google Cloud by Team Vishishta – GenAI Academy APAC Edition
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Dark mode toggle
mode_col1, mode_col2 = st.columns([0.8, 0.2])
with mode_col2:
    toggle = st.toggle("Dark mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = toggle

# Hero header
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🇮🇳 Yojana Setu: Welfare Scheme Assistant</div>
        <div class="hero-subtitle">
            Conversational eligibility checks for Indian welfare schemes — grounded in official policy, delivered in your language.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_citizen, tab_admin = st.tabs([
    f"🤝 {get_label('citizen_portal', 'English')}",
    f"📊 {get_label('admin_panel', 'English')}"
])

# ======================================================================
# 5. CITIZEN TAB
# ======================================================================
if "detected_state" not in st.session_state:
    ip = get_client_ip()
    st.session_state.detected_state = detect_user_state(ip)
    st.session_state.active_state = st.session_state.detected_state

with tab_citizen:
    col_main, col_side = st.columns([2.3, 1.2])

    # Sidebar first (so variables exist)
    with col_side:
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        initial_state = st.session_state.active_state
        mapped_language_initial = STATE_LANGUAGES.get(initial_state, "English")

        st.header(f"👤 {get_label('beneficiary_profile', mapped_language_initial)}")

        state_options = list(STATE_LANGUAGES.keys())
        selected_state = st.selectbox(
            "State of Residence",
            state_options,
            index=state_options.index(st.session_state.active_state)
        )
        st.session_state.active_state = selected_state

        st.write("")
        mapped_language = STATE_LANGUAGES.get(selected_state, "English")

        # Language selection logic with special case for "Other"
        if selected_state == "Other":
            lang_options = ["Hindi", "English"]
            default_index = 0   # auto-select Hindi
        else:
            lang_options = [mapped_language, "English"]
            default_index = 0   # auto-select regional language

        selected_lang = st.radio("Display AI responses in:", lang_options, index=default_index)

        st.write("")
        st.subheader("📊 Demographics")
        gender = st.selectbox("Gender", ["Female", "Male", "Transgender"])
        age = st.number_input("Age", min_value=0, max_value=110, value=35)
        income = st.number_input("Annual Family Income (₹)", min_value=0, value=120000)
        bpl_card = st.radio("BPL Card Holder?", ["No", "Yes"])
        is_farmer = st.radio("Farmer Family?", ["No", "Yes"])
        has_daughter = st.checkbox("I have a daughter under 10")

        st.markdown("</div>", unsafe_allow_html=True)

    # Profile context
    profile_context = (
        f"Resident of: {selected_state}, Gender: {gender}, Age: {age}, "
        f"Income: Rs. {income}, BPL: {bpl_card}, Farmer: {is_farmer}, "
        f"Daughter Under 10: {has_daughter}"
    )

    # Main column
    with col_main:
        st.markdown(
            f"<span class='detected-badge'>📍 Location detected: <strong>{st.session_state.detected_state}</strong></span>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='card'><h4>⚡ Quick Eligibility Checks</h4>"
            "<p style='font-size:13px;color:#bbb;margin-bottom:10px;'>Tap a shortcut or ask your own question below.</p>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        suggested_query = None
        if col1.button("🏥 PM-JAY Health Insurance"):
            suggested_query = "Am I eligible for PM-JAY health insurance?"
        if col2.button("🔥 PM Ujjwala Gas Subsidy"):
            suggested_query = "Can I get a gas connection under PMUY?"
        if col3.button("👧 Sukanya Samriddhi Savings"):
            suggested_query = "Can I open a Sukanya Samriddhi account?"

        st.write("")
        user_input = st.chat_input("Ask about any welfare scheme...")
        active_query = user_input or suggested_query

        if active_query:
            with st.spinner("Analyzing your profile and matching schemes..."):
                answer = query_yojana_rag(active_query, profile_context, selected_lang)

                q = active_query.lower()
                if any(k in q for k in ["pm-jay", "health", "insurance", "hospital"]):
                    scheme = "PM-JAY"
                elif any(k in q for k in ["pmuy", "gas", "ujjwala", "cylinder"]):
                    scheme = "PMUY"
                elif any(k in q for k in ["sukanya", "daughter", "girl", "ssy"]):
                    scheme = "Sukanya Samriddhi"
                else:
                    scheme = "General Inquiry"

                ineligible_keywords = ["unable to find", "no government scheme", "not qualify", "not eligible"]
                is_eligible = not any(k in answer.lower() for k in ineligible_keywords)

                append_log_entry(
                    query=active_query,
                    scheme=scheme,
                    eligible=is_eligible,
                    state=selected_state,
                    language=selected_lang
                )

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write("### 🎯 Current Inquiry Result")
            with st.chat_message("user"):
                st.markdown(active_query)
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.markdown("</div>", unsafe_allow_html=True)

# ======================================================================
# 6. ADMIN TAB
# ======================================================================
with tab_admin:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("📊 Citizen Demand Dashboard")

    df_logs = pd.DataFrame(fetch_all_logs())

    if df_logs.empty or "scheme" not in df_logs.columns:
        st.warning("No logs available yet. Ask a question in the Citizen tab to generate analytics.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='footer'>Built on Google Cloud · Prototype – GenAI Academy APAC Edition</div>", unsafe_allow_html=True)
        st.stop()

    total_queries = len(df_logs)
    eligible_rate = df_logs["eligible"].mean() * 100 if total_queries > 0 else 0
    scheme_counts = df_logs["scheme"].value_counts()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Queries", f"{total_queries:,}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Eligibility Rate", f"{eligible_rate:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Top Scheme", scheme_counts.index[0] if not scheme_counts.empty else "N/A")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.write("### 📈 Demand Distribution by Scheme")
    st.bar_chart(scheme_counts)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>Built on Google Cloud by Team Vishishta – GenAI Academy APAC Edition</div>", unsafe_allow_html=True)
