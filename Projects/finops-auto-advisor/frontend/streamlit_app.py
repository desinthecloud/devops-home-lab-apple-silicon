import requests
import streamlit as st
import pandas as pd

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
API_URL = st.secrets.get("API_URL", "").strip()

if not API_URL:
    st.error("API_URL not set. Add it to .streamlit/secrets.toml")
    st.stop()

# ---------------------------------------------------
# HELPER: fetch insights
# ---------------------------------------------------
def fetch_insights():
    try:
        response = requests.get(f"{API_URL}/insights", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch insights: {e}")
        return None

# ---------------------------------------------------
# UI LAYOUT
# ---------------------------------------------------
st.set_page_config(page_title="FinOps Auto-Advisor")

st.title("FinOps Auto-Advisor Dashboard")
st.caption("Daily AWS cost insights powered by serverless + AI")

data = fetch_insights()

if not data:
    st.stop()

# ---------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Today's Spend", f"${data['total_spend']:.2f}")
col2.metric("Prev Period", f"${data['previous_period_spend']:.2f}")
col3.metric("Change", f"{data['spend_delta_pct']:.2f}%")

st.markdown("---")

# ---------------------------------------------------
# AI SUMMARY
# ---------------------------------------------------
st.subheader("AI Summary")
st.write(data["summary"])

st.markdown("---")

# ---------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------
st.subheader("Top Recommendations")

recs_df = pd.DataFrame(data["top_recommendations"])
st.dataframe(recs_df)

# ---------------------------------------------------
# COST BY SERVICE
# ---------------------------------------------------
st.subheader("Spend by Service")

svc_df = pd.DataFrame(data["raw_findings"]["by_service"])
st.bar_chart(svc_df.set_index("service"))

# ---------------------------------------------------
# ANOMALIES
# ---------------------------------------------------
st.subheader("Anomalies Detected")

anoms = data["raw_findings"].get("anomalies", [])
if anoms:
    st.write(pd.DataFrame(anoms))
else:
    st.write("No anomalies detected.")
