import streamlit as st

params = st.query_params

st.set_page_config(page_title="Translation Verification", layout="centered")
st.title("Official Translation Verification")

st.markdown("This page displays the original data submitted by the user to our company for the purpose of driver's license translation. Please verify the printed document against the following:")

st.markdown("---")
st.write("**Name:**", params.get("name", ""))
st.write("**Address:**", params.get("address", ""))
st.write("**Date of Birth:**", params.get("dob", ""))
st.write("**Nationality:**", params.get("nationality", ""))
st.write("**Category:**", params.get("category", ""))
st.write("**Issued:**", params.get("issued", ""))
st.write("**Expires:**", params.get("expires", ""))
st.write("**First Issued:**", params.get("first_issue", ""))
st.write("**DL Number:**", params.get("dl", ""))

st.markdown("---")
st.info("Any inconsistency between this information and the printed translation document may indicate tampering. The company is not responsible for unauthorized modifications.")
