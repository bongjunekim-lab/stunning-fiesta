import streamlit as st

# 1. 공학적 핵심 로직 설명 (웹 화면용)
def show_logic_description():
    st.sidebar.markdown("### 📑 공학적 핵심 로직")
    st.sidebar.info("""
    - **저항 지수 ($R \propto L/d^2$):** 입자 크기의 제곱에 반비례하고 층 두께에 비례하는 물리 법칙 반영.
    - **순차 배출 안정성:** 앞면($125\mu m$) 저항이 뒷면($85\mu m$)보다 낮아 '이온 정류 효과' 발생.
    - **두께 제곱 이론 ($t \propto L^2$):** 전극이 두꺼워질수록 이온 확산 시간이 제곱으로 늘어나는 물리적 특성 반영.
    """)

def calculate_electrode_design(total_thickness_mm):
    p_front, p_mid, p_back = 125, 50, 85
    modes = {
        '1. 초고속형 (High-Speed)': 0.20,
        '2. 표준형 (Balanced)': 0.333,
        '3. 용량형 (High-Capacity)': 0.40
    }

    st.subheader(f"📊 설계 분석 결과 (전체 두께: {total_thickness_mm}mm)")
    
    for mode_name, mid_ratio in modes.items():
        # [두께 배분 최적화 로직]
        side_ratio = (1.0 - mid_ratio) / 2
        t_f = total_thickness_mm * side_ratio
        t_m = total_thickness_mm * mid_ratio
        t_b = total_thickness_mm * side_ratio

        # [공학적 저항 및 성능 지표 계산]
        res_f = t_f / (p_front**2) * 1000000 
        res_m = t_m / (p_mid**2) * 1000000
        res_b = t_b / (p_back**2) * 1000000
        total_res = res_f + res_m + res_b
        
        # 순차 배출 안정성 지수 (Bottleneck Safety)
        bottleneck_safety = (res_b / res_f)
        # 이온 확산 시간의 제곱 법칙 반영
        discharge_time = 0.5 * (total_res / 100) * (total_thickness_mm**2)
        # 세슘 포집 용량 예측
        capacity_unit = mid_ratio * total_thickness_mm * 150

        with st.expander(mode_name):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**[층별 두께 구성]**")
                st.write(f"앞면 ({p_front}μm): {t_f:.3f} mm")
                st.write(f"중간 ({p_mid}μm): {t_m:.3f} mm")
                st.write(f"뒷면 ({p_back}μm): {t_b:.3f} mm")
            with col2:
                st.markdown("**[공학 성능 지표]**")
                st.write(f"순차 배출 안정성: {bottleneck_safety:.2f}")
                st.write(f"예상 포집량: {capacity_unit:.1f} mg")
                st.write(f"예상 배출시간: {discharge_time:.2f} 시간")
                
            if 0.4 <= discharge_time <= 1.0:
                st.success("✅ 최적 설계 범위 (초고속 배출 가능)")
            elif discharge_time < 0.4:
                st.info("⚡ 배출 속도가 매우 빠르나 포집량이 적을 수 있음")
            else:
                st.warning("⚠️ 병목 위험: 두께를 줄이거나 중간층 비율 조정 권장")

# --- UI 레이아웃 ---
st.set_page_config(page_title="Electrode Lab", layout="wide")
st.title("⚡ 비대칭 소결 전극 설계 시뮬레이터")
st.markdown("---")

show_logic_description()

thickness = st.number_input("설계할 전극의 전체 두께(mm)를 입력하세요:", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

if st.button("설계 시뮬레이션 시작"):
    calculate_electrode_design(thickness)