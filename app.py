import streamlit as st
from verification_translations import translations

# 获取 URL 参数
params = st.query_params
lang = params.get("lang", ["English"])[0]
strings = translations.get(lang, translations["English"])

# 页面配置
st.set_page_config(page_title=strings["page_title"], layout="centered")
st.title(strings["main_title"])

# 页面描述
st.markdown(strings["description"])
st.markdown("---")

# 展示 info[...] 的内容
for key, value in params.items():
    if key.startswith("info[") and key.endswith("]"):
        clean_key = key[5:-1]  # 去掉 info[ 和 ]
        st.write(f"**{clean_key}**: {value[0]}")

st.markdown("---")
st.info(strings["footer_note"])
