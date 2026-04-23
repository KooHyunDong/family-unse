import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="우리 가족 운세 대시보드",
    page_icon="🔮",
    layout="centered"
)

# 카드형 디자인을 위한 CSS
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 120px;
        font-size: 22px;
        font-weight: bold;
        color: #333;
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        border-color: #FF4B4B;
        color: #FF4B4B;
        transform: translateY(-5px);
    }
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 30px;
        color: #1E1E1E;
    }
    </style>
    """, unsafe_allow_html=True)

# 가족 데이터 구성
# 비밀번호는 각자의 생일 4자리로 설정되어 있습니다.
family_members = {
    "김미영 (어머니)": {
        "url": "https://m.unsin.co.kr/unse/saju/free/result?name=%EA%B9%80%EB%AF%B8%EC%98%81&gender=f&birthday=1961-10-06&birthtime=08%3A30&calendar=lunar",
        "pw": "1006",
        "icon": "👩🏻"
    },
    "구현동": {
        "url": "https://m.unsin.co.kr/unse/saju/free/result?name=%EA%B5%AC%ED%98%84%EB%8F%99&gender=m&birthday=1988-04-27&birthtime=06%3A30&calendar=solar",
        "pw": "0427",
        "icon": "👨🏻"
    }
}

st.markdown('<div class="main-title">🔮 우리 가족 전용 운세 명당</div>', unsafe_allow_html=True)
st.write("본인의 이름을 선택하고 비밀번호를 입력하면 오늘 운세가 바로 나타납니다.")

# 카드 레이아웃 (2열 배치)
cols = st.columns(2)
for i, (name, info) in enumerate(family_members.items()):
    with cols[i % 2]:
        if st.button(f"{info['icon']}\n{name}"):
            st.session_state['selected_name'] = name

# 선택된 사람이 있을 경우 비밀번호 입력창 표시
if 'selected_name' in st.session_state:
    name = st.session_state['selected_name']
    target_info = family_members[name]
    
    st.divider()
    st.subheader(f"🔑 {name}님 본인 인증")
    
    # 비밀번호 입력 (생일 4자리)
    input_pw = st.text_input("비밀번호(생일 4자리)를 입력하세요", type="password", key="pw_input")
    
    if input_pw:
        if input_pw == target_info['pw']:
            st.success(f"인증 성공! 아래 버튼을 누르면 {name}님의 운세 페이지로 이동합니다.")
            st.link_button(f"👉 {name} 오늘의 운세 보기", target_info['url'], use_container_width=True)
        else:
            st.error("비밀번호가 맞지 않습니다. 다시 확인해 주세요.")

# 초기화 버튼 (사이드바)
if st.sidebar.button("🔄 화면 초기화"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("가족 전용 운세 서비스입니다.\n본인의 정보만 확인해 주세요.")
