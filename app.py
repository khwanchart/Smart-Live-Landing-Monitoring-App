import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import html
import math
import textwrap

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Aircraft Tire Line Maintenance",
    layout="wide"
)

# ------------------------------------------------------------
# Google Drive Setup
# ------------------------------------------------------------
FILE_ID = "1iDDFhpPLDiuEjgZAkw7RFrGCidiumyWO"
CSV_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"


@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def safe_text(value):
    if value is None or pd.isna(value):
        return "-"
    return html.escape(str(value))


def to_number(value):
    try:
        if value is None or pd.isna(value):
            return None

        num = float(value)

        if math.isnan(num) or math.isinf(num):
            return None

        return num

    except Exception:
        return None


def format_number(value):
    num = to_number(value)

    if num is None:
        return "-"

    if num.is_integer():
        return str(int(num))

    return str(round(num, 1))


def calculate_percent(n_landing, ref_landing):
    n = to_number(n_landing)
    ref = to_number(ref_landing)

    if n is None or ref is None or ref == 0:
        return None

    percent = (n / ref) * 100

    if math.isnan(percent) or math.isinf(percent):
        return None

    return int(round(percent))


def get_status_class(percent):
    if percent is None:
        return "empty"

    if percent >= 90:
        return "danger"

    if percent >= 80:
        return "warning"

    return "normal"


def normalize_position(value):
    if value is None or pd.isna(value):
        return ""

    text = str(value).strip().upper()
    text = text.replace("LEFT", "LH")
    text = text.replace("RIGHT", "RH")

    return text


def normalize_landing_gear(value):
    if value is None or pd.isna(value):
        return ""

    text = str(value).strip().upper()

    if "NOSE" in text or "NLG" in text:
        return "NOSE"

    if "MAIN" in text or "MLG" in text:
        return "MAIN"

    return text


def build_wheel_dict(filtered_df):
    wheels = {
        "nose": {
            "LH": None,
            "RH": None
        },
        "main": {
            "1": None,
            "2": None,
            "3": None,
            "4": None
        }
    }

    required_cols = ["Landing_Gear", "Wheel_Position", "nLanding", "Ref_nLanding"]
    missing_cols = [c for c in required_cols if c not in filtered_df.columns]

    if missing_cols:
        st.warning(f"Missing required column(s): {', '.join(missing_cols)}")
        return wheels

    for _, row in filtered_df.iterrows():
        gear = norma
