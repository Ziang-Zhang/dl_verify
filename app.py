import streamlit as st
import os
import base64
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from translate import translations  # 你的语言字典

# 页面配置
st.set_page_config(page_title="Driver License Verification", layout="centered")

# 读取 URL 参数
params = st.query_params
lang = params.get("lang", "English")
strings = translations.get(lang, translations["English"])

st.title(strings.get("main_title", "Driver License Info"))
st.markdown(strings.get("description", "The following information was retrieved from the secure QR code."))
st.markdown("---")

# 加载密钥
load_dotenv()
secret = "FERNET_SECRET=5tWZaQL6luw5mgBHZZVKRg-BVYqsneYyINBnybgOgpQ="
if not secret:
    st.error("Fernet secret key is not set. Please check .env configuration.")
    st.stop()

fernet = Fernet(secret.encode())

# 解密 info
encrypted_b64 = params.get("data")
if not encrypted_b64:
    st.warning("No encrypted data provided in URL.")
    st.stop()

try:
    decrypted_bytes = fernet.decrypt(base64.urlsafe_b64decode(encrypted_b64))
    info_dict = json.loads(decrypted_bytes.decode("utf-8"))

    for k, v in info_dict.items():
        st.write(f"**{k}**: {v}")

except Exception as e:
    st.error("Failed to decrypt the QR code data. It may be corrupted or invalid.")
    st.exception(e)

st.markdown("---")
st.info(strings.get("footer_note", "If the information above is incorrect, please contact the service provider."))
