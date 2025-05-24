import streamlit as st
from backend import get_answer

st.set_page_config(page_title="中山大學萬事通", page_icon="📘", layout="centered")

# Apply custom color theme and button layout
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: 'Helvetica Neue', sans-serif;
        background-color: #F8F8E1;
    }
    .stTextInput > div > div > input {
        font-size: 1.2rem;
        padding: 0.85rem;
        border-radius: 12px;
        border: 2px solid #8ACCD5;
        transition: all 0.3s ease-in-out;
        background-color: #fff;
        color: #222;
    }
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 10px #8ACCD5aa;
        border-color: #8ACCD5;
    }
    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FF90BB, #FFC1DA);
        color: white;
        padding: 1rem 3rem;
        font-size: 1.3rem;
        border: none;
        border-radius: 14px;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(0,0,0,0.2);
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFC1DA, #FF90BB);
        transform: scale(1.06);
    }
    .answer-box {
        padding: 1.2rem;
        background: #fff;
        border-left: 6px solid #FF90BB;
        border-radius: 10px;
        font-size: 1.15rem;
        line-height: 1.6;
        color: #212529;
        margin-top: 1.5rem;
    }
    .description {
        font-size: 1.1rem;
        color: #444;
        margin-bottom: 2rem;
        text-align: center;
    }
    </style>
    <div class="main">
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #222;'>📘 中山大學萬事通</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>即時為你解答所有關於中山大學的大小事！</p>", unsafe_allow_html=True)

question = st.text_input("輸入問題：", placeholder="例如：中山的資管系在哪棟樓？")

if st.button("送出") and question:
    with st.spinner("正在查找答案中..."):
        answer = get_answer(question)
        st.success("回答完成")
        st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)

st.markdown("""</div>""", unsafe_allow_html=True)
