import streamlit as st

# 1. 시간 변환 및 공학 헬퍼 함수
def format_time_kr(total_minutes):
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"

def get_gauge_info(value, min_val, max_val, reverse=False):
    percent = (value - min_val) / (max_val - min_val)
    percent = max(0, min(1.0, percent))
    score = 1.0 - percent if reverse else percent
    color = "#008000" if score >= 0.8 else "#FFD700" if score >= 0.4 else "#FF0000"
    return color, percent

# 2. 분석 출력 공통 함수 (자동 설계 모드와 수동 입력 모드 통합)
def render_analysis_block(title, t_f, t_m, t_b, p_f, p_m, p_b, is_special=False, expanded=False):
    total_t = t_f + t_m + t_b
    area_cm2, density, filling_rate = 900, 2.0, 0.6

    # 무게 계산
    w_f = area_cm2 * (t_f / 10) * density * filling_rate
    w_m = area_cm2 * (t_m / 10) * density * filling_rate
    w_b = area_cm2 * (t_b / 10) * density * filling_rate

    # 저항 및 지표 계산
    res_f = t_f / (p_f**2) * 1000000 
    res_m = t_m / (p_m**2) * 1000000
    res_b = t_b / (p_b**2) * 1000000
    total_res = res_f + res_m + res_b
    
    bottleneck_safety = (res_b / res_f)
    discharge_min = (0.5 * (total_res / 100) * (total_t**2)) * 60
    collection_min = (1.2 * (total_res / 150) * total_t) * 60
    total_cycle_min = discharge_min + collection_min
    capacity_unit = (t_m / total_t) * total_t * 150

    bg_color = "#f8f9fa" if is_special else "transparent"
    
    with st.expander(f"{title}", expanded=expanded):
        st.markdown(f"<div style='background-color:{bg_color}; padding:10px; border-radius:5px;'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**[층별 두께 및 추정 무게]**")
            st.write(f"앞면 ({p_f}μm): {t_f:.3f} mm → {w_f:.1f} g")
            st.write(f"중간 ({p_m}μm): {t_m:.3f} mm → {w_m:.1f} g")
            st.write(f"뒷면 ({p_b}μm): {t_b:.3f} mm → {w_b:.1f} g")
        with col2:
            st.write("**[종합 판정]**")
            if discharge_min <= 65: st.success("✅ 최적 설계 (고속)")
            else: st.info("🟡 보통 수준")
            st.progress(max(0, min(1.0, 60/discharge_min)) if discharge_min > 0 else 0)

        st.markdown("---")
        st.markdown("<h5 style='font-size: 14px; color: #666;'>[공학 성능 지표 분석]</h5>", unsafe_allow_html=True)
        
        s_color, s_per = get_gauge_info(bottleneck_safety, 0.5, 3.0)
        st.markdown(f"순차 배출 안정성: <b style='color:{s_color};'>{bottleneck_safety:.2f}</b>", unsafe_allow_html=True)
        st.progress(s_per)

        st.markdown(f"<div style='font-size: 14px; color: #0000FF; font-weight: bold; margin-top: 10px;'>🕒 포집 시간: {format_time_kr(collection_min)} ({collection_min:.1f}분)</div>", unsafe_allow_html=True)
        st.progress(max(0, min(1.0, collection_min/240)))

        st.markdown(f"예상 포집량: <b style='color:#FF8C00;'>{capacity_unit:.1f} mg</b>", unsafe_allow_html=True)
        st.progress(max(0, min(1.0, capacity_unit/300)))

        t_color, t_per = get_gauge_info(discharge_min, 6, 300, reverse=True)
        st.markdown(f"예상 배출 시간: <b style='color:#008000;'>{format_time_kr(discharge_min)} ({discharge_min:.1f}분)</b>", unsafe_allow_html=True)
        st.progress(t_per)
        
        st.markdown("---")
        st.markdown(f"""
            <div style='background-color: #eef2ff; padding: 10px; border-radius: 5px; border-left: 5px solid #4f46e5;'>
                <span style='font-size: 16px; font-weight: bold; color: #1e1b4b;'>🔄 1회 사이클 총 분석</span><br>
                <span style='font-size: 15px;'>총 포집량: <b>{capacity_unit:.1f} mg</b></span><br>
                <span style='font-size: 15px;'>총 소요 시간: <b>{format_time_kr(total_cycle_min)}</b> ({total_cycle_min:.1f}분)</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 메인 레이아웃 ---
st.set_page_config(page_title="Electrode Design Lab", layout="wide")
st.title("⚡ 중앙 기준 자동 최적화 시뮬레이터")

# 세션 상태 초기화
if 'analyze_comp' not in st.session_state: st.session_state.analyze_comp = False
if 'analyze_idea' not in st.session_state: st.session_state.analyze_idea = False

# 사이드바 설정
st.sidebar.title("🛠 분석 및 구상 도구")

# 1. 타경쟁사 제품 분석 (기존 기능 그대로 유지)
show_comp = st.sidebar.checkbox("🔍 타경쟁사 제품 분석 열기")
if show_comp:
    with st.sidebar.container():
        comp_name = st.sidebar.text_input("제품명", value="Competitor A")
        cp_f = st.sidebar.number_input("타사 앞면 입자(μm)", value=150)
        cp_m = st.sidebar.number_input("타사 중간 입자(μm)", value=50)
        cp_b = st.sidebar.number_input("타사 뒷면 입자(μm)", value=150)
        ct_f = st.sidebar.number_input("타사 앞면 두께(mm)", value=0.40)
        ct_m = st.sidebar.number_input("타사 중간 두께(mm)", value=0.40)
        ct_b = st.sidebar.number_input("타사 뒷면 두께(mm)", value=0.40)
        if st.sidebar.button("타사 분석 실행"): st.session_state.analyze_comp = True

st.sidebar.markdown("---")

# 2. 제품 구상 (중앙 기준 자동 설계 로직 적용)
show_idea = st.sidebar.checkbox("💡 제품 구상 분석 열기 (자동 최적화)")
if show_idea:
    with st.sidebar.container():
        idea_name = st.sidebar.text_input("구상 모델명", value="My New Idea")
        m_p = st.sidebar.number_input("중앙 입자 크기(μm)", value=65)
        m_t = st.sidebar.number_input("중앙 층 두께(mm)", value=0.40, step=0.01)
        
        # [자동 설계 로직 계산]
        delta = m_t * 0.125
        auto_f_p, auto_b_p = 150, 120
        auto_f_t, auto_b_t = m_t - delta, m_t + delta
        
        st.sidebar.caption(f"자동 설정: 앞 {auto_f_p}μm({auto_f_t:.2f}mm) / 뒤 {auto_b_p}μm({auto_b_t:.2f}mm)")
        if st.sidebar.button("구상 분석 실행"): st.session_state.analyze_idea = True

st.write("---")

# 분석 결과 출력
if st.session_state.analyze_comp and show_comp:
    render_analysis_block(f"🚩 타사 분석: {comp_name}", ct_f, ct_m, ct_b, cp_f, cp_m, cp_b, is_special=True, expanded=True)

if st.session_state.analyze_idea and show_idea:
    render_analysis_block(f"✨ 제품 구상: {idea_name} (중앙 {m_p}μm 최적화)", auto_f_t, m_t, auto_b_t, auto_f_p, m_p, auto_b_p, is_special=True, expanded=True)

st.write("---")
st.write("### 🏆 내 전극 설계 모델 (기준 비교)")
# 표준 최적 모델 (중앙 65, 두께 0.40 기준 자동 적용)
render_analysis_block("1. 내 설계 - 표준 최적형", 0.35, 0.40, 0.45, 150, 65, 120, expanded=True)
