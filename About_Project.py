# 라이브러리 호출
import streamlit as st
import pandas as pd
import numpy as np
import threading      # [왜 쓰나] 백그라운드 스레드 실행용
import requests       # [왜 쓰나] 자기 자신에게 HTTP 핑 전송용
import time           # [왜 쓰나] 5분 간격 타이머용

# ── Sleep 방지 ────────────────────────────────
# [왜 쓰나] Streamlit Community Cloud는 비활성 시
#           자동으로 Sleep됨 → 5분마다 자신에게
#           핑을 보내서 Sleep 방지
def keep_alive():
    while True:
        time.sleep(300)
        try:
            requests.get(
                "https://forbusanport.streamlit.app",
                timeout=10
            )
        except:
            pass

if "keep_alive_started" not in st.session_state:
    st.session_state.keep_alive_started = True
    threading.Thread(target=keep_alive, daemon=True).start()
# ─────────────────────────────────────────────

# 메인 페이지 > 프로젝트 제목 및 개요, 프로젝트 참석자, 프로젝트 기간
st.set_page_config(layout="wide")

# 프로젝트 제목
st.title("Marketing-related data analysis for revitalizing Busan Port in South Korea", anchor=False)

pjtIntro_tab_1, pjtIntro_tab_2 = st.tabs(["Project Intro(EN)", "Project Intro(KR)"])
# 프로젝트 개요 English
with pjtIntro_tab_1:
    intro_sentence_EN = '''
    The Busan Port revitalization marketing data analysis project was carried out by project participant Donghwi Kim, inspired by a meeting he had with officials from Busan Port Authority (BPA) in 2020.
    At that time, BPA was in the process of developing strategies to promote Busan Port to foreign shipping companies and encourage them to call at the port.
    Accordingly, Donghwi Kim and Seongil Kim, as project participants, aimed to develop strategic initiatives from BPA’s perspective to revitalize the port—specifically through the establishment of an online ship supply shopping mall and a time-based tourism course recommendation service—and to carry out the necessary data analysis to support these goals.
    '''
    st.markdown(intro_sentence_EN)

    #-타겟 고객
    st.subheader("1. Target Customers and Market Size 🧑🏽‍🤝‍🧑🏼", anchor=False)
    target_customer_EN = '''
    The primary customers are foreign seafarers who enter Korea aboard ships operated by shipping companies arriving at Busan Port.
    Shipping companies, also known as “carriers” or “ocean liner companies,” operate vessels and provide maritime transportation services.
    We plan to assess the size and sustainability of the foreign seafarer market through correlation analysis of cargo volume and vessel dwell time at Busan Port.
    '''
    intro_badge_EN = '''
    A shipping company operates various types of vessels such as container ships, oil tankers, and bulk carriers, manages shipping routes and sailing schedules, and enters into logistics service contracts with shippers (cargo owners).
    '''
    st.markdown(target_customer_EN)
    st.badge(intro_badge_EN, color="orange")

    #-활성화 전략
    st.subheader("2. Strategies for Revitalization 🎯", anchor=False)
    #--전략 1
    strategy_kinds_en_1 = '''
    (1) Online Ship Supply Shopping Mall
    - Currently, there is no dedicated online platform in Busan for purchasing ship supplies targeted at foreign shipping companies and international seafarers.
    - Although there are offline institutions related to ship supplies, most of the products offered are limited to items such as ropes and tubes.
    - By building an online shopping mall focused on products preferred by foreign customers, it is expected that the satisfaction level of Busan Port Authority’s member shipping companies will increase, and non-member companies could also be attracted to call at Busan Port through effective marketing.
    - To support this initiative, we plan to conduct the following data analysis and visualization activities.
    '''
    strategy_kinds_en_df1 = pd.DataFrame({
        "Type": [
            "Trend Analysis by Ship Supply Item",
            "Sourcing Online Sellers",
            "Warehouse Hub Analysis",
            "Item-wise Word Cloud"
        ],
        "Purpose of Analysis": [
            "Identify the top 2 high-demand ship supply items and designate them as initial products for the online mall",
            "Source manufacturers/sellers for the top 2 popular items",
            "Identify available warehouse spaces near Busan Port to store ordered supplies",
            "Extract key keywords by item and use them for discovering related products and companies"
        ],
        "Technologies Used": [
            "Data crawling / preprocessing / visualization",
            "Data crawling / preprocessing / visualization",
            "Data crawling / preprocessing / visualization",
            "Data crawling / preprocessing / visualization"
        ]
    })
    st.markdown(strategy_kinds_en_1)
    st.dataframe(strategy_kinds_en_df1, hide_index=True)
    #--전략 2
    strategy_kinds_en_2 = '''
    (2) Providing Busan Tourism Information Based on Length of Stay
    - The duration of stay at Busan Port varies significantly depending on the shipping company.
    - Therefore, by offering tailored tourism course information based on the length of stay, we aim to provide welfare benefits for Busan Port Authority member companies and create additional marketing value through data analysis.
    - In addition, we believe that building an online ship supply shopping mall based on the preferences of foreign visitors can increase satisfaction among current member shipping companies and attract non-member companies to call at Busan Port.
    '''
    strategy_kinds_en_df2 = pd.DataFrame({
        "Type": [
            "Stay Duration Aggregation",
            "Identifying Tourist Attractions / Accommodations / Restaurants",
            "Visualization of Tourism Information by Stay Duration"
        ],
        "Purpose of Analysis": [
            "Identify the most common stay durations using quartiles of stay times by shipping company",
            "Visualize key tourist spots, accommodations, and restaurants to support stay-duration-based tourism info",
            "Provide randomized tourism information and route visualization tailored to stay duration"
        ],
        "Technologies Used": [
            "Data crawling / preprocessing / visualization",
            "Data crawling / preprocessing / visualization",
            "Data crawling / preprocessing / visualization, OpenAI LLM"
        ]
    })
    st.markdown(strategy_kinds_en_2)
    st.dataframe(strategy_kinds_en_df2, hide_index=True)

    # 분석일정 및 R&R
    st.subheader("3. WBS(Work Breakdown Structure) and R&R(Roles and Responsibilities) 📅", anchor=False)
    st.image("./useImage/WBS_EN.png",use_container_width=True)

    # 코드컨벤션
    st.subheader("4. Code Convention Guide </>", anchor=False)
    st.badge("Throughout the project, all code must adhere to the standards outlined in this coding convention.", color="red")
    st.text("(1) Always include a header comment")
    st.code('''
    Author       : Hong Gil-dong
    Date Written : 2025-04-07
    Description  : Loads a CSV file, performs preprocessing, and visualizes the data.
    ''')
    st.text("(2) Variable Naming Rules")
    st.text("- Use CamelCase for variable names)")
    st.text("- If the variable name is long, use underscores (_) for readability")
    st.text("(3) Function Names: Use lowercase with underscores (snake_case)")
    st.code('''
    def load_data_from_csv():
        ...

    def calculate_total_sales():
        ...
    ''')
    st.text("(4) Data Storage Rules")
    st.text("- Store structured data (e.g., CSV, XLSX) in the useData/ folder")
    st.text("- Store image files (e.g., PNG, JPEG) in the useImage/ folder")
    st.code('''
    df.to_csv('useData/sales_data.csv', index=False)
    plt.savefig('useImage/sales_chart.png')
    ''')
    st.text("(5) Add purpose comments for each imported library")
    st.code('''
    import pandas as pd        # for data manipulation
    import numpy as np         # for numerical operations
    import matplotlib.pyplot as plt  # for visualization
    import seaborn as sns      # for advanced plotting
    ''')

# 프로젝트 개요 Korea
with pjtIntro_tab_2:
    intro_sentence_KR = '''
    부산항 활성화를 위한 마케팅관련 데이터 분석 프로젝트는 해당 프로젝트 참여자인 김동휘가 2020년도 대한민국 부산 항만공사 관계자와 미팅을 했을 때를 상기하며 진행한 프로젝트이다.
    당시 부산 항만공사는 해외 선사들에게 부산항 홍보 및 입항을 유도하려는 전략을 수립 중이었음.
    이에 따라 해당 프로젝트 참여자인 김동휘, 김성일은 부산항만공사 입장에서 필요한 부산항 활성화 전략수립(온라인 선용품 쇼핑몰, 체류시간별 관광코스 정보제공 서비스)과 이를 위한 데이터 분석을 진행하고자함.
    '''
    st.markdown(intro_sentence_KR)

    #-타겟 고객
    st.subheader("1. 타겟 고객 및 규모 🧑🏽‍🤝‍🧑🏼", anchor=False)
    target_customer_KR = '''
    주요 고객은 부산항에 입항하는 선사의 선박을 타고 입국하는 해외 선원들이다.
    선사(해운 회사)는 선박을 운영하고 해상 운송 서비스를 제공하는 기업으로, ‘캐리어(carrier)’ 또는 ‘오션 라이너 컴퍼니(ocean liner company)’라고도 불린다.
    우리는 부산항 입항 물동량과 체류시간 등의 상관관계 분석을 통해, 해외 선원 시장의 규모와 그 지속 가능성을 평가할 예정이다.
    '''
    intro_badge_KR = '''
    선사(해운 회사)는 컨테이너선, 유조선, 벌크선 등 다양한 종류의 선박을 운항하고, 항로 및 운항 일정을 관리하며, 화주(화물 소유주)와 물류 서비스 계약을 체결한다.
    '''
    st.markdown(target_customer_KR)
    st.badge(intro_badge_KR, color="orange")

    #-활성화 전략
    st.subheader("2. 활성화 전략 🎯", anchor=False)
    #--전략 1
    strategy_kinds_kr_1 = '''
    (1) 온라인 선용품 쇼핑몰
    - 현재 부산에는 해외선사 및 외국인 선원들을 위한 선용품 구매 플랫폼이 없는 상황임.
    - 오프라인 방식의 선용품 관련 기관이 있지만, 판매품목이 대부분 로프, 튜브 등으로 구성되어 있음.
    - 외국인이 선호하는 물품을 기반으로 온라인 선용품 쇼핑몰을 구축한다면, 부산항만공사 회원 선사들의 만족도 상승과 더불어 비회원 선사들을 부산항으로 유도 할 수 있는 마케팅 효과를 볼 수 있다고 판단함.
    - 이를 위해 우리는 아래와 같은 데이터 분석 및 시각화를 진행할 것임.
    '''
    strategy_kinds_kr_df1 = pd.DataFrame({
        "종류" : ["선용품 품목별 추이 분석", "온라인 판매기업 소싱", "창고 거점확보 분석", "품목별 워드크라우드"],
        "분석목적" : ["수요가 많은 선용품 품목 상위 2개를 뽑아, 해당 품목으로 온라인 쇼핑몰 초기 판매상품으로 지정", "상위 2개 인기품목 해당하는 제품을 생산/판매기업 소싱", "주문한 선용품을 보관할 수 있는 창고 확보를 위해 부산항 부근의 공실 파악", "품목별 핵심 키워드를 파악하여 연관상품 및 기업 소싱에 활용"],
        "활용기술" :["데이터 크롤링/전처리/시각화", "데이터 크롤링/전처리/시각화", "데이터 크롤링/전처리/시각화", "데이터 크롤링/전처리/시각화"]
    })
    st.markdown(strategy_kinds_kr_1)
    st.dataframe(strategy_kinds_kr_df1, hide_index=True)
    #--전략 2
    strategy_kinds_kr_2 = '''
    (2) 체류시간별 부산관광코스 정보 제공
    - 부산항 입항 선사들 별 체류시간은 매우 상이함
    - 이에 따라 체류시간별 관광코스등의 정보 제공을 함으로써 부산항만공사의 회원사를 위한 복지제공 및 마케팅 효과를 위해 데이터 분석 진행할 것임.
    - 외국인이 선호하는 물품을 기반으로 온라인 선용품 쇼핑몰을 구축한다면, 부산항만공사 회원 선사들의 만족도 상승과 더불어 비회원 선사들을 부산항으로 유도 할 수 있는 마케팅 효과를 볼 수 있다고 판단함.
    '''
    strategy_kinds_kr_df2 = pd.DataFrame({
        "종류" : ["체류시간 집계", "관광지/숙박업소/맛집 파악", "체류시간별 관광정보제공 시각화"],
        "분석목적" : ["입항 선사별 체류시간 4분위를 사용하여 가장 많은 체류시간 때 파악", "체류시간별 관광정보제공 시각화를 위해 주요 관광지, 숙박업소, 맛집 위치 시각화", "체류시간에 맞춰 랜덤하게 관광정보 및 경로 시각화 제공"],
        "활용기술" :["데이터 크롤링/전처리/시각화", "데이터 크롤링/전처리/시각화", "데이터 크롤링/전처리/시각화, Open-AI LLM"]
    })
    st.markdown(strategy_kinds_kr_2)
    st.dataframe(strategy_kinds_kr_df2, hide_index=True)

    # 분석일정 및 R&R
    st.subheader("3. 프로젝트 WBS 및 R&R 📅", anchor=False)
    st.image("./useImage/WBS_KR.png",use_container_width=True)

    # 코드컨벤션_KR
    st.subheader("4. 코드 컨벤션 </>", anchor=False)
    st.badge("프로젝트 수행 기간 동안 작성되는 모든 코드는 이 코드 컨벤션에 명시된 기준을 반드시 준수해야 합니다.", color="red")
    st.text("(1) 주석은 반드시 달 것")
    st.code('''
    코드 작성자 : 홍길동
    코드 작성일 : 2025-04-07
    코드 기능 및 정의 : CSV 파일을 불러와 전처리하고 시각화하는 코드
    ''')
    st.text("(2) 변수명 규칙")
    st.text("- 변수명은 카멜케이스(CamelCase)")
    st.text("- 단어가 길 경우 언더스코어(_) 사용")
    st.text("(3) 함수명은 소문자 + 언더스코어 (snake_case)로 명명")
    st.code('''
    def load_data_from_csv():
        ...

    def calculate_total_sales():
        ...
    ''')
    st.text("(4) 데이터 저장 경로 규칙")
    st.text("- 정형 데이터(csv, xlsx 등) → useData/ 폴더에 저장")
    st.text("- 이미지 파일(png, jpeg 등) → useImage/ 폴더에 저장")
    st.code('''
    df.to_csv('useData/sales_data.csv', index=False)
    plt.savefig('useImage/sales_chart.png')
    ''')
    st.text("(5)라이브러리 호출 시 사용 목적 주석 필수")
    st.code('''
    import pandas as pd     # 데이터프레임 처리용
    import numpy as np      # 수치 계산용
    import matplotlib.pyplot as plt  # 시각화
    import seaborn as sns   # 고급 시각화
    ''')
