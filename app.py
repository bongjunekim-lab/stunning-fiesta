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

# 2. 지표별 게이지 헬퍼
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

# 3. 분석 출력용 공통 함수 (포집 시간 레이아웃 및 30x30 무게 적용)
def render_analysis_block(title, t_f, t_m, t_b, p_f, p_m, p_b, is_competitor=False):
    total_t = t_f + t_m + t_b
    area_cm2 = 900
    density = 2.0
    filling_rate = 0.6

    # 30x30cm 무게 계산
    w_f = area_cm2 * (t_f / 10) * density * filling_rate
    w_m = area_cm2 * (t_m / 10) * density * filling_rate
    w_b = area_cm2 * (t_b / 10) * density * filling_rate

    # 저항 및 공학 지표 계산
    res_f = t_f / (p_f**2) * 1000000 
    res_m = t_m / (p_m**2) * 1000000
    res_b = t_b / (p_b**2) * 1000000
    total_res = res_f + res_m + res_b
    
    bottleneck_safety = (res_b / res_f)
    discharge_time = 0.5 * (total_res / 100) * (total_t**2)
    capacity_unit = (t_m / total_t) * total_t * 150
    collection_time = 1.2 * (total_res / 150) * total_t

    title_color = "#e63946" if is_competitor else "#1f77b4"
    bg_color = "#f8f9fa" if is_competitor else "transparent"
    
    st.markdown(f"""
        <div style='background-color:{bg_color}; padding:15px; border-radius:10px; border: 1px solid #ddd; margin-bottom:20px;'>
            <h2 style='font-size: 24px; color: {title_color};'>{title}</h2>
    """, unsafe_allow_html=True)
    
    with st.expander("세부 분석 데이터 보기", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**[층별 두께 및 추정 무게]**")
            st.write(f"앞면 ({p_f}μm): {t_f:.3f} mm → {w_f:.1f} g")
            st.write(f"중간 ({p_m}μm): {t_m:.3f} mm → {w_m:.1f} g")
            st.write(f"뒷면 ({p_b}μm): {t_b:.3f} mm → {w_b:.1f} g")
        with col2:
            st.write("**[종합 판정]**")
            if discharge_time <= 1.0: st.success("✅ 최적 설계")
            elif discharge_time <= 3.0: st.info("🟡 보통 수준")
            else: st.warning("⚠️ 성능 저하")
            st.progress(max(0, min(1.0, 1.0/discharge_time)) if discharge_time > 0 else 0)

        st.markdown("---")
        st.markdown("<h5 style='font-size: 14px; color: #666;'>[공학 성능 지표 분석]</h5>", unsafe_allow_html=True)
        
        # 1. 순차 배출 안정성
        s_color, s_per = get_gauge_info(bottleneck_safety, 0.5, 3.0)
        st.markdown(f"순차 배출 안정성: <b style='color:{s_color};'>{bottleneck_safety:.2f}</b>", unsafe_allow_html=True)
        st.progress(s_per)

        # 2. 포집 시간 (바 아래 독립 배치)
        st.markdown(f"<div style='font-size: 14px; color: #0000FF; font-weight: bold; margin-top: 10px;'>🕒 포집 시간: {collection_time:.2f} 시간</div>", unsafe_allow_html=True)
        st.progress(max(0, min(1.0, collection_time/4.0)))

        # 3. 예상 포집량
        c_color, c_per = get_gauge_info(capacity_unit, 0, 300)
        st.markdown(f"예상 포집량: <b style='color:{c_color};'>{capacity_unit:.1f} mg</b>", unsafe_allow_html=True)
        st.progress(c_per)

        # 4. 예상 배출 시간
        t_color, t_per = get_gauge_info(discharge_time, 0.1, 5.0, reverse=True)
        st.markdown(f"예상 배출 시간: <b style='color:{t_color};'>{discharge_time:.2f} 시간</b>", unsafe_allow_html=True)
        st.progress(t_per)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 메인 레이아웃 ---
st.set_page_config(page_title="Electrode Lab Simulator", layout="wide")
st.title("⚡ 비대칭 소결 전극 설계 시뮬레이터")
show_notice_expander()

# 사이드바: 타사 분석 입력란
st.sidebar.header("🔍 타경쟁사 제품 분석")
comp_name = st.sidebar.text_input("제품명", value="Competitor A")
cp_f = st.sidebar.number_input("타사 앞면 입자(μm)", value=150)
cp_m = st.sidebar.number_input("타사 중간 입자(μm)", value=100)
cp_b = st.sidebar.number_input("타사 뒷면 입자(μm)", value=150)
ct_f = st.sidebar.number_input("타사 앞면 두께(mm)", value=0.4, step=0.1)
ct_m = st.sidebar.number_input("타사 중간 두께(mm)", value=0.4, step=0.1)
ct_b = st.sidebar.number_input("타사 뒷면 두께(mm)", value=0.4, step=0.1)
analyze_comp = st.sidebar.button("타사 분석 실행")

st.write("---")

# 본문: 내 전극 설계 입력
st.write("### 📏 내 전극 두께 설정 (3층 구조)")
c1, c2 = st.columns([1, 2])
with c1:
    user_t = st.number_input("전체 두께 (mm):", min_value=0.1, max_value=5.0, value=1.2, step=0.1)
with c2:
    slider_t = st.slider("슬라이더 조절:", min_value=0.1, max_value=5.0, value=float(user_t), step=0.1)

final_t = slider_t if slider_t != user_t else user_t

# 내 설계 3종 동시 출력
st.markdown("### 🏆 내 전극 설계 모델 (3종 비교)")

# 1. 초고속형 (4:2:4 비중)
render_analysis_block("1. 내 전극 설계 (초고속형)", final_t*0.4, final_t*0.2, final_t*0.4, 125, 50, 85)

# 2. 표준형 (3.3:3.3:3.3 비중)
render_analysis_block("2. 내 전극 설계 (표준형)", final_t*0.333, final_t*0.334, final_t*0.333, 125, 50, 85)

# 3. 용량형 (3:4:3 비중)
render_analysis_block("3. 내 전극 설계 (용량형)", final_t*0.3, final_t*0.4, final_t*0.3, 125, 50, 85)

# 타사 분석 실행 시 하단에 별도 출력
if analyze_comp:
    st.write("---")
    render_analysis_block(f"🚩 타경쟁사 분석 결과 ({comp_name})", ct_f, ct_m, ct_b, cp_f, cp_m, cp_b, is_competitor=True)