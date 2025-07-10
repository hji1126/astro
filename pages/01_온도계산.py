import streamlit as st

st.title("나의 첫 Streamlit 앱")

st.header("Streamlit에 오신 것을 환영합니다!")

st.write("이것은 간단한 텍스트입니다.")

st.success("성공적으로 앱이 실행되었습니다! 🎉")
import streamlit as st
import numpy as np
from astropy.io import fits

st.title("🌡️ 별의 온도 계산기 (B–V 색지수 기반)")
st.header("FITS 이미지에서 색을 추출하여 온도를 계산해보세요.")
st.write("두 개의 필터(B, V)를 사용한 이미지에서 밝기를 분석해 색지수를 계산하고, 그 값으로 별의 표면 온도를 추정합니다.")

# 파일 업로더
uploaded_b = st.file_uploader("🔵 B 필터 FITS 파일을 업로드하세요", type=['fits'])
uploaded_v = st.file_uploader("🟡 V 필터 FITS 파일을 업로드하세요", type=['fits'])

# 두 파일이 모두 업로드되었을 때 실행
if uploaded_b and uploaded_v:
    try:
        with fits.open(uploaded_b) as b_hdul, fits.open(uploaded_v) as v_hdul:
            b_data = np.nan_to_num(b_hdul[0].data)
            v_data = np.nan_to_num(v_hdul[0].data)

            mean_b = np.mean(b_data)
            mean_v = np.mean(v_data)

            color_index = mean_b - mean_v

            # Ballesteros 공식으로 온도 추정
            T = 4600 * ((1 / (0.92 * color_index + 1.7)) + (1 / (0.92 * color_index + 0.62)))

            st.success("✅ 색지수 계산 완료!")
            st.metric("B–V 색지수", f"{color_index:.2f}")
            st.metric("표면 온도", f"{T:.0f} K")

            # 분광형 분류
            if T > 10000:
                spec = "O형 또는 B형"
            elif T > 7500:
                spec = "A형"
            elif T > 6000:
                spec = "F형"
            elif T > 5200:
                spec = "G형 (태양형)"
            elif T > 3700:
                spec = "K형"
            else:
                spec = "M형 (붉은 별)"

            st.info(f"📌 분광형 추정: **{spec}**")

    except Exception as e:
        st.error("⚠️ FITS 파일 처리 중 오류 발생")
        st.text(str(e))

else:
    st.info("두 개의 FITS 파일(B/V 필터용)을 업로드하면 온도를 계산할 수 있습니다.")
