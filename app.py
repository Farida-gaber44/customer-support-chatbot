import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ShopBot", page_icon="🛍️", layout="centered")

GEMINI_API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

STORE_CONTEXT = """You are ShopBot for TechStore. Be detailed and helpful.
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
            full_prompt = f"{STORE_CONTEXT}\n\nCustomer: {prompt}\nShopBot:"
            response = model.generate_content(full_prompt)
            reply = response.text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("---")
st.caption("Powered by Gemini AI | TechStore")