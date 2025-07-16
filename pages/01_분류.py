import streamlit as st

st.title("나의 첫 Streamlit 앱")

st.header("Streamlit에 오신 것을 환영합니다!")

st.write("이것은 간단한 텍스트입니다.")

st.success("성공적으로 앱이 실행되었습니다! 🎉")
import streamlit as st
from astropy.io import fits
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops

st.title("나선/타원/불규칙 은하 분류 앱")

uploaded_file = st.file_uploader("FITS 파일 업로드", type=['fits', 'fit'])

if uploaded_file is not None:
    # FITS 파일 읽기
    hdul = fits.open(uploaded_file)
    data = hdul[0].data
    
    # 이미지 정규화
    img = np.nan_to_num(data)
    img = img - np.min(img)
    img = img / np.max(img)
    img = (img * 255).astype(np.uint8)
    
    # 이미지 출력
    st.image(img, caption="은하 이미지", use_column_width=True)
    
    # 이진화 및 영역 탐색
    binary = img > threshold_otsu(img)
    label_img = label(binary)
    regions = regionprops(label_img)
    
    if len(regions) == 0:
        st.write("은하가 감지되지 않았습니다.")
    else:
        # 가장 큰 영역 선택
        largest_region = max(regions, key=lambda r: r.area)
        
        eccentricity = largest_region.eccentricity
        area = largest_region.area
        
        st.write(f"영역 면적: {area}")
        st.write(f"타원도 (eccentricity): {eccentricity:.3f}")
        
        # 분류 (임시 기준)
        if eccentricity < 0.5:
            st.success("분류 결과: 타원 은하")
        elif eccentricity < 0.85:
            st.success("분류 결과: 나선 은하 가능성 높음")
        else:
            st.success("분류 결과: 불규칙 은하 가능성")
else:
    st.info("분류를 위해 FITS 파일을 업로드해주세요.")
