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

st.title("🌌 우주망원경 vs 지상망원경 대기 소광계수 추정 앱")

# 파일 업로드
space_file = st.file_uploader("우주망원경 FITS 파일 업로드 (대기 소광 없음)", type=['fits', 'fit', 'fz'])
ground_file = st.file_uploader("지상망원경 FITS 파일 업로드 (예: U 필터)", type=['fits', 'fit', 'fz'])

# 관측 위치, 시간 입력
lat = st.number_input("관측지 위도 (°)", value=37.5665)
lon = st.number_input("관측지 경도 (°)", value=126.9780)
obs_time = st.text_input("관측 시각 (UTC, 예: 2025-07-10 12:00:00)", value=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

def mean_brightness(data, threshold=1000):
    """단순 임계값 기반 밝기 추출"""
    stars = data > threshold
    if np.any(stars):
        return np.mean(data[stars])
    else:
        return np.mean(data)

if space_file and ground_file:
    try:
        # FITS 데이터 읽기
        with fits.open(space_file) as hdul_s, fits.open(ground_file) as hdul_g:
            data_s = np.nan_to_num(hdul_s[0].data)
            data_g = np.nan_to_num(hdul_g[0].data)
            header = hdul_g[0].header

        # 밝기 계산
        brightness_space = mean_brightness(data_s)
        brightness_ground = mean_brightness(data_g)

        # 천체 좌표 읽기 (우선 지상 관측 헤더에서)
        if 'RA' in header and 'DEC' in header:
            ra = header['RA']
            dec = header['DEC']
            location = EarthLocation(lat=lat, lon=lon)
            time = Time(obs_time)
            sky_coord = SkyCoord(ra=ra, dec=dec, unit=('hourangle', 'deg'))
            altaz = sky_coord.transform_to(AltAz(obstime=time, location=location))
            altitude = altaz.alt.degree

            # air mass 계산
            if altitude > 0:
                air_mass = 1 / np.sin(np.radians(altitude))
            else:
                air_mass = float('inf')

            # 소광량 (mag) = -2.5 * log10(밝기 비율)
            extinction_mag = -2.5 * np.log10(brightness_ground / brightness_space)

            # 대기 소광계수 k = extinction_mag / air_mass
            if air_mass == float('inf'):
                k = None
                st.warning("천체가 지평선 아래에 있어 소광계수 계산 불가")
            else:
                k = extinction_mag / air_mass

            # 결과 출력
            st.metric("관측 천체 고도 (°)", f"{altitude:.2f}")
            st.metric("대기 광경로 (Air Mass)", f"{air_mass:.2f}")
            st.metric("대기 소광량 (mag)", f"{extinction_mag:.2f}")
            if k is not None:
                st.metric("대기 소광계수 k (mag/airmass)", f"{k:.3f}")

            # 추가 시각화 가능 (밝기 비교 등)
            st.write(f"우주망원경 평균 밝기: {brightness_space:.2f}")
            st.write(f"지상망원경 평균 밝기: {brightness_ground:.2f}")

        else:
            st.warning("FITS 헤더에 RA, DEC 정보가 없습니다.")

    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("우주망원경 및 지상망원경 FITS 파일을 모두 업로드하세요.")
