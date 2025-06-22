import streamlit as st

st.write("Hello world")

if not st.user.is_logged_in:
    if st.button("Log in with Google"):
        st.login()
    st.stop()

if st.button("Log out"):
    st.logout()


st.markdown(f"Welcome! {st.user.name}")
st.write(st.user)
st.write(st.secrets.get('auth').get('cookie_secret'))

