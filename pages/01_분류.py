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
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops

st.title("나선/타원/불규칙 은하 분류 앱")

uploaded_file = st.file_uploader("FITS 이미지 업로드", type=['fits', 'fit'])

if uploaded_file is not None:
    # FITS 파일 열기
    hdul = fits.open(uploaded_file)
    data = hdul[0].data
    
    # 데이터 시각화 (이미지 축소 및 정규화)
    img = data
    img = np.nan_to_num(img)  # NaN 제거
    img = img - np.min(img)
    img = img / np.max(img)
    img = (img * 255).astype(np.uint8)
    
    st.image(img, caption="은하 이미지", use_column_width=True)
    
    # 간단한 특징 추출 예: 밝기 중심, 타원도, 면적 등
    binary = img > threshold_otsu(img)  # 이진화
    
    label_img = label(binary)
    regions = regionprops(label_img)
    
    if len(regions) == 0:
        st.write("은하가 감지되지 않았습니다.")
    else:
        # 가장 큰 영역 선택
        largest_region = max(regions, key=lambda r: r.area)
        
        # 특징 출력
        eccentricity = largest_region.eccentricity
        area = largest_region.area
        st.write(f"영역 면적: {area}")
        st.write(f"타원도 (eccentricity): {eccentricity:.3f}")
        
        # 간단한 분류 기준 (임시)
        if eccentricity < 0.5:
            st.success("분류 결과: 타원 은하")
        elif eccentricity >= 0.5 and eccentricity < 0.85:
            st.success("분류 결과: 나선 은하 가능성 높음")
        else:
            st.success("분류 결과: 불규칙 은하 가능성")
import streamlit as st

st.title("은하 분류 페이지")

uploaded_file = st.file_uploader("FITS 파일 업로드 (분류용)", type=['fits', 'fit'])

if uploaded_file is not None:
    st.write(f"{uploaded_file.name} 파일 업로드 완료!")
    # 여기서 이미지 분석 코드 실행
else:
    st.info("파일을 업로드해주세요.")
