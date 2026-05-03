import streamlit as st

# 1. 공학적 핵심 로직 설명 (웹 화면용 사이드바)
def show_logic_description():
    st.sidebar.markdown("### 📑 공학적 핵심 로직")
    st.sidebar.info("""
    - **저항 지수 ($R \propto L/d^2$):** 입자 크기의 제곱에 반비례하고 층 두께에 비례하는 물리 법칙 반영.
    - **순차 배출 안정성:** 앞면($125\mu m$) 저항이 뒷면($85\mu m$)보다 낮아 '이온 정류 효과' 발생.
    - **두께 제곱 이론 ($t \propto L^2$):** 전극이 두꺼워질수록 이온 확산 시간이 제곱으로 늘어나는 물리적 특성 반영.
    """)

# 2. 지표별 게이지 색상 및 비율 산출 함수
def get_gauge_info(value, min_val, max_val, reverse=False):
    percent = (value - min_val) / (max_val - min_val)
    percent = max(0, min(1.0, percent))
    score = 1.0 - percent if reverse else percent
        
    if score >= 0.8: color = "#008000"  # 최적 (초록)
    elif score >= 0.6: color = "#32CD32" # 양호 (연두)
    elif score >= 0.4: color = "#FFD700" # 보통 (노랑)
    elif score >= 0.2: color = "#FF8C00" # 주의 (주황)
    else: color = "#FF0000" # 위험 (빨강)
    
    return color, percent

def calculate_electrode_design(total_thickness_mm):
    p_front, p_mid, p_back = 125, 50, 85
    modes = {
        '1. 초고속형 (High-Speed)': 0.20,
        '2. 표준형 (Balanced)': 0.333,
        '3. 용량형 (High-Capacity)': 0.40
    }

    st.subheader(f"📊 설계 분석 결과 (전체 두께: {total_thickness_mm:.2f} mm)")
    
    for mode_name, mid_ratio in modes.items():
        side_ratio = (1.0 - mid_ratio) / 2
        t_f, t_m, t_b = total_thickness_mm * side_ratio, total_thickness_mm * mid_ratio, total_thickness_mm * side_ratio

        res_f = t_f / (p_front**2) * 1000000 
        res_m = t_m / (p_mid**2) * 1000000
        res_b = t_b / (p_back**2) * 1000000
        total_res = res_f + res_m + res_b
        
        bottleneck_safety = (res_b / res_f)
        discharge_time = 0.5 * (total_res / 100) * (total_thickness_mm**2)
        capacity_unit = mid_ratio * total_thickness_mm * 150

        with st.expander(mode_name, expanded=True):
            # 상단 구역: 두께 구성 및 종합 판정
            col1, col2 = st.columns(2)
            with col1:
                st.write("**[층별 두께 구성]**")
                st.write(f"앞면 ({p_front}μm): {t_f:.3f} mm")
                st.write(f"중간 ({p_mid}μm): {t_m:.3f} mm")
                st.write(f"뒷면 ({p_back}μm): {t_b:.3f} mm")
            with col2:
                st.write("**[종합 판정]**")
                if discharge_time <= 1.0:
                    st.success("✅ 초고속 배출 최적 설계")
                elif discharge_time <= 3.0:
                    st.info("🟡 보통 수준: 배출 속도 다소 지연")
                else:
                    st.warning("⚠️ 병목 위험: 설계 조정 권장")

            st.markdown("---")
            
            # 하단 구역: 공학 성능 지표 분석 (요청하신 대로 이동됨)
            st.markdown("#### [공학 성능 지표 분석]")
            
            # 1. 순차 배출 안정성 바
            s_color, s_per = get_gauge_info(bottleneck_safety, 0.5, 3.0)
            st.markdown(f"**순차 배출 안정성: <span style='color:{s_color};'>{bottleneck_safety:.2f}</span>**", unsafe_allow_html=True)
            st.progress(s_per)
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

            # 2. 예상 포집량 바
            c_color, c_per = get_gauge_info(capacity_unit, 0, 300)
            st.markdown(f"**예상 포집량: <span style='color:{c_color};'>{capacity_unit:.1f} mg</span>**", unsafe_allow_html=True)
            st.progress(c_per)
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

            # 3. 예상 배출 시간 바
            t_color, t_per = get_gauge_info(discharge_time, 0.1, 5.0, reverse=True)
            st.markdown(f"**예상 배출 시간: <span style='color:{t_color};'>{discharge_time:.2f} 시간</span>**", unsafe_allow_html=True)
            st.progress(t_per)

# --- 메인 레이아웃 ---
st.set_page_config(page_title="Electrode Design Lab", layout="wide")
st.title("⚡ 비대칭 소결 전극 설계 시뮬레이터")
st.write("알갱이 크기 조합: $125\mu m$ - $50\mu m$ - $85\mu m$")
st.markdown("---")

show_logic_description()

st.write("### 📏 전극 두께 설정")
c1, c2 = st.columns([1, 2])
with c1:
    input_val = st.number_input("두께 직접 입력 (mm):", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
with c2:
    slider_val = st.slider("슬라이더로 두께 조절:", min_value=0.1, max_value=5.0, value=float(input_val), step=0.1)

final_thickness = slider_val if slider_val != input_val else input_val

calculate_electrode_design(final_thickness)