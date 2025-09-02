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
version = params.get("v", "2")  # 默认为v2
strings = translations.get(lang, translations["English"])

# v=1时的固定字段顺序
INFO_V1_ORDER = [
    "firstname",
    "lastname", 
    "license_address",
    "dateofbirth",
    "placeofbirth",
    "category",
    "issued",
    "expires",
    "dl_number",
    "dl_first_issued",
]

# v=1时的字段映射（英法两种语言）
FIELD_MAPPINGS = {
    "English": {
        "firstname": "First Name",
        "lastname": "Last Name",
        "license_address": "License Address", 
        "dateofbirth": "Date of Birth",
        "placeofbirth": "Place of Birth",
        "category": "Category",
        "issued": "Issued",
        "expires": "Expires",
        "dl_number": "DL Number",
        "dl_first_issued": "DL First Issued"
    },
    "French": {
        "firstname": "Prénom",
        "lastname": "Nom de famille",
        "license_address": "Adresse du permis",
        "dateofbirth": "Date de naissance", 
        "placeofbirth": "Lieu de naissance",
        "category": "Catégorie",
        "issued": "Émis",
        "expires": "Expire",
        "dl_number": "Numéro de permis",
        "dl_first_issued": "Première émission"
    }
}

# 顶部标题和说明
if lang == "Arabic":
    st.markdown(f"""
    <div dir="rtl" style="text-align: right;">
        <h2>{strings.get("main_title", "Driver License Info")}</h2>
        <p>{strings.get("description", "")}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.title(strings.get("main_title", "Driver License Info"))
    st.markdown(strings.get("description", "The following information was retrieved from the secure QR code."))

st.markdown("---")

# 加载密钥
load_dotenv()
# secret = os.getenv("FERNET_SECRET")
secret = "5tWZaQL6luw5mgBHZZVKRg-BVYqsneYyINBnybgOgpQ="
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
    decrypted_data = json.loads(decrypted_bytes.decode("utf-8"))
    
    # 根据版本处理数据
    if version == "1":
        # v=1: 解密得到数组，按固定顺序映射字段
        if isinstance(decrypted_data, list):
            # 确保语言为英法之一
            display_lang = "French" if lang == "French" else "English"
            field_mapping = FIELD_MAPPINGS[display_lang]
            
            # 创建字段映射字典
            info_dict = {}
            for i, value in enumerate(decrypted_data):
                if i < len(INFO_V1_ORDER):
                    field_key = INFO_V1_ORDER[i]
                    field_name = field_mapping[field_key]
                    info_dict[field_name] = value
        else:
            st.error("Invalid data format for v=1. Expected array.")
            st.stop()
    else:
        # v=2或无v: 解密为对象，走原解析
        info_dict = decrypted_data

    # 显示信息
    if lang == "Arabic":
        html = '<div dir="rtl" style="text-align: right; font-size: 1.1em; line-height: 2;">'
        for k, v in info_dict.items():
            html += f"<b>{k}:</b> {v}<br>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        for k, v in info_dict.items():
            st.write(f"**{k}**: {v}")

except Exception as e:
    st.error("Failed to decrypt the QR code data. It may be corrupted or invalid.")
    st.exception(e)

st.markdown("---")

# 底部提醒
if lang == "Arabic":
    st.markdown(f"""
    <div dir="rtl" style="text-align: right;">
        <small>{strings.get("footer_note", "If the information above is incorrect, please contact the service provider.")}</small>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info(strings.get("footer_note", "If the information above is incorrect, please contact the service provider."))
