import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(page_title="우리 가족 운세 대시보드", page_icon="🔮", layout="centered")

# 카드 버튼 스타일링 CSS
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

# Payload 데이터 세팅
family_members = {
    "김미영 (어머니)": {
        "pw": "1006",
        "icon": "👩🏻",
        "form_data": {
            "cate1": "free",
            "cate2": "todayline",
            "free_yn": "Y",
            "login_yn": "N",
            "user_name": "김미영",
            "sex": "여",           
            "birth_yyyy": "1961",
            "birth_mm": "10",
            "birth_dd": "06",
            "birth_hh": "08",      
            "birth_solunar": "L_C", 
            "target_yyyy": "2026"
        }
    },
    "구현동": {
        "pw": "0427",
        "icon": "👨🏻",
        "form_data": {
            "cate1": "free",
            "cate2": "todayline",
            "free_yn": "Y",
            "login_yn": "N",
            "user_name": "구현동",
            "sex": "남",
            "birth_yyyy": "1988",
            "birth_mm": "04",
            "birth_dd": "27",
            "birth_hh": "06",      
            "birth_solunar": "S_C", 
            "target_yyyy": "2026"
        }
    }
}

st.markdown('<div class="main-title">🔮 우리 가족 전용 운세 명당</div>', unsafe_allow_html=True)
st.write("본인의 이름을 선택하고 비밀번호를 입력하면 오늘 운세가 바로 나타납니다.")

# 2열로 카드 레이아웃 배치
cols = st.columns(2)
for i, (name, info) in enumerate(family_members.items()):
    with cols[i % 2]:
        if st.button(f"{info['icon']}\n{name}"):
            st.session_state['selected_name'] = name

# 이름 선택 시 비밀번호 입력창 표시
if 'selected_name' in st.session_state:
    name = st.session_state['selected_name']
    target_info = family_members[name]
    
    st.divider()
    st.subheader(f"🔑 {name}님 본인 인증")
    
    input_pw = st.text_input("비밀번호(생일 4자리)를 입력하세요", type="password", key="pw_input")
    
    if input_pw:
        if input_pw == target_info['pw']:
            st.success("인증 성공! 아래 버튼을 누르면 운세 페이지로 이동합니다.")
            
            # 딕셔너리를 HTML hidden input 태그로 변환
            inputs_html = ""
            for key, value in target_info['form_data'].items():
                inputs_html += f'<input type="hidden" name="{key}" value="{value}">\n'
            
            # 🔥 ACTION URL 수정 완료 🔥
            html_code = f"""
            <form id="autoSubmit" action="https://www.unsin.co.kr/unse/free/today/result" method="POST" target="_blank" style="display:none;">
                {inputs_html}
            </form>
            <button onclick="document.getElementById('autoSubmit').submit()" 
                    style="width: 100%; height: 50px; font-size: 16px; font-weight: bold; color: white; background-color: #FF4B4B; border: none; border-radius: 8px; cursor: pointer;">
                👉 {name} 오늘의 운세 결과 보기
            </button>
            """
            components.html(html_code, height=60)
        else:
            st.error("비밀번호가 맞지 않습니다. 다시 확인해 주세요.")

# 화면 초기화 버튼
if st.sidebar.button("🔄 처음으로"):
    st.session_state.clear()
    st.rerun()
