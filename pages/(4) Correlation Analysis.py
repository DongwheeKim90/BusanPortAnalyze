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
analyzerGTCT = CorrelationAnalyzer(df_yearly, 'GT(Gross Tonnage)', 'CT(Cargo Throughput)', time_col='Year', x_color='red',y_color='blue',scatter_color='darkorange')
analyzerCTST = CorrelationAnalyzer(df_monthly, 'CT(Cargo Throughput)', 'Stay Time', time_col='Date', x_color='blue',y_color='green',scatter_color='deepskyblue')

# 그래프
line1 = analyzerGTCT.plot_time_series("Yearly Trend of GT and CT in Busan Port")
line2 = analyzerCTST.plot_time_series("Monthly Trend of CT and Residence Time in Busan Port")

# 탭 생성
tab1, tab2, tab3 = st.tabs(["Analysis Proccess(EN)", "Analysis Proccess(KR)", "Data Preprocessing"])

# 탭1: English Analysis Process
with tab1:
    # Description Text
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>Overview of Time-Series and Correlation Analysis for Busan Port</span><br>
    In the (3) Top 3 Ports in Busan page, visualizations of the three major ports in Busan show that while the <span style='font-weight:bold; font-size:20px;'>number of arriving ships is decreasing</span>, the <span style='font-weight:bold; font-size:20px;'>cargo throughput (CT) is increasing</span>. This is because shipping companies have been <span style='font-weight:bold; font-size:20px;'>switching to larger cargo ships to improve transportation efficiency</span>.<br>
    Based on the hypothesis that there is sufficient potential demand for an <span style='color:orange; font-weight:bold; font-size:20px'>online ship supplies shopping mall centered around Busan Port</span>, we conducted the following <span style='color:orange; font-weight:bold; font-size:20px'>time-series</span> and <span style='color:orange; font-weight:bold; font-size:20px'>correlation analyses</span>.
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("""
        - <span style='color:orange; font-weight:bold; font-size:20px;'>GT (Gross Tonnage)</span>: Total volume of arriving ships (including count and weight)
        - <span style='color:orange; font-weight:bold; font-size:20px;'>CT (Cargo Throughput)</span>: Total volume of cargo handled at the port
        - <span style='color:orange; font-weight:bold; font-size:20px;'>Residence Time</span>: Time the vessel (and crew) stays at the port
        - <span style='color:orange; font-weight:bold; font-size:20px;'>Correlation</span>: Concept indicating whether two variables tend to change together
        - <span style='color:orange; font-weight:bold; font-size:20px;'>Correlation Coefficient</span>: A value between -1 and 1 indicating the strength/direction of the correlation
        - <span style='color:orange; font-weight:bold; font-size:20px;'>p-value</span>: Probability that the observed correlation occurred by chance (not statistically significant if > 0.05)
        """, unsafe_allow_html=True)

    st.plotly_chart(line1)

    st.markdown("""
    The graph above visualizes the annual GT (Gross Tonnage) and CT (Cargo Throughput) of cargo ships arriving at Busan Port. Both GT and CT show a <span style='font-weight:bold;font-size:20px; color:orange;'>general upward trend</span>, though <span style='font-weight:bold;font-size:20px;'>outliers</span> are also identified.<br>
    <span style='font-weight:bold;font-size:20px;color:orange;'>GT</span> steadily increased until 2019, then slightly declined in 2020 and sharply dropped in 2021, continuing into 2022. This was mainly due to the <span style='font-weight:bold;font-size:20px;'>decrease in ship entries due to COVID-19 infection concerns</span>.<br>
    <span style='font-weight:bold;font-size:20px;color:orange;'>CT</span> also steadily increased until 2019, briefly declined in 2020, then <span style='font-weight:bold; font-size:20px;'>recovered in 2021</span>. This trend suggests that while the number of ships declined, <span style='font-weight:bold; font-size:20px;'>small/medium vessels were replaced by larger ones</span>, thereby <span style='font-weight:bold; font-size:20px;'>increasing cargo volume per vessel</span>.
    """, unsafe_allow_html=True)

    scatter1_en, corr1_en, p1_en = analyzerGTCT.analyze_and_plot(language='en')
    st.plotly_chart(scatter1_en)

    st.markdown(f"""
    The graph above shows a correlation analysis between GT and CT of cargo ships entering Busan Port. <span style='font-weight:bold; font-size:20px;color:orange'>Correlation Coefficient: {round(corr1_en,4)} / 
    p-value: {round(p1_en,4)}</span><br>
    Since the p-value is less than 0.05, it is interpreted as a <span style='font-weight:bold; font-size:20px;'>statistically significant positive correlation</span>.<br>
    In other words, <span style='color:orange; font-weight:bold; font-size:20px;'>as GT increases, CT also tends to increase</span>.
    """, unsafe_allow_html=True)

    st.markdown("""
    It has been confirmed that the gross tonnage (GT) of cargo ships—i.e., their size—correlates with increased cargo throughput (CT). Industry insights and GPT research also suggest that <span style='font-weight:bold; font-size:20px;'>larger ships tend to have more crew members</span>. Based on this, we hypothesized that <span style='font-weight:bold; font-size:20px;color:orange'>as cargo volume increases, unloading/loading times also increase, leading to longer vessel residence times</span>. Accordingly, we conducted the following <span style='font-weight:bold; font-size:20px;'>correlation analysis between cargo throughput and residence time</span>.
    """, unsafe_allow_html=True)

    st.plotly_chart(line2)

    st.markdown("""
    Both CT and residence time show a <span style='font-weight:bold; font-size:20px;color:orange'>general upward trend</span>, with some <span style='font-weight:bold; font-size:20px;'>outliers</span>.<br>
    <span style='font-weight:bold; font-size:20px;color:orange;'>Residence time</span> increased sharply from <span style='font-weight:bold; font-size:20px;'>January 2015</span> and then fluctuated somewhat in line with CT trends, with another sharp increase in <span style='font-weight:bold; font-size:20px;'>January 2020</span>.<br>
    The 2015 spike was due to <span style='font-weight:bold; font-size:20px;'>inefficient operations and bottlenecks</span> caused by divided terminal operators. The 2020 spike was attributed to <span style='font-weight:bold; font-size:20px;'>stricter quarantine procedures during the initial COVID-19 response, delaying crew disembarkation</span>.<br>
    Meanwhile, <span style='font-weight:bold; font-size:25px;color:orange;'>CT</span> dropped sharply in <span style='font-weight:bold; font-size:20px;'>July 2017</span> but rebounded significantly in <span style='font-weight:bold; font-size:20px;'>April–May 2018</span>.<br>
    The 2017 drop was due to a <span style='font-weight:bold; font-size:20px;'>decline in transshipment demand</span> at Busan Port triggered by <span style='font-weight:bold; font-size:20px;'>U.S.–China tariff conflicts</span>. The 2018 rebound was driven by <span style='font-weight:bold; font-size:20px;'>China preemptively shipping goods ahead of the tariffs scheduled for January 2019</span>.
    """, unsafe_allow_html=True)

    scatter2_en, corr2_en, p2_en = analyzerCTST.analyze_and_plot(language='en')
    st.plotly_chart(scatter2_en)

    st.markdown(f"""
    The graph above visualizes the correlation between cargo ship residence time and CT at Busan Port. <span style='font-weight:bold; font-size:20px;color:orange'>Correlation Coefficient: {round(corr2_en,4)} / 
    p-value: {round(p2_en,4)}</span><br>
    Since the p-value is very close to 0, we can conclude there is a <span style='font-weight:bold; font-size:20px;'>statistically significant positive correlation</span>.<br>
    That is, <span style='color:orange; font-weight:bold; font-size:20px;'>as cargo throughput (CT) increases, so does the vessel's residence time</span>.
    """, unsafe_allow_html=True)

    # Conclusion
    st.subheader('Conclusion', False)
    st.markdown("""
    Cargo throughput and vessel (crew) residence times at Busan Port have been steadily increasing over time. This indicates a continuous rise in the number of crew members entering via vessels.<br>
    Such trends point to an <span style='font-size:20px; font-weight:bold;color:orange'>expanding potential customer base</span> for both an <span style='font-size:20px; font-weight:bold;color:orange'>online ship supplies mall</span> and <span style='font-size:20px; font-weight:bold;color:orange'>local businesses near Busan Port</span>. Therefore, the data from this correlation analysis <span style='color:orange; font-size:20px; font-weight:bold;'>provides strong justification</span> for building an online ship supplies mall centered on Busan Port based on clear market viability and demand.
    """, unsafe_allow_html=True)

# 탭2: 한국어 분석 프로세스
with tab2:
    # 설명 텍스트
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>부산항 시계열 및 상관관계 분석 개요</span><br>
    (3)Top 3 Ports in Busan 페이지에서 부산 3개 항구 시각화 결과, <span style='font-weight:bold; font-size:20px;'>입항 선박 수는 감소</span>하고 있는 반면, <span style='font-weight:bold; font-size:20px;'>화물 처리량(CT)은 증가</span>하는 추세를 보이고 있습니다. 이는 선사들이 운송 효율성을 높이기 위해 <span style='font-weight:bold; font-size:20px;'>대형 카고선으로 대체 운항</span>했기 때문입니다.
    따라서 <span style='color:orange; font-weight:bold; font-size:20px'>부산항을 중심으로 한 온라인 선용품 쇼핑몰 구축</span>에 있어 잠재고객은 충분할 것이다 라는 가설을 바탕으로, 아래와 같이 <span style='color:orange; font-weight:bold; font-size:20px'>시계열</span> 및 <span style='color:orange; font-weight:bold; font-size:20px'>상관관계 분석</span>을 진행했습니다.<br>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # 용어 정리
        st.markdown("""
        - <span style='color:orange; font-weight:bold; font-size:20px;'>GT (Gross Tonnage)</span> : 입항 선박의 총 부피 (선박 수와 무게 포함)
        - <span style='color:orange; font-weight:bold; font-size:20px;'>CT (Cargo Throughput)</span> : 항만에서 처리되는 화물의 총량
        - <span style='color:orange; font-weight:bold; font-size:20px;'>체류 시간</span> : 선박(및 선원)이 항만에 머무는 시간
        - <span style='color:orange; font-weight:bold; font-size:20px;'>상관관계</span> : 두 변수 간 함께 변하는 경향이 있는지를 나타내는 개념
        - <span style='color:orange; font-weight:bold; font-size:20px;'>상관계수</span> : 상관관계를 -1 ~ 1 사이의 수치로 표현 (1에 가까울수록 양의 상관관계, -1에 가까울수록 음의 상관관계)
        - <span style='color:orange; font-weight:bold; font-size:20px;'>p-value</span> : 관찰된 상관관계가 우연히 발생했을 확률 (0.05보다 크면 통계적으로 유의미하지 않음)
        """, unsafe_allow_html=True)

    # 연도별 GT-CT 라인그래프 설명
    st.plotly_chart(line1, key='line1')

    st.markdown("""
    위 그래프는 년간 부산항에 입항되는 카고선 기준 GT(Gross Tonnage)와 CT(Cargo Throughput)에 대한 시계열 시각화 자료입니다. GT(Gross Tonnage)와 CT(Cargo Throughput) 모두 <span style='font-weight:bold;font-size:20px; color:orange;'>전반적으로 증가하는 추세</span>를 보이지만, 중간에 <span style='font-weight:bold;font-size:20px;'>이상치(outlier)</span>가 확인됩니다.<br>
    <span style='font-weight:bold;font-size:20px;color:orange;'>GT(Gross Toannge)</span>는 2019년까지 꾸준히 증가세를 보이다가, <span style='font-weight:bold;font-size:20px;'>2020년 소폭 감소 후 2021년 급감</span>하였으며, 이러한 하락세는 2022년까지 이어졌습니다. 이는 <span style='font-weight:bold;font-size:20px;'>COVID-19</span>로 인한 <span style='font-weight:bold; font-size:20px;'>감염 우려로 인해 입항 선박 수가 감소</span>한 것이 주요 원인으로 작용했습니다.<br>
    <span style='font-weight:bold;font-size:20px;color:orange;'>CT(Cargo Throughput)</span> 또한 2019년까지는 지속적으로 증가하다가 <span style='font-weight:bold; font-size:20px;'>2020년 일시 감소</span>했으나, <span style='font-weight:bold; font-size:20px;'>2021년부터 다시 회복세</span>로 전환되었습니다. 이는 입항 선박 수는 감소했지만, <span style='font-weight:bold; font-size:20px;'>소/중형의 선박이 대형으로 대체</span>되면서 <span style='font-weight:bold; font-size:20px;'>선박 한 척당 처리하는 화물량이 증가</span>했기 때문으로 해석할 수 있습니다.
    """, unsafe_allow_html=True)

    # GT-CT 상관관계 분석
    scatter1_kr, corr1_kr, p1_kr = analyzerGTCT.analyze_and_plot(language='kr')
    st.plotly_chart(scatter1_kr, key='scatter1')

    st.markdown(f"""
    위 그래프는 부산항에 입항되는 카고선의 GT와 CT에 대한 상관관계 분석을 시각화한 결과입니다. <span style='font-weight:bold; font-size:20px;color:orange'>상관계수 : {round(corr1_kr,4)} / 
    p-value : {round(p1_kr,4)}</span><br>
    p-value가 0.05보다 작기 때문에 <span style='font-weight:bold; font-size:20px;'>통계적으로 유의미한 양의 상관관계</span>라고 판단할 수 있습니다.
    즉, <span style='color:orange; font-weight:bold; font-size:20px;'>GT가 증가할수록 CT도 함께 증가하는 경향</span>이 있습니다.
    """, unsafe_allow_html=True)

    # 월별 CT - 체류 시간 추이
    st.markdown("""
    카고선의 총톤수(GT, Gross Tonnage), 즉 선박의 크기가 커질수록 컨테이너 처리량(CT, Container Throughput) 또한 증가한다는 경향이 있음을 확인하였습니다. 또한 인터넷 자료 및 GPT를 통해 선박 규모가 클수록 승선 인원 수도 증가한다는 업계의 일반적인 사실을 파악하였습니다. 이를 바탕으로, <span style='font-weight:bold; font-size:20px;color:orange'>물동량이 증가할수록
    양하 및 양륙 작업에 소요되는 시간이 길어져 선박의 항만 체류시간 또한 증가할 것</span>이라는 가설을 설정하였습니다. 이러한 가설에 따라, <span style='font-weight:bold; font-size:20px;'>물동량과 선사별 체류시간 간의 상관관계를 아래와 같이 분석</span>했습니다.
    """,unsafe_allow_html=True)

    st.plotly_chart(line2, key='line2')

    st.markdown("""
    CT(Cargo Throughput)와 체류시간 모두 <span style='font-weight:bold; font-size:20px;color:orange'>전반적으로 증가하는 추세</span>를 보이며, 특정 시점에서는 <span style='font-weight:bold; font-size:20px;'>이상치(outlier)</span>가 관찰됩니다.<br>
    <span style='font-weight:bold; font-size:20px;color:orange;'>체류시간</span>은 <span style='font-weight:bold; font-size:20px;'>2015년 1월부터 급증</span>한 후, 이후에는 CT의 흐름을 어느 정도 따라 증감하는 양상을 보이다가, <span style='font-weight:bold; font-size:20px;'>2020년 1월에 다시 한 번 급증</span>합니다.
    2015년 체류시간이 급증한 원인으로, 당시 터미널 간의 운영사가 분리되면서 발생한 <span style='font-weight:bold; font-size:20px;'>비효율적인 운영 및 병목 현상</span>이 있습니다. 또한 2020년의 급증은 <span style='font-weight:bold; font-size:20px;'>COVID-19의 초기 대응 과정에서 검역 절차가 강화되고, 이에 따라 선원들의 하선이 지연</span>된 영향으로 해석할 수 있습니다.<br>
    한편 <span style='font-weight:bold; font-size:25px;color:orange;'>CT</span>는 <span style='font-weight:bold; font-size:20px;'>2017년 7월에 급격히 감소</span>한 뒤, <span style='font-weight:bold; font-size:20px;'>2018년 4 ~ 5월에 급격히 증가</span>합니다.
    2017년 7월의 감소는 <span style='font-weight:bold; font-size:20px;'>미·중 간 관세 갈등</span>으로 인해, 부산항의 물동량 중 상당 부분을 차지하던 <span style='font-weight:bold; font-size:20px;'>환적화물 수요가 급감</span>한 것이 주요 원인입니다.
    이후 2018년 4 ~ 5월의 급증은 <span style='font-weight:bold; font-size:20px;'>2019년 1월부터 부과 예정인 추가 관세에 대한 우려</span>로, 중국이 <span style='font-weight:bold; font-size:20px;'>사전에 물량을 선제 출하한 결과</span>로 분석됩니다.
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------------------
    # CT - 체류 시간 상관관계
    scatter2_kr, corr2_kr, p2_kr = analyzerCTST.analyze_and_plot(language='kr')
    st.plotly_chart(scatter2_kr, key='scatter2')

    st.markdown(f"""
    위 그래프는 부산항에 입항한 카고선의 체류시간과 CT에 대한 상관관계를 시각화 분석한 결과입니다. <span style='font-weight:bold; font-size:20px;color:orange'>상관계수 : {round(corr2_kr,4)} / 
    p-value : {round(p2_kr,4)}</span><br>
    p-value가 0에 매우 가까우므로, <span style='font-weight:bold; font-size:20px;'>통계적으로 유의미한 양의 상관관계</span>임을 확인할 수 있습니다. 즉, <span style='color:orange; font-weight:bold; font-size:20px;'>화물 처리량(CT)이 증가할수록 선박의 체류 시간도 함께 증가</span>한다는 결론을 도출했습니다.
    """, unsafe_allow_html=True)

    # 결론
    st.subheader('결론',False)
    st.markdown("""
    부산항의 화물 처리량과 선박(선원) 체류 시간이 시간이 지남에 따라 꾸준히 증가하고 있습니다. 이는 부산항에 입항하는 선박과 함께 유입되는 선원 수가 지속적으로 늘고 있다는 점을 보여줍니다. 이러한 흐름은 
    <span style='font-size:20px; font-weight:bold;color:orange'>온라인 선용품 쇼핑몰</span>과 <span style='font-size:20px; font-weight:bold;color:orange'>부산항 인근 상권의 잠재 고객층</span>이 확대되고 있다는 점을 보여주며, 따라서 해당 상관관계 분석 결과에 대한 데이터는 <span style='color:orange; font-size:20px; font-weight:bold;'>부산항을 중심으로 한 온라인 선용품 쇼핑몰 구축</span>은 명확한 시장성과 고객 수요를 기반으로 추진할 수 있는 타당한 근거자료가 됩니다.</br>
    """, unsafe_allow_html=True)

# 탭3: 데이터 준비 및 EDA
with tab3:
    def jupyter_reader(path:str):
        # 노트북 파일 열기
        with open(path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # 코드 셀만 추출
        code_cells = [cell['source'] for cell in notebook.cells if cell['cell_type'] == 'code']
        code_content = '\n\n'.join(code_cells)
        return code_content
    codeCTC = jupyter_reader('./sourceCode/busanCargoThroughput.ipynb')
    codeCP = jupyter_reader('./sourceCode/busanPortCorrPrep.ipynb')

    st.markdown('''
    (1) Data Source : https://www.chainportal.co.kr/nexacro/index.html?screenid=screen_main <br>
    (2) Collected Data : Data collection of montly cargo throughput for the entire Port of Busan(월별 부산항 전체항구의 화물처리량 데이터 수집)<br>
    (3) Data Type : Structured Data(정형 데이터)<br>
    (4) Technologies Used : Selenium, Pandas, Scikit-learn<br>
    (5) Data Collection and Preprocessing Process
    ''',unsafe_allow_html=True)
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Collection (데이터 수집)</span>", unsafe_allow_html=True)
    st.video("./useData/busanCargoThroughput.mp4")
    # Streamlit에 코드박스로 표시
    st.code(codeCTC, language='python')
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Preprocessing (데이터 가공)</span>", unsafe_allow_html=True)
    st.code(codeCP, language='python')
