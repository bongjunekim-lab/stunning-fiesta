import streamlit as st

# 1. 공학적 핵심 로직 설명 (웹 화면용 사이드바)
def show_logic_description():
    st.sidebar.markdown("### 📑 공학적 핵심 로직")
    st.sidebar.info("""
    - **저항 지수 ($R \propto L/d^2$):** 입자 크기의 제곱에 반비례하고 층 두께에 비례하는 물리 법칙 반영.
    - **순차 배출 안정성:** 앞면($125\mu m$) 저항이 뒷면($85\mu m$)보다 낮아 '이온 정류 효과' 발생.
    - **두께 제곱 이론 ($t \propto L^2$):** 전극이 두꺼워질수록 이온 확산 시간이 제곱으로 늘어나는 물리적 특성 반영.
    """)

def calculate_electrode_design(total_thickness_mm):
    # 입자 크기 고정 (사용자 고유 설계값)
    p_front, p_mid, p_back = 125, 50, 85
    
    # 배치 모드 정의 (중간층 비중)
    modes = {
        '1. 초고속형 (High-Speed)': 0.20,
        '2. 표준형 (Balanced)': 0.333,
        '3. 용량형 (High-Capacity)': 0.40
    }

    st.subheader(f"📊 설계 분석 결과 (전체 두께: {total_thickness_mm:.2f} mm)")
    
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

        # 결과 출력 (확장 칸)
        with st.expander(mode_name, expanded=True if mode_name.startswith('1') else False):
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
                st.write(f"예상 배출시간: **{discharge_time:.2f} 시간**")
                
            # 성능에 따른 상태 메시지
            if discharge_time <= 1.0:
                st.success("✅ 최적 설계 범위 (초고속 배출 가능)")
            elif 1.0 < discharge_time <= 3.0:
                st.info("🟡 보통 수준: 두께 증가로 인해 배출 속도가 다소 느림")
            else:
                st.warning("⚠️ 병목 위험: 두께를 줄이거나 중간층 비율 조정을 강력히 권장")

# --- UI 레이아웃 설정 ---
st.set_page_config(page_title="Electrode Lab Simulator", layout="wide")
st.title("⚡ 비대칭 소결 전극 설계 시뮬레이터")
st.write("알갱이 크기 조합: $125\mu m$(앞) - $50\mu m$(중간) - $85\mu m$(뒤)")
st.markdown("---")

# 사이드바에 공학 설명 표시
show_logic_description()

# 두께 조절 UI (숫자 입력과 슬라이더 연동)
st.write("### 📏 전극 두께 설정")
col_input1, col_input2 = st.columns([1, 2])

with col_input1:
    # 1. 숫자 직접 입력 방식
    input_thickness = st.number_input("두께 입력 (mm):", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

with col_input2:
    # 2. 슬라이더 조절 방식 (입력창과 연동됨)
    slider_thickness = st.slider("슬라이더로 조절하기:", min_value=0.1, max_value=10.0, value=float(input_thickness), step=0.1)

# 최종 두께 결정 (슬라이더나 입력창 중 마지막으로 변경된 값 사용)
final_thickness = slider_thickness if slider_thickness != input_thickness else input_thickness

# 시뮬레이션 버튼 (혹은 슬라이더 변경 시 즉시 실행)
if st.button("설계 시뮬레이션 시작") or final_thickness != 1.0:
    calculate_electrode_design(final_thickness)