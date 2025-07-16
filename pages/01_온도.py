import streamlit as st

st.title("나의 첫 Streamlit 앱")

st.header("Streamlit에 오신 것을 환영합니다!")

st.write("이것은 간단한 텍스트입니다.")

st.success("성공적으로 앱이 실행되었습니다! 🎉")
import streamlit as st
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

st.title("FITS 이미지 → RGB 추출 및 온도 계산 앱")

uploaded_file = st.file_uploader("FITS 파일 업로드", type=['fits', 'fit'])
if uploaded_file:
    with fits.open(uploaded_file) as hdul:
        data = hdul[0].data
        header = hdul[0].header

    # 데이터가 3차원일 때 RGB 혹은 3 밴드로 가정
    if data.ndim == 3 and data.shape[0] >= 3:
        # 보통 (밴드, 높이, 너비) 형태
        r_band = data[0]
        g_band = data[1]
        b_band = data[2]
    else:
        st.error("3 밴드 이상 데이터가 필요합니다 (3차원 배열).")
        st.stop()

    # 각 밴드 정규화 (0~1)
    def normalize(arr):
        arr = np.nan_to_num(arr)
        arr = arr - np.min(arr)
        if np.max(arr) > 0:
            arr = arr / np.max(arr)
        return arr

    r_norm = normalize(r_band)
    g_norm = normalize(g_band)
    b_norm = normalize(b_band)

    # RGB 합성 이미지 만들기
    rgb_img = np.dstack([r_norm, g_norm, b_norm])
    st.image(rgb_img, caption="RGB 합성 이미지", use_column_width=True)

    # 스펙트럼 플롯 (밴드별 평균 밝기)
    r_mean = np.mean(r_band)
    g_mean = np.mean(g_band)
    b_mean = np.mean(b_band)

    wavelengths = [620, 530, 460]  # 예: R, G, B 대략 파장 (nm)
    intensities = [r_mean, g_mean, b_mean]

    fig, ax = plt.subplots()
    ax.plot(wavelengths, intensities, 'o-', color='purple')
    ax.set_xlabel("파장 (nm)")
    ax.set_ylabel("평균 밝기")
    ax.set_title("스펙트럼 플롯")
    st.pyplot(fig)

    # 간단 온도 추정 (흑체 온도 근사, 단순 비례식)
    # ※ 실제 온도 계산은 복잡하며 이 예시는 참고용입니다
    temperature = 5000 * (intensities[0] / max(intensities))  # 임의 공식
    st.metric("추정 온도 (단순 계산)", f"{temperature:.1f} K")

else:
    st.info("FITS 파일을 업로드해주세요.")
