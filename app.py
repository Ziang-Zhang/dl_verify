import streamlit as st

params = st.query_params

st.set_page_config(page_title="Translation Verification", layout="centered")
st.title("Official Translation Verification")

st.markdown("This page displays the original data submitted by the user to our company for the purpose of driver's license translation. Please verify the printed document against the following:")

st.markdown("---")

for key, value in params.items():
    st.write(f"**{key}**: {value}")

st.markdown("---")
st.info("Any inconsistency between this information and the printed translation document may indicate tampering. The company is not responsible for unauthorized modifications.")
