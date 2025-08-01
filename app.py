import streamlit as st
from translate import translations  # 语言字典

# 获取 URL 参数
params = st.query_params
lang = params.get("lang", "English")
strings = translations.get(lang, translations["English"])

# 页面配置
st.set_page_config(page_title=strings["page_title"], layout="centered")
st.title(strings["main_title"])
st.markdown(strings["description"])
st.markdown("---")

# 展示 info[...] 字段
for key, value in params.items():
    if key.startswith("info[") and key.endswith("]"):
        display_key = key[5:-1]
        # 判断是 list 还是字符串
        if isinstance(value, list):
            display_value = value[0]
        else:
            display_value = value
        st.write(f"**{display_key}**: {display_value}")

st.markdown("---")
st.info(strings["footer_note"])
