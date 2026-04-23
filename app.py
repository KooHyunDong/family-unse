import streamlit as st
import requests
from bs4 import BeautifulSoup

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
    .unse-result {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        line-height: 1.8;
        font-size: 16px;
        border-left: 5px solid #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# 맥북 개발자 도구에서 추출한 정확한 Payload 적용
family_members = {
    "김미영": {
        "pw": "1113",
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
st.write("본인의 이름을 선택하고 비밀번호를 입력하면 광고 없이 결과만 바로 나타납니다.")

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
            st.success("인증 완료! 데이터를 불러옵니다.")
            
            with st.spinner('운세 결과를 가져오는 중입니다...'):
                try:
                    # 1. 서버로 POST 요청
                    url = "https://www.unsin.co.kr/unse/free/today/result"
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                    res = requests.post(url, data=target_info['form_data'], headers=headers)
                    res.raise_for_status()
                    res.encoding = 'utf-8' # 한글 깨짐 방지
                    
                    # 2. 결과 HTML 파싱 및 운세 텍스트 추출 (class="unse_view" 적용)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    fortune_div = soup.find('div', class_='unse_view')
                    
                    st.markdown("---")
                    st.subheader(f"📜 {name}님의 오늘의 운세")
                    
                    if fortune_div:
                        # 텍스트만 추출하고, 문단 구분을 위해 \n\n 추가
                        fortune_text = fortune_div.get_text(separator='\n\n', strip=True)
                        st.markdown(f'<div class="unse-result">{fortune_text}</div>', unsafe_allow_html=True)
                    else:
                        st.error("운세 결과를 찾을 수 없습니다. 사이트 구조가 변경되었을 수 있습니다.")
                        
                except Exception as e:
                    st.error(f"서버와 통신 중 문제가 발생했습니다: {e}")

        else:
            st.error("비밀번호가 맞지 않습니다. 다시 확인해 주세요.")

# 화면 초기화 버튼
st.markdown("<br><br>", unsafe_allow_html=True)
if st.sidebar.button("🔄 처음으로"):
    st.session_state.clear()
    st.rerun()
