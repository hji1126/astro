import streamlit as st

st.title("나의 첫 Streamlit 앱")

st.header("Streamlit에 오신 것을 환영합니다!")

st.write("이것은 간단한 텍스트입니다.")

st.success("성공적으로 앱이 실행되었습니다! 🎉")
import streamlit as st
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

st.title("FITS 기반 은하 분류기")

st.header("🌌 은하 이미지 업로드")
st.write("FITS 형식의 천체 이미지를 업로드하면, 자동으로 은하 종류를 예측합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("FITS 파일을 업로드하세요", type=["fits"])

if uploaded_file is not None:
    st.success("파일이 성공적으로 업로드되었습니다!")

    # FITS 파일 열기
    with fits.open(uploaded_file) as hdul:
        image_data = hdul[0].data  # 가장 첫 번째 HDU에서 데이터 추출

    # 데이터 정규화 및 시각화
    if image_data is not None:
        image_data = np.nan_to_num(image_data)  # NaN 제거
        image_data = np.clip(image_data, np.percentile(image_data, 1), np.percentile(image_data, 99))  # 이상치 제거
        image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))  # 0~1 정규화

        st.subheader("🔭 이미지 미리보기")

        # 이미지 보여주기
        fig, ax = plt.subplots()
        ax.imshow(image_data, cmap='gray')
        ax.axis('off')
        st.pyplot(fig)

        # ✨ 은하 분류 예시 출력 (나중에 모델 연결 가능)
        st.subheader("🔍 예측 결과 (예시)")
        st.write("🌀 예측된 은하 유형: **나선 은하 (Spiral Galaxy)**")
        st.write("📊 확률 분포: 나선 87% | 타원 9% | 불규칙 4%")
