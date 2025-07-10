import streamlit as st

st.title("나의 첫 Streamlit 앱")

st.header("Streamlit에 오신 것을 환영합니다!")

st.write("이것은 간단한 텍스트입니다.")

st.success("성공적으로 앱이 실행되었습니다! 🎉")
import streamlit as st
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

st.title("🌟 성단 색지수 분석으로 소광 추정하기")

st.write("""
성단의 B, V 필터 FITS 이미지를 업로드하면,  
별들의 색지수(B–V)를 계산하여 소광(빛 흡수 및 산란)을 추정합니다.
""")

uploaded_b = st.file_uploader("🔵 B 필터 FITS 파일 업로드", type=['fits'])
uploaded_v = st.file_uploader("🟡 V 필터 FITS 파일 업로드", type=['fits'])

def extract_star_brightness(data, threshold=1000):
    # 단순 임계값으로 별 영역 픽셀 선택
    stars = data > threshold
    return data[stars]

if uploaded_b and uploaded_v:
    try:
        with fits.open(uploaded_b) as b_hdul, fits.open(uploaded_v) as v_hdul:
            b_data = np.nan_to_num(b_hdul[0].data)
            v_data = np.nan_to_num(v_hdul[0].data)

            # 밝기 추출 (임계값 초과하는 픽셀만)
            b_stars = extract_star_brightness(b_data)
            v_stars = extract_star_brightness(v_data)

            # 별 수 맞추기 위해 작은 쪽 크기에 맞춤
            n = min(len(b_stars), len(v_stars))
            b_stars = b_stars[:n]
            v_stars = v_stars[:n]

            # 색지수 배열 계산
            color_index = b_stars - v_stars

            # 소광 추정을 위해 기준 내재 색지수 예시 (0.0 이상 ~ 0.5 이하)
            intrinsic_bv = 0.3

            # 소광량 A_v = 3.1 * E(B–V), 여기서 E(B–V) = 관측색지수 - 내재색지수
            E_bv = np.mean(color_index) - intrinsic_bv
            A_v = 3.1 * E_bv

            st.success("✅ 소광 계산 완료!")
            st.metric("평균 관측 B–V 색지수", f"{np.mean(color_index):.2f}")
            st.metric("추정 소광량 A_v (mag)", f"{A_v:.2f}")

            # 색지수 히스토그램
            fig, ax = plt.subplots()
            ax.hist(color_index, bins=30, color='purple', alpha=0.7)
            ax.axvline(intrinsic_bv, color='orange', linestyle='--', label='기준 내재색지수')
            ax.set_xlabel("B–V 색지수")
            ax.set_ylabel("별 수")
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"오류 발생: {e}")

else:
    st.info("B, V 필터 FITS 파일을 모두 업로드 해주세요.")
