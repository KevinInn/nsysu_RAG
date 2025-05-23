import streamlit as st
from backend import get_answer

st.set_page_config(page_title="學校RAG系統")
st.title("📘 學校問答系統（RAG Demo）")

question = st.text_input("請輸入你的問題：")

if st.button("送出") and question:
    with st.spinner("正在查找答案中..."):
        answer = get_answer(question)
        st.success("回答完成")
        st.markdown(f"**回答：** {answer}")
