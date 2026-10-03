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
        gear = normalize_landing_gear(row["Landing_Gear"])
        position = normalize_position(row["Wheel_Position"])

        n_landing = row["nLanding"]
        ref_landing = row["Ref_nLanding"]
        percent = calculate_percent(n_landing, ref_landing)

        item = {
            "position": position,
            "nLanding": n_landing,
            "Ref_nLanding": ref_landing,
            "percent": percent,
            "label": f"{format_number(n_landing)}/{format_number(ref_landing)}",
            "status": get_status_class(percent)
        }

        if gear == "NOSE" and position in wheels["nose"]:
            wheels["nose"][position] = item

        elif gear == "MAIN" and position in wheels["main"]:
            wheels["main"][position] = item

        elif position in wheels["main"]:
            wheels["main"][position] = item

        elif position in wheels["nose"]:
            wheels["nose"][position] = item

    return wheels


def wheel_html(label, item, size="small"):
    if item is None:
        return f"""
<div class="wheel-block {size}">
    <div class="percent-placeholder">&nbsp;</div>
    <div class="wheel-box empty">{safe_text(label)}</div>
    <div class="landing-value empty">-</div>
</div>
"""

    percent = item.get("percent")
    percent_text = f"{percent}%" if percent is not None else "&nbsp;"
    status = item.get("status", "empty")
    landing_label = item.get("label", "-")

    return f"""
<div class="wheel-block {size}">
    <div class="percent-text {status}">{percent_text}</div>
    <div class="wheel-box {status}">{safe_text(label)}</div>
    <div class="landing-value {status}">{safe_text(landing_label)}</div>
</div>
"""


def render_aircraft_card(selected_reg, ac_type, updated_date, wheels):
    nose_lh = wheel_html("LH", wheels["nose"].get("LH"), size="small")
    nose_rh = wheel_html("RH", wheels["nose"].get("RH"), size="small")

    main_1 = wheel_html("1", wheels["main"].get("1"), size="large")
    main_2 = wheel_html("2", wheels["main"].get("2"), size="large")
    main_3 = wheel_html("3", wheels["main"].get("3"), size="large")
    main_4 = wheel_html("4", wheels["main"].get("4"), size="large")

    card_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    html, body {{
        margin: 0;
        padding: 0;
        background: transparent;
        font-family: Arial, Helvetica, sans-serif;
    }}

    .page-wrapper {{
        display: flex;
        justify-content: center;
        align-items: flex-start;
        width: 100%;
        padding-top: 10px;
        box-sizing: border-box;
    }}

    .aircraft-card {{
        width: 320px;
        min-height: 480px;
        border: 4px solid #000000;
        border-radius: 42px;
        background: #ffffff;
        overflow: hidden;
        color: #000000;
        box-sizing: border-box;
    }}

    .updated-date {{
        text-align: center;
        font-size: 22px;
        font-weight: 400;
        padding-top: 30px;
        padding-bottom: 6px;
        line-height: 1.2;
    }}

    .gold-strip {{
        background: #ead27a;
        text-align: center;
        font-size: 28px;
        font-weight: 400;
        line-height: 1.15;
        padding: 0 10px;
        box-sizing: border-box;
        width: 100%;
    }}

    .gold-strip.second {{
        margin-top: 4px;
    }}

    .nose-section {{
        margin-top: 12px;
        display: flex;
        justify-content: center;
    }}

    .main-section {{
        margin-top: 28px;
        display: flex;
        justify-content: center;
        gap: 32px;
    }}

    .wheel-pair {{
        position: relative;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        box-sizing: border-box;
    }}

    .wheel-pair.nose-pair {{
        gap: 8px;
    }}

    .wheel-pair.main-pair {{
        gap: 8px;
    }}

    /*
       Black connector elements between each pair of blocks.
       They are placed behind the tire blocks and centered vertically
       with the wheel boxes.
    */
    .connector {{
        position: absolute;
        background: #000000;
        z-index: 1;
        border-radius: 2px;
        pointer-events: none;
    }}

    .connector.nose-connector {{
        width: 26px;
        height: 8px;
        top: 45px;
        left: 50%;
        transform: translateX(-50%);
    }}

    .connector.main-connector {{
        width: 26px;
        height: 9px;
        top: 51px;
        left: 50%;
        transform: translateX(-50%);
    }}

    .wheel-block {{
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        box-sizing: border-box;
    }}

    .wheel-block.small {{
        width: 52px;
    }}

    .wheel-block.large {{
        width: 52px;
    }}

    .percent-text {{
        font-size: 16px;
        line-height: 1.1;
        min-height: 22px;
        color: #ff6426;
        font-weight: 400;
        width: 100%;
        text-align: center;
        white-space: nowrap;
    }}

    .percent-placeholder {{
        min-height: 22px;
        line-height: 1.1;
        font-size: 16px;
        width: 100%;
    }}

    .wheel-box {{
        display: flex;
        justify-content: center;
        align-items: center;
        border: 2px solid #00304b;
        box-sizing: border-box;
        font-weight: 400;
        color: #ffffff;
        position: relative;
        z-index: 3;
    }}

    .wheel-block.small .wheel-box {{
        width: 45px;
        height: 38px;
        border-radius: 7px;
        font-size: 15px;
    }}

    .wheel-block.large .wheel-box {{
        width: 43px;
        height: 50px;
        border-radius: 7px;
        font-size: 22px;
    }}

    .wheel-box.warning {{
        background: #ffc20a;
        color: #ffffff;
    }}

    .wheel-box.danger {{
        background: #f34b3f;
        color: #ffffff;
    }}

    .wheel-box.normal {{
        background: #9fa8ad;
        color: #ffffff;
    }}

    .wheel-box.empty {{
        background: #9fa8ad;
        color: #ffffff;
    }}

    .landing-value {{
        min-height: 26px;
        margin-top: 7px;
        font-size: 20px;
        line-height: 1.1;
        color: #ff6426;
        font-weight: 400;
        white-space: nowrap;
        width: 95px;
        text-align: center;
        box-sizing: border-box;
    }}

    .landing-value.empty {{
        color: transparent;
    }}

    .percent-text.empty {{
        color: transparent;
    }}

    .card-bottom-space {{
        height: 80px;
    }}
</style>
</head>

<body>
    <div class="page-wrapper">
        <div class="aircraft-card">
            <div class="updated-date">Update: {safe_text(updated_date)}</div>

            <div class="gold-strip">{safe_text(selected_reg)}</div>
            <div class="gold-strip second">{safe_text(ac_type)}</div>

            <div class="nose-section">
                <div class="wheel-pair nose-pair">
                    <div class="connector nose-connector"></div>
                    {nose_lh}
                    {nose_rh}
                </div>
            </div>

            <div class="main-section">
                <div class="wheel-pair main-pair">
                    <div class="connector main-connector"></div>
                    {main_1}
                    {main_2}
                </div>

                <div class="wheel-pair main-pair">
                    <div class="connector main-connector"></div>
                    {main_3}
                    {main_4}
                </div>
            </div>

            <div class="card-bottom-space"></div>
        </div>
    </div>
</body>
</html>
"""

    card_html = textwrap.dedent(card_html)

    components.html(
        card_html,
        height=540,
        scrolling=False
    )


# ------------------------------------------------------------
# App UI
# ------------------------------------------------------------
st.title("Aircraft Tire Line Maintenance")
st.caption("Live tire status by aircraft registration from Google Drive CSV")

top_col_1, top_col_2 = st.columns([5, 1])

with top_col_2:
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()

try:
    data = load_data(CSV_URL)

    required_main_column = "Aircraft_Registration"

    if required_main_column not in data.columns:
        st.error(f"Missing required column: {required_main_column}")
        st.stop()

    registrations = sorted(data["Aircraft_Registration"].dropna().astype(str).unique())

    if len(registrations) == 0:
        st.warning("No aircraft registrations found in the CSV.")
        st.stop()

    selected_reg = st.selectbox(
        "Select Aircraft Registration:",
        options=registrations,
        index=0
    )

    filtered_df = data[data["Aircraft_Registration"].astype(str) == selected_reg].copy()

    if filtered_df.empty:
        st.warning("No data found for the selected aircraft registration.")
        st.stop()

    ac_type = (
        filtered_df["Aircraft_Type"].iloc[0]
        if "Aircraft_Type" in filtered_df.columns
        else "N/A"
    )

    updated_date = (
        filtered_df["Updated_Date"].iloc[0]
        if "Updated_Date" in filtered_df.columns
        else "N/A"
    )

    wheels = build_wheel_dict(filtered_df)

    render_aircraft_card(
        selected_reg=selected_reg,
        ac_type=ac_type,
        updated_date=updated_date,
        wheels=wheels
    )

    with st.expander("Show source data"):
        display_cols = [
            "Aircraft_Registration",
            "Aircraft_Type",
            "Updated_Date",
            "Landing_Gear",
            "Wheel_Position",
            "nLanding",
            "Ref_nLanding"
        ]

        existing_cols = [c for c in display_cols if c in filtered_df.columns]

        st.dataframe(
            filtered_df[existing_cols].fillna("-"),
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error(f"Error loading or parsing CSV: {e}")
    st.info(
        "Please verify that the Google Drive file permission is set to "
        "'Anyone with the link can view'."
    )
