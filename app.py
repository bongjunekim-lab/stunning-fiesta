import streamlit as st

# 1. 공학적 핵심 로직 설명 (무게 추정 원칙 추가)
def show_logic_description():
    st.sidebar.markdown("### 📑 공학적 핵심 로직")
    st.sidebar.info("""
    - **저항 지수 ($R \propto L/d^2$):** 입자 크기 제곱 반비례 및 층 두께 비례 법칙.
    - **순차 배출 안정성:** 앞면($125\mu m$) 저항이 뒷면($85\mu m$)보다 낮아 '이온 정류 효과' 발생.
    - **두께 제곱 이론 ($t \propto L^2$):** 전극 두께 증가 시 이온 확산 시간 제곱 비례 증가.
    - **무게 추정 원칙:** 
        1. 기준 면적 $30 \times 30 \text{cm}$ ($900\text{cm}^2$) 적용.
        2. 소재 평균 밀도 $2.0\text{g/cm}^3$, 충진율 $60\%$ 가정.
        3. 소결 전 '그린 바디' 기준 무게이며 소결 후 약 $5\sim 10\%$ 감소 가능.
    """)

def calculate_electrode_design(total_thickness_mm):
    p_front, p_mid, p_back = 125, 50, 85
    modes = {
        '1. 초고속형 (High-Speed)': 0.20,
        '2. 표준형 (Balanced)': 0.333,
        '3. 용량형 (High-Capacity)': 0.40
    }

    # 30x30cm 면적 (cm2)
    area_cm2 = 30 * 30 
    density = 2.0 # g/cm3
    filling_rate = 0.6 # 60%

    st.subheader(f"📊 설계 분석 결과 (전체 두께: {total_thickness_mm:.2f} mm)")
    
    for mode_name, mid_ratio in modes.items():
        side_ratio = (1.0 - mid_ratio) / 2
        t_f, t_m, t_b = total_thickness_mm * side_ratio, total_thickness_mm * mid_ratio, total_thickness_mm * side_ratio

        # 층별 추정 무게 계산 (g) = 면적(cm2) * 두께(cm) * 밀도(g/cm3) * 충진율
        w_f = area_cm2 * (t_f / 10) * density * filling_rate
        w_m = area_cm2 * (t_m / 10) * density * filling_rate
        w_b = area_cm2 * (t_b / 10) * density * filling_rate

        res_f = t_f / (p_front**2) * 1000000 
        res_m = t_m / (p_mid**2) * 1000000
        res_b = t_b / (p_back**2) * 1000000
        total_res = res_f + res_m + res_b
        
        bottleneck_safety = (res_b / res_f)
        discharge_time = 0.5 * (total_res / 100) * (total_thickness_mm**2)
        capacity_unit = mid_ratio * total_thickness_mm * 150
        collection_time = 1.2 * (total_res / 150) * total_thickness_mm

        st.markdown(f"<h2 style='font-size: 28px; color: #1f77b4; margin-bottom: -10px;'>{mode_name}</h2>", unsafe_allow_html=True)
        
        with st.expander("세부 분석 보기", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**[층별 두께 및 추정 무게]**")
                st.write(f"앞면 ({p_front}μm): {t_f:.3f} mm → **{w_f:.1f} g**")
                st.write(f"중간 ({p_mid}μm): {t_m:.3f} mm → **{w_m:.1f} g**")
                st.write(f"뒷면 ({p_back}μm): {t_b:.3f} mm → **{w_b:.1f} g**")
                st.caption("*(30x30cm 면적, 60% 충진율 기준 무게)*")
            with col2:
                st.write("**[종합 판정]**")
                if discharge_time <= 1.0:
                    st.success("✅ 초고속 배출 최적 설계")
                    s_per = 1.0
                elif discharge_time <= 3.0:
                    st.info("🟡 보통 수준: 배출 속도 다소 지연")
                    s_per = 0.6
                else:
                    st.warning("⚠️ 병목 위험: 설계 조정 권장")
                    s_per = 0.3
                st.progress(s_per)

            st.markdown("---")
            st.markdown("<h5 style='font-size: 16px; color: #555;'>[공학 성능 지표 분석]</h5>", unsafe_allow_html=True)
            
            s_color, s_per = get_gauge_info(bottleneck_safety, 0.5, 3.0)
            st.markdown(f"순차 배출 안정성: <b style='color:{s_color};'>{bottleneck_safety:.2f}</b> / <b style='color:#0000FF;'>포집 시간: {collection_time:.2f} 시간</b>", unsafe_allow_html=True)
            st.progress(s_per)

            c_color, c_per = get_gauge_info(capacity_unit, 0, 300)
            st.markdown(f"예상 포집량: <b style='color:{c_color};'>{capacity_unit:.1f} mg</b>", unsafe_allow_html=True)
            st.progress(c_per)

            t_color, t_per = get_gauge_info(discharge_time, 0.1, 5.0, reverse=True)
            st.markdown(f"예상 배출 시간: <b style='color:{t_color};'>{discharge_time:.2f} 시간</b>", unsafe_allow_html=True)
            st.progress(t_per)

# --- 이하 메인 레이아웃 및 헬퍼 함수 생략 (기존 get_gauge_info 포함) ---
def get_gauge_info(value, min_val, max_val, reverse=False):
    percent = (value - min_val) / (max_val - min_val)
    percent = max(0, min(1.0, percent))
    score = 1.0 - percent if reverse else percent
    if score >= 0.8: color = "#008000"
    elif score >= 0.6: color = "#32CD32"
    elif score >= 0.4: color = "#FFD700"
    elif score >= 0.2: color = "#FF8C00"
    else: color = "#FF0000"
    return color, percent

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