import streamlit as st
import pandas as pd
import nbformat
from analyzer.corrAnalyzer import *
# 페이지 설정
st.set_page_config(layout="wide")

st.title("Correlation Analysis", anchor=False)

# 데이터 로딩
df_yearly = pd.read_csv("useData/busanPortCorrScaled.csv", index_col=0, encoding='utf-8-sig')
df_monthly = pd.read_csv("useData/busanPortCorrMonthlyScaled.csv", index_col=0, encoding='utf-8-sig')

# 분석 객체
analyzerGTCT = CorrelationAnalyzer(df_yearly, 'GT(Gross Tonnage)', 'CT(Cargo Throughput)', time_col='Year',x_color='red',y_color='blue',scatter_color='darkorange')
analyzerCTST = CorrelationAnalyzer(df_monthly, 'CT(Cargo Throughput)', 'Stay Time', time_col='Date', x_color='blue',y_color='green',scatter_color='deepskyblue')

# 그래프
line1 = analyzerGTCT.plot_time_series("Yearly Trend of GT and CT in Busan Port")
scatter1, corr1, p1 = analyzerGTCT.analyze_and_plot()
line2 = analyzerCTST.plot_time_series("Monthly Trend of CT and Residence Time in Busan Port")
scatter2, corr2, p2 = analyzerCTST.analyze_and_plot()

# 탭 생성
tab1, tab2, tab3 = st.tabs(["Analysis Proccess(EN)", "Analysis Proccess(KR)", "Data Prep&EDA"])

# 탭1: English Analysis Process
with tab1:
    with st.container():
        st.markdown("""
        <span style='font-weight:bold; font-size:25px;'>Yearly Trends in GT (Gross Tonnage) and CT (Cargo Throughput)</span>""",unsafe_allow_html=True)

        st.plotly_chart(line1)

        st.markdown("""
        Both <span style='color:orange; font-weight:bold; font-size:20px;'>GT</span> and <span style='color:orange; font-weight:bold; font-size:20px;'>CT</span> show an overall increasing trend over the years. <br><br>

        - <span style='color:orange; font-weight:bold; font-size:20px;'>GT</span> steadily increased until 2019, experienced a slight drop in 2020, then <span style='color:orange; font-weight:bold; font-size:20px;'>sharply declined in 2021</span>.  
        In 2022, the value remained low, but in 2023, it <span style='color:orange; font-weight:bold; font-size:20px;'>surged again and recovered</span>.  
        This trend seems that <span style='color:orange; font-weight:bold; font-size:20px;'>COVID-19 had a significant impact</span> on maritime volume, particularly around 2020–2022.<br><br>

        - <span style='color:orange; font-weight:bold; font-size:20px;'>CT</span> also generally followed an upward trend, although there was a <span style='color:orange; font-weight:bold; font-size:20px;'>noticeable decline in 2020</span>,  
        which can also be attributed to the pandemic. From 2021 onwards, CT has been <span style='color:orange; font-weight:bold; font-size:20px;'>increasing gradually and stably</span>.<br><br>

        Despite the temporary anomalies caused by <span style='color:orange; font-weight:bold; font-size:20px;'>COVID-19</span>,  
        the <span style='color:orange; font-weight:bold; font-size:20px;'>long-term trajectory of both GT and CT remains upward</span>,  
        reflecting the resilience and eventual recovery of South Korea’s maritime trade.
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown(f"""
        <span style='font-weight:bold; font-size:25px;'>Correlation Between GT (Gross Tonnage) and CT (Cargo Throughput)</span>""", unsafe_allow_html=True)
        st.plotly_chart(scatter1)

        st.markdown(f"""
        The correlation coefficient between <span style='color:orange; font-weight:bold; font-size:20px;'>GT</span> and <span style='color:orange; font-weight:bold; font-size:20px;'>CT</span> is <span style='color:orange; font-weight:bold; font-size:20px;'>{round(corr1,4)}</span>, and the corresponding <span style='color:orange; font-weight:bold; font-size:20px;'>p-value is {round(p1,4)}</span>.<br>
        Since the <span style='color:orange; font-weight:bold; font-size:20px;'>p-value is less than 0.05</span>, this indicates that the correlation is <span style='color:orange; font-weight:bold; font-size:20px;'>statistically significant</span>.<br><br>
        Therefore, we can conclude that <span style='color:orange; font-weight:bold; font-size:20px;'>GT and CT have a meaningful positive correlation</span>.  
        In other words, as <span style='color:orange; font-weight:bold; font-size:20px;'>GT increases, CT tends to increase as well</span>.
        """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <span style='font-weight:bold; font-size:25px;'>Monthly Trends in CT (Cargo Throughput) and Stay Time</span>""",unsafe_allow_html=True)
        st.plotly_chart(line2)
        st.markdown("""
        <span style='color:orange; font-weight:bold; font-size:20px;'>In January 2015, there was a significant increase in vessel stay time</span> at the port.<br>
        This was mainly due to <span style='color:red; font-weight:bold;'>berthing congestion</span> and <span style='color:red; font-weight:bold;'>inefficient terminal operations</span>.<br>
        The <span style='font-weight:bold;'>number of vessels waiting over 12 hours</span> surged from 13 in 2013 to <span style='font-weight:bold;'>86 in 2015</span>, causing a dramatic increase in waiting time.  
        This occurred because <span style='color:orange; font-weight:bold; font-size:16px;'>different operators were managing each terminal, making flexible berth management difficult</span>.<br>
        <span style='font-size:14px;'>Source: <a href='https://www.yna.co.kr/view/AKR20170809074100051'>Yonhap News (2017)</a></span><br><br>

        <span style='color:orange; font-weight:bold; font-size:20px;'>In July 2017, Cargo Throughput (CT) dropped significantly</span>.<br>
        This was primarily caused by a <span style='color:red; font-weight:bold;'>decline in transshipment cargo</span> due to the <span style='color:red; font-weight:bold;'>U.S.-China trade conflict</span>.<br>
        The trade war between the U.S. and China led to a sharp drop in transshipment demand at Busan Port, where transshipment cargo accounted for <span style='font-weight:bold;'>more than half of the total cargo volume</span>.<br>
        <span style='font-size:14px;'>Source: <a href='https://en.yna.co.kr/view/AEN20190808002200320'>Yonhap News English (2019)</a></span><br><br>

        <span style='color:orange; font-weight:bold; font-size:20px;'>Between April and May 2018, CT surged</span>.<br>
        This was due to <span style='color:red; font-weight:bold;'>an increase in transshipment cargo</span> and the <span style='color:red; font-weight:bold;'>continued impact of the U.S.-China trade conflict</span>.<br>
        While import/export cargo volumes remained stagnant, <span style='font-weight:bold;'>transshipment cargo increased by more than 10%</span>, enhancing <span style='font-weight:bold;'>Busan Port’s role as a transshipment hub in Asia</span>.<br>
        <span style='font-size:14px;'>Source: <a href='https://www.yna.co.kr/view/AKR20181205136200051'>Yonhap News (2018)</a>, <a href='https://www.mk.co.kr/economy/view.php?no=766544&sc=50000001&year=2018'>Maeil Business News (2018)</a></span><br><br>

        <span style='color:orange; font-weight:bold; font-size:20px;'>In January 2020, seafarer stay time increased</span> significantly.<br>
        This was mainly caused by <span style='color:red; font-weight:bold;'>quarantine reinforcement</span> and <span style='color:red; font-weight:bold;'>concerns over onboard COVID-19 infection</span> due to the <span style='color:red; font-weight:bold;'>early response to the COVID-19 pandemic</span>.<br>
        At the time, some ships entering Busan Port had <span style='font-weight:bold;'>confirmed COVID-19 cases</span>, which led to <span style='font-weight:bold;'>full crew testing and isolation procedures</span>.<br>
        <span style='font-weight:bold;'>Disembarkation was delayed to prevent virus spread</span>, leading to a significant increase in stay times. In Gamcheon Port and other areas, <span style='font-weight:bold;'>more than 14 confirmed cases</span> were reported.<br>
        <span style='font-size:14px;'>Source: <a href='https://www.newsis.com/view/NISX20201013_0001195710'>Newsis (2020)</a>, <a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC10348537/'>PMC Study (2020)</a></span>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown(f"""
        <span style='font-weight:bold; font-size:25px;'>Correlation Between CT (Cargo Throughput) and Stay Time</span>""", unsafe_allow_html=True)
        st.plotly_chart(scatter2)
        st.markdown(f"""
        <span style='color:orange; font-weight:bold; font-size:20px;'>The correlation coefficient between CT</span> and <span style='color:orange; font-weight:bold; font-size:20px;'>vessel stay time</span> is <span style='color:orange; font-weight:bold; font-size:20px;'>{round(corr2,4)}</span>, and the corresponding <span style='color:orange; font-weight:bold; font-size:20px;'>p-value is {round(p2,4)}</span>.<br>
        <span style='font-size:15px;'>(Rounded to the fourth decimal place.)</span><br>
        <span style='color:orange; font-weight:bold; font-size:20px;'>Since the p-value is very close to 0</span>, this correlation is considered <span style='color:orange; font-weight:bold; font-size:20px;'>statistically significant</span>.<br><br>
        Therefore, it can be concluded that <span style='color:orange; font-weight:bold; font-size:20px;'>CT and vessel stay time have a meaningful positive correlation</span>.<br>
        In other words, <span style='color:orange; font-weight:bold; font-size:20px;'>as CT increases, vessel stay time tends to increase as well</span>.
        """, unsafe_allow_html=True)

# 탭2: 한국어 분석 프로세스
with tab2:
    # 설명 텍스트
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>부산항 시계열 및 상관관계 분석 개요</span><br><br>

    부산의 3개 항만 기준으로 볼 때, <span style='font-weight:bold; font-size:20px;'>입항 선박 수는 감소</span>하고 있는 반면, <span style='font-weight:bold; font-size:20px;'>화물 처리량(CT)은 증가</span>하는 추세를 보이고 있습니다. 이는 선사들이 운송 효율성을 높이기 위해 <span style='font-weight:bold; font-size:20px;'>더 대형의 카고선으로 대체 운항</span>했기 때문입니다.
    따라서 처리되는 화물량이 증가하면, <span style='font-weight:bold; font-size:20px;'>선박 및 선원들의 체류 시간도 늘어날 수 있으며</span>, 이는 곧 <span style='color:orange; font-weight:bold; font-size:20px;'>카고선 선원들이 부산항 인근 상권의 잠재적인 고객이 될 수 있음</span>을 시사합니다.<br>
    이러한 가설을 바탕으로, 본 페이지에서는 <span style='color:orange; font-weight:bold; font-size:20px'>시계열 분석</span> 및 <span style='color:orange; font-weight:bold; font-size:20px'>상관관계 분석</span>을 진행하고자 합니다.<br><br>
    본격적인 분석 이전에, 용어부터 정리하겠습니다.
    """, unsafe_allow_html=True)

    # 📘 용어 정리
    st.markdown("""
    ##### 주요 용어 정리

    - <span style='color:orange; font-weight:bold; font-size:20px;'>GT (Gross Tonnage)</span> : 입항 선박의 총 부피 (선박 수와 무게 포함)
    - <span style='color:orange; font-weight:bold; font-size:20px;'>CT (Cargo Throughput)</span> : 항만에서 처리되는 화물의 총량
    - <span style='color:orange; font-weight:bold; font-size:20px;'>체류 시간</span> : 선박(및 선원)이 항만에 머무는 시간
    - <span style='color:orange; font-weight:bold; font-size:20px;'>상관관계</span> : 두 변수 간 함께 변하는 경향이 있는지를 나타내는 개념
    - <span style='color:orange; font-weight:bold; font-size:20px;'>상관계수</span> : 상관관계를 -1 ~ 1 사이의 수치로 표현 (1에 가까울수록 양의 상관관계, -1에 가까울수록 음의 상관관계)
    - <span style='color:orange; font-weight:bold; font-size:20px;'>p-value</span> : 관찰된 상관관계가 우연히 발생했을 확률 (0.05보다 크면 통계적으로 유의미하지 않음)
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------------------
    # 연도별 GT-CT 라인그래프 설명
    st.plotly_chart(line1, key='line1')

    st.markdown("""
    GT와 CT 모두 <span style='font-weight:bold;font-size:20px; color:orange;'>전반적으로 증가하는 추세</span>를 보이지만, 중간에 <span style='font-weight:bold;font-size:20px;'>이상치(outlier)</span>가 확인됩니다.<br>
    <span style='font-weight:bold;font-size:20px;'>GT</span>는 2019년까지 꾸준히 증가하다, <span style='font-weight:bold;font-size:20px;'>2020년 소폭 감소, 2021년 급감, 2022년까지 하락세가 지속</span>됩니다. 이는 <span style='font-weight:bold;font-size:20px;'>COVID-19</span>로 인한 <span style='font-weight:bold; font-size:20px;'>감염 우려로 입항 선박 수가 감소</span>한 영향으로 보입니다.<br>
    <span style='font-weight:bold;font-size:20px;'>CT</span> 역시 2019년까지 증가하다가 <span style='font-weight:bold; font-size:20px;'>2020년 일시 감소</span>, 이후 <span style='font-weight:bold; font-size:20px;'>2021년부터 회복세</span>입니다. 이는 <span style='font-weight:bold; font-size:20px;'>입항 선박 수는 줄었지만, 선박당 화물량이 증가</span>해 수요를 충족한 결과로 해석됩니다.
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------------------
    # GT-CT 상관관계 분석
    st.plotly_chart(scatter1, key='scatter1')

    st.markdown(f"""
    <span style='font-weight:bold; font-size:20px;'>상관계수 : {round(corr1,4)} / 
    p-value : {round(p1,4)}</span><br>
    p-value가 0.05보다 작기 때문에 <span style='font-weight:bold; font-size:20px;'>통계적으로 유의미한 양의 상관관계</span>라고 판단할 수 있습니다.
    즉, <span style='color:orange; font-weight:bold; font-size:20px;'>GT가 증가할수록 CT도 함께 증가하는 경향</span>이 있습니다.
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------------------
    # 월별 CT - 체류 시간 추이
    st.plotly_chart(line2, key='line2')

    st.markdown("""
    CT와 체류시간 모두 <span style='font-weight:bold; font-size:20px;color:orange'>전반적으로 증가하는 추세</span>를 보이며, 특정 시점에 <span style='font-weight:bold; font-size:20px;'>이상치</span>가 나타납니다.<br>
    <span style='font-weight:bold; font-size:20px;'>체류시간</span>은 <span style='font-weight:bold; font-size:20px;'>2015년 1월부터 급증</span>하고 이후 CT를 어느정도 증감하는 모습을 보이다가 <span style='font-weight:bold; font-size:20px;'>2020년 1월에 급증</span>합니다.
    2015년에 급증한 이유는 당시 터미널 간의 운영사 분리로 인한 <span style='font-weight:bold; font-size:20px;'>운영의 비효율 및 병목 현상이 발생</span>했기 때문입니다. 그리고 2020년의 급증은 <span style='font-weight:bold; font-size:20px;'>코로나19의 초기 대응</span>으로 인한 검역 강화가 <span style='font-weight:bold; font-size:20px;'>하선 지연을 발생</span>시켰기 때문입니다.<br>
    <span style='font-weight:bold; font-size:20px;'>CT</span>는 <span style='font-weight:bold; font-size:20px;'>2017년 7월에 급격히 감소</span>하고 상승세를 타지 못하다가 <span style='font-weight:bold; font-size:20px;'>2018년 4-5월에 급격히 증가</span>합니다. 2017년 7월의 급격히 감소한 이유는 <span style='font-weight:bold; font-size:20px;'>미-중 관세갈등</span>에 따라 <span style='font-weight:bold; font-size:20px;'>환적화물의 수요가 급격히 감소</span>했기 때문입니다.
    그리고 2018년 4-5월에 다시 급증한 것은 관세갈등의 연장선으로 2019년 1월부터 <span style='font-weight:bold; font-size:20px;'>더욱 부과될 관세를 우려한 중국의 물량 선제 출하</span>가 원인입니다.<br>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------------------
    # CT - 체류 시간 상관관계
    st.plotly_chart(scatter2, key='scatter2')

    st.markdown(f"""
    <span style='font-weight:bold; font-size:20px;'>상관계수 : {round(corr2,4)} / 
    p-value : {round(p2,4)}</span><br>
    p-value가 0에 매우 가까우므로, <span style='font-weight:bold; font-size:20px;'>통계적으로 유의미한 양의 상관관계</span>임을 확인할 수 있습니다. 즉, <span style='color:orange; font-weight:bold; font-size:20px;'>화물 처리량(CT)이 증가할수록 선박의 체류 시간도 함께 증가</span>하는 경향이 있습니다.
    """, unsafe_allow_html=True)

    # 결론
    st.markdown("""
    ### 결론
    부산항의 화물 처리량과 선박(선원) 체류 시간이 시간이 지남에 따라 꾸준히 증가하고 있습니다. 이는 부산항에 입항하는 선박과 함께 유입되는 선원 수가 지속적으로 늘고 있다는 점을 보여줍니다. 이러한 흐름은 <span style='font-size:20px; font-weight:bold;'>온라인 선용품 쇼핑몰</span>과 <span style='font-size:20px; font-weight:bold;'>부산항 인근 상권의 잠재 고객층</span>이 확대되고 있음을 시사합니다. 따라서 <span style='color:orange; font-size:20px; font-weight:bold;'>부산항을 중심으로 한 온라인 선용품 쇼핑몰 구축</span>은 명확한 시장성과 고객 수요를 기반으로 추진할 수 있으며, <span style='color:orange; font-size:20px; font-weight:bold;'>충분한 잠재력이 존재</span>한다고 판단됩니다.
    """, unsafe_allow_html=True)

# 탭3: 데이터 준비 및 EDA
with tab3:
    # 노트북 파일 열기
    with open("sourceCode/busanPortCorrPrep.ipynb", "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # 코드 셀만 추출
    code_cells = [cell['source'] for cell in notebook.cells if cell['cell_type'] == 'code']
    code_content = '\n\n'.join(code_cells)

    # Streamlit에 코드박스로 표시
    st.code(code_content, language='python')
