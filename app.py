import streamlit as st

# 1. 공학적 핵심 로직 설명 (웹 화면용 사이드바)
def show_logic_description():
    st.sidebar.markdown("### 📑 공학적 핵심 로직")
    st.sidebar.info("""
    - **저항 지수 ($R \propto L/d^2$):** 입자 크기의 제곱에 반비례하고 층 두께에 비례하는 물리 법칙 반영.
    - **순차 배출 안정성:** 앞면($125\mu m$) 저항이 뒷면($85\mu m$)보다 낮아 '이온 정류 효과' 발생.
    - **두께 제곱 이론 ($t \propto L^2$):** 전극이 두꺼워질수록 이온 확산 시간이 제곱으로 늘어나는 물리적 특성 반영.
    """)

# 2. [추가] 배출 성능(시간) 5단계 판정 함수
def get_perf_info(t):
    if t <= 0.5: return "⭐⭐⭐⭐⭐ [최적] 초고속 배출 구간", "#008000", 100
    elif t <= 1.0: return "⭐⭐⭐⭐ [양호] 안정적 배출 구간", "#32CD32", 80
    elif t <= 2.0: return "⭐⭐⭐ [보통] 배출 속도 저하 시작", "#FFD700", 60
    elif t <= 4.0: return "⭐⭐ [주의] 병목 현상 발생 위험", "#FF8C00", 40
    else: return "⭐ [위험] 배출 불가/극저속 구간", "#FF0000", 20

# 3. [추가] 순차 배출 안정성 5등급 판정 함수
def get_stab_info(s):
    if s >= 2.5: return "S등급 (이상적)", "#008000"
    elif s >= 2.0: return "A등급 (우수)", "#32CD32"
    elif s >= 1.5: return "B등급 (보통)", "#FFD700"
    elif s >= 1.0: return "C등급 (불안정)", "#FF8C00"
    else: return "D등급 (위험/역류)", "#FF0000"

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

        # 등급 정보 가져오기
        perf_text, perf_color, perf_val = get_perf_info(discharge_time)
        stab_text, stab_color = get_stab_info(bottleneck_safety)

        with st.expander(mode_name, expanded=True):
            # 성능 상태 바 출력
            st.markdown(f"<p style='color:{perf_color}; font-weight:bold; margin-bottom:0;'>{perf_text}</p>", unsafe_allow_html=True)
            st.progress(perf_val / 100)

            col1, col2, col3 = st.columns([1, 1, 1.2])
            with col1:
                st.markdown("**[층별 두께 구성]**")
                st.write(f"앞면: {t_f:.3f} mm")
                st.write(f"중간: {t_m:.3f} mm")
                st.write(f"뒷면: {t_b:.3f} mm")
            with col2:
                st.markdown("**[성능 수치]**")
                st.write(f"예상 포집량: {capacity_unit:.1f} mg")
                st.write(f"배출 시간: **{discharge_time:.2f} h**")
            with col3:
                st.markdown("**[순차배출 안정성]**")
                st.markdown(f"<h3 style='color:{stab_color}; margin:0;'>{stab_text}</h3>", unsafe_allow_html=True)
                st.write(f"지수: {bottleneck_safety:.2f}")

# --- UI 레이아웃 설정 ---
st.set_page_config(page_title="Electrode Lab Simulator", layout="wide")
st.title("⚡ 비대칭 소결 전극 설계 시뮬레이터")
st.write("알갱이 크기 조합: $125\mu m$(앞) - $50\mu m$(중간) - $85\mu m$(뒤)")
st.markdown("---")

show_logic_description()

st.write("### 📏 전극 두께 설정")
col_input1, col_input2 = st.columns([1, 2])
with col_input1:
    input_thickness = st.number_input("두께 입력 (mm):", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
with col_input2:
    slider_thickness = st.slider("슬라이더로 조절하기:", min_value=0.1, max_value=10.0, value=float(input_thickness), step=0.1)

final_thickness = slider_thickness if slider_thickness != input_thickness else input_thickness

# 버튼을 누르거나 슬라이더 값이 변경되면 즉시 시뮬레이션 실행
if st.button("설계 시뮬레이션 시작") or final_thickness != 1.0:
    calculate_electrode_design(final_thickness)
