import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page layout to wide (Streamlit 페이지 레이아웃을 와이드로 설정)
st.set_page_config(layout="wide")

st.title("Results of the Project Analysis", anchor=False)

tab_1, tab_2 = st.tabs(["Conclusion Content(EN)","Conclusion Content(KR)"])

with tab_1:
    st.subheader("We conducted a data analysis from the perspective of the Busan Port Authority to identify and develop services that could be offered to foreign shipping companies registered as its member firms.", anchor=False)

    st.subheader("1. Data Collection and Objectives", anchor=False)
    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>Building an Online Ship Supplies Platform</span>
    ''', unsafe_allow_html=True)
    kr_data_1 = pd.DataFrame({
        "Collected Data": [
            "Yearly data on cargo ship entries and cargo throughput at Korean ports",
            "Yearly cargo ship entries and GT (Gross Tonnage) at Busan ports",
            "Yearly cargo ship entries and Cargo Throughput at Busan ports",
            "Vessel dwell time data by shipping company at Busan SinHang port",
            "Annual sales volume and sales amount of ship supplies",
            "Company data related to ship supply product categories",
            "SNS data related to product categories",
            "Warehouse vacancy data"
        ],
        "Data Collected": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
        "Purpose of Collection": [
            "Identify ports with the highest number of ship entries and cargo throughput",
            "Analyze trends and correlations between ship entries and 'ship + cargo volume' across Busan's three major ports",
            "Analyze trends and correlations between ship entries and cargo throughput across Busan's three major ports",
            "Identify vessel dwell time quartiles by shipping company in Busan",
            "Select product categories for the online ship supplies platform",
            "Source suppliers for the online ship supplies platform",
            "Utilize for sourcing companies and marketing based on specific products",
            "Secure logistics warehouse hubs for the online platform"
        ],
        "Data Utilization": [
            "Visual analysis of maximum foreign ship entries and cargo throughput",
            "Analyze correlation between GT (Gross Tonnage) and CT (Cargo Throughput) of foreign ships entering Busan",
            "Analyze correlation between CT (Cargo Throughput) and GT (Gross Tonnage) of foreign ships entering Busan",
            "Analyze dwell time quartiles and their correlation with CT (Cargo Throughput)",
            "Select long-term and competitive ship supplies",
            "Identify domestic companies and Busan-area companies for sourcing",
            "Conduct indirect demand analysis for ship supplies based on foreign data",
            "Support logistics hub planning and budget allocation"
        ]
        })
    st.dataframe(kr_data_1, hide_index=True, use_container_width=True)

    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>Time-Based Busan Tourism Recommendations</span>
    ''', unsafe_allow_html=True)
    kr_data_2 = pd.DataFrame({
        "Collected Data": [
            "Vessel dwell time data by shipping company at Busan SinHang Port",
            "Busan tourist attraction data",
            "Busan local restaurant data",
            "Busan accommodation data"
        ],
        "Data Collected": ["✅", "✅", "✅", "✅"],
        "Purpose of Collection": [
            "Identify dwell time distribution of crew members upon entry",
            "Recommend tourist attractions based on dwell time",
            "Recommend restaurants based on dwell time",
            "Recommend accommodations based on dwell time"
        ],
        "Data Utilization": [
            "Group crew members based on dwell time",
            "Provide Busan travel courses by group based on dwell time",
            "Provide Busan travel courses by group based on dwell time",
            "Provide Busan travel courses by group based on dwell time"
        ]
        })
    st.dataframe(kr_data_2, hide_index=True, use_container_width=True)

    st.subheader("2. Process of Data Analysis", anchor=False)
    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>GT (Gross Tonnage) and CT (Cargo Throughput) at Busan Port</span>
    ''', unsafe_allow_html=True)
    col_1, col_2 = st.columns(2)
    with col_1:
        st.image("./useData/conclusion_img/busan_ship_gt.png")
        st.image("./useData/conclusion_img/busan_gt_trend.png")
    with col_2:
        with st.container(border=True):
            st.markdown('''
            <br>
            <br>
            <br>
            Busan is the port with the highest number of foreign vessel arrivals and <span style='color:Orange; font-weight:bold; font-size:16px;'>CT (Cargo Throughput)</span> in South Korea. While the <span style='color:Orange; font-weight:bold; font-size:16px;'>annual total volume of vessels, measured by GT (Gross Tonnage), continues to rise</span>, the number of arriving ships shows a declining trend.<br>
            Time-series analysis indicates that <span style='color:Orange; font-weight:bold; font-size:16px;'>the total GT (Gross Tonnage) of vessels entering Busan Port is steadily increasing</span>.<br>
            This trend reflects the maritime logistics industry’s pursuit of efficiency, as most shipping companies are <span style='color:white; font-weight:bold; font-size:18px;'>transitioning from small and medium-sized cargo vessels to larger ones</span> for transporting goods.
            <br>
            <br>
            <br>
            <br>
            ''', unsafe_allow_html=True)

    st.markdown('---')
    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>Identifying Potential Customers Through Correlation Analysis Between GT (Gross Tonnage), CT (Cargo Throughput), and Vessel Dwell Time at Busan Port</span>
    ''', unsafe_allow_html=True)

    col_3, col_4 = st.columns(2)
    with col_3:
        st.image("./useData/conclusion_img/busan_GT_CT.png")
        st.image("./useData/conclusion_img/busan_GT_CT_CORR.png")
    with col_4:
        st.image("./useData/conclusion_img/busan_CT_STAY.png")
        st.image("./useData/conclusion_img/busan_CT_STAY_CORR.png")
    with st.container(border=True):
        st.markdown('''
        A time-series analysis of Busan’s annual <span style='color:Orange; font-weight:bold; font-size:16px;'>CT (Cargo Throughput) and GT (Gross Tonnage)</span> shows that both indicators exhibit a similar upward trend.
        As a result, a correlation analysis between yearly CT and GT at Busan Port revealed a <span style='color:Orange; font-weight:bold; font-size:16px;'>correlation coefficient of 0.5942 and a p-value of 0.0416</span>, indicating a statistically significant positive correlation.
        In other words, <span style='color:Orange; font-weight:bold; font-size:16px;'>as GT increases, CT tends to increase as well</span>.
        Given that GT (Gross Tonnage) is on the rise and is positively correlated with CT (Cargo Throughput), we conducted an additional analysis to explore the correlation between <span style='color:Orange; font-weight:bold; font-size:16px;'>CT and vessel dwell time, based on the assumption that an increase in cargo volume would result in longer loading/unloading durations</span>.
        The results showed a <span style='color:Orange; font-weight:bold; font-size:16px;'>correlation coefficient of 0.5105 and a p-value of 0.0</span>, confirming that <span style='color:Orange; font-weight:bold; font-size:16px;'>as CT (Cargo Throughput) increases, vessel dwell time also tends to increase</span>.
        Assuming an average of 15 crew members per foreign vessel entering Busan Port, it is estimated that approximately <span style='color:orange; font-weight:bold; font-size:16px;'>244,395 to 290,790 crew members</span> arrive annually.
        This figure provides a solid quantitative basis for the Busan Port Authority to actively pursue strategies such as establishing an online ship supplies platform and developing targeted marketing plans for its member companies.
        ''', unsafe_allow_html=True)

    st.markdown('---')
    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>Key Tasks and Data Insights for Establishing an Online Ship Supplies Store</span>
    ''', unsafe_allow_html=True)

    col_5, col_6 = st.columns(2)
    with col_5:
        st.image("./useData/conclusion_img/all_prod.png")
        st.image("./useData/conclusion_img/top3_prod.png")
    with col_6:
        st.image("./useData/conclusion_img/food_prod_trend.png")
        st.image("./useData/conclusion_img/meat_prod_trend.png")
    with st.container(border=True):
        st.markdown('''
            When building an online ship supplies store, selecting which products to offer is a critical decision.
            To support this, we collected and visualized annual data on the number of ship supply sales and total revenue.
            The analysis revealed that meat, food, and alcohol were the most frequently sold product categories.
            However, we determined that sales volume alone was not sufficient justification for selection.
            Therefore, we conducted an additional <span style='color:Orange; font-weight:bold; font-size:16px;'>visualization analysis of sales trends by product category</span>.
            As a result, only <span style='color:Orange; font-weight:bold; font-size:16px;'>meat and food</span> showed a consistent upward trend, leading us to select these two categories as the primary products for the store.
        ''', unsafe_allow_html=True)


    st.image("./useData/conclusion_img/prod_wordcloud.png")
    with st.container(border=True):
        st.markdown('''
        As meat and food were selected as the primary product categories, we collected relevant data from <span style='color:Orange; font-weight:bold; font-size:16px;'>SNS platforms and blogs uploaded by foreign users</span> to better understand detailed product trends.
        Based on this data, we conducted a <span style='color:Orange; font-weight:bold; font-size:16px;'>word cloud visualization</span> for marketing analysis.

        The results provide valuable insights not only for the Busan Port Authority to source potential vendors for the online ship supplies store,
        but also for existing vendors to utilize in shaping effective marketing strategies.
        ''', unsafe_allow_html=True)
    col_7, col_8 = st.columns(2)
    with col_7:
        st.image("./useData/conclusion_img/prod_company.png")
    with col_8:
        st.image("./useData/conclusion_img/Vacancy.png")
    with st.container(border=True):
        st.markdown('''
        Based on the previous analysis, we collected and visualized data on companies handling meat and food products.
        This allows the Busan Port Authority to <span style='color:Orange; font-weight:bold; font-size:16px;'>identify relevant companies near the Busan area and build an effective distribution network</span>.
        Additionally, anticipating the need for storage space for customer orders when launching the online ship supplies store,
        we preemptively collected and visualized vacancy data around the three major ports of Busan.
        This information can be used to <span style='color:Orange; font-weight:bold; font-size:16px;'>secure storage facilities within budget or establish efficient logistics hubs</span>.
        ''', unsafe_allow_html=True)


    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>Providing Busan Tourism Information Based on Vessel Dwell Time</span>
    ''', unsafe_allow_html=True)

    col_9, col_10 = st.columns(2)
    with col_9:
        st.image("./useData/conclusion_img/residence_fourResult.png")
    with col_10:
        st.image("./useData/conclusion_img/residence_fourResult_shipcompany.png")
    with st.container(border=True):
        st.markdown('''
        Previous correlation analysis confirmed that <span style='color:Orange; font-weight:bold; font-size:16px;'>as CT (Cargo Throughput) increases, vessel dwell time also tends to increase</span>.
        Furthermore, <span style='color:Orange; font-weight:bold; font-size:16px;'>there is a significant correlation between GT (Gross Tonnage) and CT (Cargo Throughput)</span>.
        Given the consistent upward trend in GT, it can be inferred that CT will also rise in the future, and as a result, vessel dwell time is likely to increase as well.
        Based on this analysis, the Busan Port Authority determined that offering services such as recommended tourism courses and information tailored to vessel dwell times
        for foreign shipping companies and crew members calling at Busan Port could help improve satisfaction among existing members and attract new member companies.
        Additionally, based on box plot visualizations using dwell time quartiles,
        we categorized dwell time into <span style='color:Orange; font-weight:bold; font-size:16px;'>short stay group (24–42 hours), medium stay group (43–44 hours), and long stay group (45 hours or more)</span>,
        and provided customized tourism courses for each group accordingly.
        ''', unsafe_allow_html=True)

    st.markdown('---')

    st.subheader("3. Conclusion", anchor=False)
    st.markdown('''
    Through this project, we planned two feasible initiatives for the Busan Port Authority: the establishment of an online ship supplies platform and a tourism information service based on vessel dwell time.
    We also systematically carried out data analysis required for each stage of development.
    The <span style='color:Orange; font-weight:bold; font-size:16px;'>quantitative evidence derived from correlation analysis between GT (Gross Tonnage), CT (Cargo Throughput), and vessel dwell time</span> strongly supports the feasibility of these services from the perspective of the Busan Port Authority.
    Simply put, there is clear potential demand, and by effectively utilizing and analyzing the data already available,
    the Busan Port Authority has the capability to manage existing customers and attract new ones independently.
    Furthermore, if these services are <span style='color:Orange; font-weight:bold; font-size:16px;'>gradually advanced based on the current analysis, they could expand the customer base not only to shipping companies but also to their crew members</span>,
    ultimately creating unexpected added value.
    This project also reinforced our belief that planning and executing new business or services should not rely solely on intuition or ideas.
    We are convinced that collecting data from a broad environment, narrowing the scope through step-by-step analysis, identifying correlations among data points, and making data-driven decisions
    are the true starting points for business or service development.
    <span style='color:Orange; font-weight:bold; font-size:16px;'>There is no such thing as meaningless data.</span>
    Over time, accumulated <span style='color:Orange; font-weight:bold; font-size:16px;'>data will inevitably provide insight, and within those insights lie the opportunities and rationales for action</span>.
    We will continue to approach our assignments with this mindset and give our utmost effort.
    ''', unsafe_allow_html=True)

with tab_2:
    st.subheader("앞서 우리는 부산항만공사의 입장에서, 자사 회원사인 외국 선사들을 대상으로 제공할 수 있는 서비스를 시행하기 위한 데이터 분석을 수행했습니다.", anchor=False)

    st.subheader("1. 데이터 수집과 목적", anchor=False)
    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>온라인 선용품 플랫품 구축</span>
    ''', unsafe_allow_html=True)
    kr_data_1 = pd.DataFrame({
        "수집 데이터":["년도별 대한민국 항구 입항 카고선 수와 물동량 데이터", "년도별 부산 항구 입항 카고선 수와 GT(Gross Tonge)", "년도별 부산 항구 입항 카고선 수와 Cargo Throughput(Cargo Throughput)", "부산 신항항구 선사별 체류시간 데이터", "년도별 선용품 판매건수 및 판매금액 데이터", "선용품 품목관련 취급 기업 데이터", "품목관련 SNS 데이터", "부동산 공실 데이터"],
        "수집 여부" : ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
        "수집 목적" : ["최대 입항 수 및 물동량 항구 파악", "부산 3대 항구별 입항 선박수와 '선박+물동량'에 대한 추이 및 상관관계분석" , "부산 3대 항구별 입항 선박수와 물동량에 대한 추이 및 상관관계분석", "부산 선사별 체류시간 사분위수 파악", "온라인 선용품 구축시 판매할 품목 선정", "온라인 선용품 구축시 판매기업 소싱", "온라인 선용품 구축시 구체적인 판매제품과 이를 취급하는 기업소싱 및 마케팅에 활용", "온라인 선용품 구축시 물류창고 거점 확보"],
        "데이터 활용" :["최대 외국선 입항 수/물동량에 대한 시각화 분석", "부산 입항 외국선 GT(Gross Tonge) 파악 및 CT(Cargo Throughput)와의 상관관계 분석", "부산 입항 외국선 CT(Cargo Throughput) 파악 및 GT(Gross Tonge)와의 상관관계 분석", "체류시간 사분위수 파악과 CT(Cargo Throughput)와의 상관관계 분석", "장기적이고 경쟁력있는 선용품 선정", "기업 소싱을 위한 국내 기업분포와 부산 인근 기업파악", "외국인의 선용품 품목별 간접 수요조사", "유통 거점 확보 및 예산편성에 참고"]
    })
    st.dataframe(kr_data_1, hide_index=True, use_container_width=True)

    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>체류시간별 부산관광 정보 제공</span>
    ''', unsafe_allow_html=True)
    kr_data_2 = pd.DataFrame({
        "수집 데이터":["부산 신항항구 선사별 체류시간 데이터", "부산 관광지 데이터", "부산 맛집 데이터", "부산 숙박업소 데이터"],
        "수집 여부" : ["✅", "✅", "✅", "✅"],
        "수집 목적" : ["입항 선원 체류시간 분포 파악", "체류시간별 관광지 추천", "체류시간별 맛집 추천", "체류시간별 숙박업소 추천"],
        "데이터 활용" :["체류시간별 선원 그룹화", "체류시간에 따른 선원 그룹별 부산 여행코스 제공", "체류시간에 따른 선원 그룹별 부산 여행코스 제공", "체류시간에 따른 선원 그룹별 부산 여행코스 제공"]
    })
    st.dataframe(kr_data_2, hide_index=True, use_container_width=True)

    st.subheader("2. 데이터 분석과정", anchor=False)
    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>부산항 GT(Gross Tonge)와 CT(Cargo Throughput)</span>
    ''', unsafe_allow_html=True)
    col_1, col_2 = st.columns(2)
    with col_1:
        st.image("./useData/conclusion_img/busan_ship_gt.png")
        st.image("./useData/conclusion_img/busan_gt_trend.png")
    with col_2:
        with st.container(border=True):
            st.markdown('''
            <br>
            <br>
            <br>
            부산은 대한민국에서 외국 선박의 <span style='color:Orange; font-weight:bold; font-size:16px;'>입항 수와 CT(Cargo Throughput, 물동량)</span>이 가장 많은 항구로, 연간 물동량을 포함한 <span style='color:Orange; font-weight:bold; font-size:16px;'>선박의 총 부피인 GT(Gross Tonge)는 지속적으로 증가하는 반면, 입항 선박 수는 감소하는 추세</span>를 보이고 있습니다.<br>
            추세 분석 결과, <span style='color:Orange; font-weight:bold; font-size:16px;'>부산항에 입항하는 선박의 총 GT(Gross Tonge)는 꾸준히 상승</span>하고 있는 것으로 나타났습니다.<br>
            이는 해상 물류 업계의 효율성 추구로 인해, 대부분의 선사들이 <span style='color:white; font-weight:bold; font-size:18px;'>소형 또는 중형 카고선에서 대형 카고선으로 교체</span>하여 화물을 운반하고 있기 때문에 나타난 현상입니다.
            <br>
            <br>
            <br>
            <br>
            ''', unsafe_allow_html=True)

    st.markdown('---')
    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>부산항 GT(Gross Tonge), 부산항 CT(Cargo Throughput), 체류시간 상관분석에 따른 잠재고객 파악</span>
    ''', unsafe_allow_html=True)
    col_3, col_4 = st.columns(2)
    with col_3:
        st.image("./useData/conclusion_img/busan_GT_CT.png")
        st.image("./useData/conclusion_img/busan_GT_CT_CORR.png")
    with col_4:
        st.image("./useData/conclusion_img/busan_CT_STAY.png")
        st.image("./useData/conclusion_img/busan_CT_STAY_CORR.png")
    with st.container(border=True):
        st.markdown('''
            부산의 연간 <span style='color:Orange; font-weight:bold; font-size:16px;'>CT(Cargo Throughput)와 GT(Gross Tonge)를 시계열로 분석한 결과, 두 지표는 유사한 상승 추세</span>를 보이는 것으로 나타났습니다.
            이에 따라 부산항의 연도별 CT(Cargo Throughput)와 GT(Gross Tonge) 간의 상관관계를 분석한 결과, <span style='color:Orange; font-weight:bold; font-size:16px;'>상관계수 0.5942, p-value 0.0416으로, 통계적으로 유의미한 양의 상관관계</span>가 확인되었습니다.
            즉, <span style='color:Orange; font-weight:bold; font-size:16px;'>GT가 증가할수록 CT도 함께 증가하는 경향</span>을 보인다는 것입니다.
            앞서 확인한 바와 같이 GT(Gross Tonge)가 상승세에 있으며, CT(Cargo Throughput)와 양의 상관관계를 가지는 점에 주목하여, <span style='color:Orange; font-weight:bold; font-size:16px;'>물동량 증가에 따라 선박의 양하 및 양륙 작업 시간 또한 늘어날 것이라는 가정 하에, CT(Cargo Throughput)와 체류시간 간의 상관관계 분석을 추가로 수행</span>했습니다.
            그 결과, <span style='color:Orange; font-weight:bold; font-size:16px;'>상관계수 0.5105, p-value 0.0으로, CT(Cargo Throughput)의 증가에 따라 선박의 체류시간도 함께 증가</span>하는 경향이 확인되었습니다.
            또한, 부산항에 입항하는 외국 선박의 평균 탑승 인원을 15명으로 가정할 경우, 연간 약 <span style='color:orange; font-weight:bold; font-size:16px;'>244,395명에서 290,790명</span>에 달하는 선원이 부산에 입항하는 것으로 추정됩니다.
            이 수치는 부산항만공사가 ‘온라인 선용품 플랫폼 구축’과 회원사를 대상으로 한 마케팅 기획 및 실행 전략에 적극적으로 나서야 하는 정량적 근거가 될 수 있습니다.
            ''', unsafe_allow_html=True)

    st.markdown('---')

    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>온라인 선용품 쇼핑몰 구축시 필요한 과업과 데이터 분석</span>
    ''', unsafe_allow_html=True)
    col_5, col_6 = st.columns(2)
    with col_5:
        st.image("./useData/conclusion_img/all_prod.png")
        st.image("./useData/conclusion_img/top3_prod.png")
    with col_6:
        st.image("./useData/conclusion_img/food_prod_trend.png")
        st.image("./useData/conclusion_img/meat_prod_trend.png")
    with st.container(border=True):
        st.markdown('''
            온라인 선용품 쇼핑몰을 구축할 경우, 어떤 품목을 판매할지 결정하는 것이 핵심입니다.
            이를 위해 저희는 연간 선용품 판매 건수 및 판매 금액 데이터를 확보하여 가공 및 시각화를 진행한 결과, 육류, 음식, Alcohol 품목이 가장 많이 판매되는 것으로 나타났습니다.
            그러나 단순히 판매 수치가 높다는 이유만으로 품목을 선정하기에는 근거가 부족하다고 판단하여, <span style='color:Orange; font-weight:bold; font-size:16px;'>제품별 판매 추세를 분석하는 시각화 작업</span>을 추가로 수행했습니다.
            그 결과, <span style='color:Orange; font-weight:bold; font-size:16px;'>육류와 음식</span>만이 지속적인 상승 추세를 보였으며, 이를 바탕으로 최종적으로 해당 두 품목을 쇼핑몰의 주요 판매 품목으로 선정하였습니다.
            ''', unsafe_allow_html=True)

    st.image("./useData/conclusion_img/prod_wordcloud.png")
    with st.container(border=True):
        st.markdown('''
            판매 품목이 고기 및 음식류로 결정됨에 따라, 구체적인 제품 트렌드를 파악하기 위해 외국인이 업로드한 <span style='color:Orange; font-weight:bold; font-size:16px;'>SNS 및 블로그 등에서 관련 데이터를 수집</span>하였습니다.
            이 데이터를 기반으로 마케팅 분석을 위한 <span style='color:Orange; font-weight:bold; font-size:16px;'>워드클라우드 시각화</span>를 수행했습니다.
            해당 결과는 부산항만공사 입장에서 온라인 선용품 쇼핑몰에 입점할 판매 기업을 소싱하는 데 참고할 수 있을 뿐만 아니라,
            이미 입점한 판매 기업에서도 마케팅 전략 수립 시 활용 가능한 인사이트를 제공합니다.
            ''', unsafe_allow_html=True)
    col_7, col_8 = st.columns(2)
    with col_7:
        st.image("./useData/conclusion_img/prod_company.png")
    with col_8:
        st.image("./useData/conclusion_img/Vacancy.png")
    with st.container(border=True):
        st.markdown('''
            앞선 분석을 바탕으로, 육류와 음식을 취급하는 기업들의 데이터를 수집하고 시각화를 수행했습니다.
            이를 통해 부산항만공사는 <span style='color:Orange; font-weight:bold; font-size:16px;'>부산 인근의 관련 기업을 파악하고, 효과적인 유통망을 구축</span>하는 데 활용할 수 있습니다.
            또한 온라인 선용품 쇼핑몰을 구축할 경우, 고객이 주문한 제품을 보관할 공간이 필요할 것으로 판단하여, 부산 3대 항구 인근 지역의 공실 데이터를 미리 수집하고 시각화 작업을 진행하였습니다.
            이를 바탕으로, <span style='color:Orange; font-weight:bold; font-size:16px;'>예산에 맞는 창고 공간을 확보하거나 효율적인 유통 거점</span>을 마련하는 데 활용할 수 있습니다.
            ''', unsafe_allow_html=True)

    st.markdown('''
    <span style='color:Orange; font-weight:bold; font-size:20px;'>체류시간별 부산관광정보 제공</span>
    ''', unsafe_allow_html=True)
    col_9, col_10 = st.columns(2)
    with col_9:
        st.image("./useData/conclusion_img/residence_fourResult.png")
    with col_10:
        st.image("./useData/conclusion_img/residence_fourResult_shipcompany.png")
    with st.container(border=True):
        st.markdown('''
            앞서 상관관계 분석 결과, <span style='color:Orange; font-weight:bold; font-size:16px;'>CT(Cargo Throughput, 물동량)이 증가할수록 선박의 체류시간도 함께 증가하는 경향</span>이 확인되었습니다.
            또한 <span style='color:Orange; font-weight:bold; font-size:16px;'>GT(Gross Tonge)와 CT(Cargo Throughput) 간에도 유의미한 상관관계가 있으며, GT가 지속적으로 증가하는 추세라는 점을 고려할 때, 향후 CT도 증가하고, 이에 따라 체류시간 또한 길어질 가능성이 높다는 결론</span>을 도출할 수 있습니다.
            이러한 분석을 바탕으로, 부산항만공사는 부산항에 입항하는 외국 선사 및 선원들을 대상으로 체류시간에 맞춘 관광 코스를 추천하거나 관련 정보를 제공하는 서비스를 통해, 기존 회원사 만족도 제고와 신규 회원사 확보에 기여할 수 있을 것으로 판단하였습니다.
            또한, 체류시간 사분위수(4분위)를 기반으로 박스플롯 시각화를 진행한 결과,
            체류시간을 기준으로 <span style='color:Orange; font-weight:bold; font-size:16px;'>단기 체류 그룹(24 ~ 42시간), 중기 체류 그룹(43 ~ 44시간), 장기 체류 그룹(45시간 이상)</span>으로 나누고, 각 그룹에 적합한 관광 코스를 제공하였습니다.
            ''', unsafe_allow_html=True)

    st.markdown('---')

    st.subheader("3. 결론", anchor=False)
    st.markdown('''
        이번 프로젝트를 통해, 우리는 부산항만공사에서 추진 가능한 사업으로 온라인 선용품 플랫폼 구축과 체류시간 기반 관광정보 제공 서비스를 기획하였으며, 각 단계에 필요한 데이터 분석을 체계적으로 수행하였습니다.
        <span style='color:Orange; font-weight:bold; font-size:16px;'>GT(Gross Tonge), CT(Cargo Throughput), 체류시간 간의 상관관계 분석을 통해 도출된 정량적 근거</span>는, 해당 서비스들이 부산항만공사 입장에서 충분히 실행 가능한 사업임을 뒷받침합니다.
        쉽게 말해, 잠재 고객은 분명 존재하며, 기존에 보유한 데이터를 적극적으로 활용하고 분석한다면, 부산항만공사 자체 역량만으로도 기존 고객 관리 및 신규 고객 유치가 충분히 가능하다고 판단됩니다.
        나아가, 본 분석을 기반으로 <span style='color:Orange; font-weight:bold; font-size:16px;'>해당 서비스들을 단계적으로 고도화해 나간다면, 선사뿐만 아니라 선사에 소속된 선원들까지 아우르는 새로운 고객군을 확보</span>할 수 있으며, 이는 예상치 못했던 부가가치를 창출할 수 있는 기회가 될 것입니다.
        이번 프로젝트를 통해 우리는, 신규 사업이나 서비스를 기획하고 실행할 때 단순한 직관이나 아이디어에만 의존하는 것은 위험한 접근이라는 점을 다시금 인식하게 되었습니다.
        광범위한 환경 속에서 데이터를 수집하고, 점진적으로 분석 범위를 좁혀가며, 데이터 간의 상관관계를 파악하고 수치 기반의 객관적 판단을 내리는 과정이 곧 사업 또는 서비스 기획의 출발점임을 확신하게 되었습니다.
        <span style='color:Orange; font-weight:bold; font-size:16px;'>무의미한 데이터는 존재하지 않습니다.</span>
        시간이 지나 쌓인 <span style='color:Orange; font-weight:bold; font-size:16px;'>데이터는 결국 우리에게 인사이트를 제공하며, 그 인사이트 속에서 기회와 실행 근거</span>를 찾아내는 것이 핵심입니다.
        앞으로도 이러한 관점을 바탕으로 주어진 과업에 최선을 다할 것입니다.
        ''', unsafe_allow_html=True)
