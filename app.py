import streamlit as st
from google import genai

st.set_page_config(page_title="ShopBot", page_icon="🛍️", layout="centered")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

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
            full_prompt = f"{STORE_CONTEXT}\n\nCustomer: {prompt}\nShopBot:"
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt
            )
            reply = response.text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("---")
st.caption("Powered by Gemini AI | TechStore")
