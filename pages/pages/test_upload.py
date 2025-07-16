import streamlit as st

st.title("업로드 테스트")

uploaded_file = st.file_uploader("FITS 파일 업로드", type=['fits', 'fit'])

if uploaded_file:
    st.write(f"업로드 파일명: {uploaded_file.name}")
else:
    st.info("파일을 업로드 해주세요.")
