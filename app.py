import streamlit as st
from groq import Groq

st.set_page_config(page_title="ShopBot", page_icon="🛍️", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

STORE_CONTEXT = """You are ShopBot for TechStore. Be helpful and brief.
Products: laptops($499+), phones($299+), tablets($199+), headphones($49+).
Shipping: free above $50, 3-5 days. Returns: 14 days. Email: support@techstore.com"""

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🛍️ ShopBot — Customer Support")
st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": STORE_CONTEXT},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("---")
st.caption("Powered by Groq & LLaMA3 | TechStore")
