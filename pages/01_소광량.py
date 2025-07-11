import streamlit as st

st.title("나의 첫 Streamlit 앱")

st.header("Streamlit에 오신 것을 환영합니다!")

st.write("이것은 간단한 텍스트입니다.")

st.success("성공적으로 앱이 실행되었습니다! 🎉")
import streamlit as st
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from datetime import datetime
import math

st.title("🌤️ 대기 소광 보정 앱")

uploaded_file = st.file_uploader("FITS 이미지 업로드", type=['fits'])

# 위치 및 시간 입력
lat = st.number_input("관측지 위도(°)", value=37.5665)
lon = st.number_input("관측지 경도(°)", value=126.9780)
obs_time = st.text_input("관측 시각 (UTC, 예: 2025-07-10 12:00:00)", value=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

if uploaded_file:
    try:
        # FITS 열기
        with fits.open(uploaded_file) as hdul:
            data = np.nan_to_num(hdul[0].data)
            header = hdul[0].header

        # 천체 좌표 읽기 (RA, DEC)
        if 'RA' in header and 'DEC' in header:
            ra = header['RA']
            dec = header['DEC']

            # 관측 시간, 위치 설정
            location = EarthLocation(lat=lat, lon=lon)
            time = Time(obs_time)

            # 천체 고도 계산
            sky_coord = SkyCoord(ra=ra, dec=dec, unit=('hourangle', 'deg'))
            altaz = sky_coord.transform_to(AltAz(obstime=time, location=location))
            altitude = altaz.alt.degree

            # air mass 근사 계산
            if altitude > 0:
                air_mass = 1 / np.sin(np.radians(altitude))
            else:
                air_mass = float('inf')  # 지평선 아래는 무한대

            # 대기 소광량 (mag), 보통 k=0.2 ~ 0.3 mag/airmass 가 보통
            k = 0.25  # 대기 투과 계수 (임의 값)
            extinction = k * air_mass

            # 이미지 평균 밝기와 보정
            mean_brightness = np.mean(data)
            corrected_brightness = mean_brightness * 10**(0.4 * extinction)

            st.metric("관측 천체 고도 (°)", f"{altitude:.2f}")
            st.metric("대기 광경로 (Air Mass)", f"{air_mass:.2f}")
            st.metric("대기 소광량 (mag)", f"{extinction:.2f}")
            st.metric("평균 밝기 (관측값)", f"{mean_brightness:.2f}")
            st.metric("평균 밝기 (대기 보정 후)", f"{corrected_brightness:.2f}")

        else:
            st.warning("FITS 헤더에 RA, DEC 정보가 없습니다.")

    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("FITS 파일을 업로드하세요.")
uploaded_file = st.file_uploader(
    "FITS 또는 압축 FITS 파일 업로드",
    type=['fits', 'fit', 'fz']
)
from astropy.io import fits

# .fz 압축 FITS 파일 경로
input_fz = '파일경로/filename.fz'

# 변환할 .fits 파일 경로
output_fits = '파일경로/filename.fits'

# 압축 해제 후 저장
with fits.open(input_fz) as hdul:
    hdul.writeto(output_fits, overwrite=True)
