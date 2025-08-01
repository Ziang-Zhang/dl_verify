import streamlit as st
from translate import translations  # 语言字典

# 获取 URL 参数
params = st.query_params
lang = params.get("lang", ["English"])[0]

st.write("🧪 Raw query params:", params)
st.write(lang)

strings = translations.get(lang, translations["English"])

# 页面配置
st.set_page_config(page_title=strings["page_title"], layout="centered")
st.title(strings["main_title"])
st.markdown(strings["description"])
st.markdown("---")

# 展示 info[...] 字段（遍历所有 info[字段名]）
info_items = [
    (key[5:-1], value[0] if value else "")
    for key, value in params.items()
    if key.startswith("info[") and key.endswith("]")
]

# 按字段名排序后展示（可选）
info_items.sort()

for field, val in info_items:
    st.write(f"**{field}**: {val}")

st.markdown("---")
st.info(strings["footer_note"])
