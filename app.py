import streamlit as st
import pandas as pd

# Configure page layout
st.set_page_config(page_title="Tire Line Maintenance Dashboard", layout="wide")

st.title("🛩️ Aircraft Tire Line Maintenance")
st.caption("Live tire status by aircraft registration from Google Drive CSV")

# --- Google Drive Setup ---
# Replace with your actual Google Drive File ID
FILE_ID = "1iDDFhpPLDiuEjgZAkw7RFrGCidiumyWO"
CSV_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    # Strip whitespace from column names just in case
    df.columns = df.columns.str.strip()
    return df

# Button to manually clear cache and pull latest file
col_title, col_btn = st.columns([5, 1])
with col_btn:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

try:
    data = load_data(CSV_URL)

    # 1. Dropdown Selector for Aircraft_Registration
    registrations = sorted(data["Aircraft_Registration"].dropna().unique())
    
    selected_reg = st.selectbox(
        "Select Aircraft Registration:",
        options=registrations,
        index=0 if len(registrations) > 0 else None
    )

    if selected_reg:
        # Filter table by selected aircraft
        filtered_df = data[data["Aircraft_Registration"] == selected_reg].copy()

        # Display Top Summary Metrics
        ac_type = filtered_df["Aircraft_Type"].iloc[0] if "Aircraft_Type" in filtered_df.columns else "N/A"
        updated_date = filtered_df["Updated_Date"].iloc[0] if "Updated_Date" in filtered_df.columns else "N/A"
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Aircraft Registration", selected_reg)
        m2.metric("Aircraft Type", ac_type)
        m3.metric("Last Updated Date", str(updated_date))

        st.divider()

        # 2. Detail Table
        st.subheader(f"Tire & Landing Gear Details for {selected_reg}")
        
        # Select columns to display in the table
        display_cols = [
            "Landing_Gear", 
            "Wheel_Position", 
            "nLanding", 
            "Ref_nLanding"
        ]
        
        # Only keep columns that actually exist in the CSV
        existing_cols = [c for c in display_cols if c in filtered_df.columns]
        
        # Format the table cleanly
        st.dataframe(
            filtered_df[existing_cols].fillna("-"),
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error(f"Error loading or parsing CSV: {e}")
    st.info("Please verify the Google Drive file permissions are set to 'Anyone with the link can view'.")
