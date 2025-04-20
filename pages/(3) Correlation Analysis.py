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
line1 = analyzerGTCT.plot_time_series("GT and CT")
scatter1, corr1, p1 = analyzerGTCT.analyze_and_plot()
line2 = analyzerCTST.plot_time_series("CT and Stay Time")
scatter2, corr2, p2 = analyzerCTST.analyze_and_plot()

# 탭 생성
tab1, tab2, tab3 = st.tabs(["Analysis Proccess(EN)", "Analysis Proccess(KR)", "Data Prep&EDA"])

# 탭1: English Analysis Process
with tab1:
    with st.container(border=True):
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
    
    with st.container(border=True):
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
    with st.container(border=True):
        st.markdown("""
        <span style='font-weight:bold; font-size:25px;'>연도별 GT(Gross Tonnage)와 CT(Cargo Throughput) 추이 분석</span>
        """, unsafe_allow_html=True)

        st.plotly_chart(line1, key="line1")

        st.markdown("""
        <span style='color:orange; font-weight:bold; font-size:20px;'>GT</span>와 <span style='color:orange; font-weight:bold; font-size:20px;'>CT</span> 모두 전반적으로 증가하는 추세를 보이고 있습니다.<br><br>

        - <span style='color:orange; font-weight:bold; font-size:20px;'>GT</span>는 2019년까지 꾸준히 증가하다가, 2020년에 소폭 감소하고  
        <span style='color:orange; font-weight:bold; font-size:20px;'>2021년에 급감</span>하는 모습을 보였습니다.  
        2022년에는 낮은 수치를 유지하다가, 2023년에 <span style='color:orange; font-weight:bold; font-size:20px;'>다시 급증하며 회복세</span>를 나타냈습니다.  
        이는 <span style='color:orange; font-weight:bold; font-size:20px;'>코로나19의 영향이 매우 크다고</span> 볼 수 있습니다.<br><br>

        - <span style='color:orange; font-weight:bold; font-size:20px;'>CT</span> 역시 전반적인 증가 추세를 보였지만  
        <span style='color:orange; font-weight:bold; font-size:20px;'>2020년에 뚜렷한 감소</span>가 나타났고,  
        이후 <span style='color:orange; font-weight:bold; font-size:20px;'>2021년부터 완만하게 증가</span>하는 양상을 보이고 있습니다.<br><br>

        결론적으로, <span style='color:orange; font-weight:bold; font-size:20px;'>코로나19라는 변수로 인해 일시적인 이상치가 발생했지만</span>,  
        <span style='color:orange; font-weight:bold; font-size:20px;'>GT와 CT 모두 장기적으로는 상승세</span>를 유지하고 있으며,  
        이는 우리나라 해운물류의 회복력과 성장 가능성을 보여줍니다.
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown(f"""
        <span style='font-weight:bold; font-size:25px;'>GT(Gross Tonnage)와 CT(Cargo Throughput)의 상관관계</span>""", unsafe_allow_html=True)
        st.plotly_chart(scatter1,key='scatter1')
        st.markdown(f"""
            <span style='color:orange; font-weight:bold; font-size:20px;'>GT</span>와 <span style='color:orange; font-weight:bold; font-size:20px;'>CT</span> 사이의 상관계수는 <span style='color:orange; font-weight:bold; font-size:20px;'>{round(corr1,4)}</span>이고, 대응하는 <span style='color:orange; font-weight:bold; font-size:20px;'>p-value는 {round(p1,4)}</span>입니다.<br>
            <span style='color:orange; font-weight:bold; font-size:20px;'>p-value가 0.05보다 작기 때문에</span>, 이 상관관계는 <span style='color:orange; font-weight:bold; font-size:20px;'>통계적으로 유의미하다</span>고 할 수 있습니다.<br><br>
            따라서 <span style='color:orange; font-weight:bold; font-size:20px;'>GT와 CT는 유의미한 양의 상관관계를 가진다</span>고 결론지을 수 있습니다.  
            즉, <span style='color:orange; font-weight:bold; font-size:20px;'>GT가 증가할수록 CT도 함께 증가하는 경향</span>이 있습니다.
            """, unsafe_allow_html=True)
        
    with st.container(border=True):
        st.markdown("""
        <span style='font-weight:bold; font-size:25px;'>월별 CT(Cargo Throughput)와 체류 시간 추이 분석</span>
        """, unsafe_allow_html=True)
        st.plotly_chart(line2,key='line2')
        with st.container(border=True):
            st.markdown("#### 예시 1")
            with st.expander("**📌 2015년 1월 – 선박 체류시간 급증**"):
                st.markdown("""
                - **원인:** <span style='color:red; font-weight:bold;'>체선 현상</span> 및 <span style='color:red; font-weight:bold;'>터미널 간 운영 비효율</span><br>
                - **설명:**<br>
                12시간 이상 대기한 선박 수가 2013년 13척에서 2015년 86척으로 급증했습니다.  
                이는 터미널 간 유연한 선석 운영이 어려웠기 때문입니다.<br>
                - <span style='font-size:14px;'>출처: <a href='https://www.yna.co.kr/view/AKR20170809074100051' target='_blank'>연합뉴스 (2017)</a></span>
                """, unsafe_allow_html=True)

            with st.expander("**📌 2017년 7월 – Cargo Throughput 급감**"):
                st.markdown("""
                - **원인:** <span style='color:red; font-weight:bold;'>미·중 무역 갈등</span>으로 인한 <span style='color:red; font-weight:bold;'>환적 화물 감소</span><br>
                - **설명:**<br>
                미국과 중국의 관세 전쟁 여파로 부산항의 환적 수요가 급감했습니다.  
                환적 화물은 부산항 전체 물동량의 절반 이상을 차지하고 있었기 때문에 큰 영향을 받았습니다.<br>
                - <span style='font-size:14px;'>출처: <a href='https://en.yna.co.kr/view/AEN20190808002200320' target='_blank'>연합뉴스 영어판 (2019)</a></span>
                """, unsafe_allow_html=True)

            with st.expander("**📌 2018년 4~5월 – 컨테이너 처리량(CT) 급증**"):
                st.markdown("""
                - **원인:** <span style='color:red; font-weight:bold;'>환적 화물 증가</span> 및 <span style='color:red; font-weight:bold;'>미·중 무역 갈등 영향</span><br>
                - **설명:**<br>
                수출입 화물은 정체된 반면, 환적 화물은 10% 이상 증가하면서  
                부산항이 아시아 환적 허브로서의 기능을 더욱 강화하게 되었습니다.<br>
                - <span style='font-size:14px;'>출처: <a href='https://www.yna.co.kr/view/AKR20181205136200051' target='_blank'>연합뉴스 (2018)</a>, <a href='https://www.mk.co.kr/economy/view.php?no=766544&sc=50000001&year=2018' target='_blank'>매일경제 (2018)</a></span>
                """, unsafe_allow_html=True)

            with st.expander("**📌 2020년 1월 – 선원 체류시간 증가**"):
                st.markdown("""
                - **원인:** <span style='color:red; font-weight:bold;'>COVID-19 팬데믹 초기 대응</span>으로 인한 <span style='color:red; font-weight:bold;'>검역 강화</span> 및 <span style='color:red; font-weight:bold;'>선박 내 감염 우려</span><br>
                - **설명:**<br>
                부산항에 입항한 일부 선박에서 COVID-19 확진자가 발생하였고,  
                이에 따라 선원 전원에 대한 전수 검사 및 격리 조치가 시행되었습니다.  
                감염 확산 방지를 위한 하선 지연으로 체류 시간이 급증했으며,  
                실제로 감천항 등에서 14명 이상의 확진 사례도 보고되었습니다.<br>
                - <span style='font-size:14px;'>출처: <a href='https://www.newsis.com/view/NISX20201013_0001195710' target='_blank'>Newsis 보도 (2020)</a>, <a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC10348537/' target='_blank'>PMC 연구 (2020)</a></span>
                """, unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("#### 예시 2")
            with st.expander("**추이 분석 및 이상치 원인 탐색**"):
                st.markdown("""
                <span style='color:orange; font-weight:bold; font-size:20px;'>2015년 1월, 선박 체류시간이 급격히 증가</span>하는 현상이 발생했습니다.<br>
                이는 <span style='color:red; font-weight:bold;'>체선 현상</span>과 <span style='color:red; font-weight:bold;'>터미널 간 운영의 비효율성</span>이 주요 원인으로 분석됩니다.<br>
                <span style='font-weight:bold;'>12시간 이상 대기한 선박 수</span>가 2013년 13척에서 2015년에는 <span style='font-weight:bold;'>86척으로 급증</span>하며 대기 시간이 급격히 증가했습니다.  
                이는 <span style='color:orange; font-weight:bold; font-size:16px;'>터미널 간 운영사가 달라 유연한 선석 운영이 어려웠기 때문</span>입니다.<br>
                <span style='font-size:14px;'>출처: <a href='https://www.yna.co.kr/view/AKR20170809074100051'>연합뉴스 보도 (2017)</a></span><br><br>

                <span style='color:orange; font-weight:bold; font-size:20px;'>2017년 7월에는 Cargo Throughput(CT)이 급감</span>했습니다.<br>
                이는 <span style='color:red; font-weight:bold;'>미·중 무역 갈등</span>으로 인한 <span style='color:red; font-weight:bold;'>환적 화물 감소</span>가 주요 원인이었습니다.<br>
                미국과 중국의 관세 전쟁 여파로 부산항의 환적 수요가 급감했고, 환적 화물은 <span style='font-weight:bold;'>부산항 전체 물동량의 절반 이상</span>을 차지하고 있었기 때문입니다. 
                <br>
                <span style='font-size:14px;'>출처: <a href='https://en.yna.co.kr/view/AEN20190808002200320'>연합뉴스 영어판 (2019)</a></span><br><br>

                <span style='color:orange; font-weight:bold; font-size:20px;'>2018년 4월부터 5월 사이에는 CT가 급증</span>했습니다.<br>
                이는 <span style='color:red; font-weight:bold;'>환적 화물의 증가</span>와 <span style='color:red; font-weight:bold;'>미·중 무역 갈등</span>의 지속적인 영향 때문입니다.<br>
                수출입 화물은 정체된 반면, <span style='font-weight:bold;'>환적 화물은 10% 이상 증가</span>하면서 <span style='font-weight:bold;'>부산항이 아시아 환적 허브로서의 기능을 강화</span>하게 되었습니다.<br>
                <span style='font-size:14px;'>출처: <a href='https://www.yna.co.kr/view/AKR20181205136200051'>연합뉴스 (2018)</a>, <a href='https://www.mk.co.kr/economy/view.php?no=766544&sc=50000001&year=2018'>매일경제 (2018)</a></span><br><br>
                                    
                <span style='color:orange; font-weight:bold; font-size:20px;'>2020년 1월에는 선원 체류시간이 증가</span>하는 현상이 뚜렷하게 나타났습니다.<br>
                이는 <span style='color:red; font-weight:bold;'>COVID-19 팬데믹 초기 대응</span>으로 인한 <span style='color:red; font-weight:bold;'>검역 강화</span> 및 <span style='color:red; font-weight:bold;'>선박 내 감염 우려</span>가 주요 원인으로 작용했습니다.<br>
                당시 부산항에 입항한 일부 선박에서 <span style='font-weight:bold;'>COVID-19 확진자가 발생</span>하였고, 이에 따라 <span style='font-weight:bold;'>선원 전원에 대한 전수 검사 및 격리 조치</span>가 시행되었습니다.<br>
                <span style='font-weight:bold;'>감염 확산 방지를 위해 선원들의 하선이 지연</span>되면서 체류 시간이 급증했으며, 실제로 감천항 등에서는 <span style='font-weight:bold;'>14명 이상 확진된 사례</span>도 보고되었습니다.<br>
                <span style='font-size:14px;'>출처: <a href='https://www.newsis.com/view/NISX20201013_0001195710'>Newsis 보도 (2020)</a>, <a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC10348537/'>PMC 연구 (2020)</a></span>
                """, unsafe_allow_html=True)

        st.divider()

        st.markdown(f"""
        <span style='font-weight:bold; font-size:25px;'>CT(Cargo Throughput)와 체류 시간의 상관관계</span>""", unsafe_allow_html=True)
        st.plotly_chart(scatter2,key='scatter2')
        st.markdown(f"""
        <span style='color:orange; font-weight:bold; font-size:20px;'>CT</span>와 <span style='color:orange; font-weight:bold; font-size:20px;'>체류 시간</span> 사이의 상관계수는 <span style='color:orange; font-weight:bold; font-size:20px;'>{round(corr2,4)}</span>이고, 대응하는 <span style='color:orange; font-weight:bold; font-size:20px;'>p-value는 {round(p2,4)}</span>입니다.<br>
        <span systle='font-size:5px;'>(소수점 넷째 자리까지 반올림 한 수치입니다.)<br>
        <span style='color:orange; font-weight:bold; font-size:20px;'>p-value가 0과 매우 가깝기 때문에</span>, 이 상관관계는 <span style='color:orange; font-weight:bold; font-size:20px;'>통계적으로 유의미하다</span>고 할 수 있습니다.<br><br>
        따라서 <span style='color:orange; font-weight:bold; font-size:20px;'>CT와 체류 시간은 유의미한 양의 상관관계를 가진다</span>고 결론지을 수 있습니다.  
        즉, <span style='color:orange; font-weight:bold; font-size:20px;'>CT가 증가할수록 체류 시간도 증가하는 경향</span>이 있습니다.
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