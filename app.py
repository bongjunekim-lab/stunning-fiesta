import streamlit as st

# 1. [공지사항] 접이식 메뉴로 본문 상단 이동
def show_notice_expander():
    with st.expander("📑 공학적 핵심 로직 및 무게 추정 원칙 (클릭하여 보기)"):
        st.info("""
        - **저항 지수 ($R \propto L/d^2$):** 입자 크기 제곱 반비례 및 층 두께 비례 법칙.
        - **순차 배출 안정성:** 앞면($125\mu m$) 저항이 뒷면($85\mu m$)보다 낮아 '이온 정류 효과' 발생.
        - **두께 제곱 이론 ($t \propto L^2$):** 전극 두께 증가 시 이온 확산 시간 제곱 비례 증가.
        - **무게 추정 원칙:** 
            1. 기준 면적 $30 \times 30 \text{cm}$ ($900\text{cm}^2$) 적용.
            2. 소재 평균 밀도 $2.0\text{g/cm}^3$, 충진율 $60\%$ 가정.
            3. 소결 전 '그린 바디' 기준 무게이며 소결 후 약 $5\sim 10\%$ 감소 가능.
        """)

# 2. 지표별 게이지 헬퍼 함수
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

# 3. 분석 출력용 공통 함수
def render_analysis_block(title, t_f, t_m, t_b, p_f, p_m, p_b, is_competitor=False):
    total_t = t_f + t_m + t_b
    area_cm2 = 900
    density = 2.0
    filling_rate = 0.6

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
    discharge_time = 0.5 * (total_res / 100) * (total_t**2)
    capacity_unit = (t_m / total_t) * total_t * 150
    collection_time = 1.2 * (total_res / 150) * total_t

    bg_color = "#f0f2f6" if is_competitor else "transparent"
    
    st.markdown(f"<div style='background-color:{bg_color}; padding:15px; border-radius:10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='font-size: 28px; color: {'#e63946' if is_competitor else '#1f77b4'};'>{title}</h2>", unsafe_allow_html=True)
    
    with st.expander("세부 분석 데이터 보기", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.write("**[층별 두께 및 추정 무게]**")
            st.write(f"앞면 ({p_f}μm): {t_f:.3f} mm → {w_f:.1f} g")
            st.write(f"중간 ({p_m}μm): {t_m:.3f} mm → {w_m:.1f} g")
            st.write(f"뒷면 ({p_b}μm): {t_b:.3f} mm → {w_b:.1f} g")
        with c2:
            st.write("**[종합 판정]**")
            if discharge_time <= 1.0: st.success("✅ 최적 설계")
            elif discharge_time <= 3.0: st.info("🟡 보통 수준")
            else: st.warning("⚠️ 성능 저하")
            st.progress(max(0, min(1.0, 1.0/discharge_time)) if discharge_time > 0 else 0)

        st.markdown("---")
        st.markdown("<h5 style='font-size: 14px; color: #666;'>[공학 성능 지표 분석]</h5>", unsafe_allow_html=True)
        
        s_color, s_per = get_gauge_info(bottleneck_safety, 0.5, 3.0)
        st.markdown(f"순차 배출 안정성: <b style='color:{s_color};'>{bottleneck_safety:.2f}</b> / <b style='color:#0000FF;'>포집 시간: {collection_time:.2f}h</b>", unsafe_allow_html=True)
        st.progress(s_per)

        c_color, c_per = get_gauge_info(capacity_unit, 0, 300)
        st.markdown(f"예상 포집량: <b style='color:{c_color};'>{capacity_unit:.1f} mg</b>", unsafe_allow_html=True)
        st.progress(c_per)

        t_color, t_per = get_gauge_info(discharge_time, 0.1, 5.0, reverse=True)
        st.markdown(f"예상 배출 시간: <b style='color:{t_color};'>{discharge_time:.2f} h</b>", unsafe_allow_html=True)
        st.progress(t_per)
    st.markdown("</div>", unsafe_allow_html=True)

# --- UI 레이아웃 ---
st.set_page_config(page_title="Electrode Lab Pro", layout="wide")
st.title("⚡ 비대칭 소결 전극 설계 시뮬레이터")

# 1. 본문 상단 공지사항 이동
show_notice_expander()

# 2. 사이드바: 타경쟁사 분석 입력창
st.sidebar.header("🔍 타경쟁사 제품 분석")
with st.sidebar.container():
    st.write("비교할 타사 제품의 사양을 입력하세요.")
    comp_name = st.text_input("경쟁사/제품명", value="Competitor A")
    
    st.write("**[입자 크기 설정 - μm]**")
    cp_f = st.number_input("타사 앞면 입자", value=100)
    cp_m = st.number_input("타사 중간 입자", value=100)
    cp_b = st.number_input("타사 뒷면 입자", value=100)
    
    st.write("**[층별 두께 설정 - mm]**")
    ct_f = st.number_input("타사 앞면 두께", value=0.5, step=0.1)
    ct_m = st.number_input("타사 중간 두께", value=0.5, step=0.1)
    ct_b = st.number_input("타사 뒷면 두께", value=0.5, step=0.1)
    
    analyze_comp = st.sidebar.button("타경쟁사 분석 실행")

st.write("---")

# 3. 본문: 사용자 전극 두께 설정
st.write("### 📏 내 전극 두께 설정 (3층 구조)")
c1, c2 = st.columns([1, 2])
with c1:
    user_t = st.number_input("전체 두께 입력 (mm):", min_value=0.1, max_value=5.0, value=1.2, step=0.1)
with c2:
    user_t_slider = st.slider("슬라이더 조절:", min_value=0.1, max_value=5.0, value=float(user_t), step=0.1)

current_t = user_t_slider if user_t_slider != user_t else user_t

# 4. 결과 출력 구역
if analyze_comp:
    st.warning(f"❗ {comp_name} 제품 분석 결과가 추가되었습니다. 아래에서 비교해 보세요.")
    render_analysis_block(f"🚩 {comp_name} (타사 분석)", ct_f, ct_m, ct_b, cp_f, cp_m, cp_b, is_competitor=True)
    st.write("---")

# 사용자 모델 출력 (초고속형 기준 예시)
render_analysis_block("1. 내 전극 설계 (초고속형)", current_t*0.4, current_t*0.2, current_t*0.4, 125, 50, 85)