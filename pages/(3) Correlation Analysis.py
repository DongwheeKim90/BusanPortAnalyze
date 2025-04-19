import streamlit as st
import pandas as pd
import nbformat
from analyzer.analyzer import *

# 페이지 설정
st.set_page_config(
    page_title="Correlation Analysis",
    layout="wide"
)

# 📦 데이터 로딩
df_yearly = pd.read_csv("useData/busanPortCorrScaled.csv", index_col=0, encoding='utf-8-sig')
df_monthly = pd.read_csv("useData/busanPortCorrMonthlyScaled.csv", index_col=0, encoding='utf-8-sig')

# 🔍 분석 객체
analyzerGTCT = CorrelationAnalyzer(df_yearly, 'GT(Gross Tonnage)', 'CT(Cargo Throughput)', time_col='Year',x_color='red',y_color='blue',scatter_color='darkorange')
analyzerCTST = CorrelationAnalyzer(df_monthly, 'CT(Cargo Throughput)', 'Stay Time', time_col='Date', x_color='blue',y_color='green',scatter_color='deepskyblue')

# 📊 그래프
line1 = analyzerGTCT.plot_time_series("GT and CT")
scatter1, corr1, p1 = analyzerGTCT.analyze_and_plot()
line2 = analyzerCTST.plot_time_series("CT and Stay Time")
scatter2, corr2, p2 = analyzerCTST.analyze_and_plot()

# 페이지 타이틀
st.title("📊 Correlation Analysis")

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
        st.divider()
        st.plotly_chart(scatter2)

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