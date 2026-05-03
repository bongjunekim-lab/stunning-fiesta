import streamlit as st

# 1. 공지사항 (접이식 메뉴)
def show_notice_expander():
    with st.expander("📑 공학적 핵심 로직 및 무게 추정 원칙 (클릭하여 보기)"):
        st.info("""
        - **저항 지수 ($R \propto L/d^2$):** 입자 크기 제곱 반비례 및 층 두께 비례 법칙.
        - **순차 배출 안정성:** 앞면($125\mu m$) 저항이 뒷면($85\mu m$)보다 낮아 '이온 정류 효과' 발생.
        - **두께 제곱 이론 ($t \propto L^2$):** 전극 두께 증가 시 이온 확산 시간 제곱 비례 증가.
        - **무게 추정 원칙:** 30x30cm 기준, 소재 밀도 2.0g/cm³, 충진율 60% 반영.
        """)

# 2. 시간 변환 헬퍼 (n시간 n분)
def format_time_kr(total_minutes):
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    if hours > 0:
        return f"{hours}시간 {minutes}분"
    return f"{minutes}분"

# 3. 지표별 게이지 헬퍼
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

# 4. 분석 출력용 공통 함수
def render_analysis_block(title, t_f, t_m, t_b, p_f, p_m, p_b, is_special=False, color_theme="#1f77b4", expanded=False):
    total_t = t_f + t_m + t_b
    area_cm2 = 900
    density = 2.0
    filling_rate = 0.6

    w_f = area_cm2 * (t_f / 10) * density * filling_rate
    w_m = area_cm2 * (t_m / 10) * density * filling_rate
    w_b = area_cm2 * (t_b / 10) * density * filling_rate

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
            if discharge_min <= 60: st.success("✅ 최적 설계 (고속)")
            elif discharge_min <= 180: st.info("🟡 보통 수준")
            else: st.warning("⚠️ 성능 저하 (저속)")
            st.progress(max(0, min(1.0, 60/discharge_min)) if discharge_min > 0 else 0)

        st.markdown("---")
        st.markdown("<h5 style='font-size: 14px; color: #666;'>[공학 성능 지표 분석]</h5>", unsafe_allow_html=True)
        
        s_color, s_per = get_gauge_info(bottleneck_safety, 0.5, 3.0)
        st.markdown(f"순차 배출 안정성: <b style='color:{s_color};'>{bottleneck_safety:.2f}</b>", unsafe_allow_html=True)
        st.progress(s_per)

        st.markdown(f"<div style='font-size: 14px; color: #0000FF; font-weight: bold; margin-top: 10px;'>🕒 포집 시간: {format_time_kr(collection_min)} ({collection_min:.1f}분)</div>", unsafe_allow_html=True)
        st.progress(max(0, min(1.0, collection_min/240)))

        c_color, c_per = get_gauge_info(capacity_unit, 0, 300)
        st.markdown(f"예상 포집량: <b style='color:{c_color};'>{capacity_unit:.1f} mg</b>", unsafe_allow_html=True)
        st.progress(c_per)

        t_color, t_per = get_gauge_info(discharge_min, 6, 300, reverse=True)
        st.markdown(f"예상 배출 시간: <b style='color:{t_color};'>{format_time_kr(discharge_min)} ({discharge_min:.1f}분)</b>", unsafe_allow_html=True)
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
st.title("⚡ 비대칭 소결 전극 설계 시뮬레이터")
show_notice_expander()

# 세션 상태 및 변수 초기화 (NameError 방지 핵심)
if 'analyze_comp' not in st.session_state: st.session_state.analyze_comp = False
if 'analyze_idea' not in st.session_state: st.session_state.analyze_idea = False

# 사이드바 설정
st.sidebar.title("🛠 분석 및 구상 도구")

# 1. 타사 분석 입력창
show_comp = st.sidebar.checkbox("🔍 타경쟁사 제품 분석 열기")
if show_comp:
    comp_name = st.sidebar.text_input("제품명", value="Competitor A")
    cp_f = st.sidebar.number_input("타사 앞면 입자(μm)", value=150)
    cp_m = st.sidebar.number_input("타사 중간 입자(μm)", value=75)
    cp_b = st.sidebar.number_input("타사 뒷면 입자(μm)", value=150)
    ct_f = st.sidebar.number_input("타사 앞면 두께(mm)", value=0.4)
    ct_m = st.sidebar.number_input("타사 중간 두께(mm)", value=0.4)
    ct_b = st.sidebar.number_input("타사 뒷면 두께(mm)", value=0.4)
    if st.sidebar.button("타사 분석 실행"): st.session_state.analyze_comp = True

st.sidebar.markdown("---")

# 2. 구상 분석 입력창
show_idea = st.sidebar.checkbox("💡 제품 구상 분석 열기")
if show_idea:
    idea_name = st.sidebar.text_input("구상 모델명", value="My New Idea")
    ip_f = st.sidebar.number_input("구상 앞면 입자(μm)", value=150)
    ip_m = st.sidebar.number_input("구상 중간 입자(μm)", value=75)
    ip_b = st.sidebar.number_input("구상 뒷면 입자(μm)", value=120)
    it_f = st.sidebar.number_input("구상 앞면 두께(mm)", value=0.4)
    it_m = st.sidebar.number_input("구상 중간 두께(mm)", value=0.4)
    it_b = st.sidebar.number_input("구상 뒷면 두께(mm)", value=0.4)
    if st.sidebar.button("구상 분석 실행"): st.session_state.analyze_idea = True

st.write("---")
user_t = st.slider("📏 기본 전극 전체 두께 설정 (mm):", 0.1, 5.0, 1.2, 0.1)

# 분석 결과 출력 (변수 정의 여부 체크 조건 추가)
if st.session_state.analyze_comp and show_comp:
    render_analysis_block(f"🚩 타사 분석: {comp_name}", ct_f, ct_m, ct_b, cp_f, cp_m, cp_b, is_special=True, color_theme="#e63946", expanded=True)

if st.session_state.analyze_idea and show_idea:
    render_analysis_block(f"✨ 제품 구상: {idea_name}", it_f, it_m, it_b, ip_f, ip_m, ip_b, is_special=True, color_theme="#008000", expanded=True)

st.write("---")
st.write("### 🏆 내 전극 설계 모델 (3종 비교)")
render_analysis_block("1. 내 설계 - 초고속형", user_t*0.4, user_t*0.2, user_t*0.4, 125, 50, 85, expanded=True)
render_analysis_block("2. 내 설계 - 표준형", user_t*0.333, user_t*0.334, user_t*0.333, 125, 50, 85, expanded=False)
render_analysis_block("3. 내 설계 - 용량형", user_t*0.3, user_t*0.4, user_t*0.3, 125, 50, 85, expanded=False)