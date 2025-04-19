import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.features import CustomIcon
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide")

st.title("Data Analysis for Sourcing Item-Related Companies for an Online Ship Supply Platform", anchor=False)

tab_1, tab_2, tab_3 = st.tabs(["Analysis Process(EN)", "Analysis Process(KR)", "Data Prep&EDA"])

with tab_1:
    st.markdown("""
    When building an online ship supply platform, <span style='color:orange; font-weight:bold; font-size:20px;'>selecting the right products and sourcing companies that handle and distribute those items</span> is just as important as acquiring customers.
    To support this, we conducted a visual analysis of annual ship supply item data.
    We first visualized the <span style='color:white; font-weight:bold; font-size:20px;'>number of sales per item category</span> after preprocessing.
    """, unsafe_allow_html=True)



    yearsCount = pd.read_csv("./useData/finishPrepro/finish_prod_totalCount.csv")
    yearsCount = yearsCount.iloc[:,1:]
    # 컬럼명 변경 : count : 제외
    yc_columns = yearsCount.columns
    new_yc_columns = list()

    for v in yc_columns:
        if "count : " in v:
            v = v.replace("count : ", "")
            new_yc_columns.append(v)

    #영문 번역걸럼으로 대체
    new_yc_columns = ["Alcohol","Tobacco","Meat","Food","Electronics","Cookware","Ship Parts","Accessories","Fuel","Conditional Ship Stores","Ship Waste","Others"]
    yearsCount.columns = [yearsCount.columns[0]] + new_yc_columns

    # 시각화 : 전체품목
    # -년도
    visual_years = yearsCount["Years"].unique()
    visual_prod = yearsCount.columns[1:]
    yearsCount = yearsCount.iloc[:,1:]

    # -그래프 요소를 르트로 담음
    visual_count = list()

    for v in visual_prod:
        pd_count = yearsCount.loc[:,v]
        visual_count.append(
            go.Bar(
                x=visual_years,
                y=pd_count,
                name=v,
                text=pd_count,
                textposition="outside",#inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

        fig = go.Figure(data=visual_count)

        fig.update_layout(
            barmode="group",
            title=dict(
                text="<b>Number of pre-sale item</b> by year",
                x=0.35,
                y=0.9,
                font={"size": 20,
                    "color":"white"}
            ),
            xaxis=dict(title="Year"),
            yaxis_title="Number of purchases",
            legend=dict(
                bordercolor="grey",
                borderwidth=0.5
            )
        )

    #최대값 추출
    max_count_list = list()
    for v in visual_prod:

        w = yearsCount.loc[:, v]

        max_count_list.append(w.max())
        # 최대값
        max_value = max(max_count_list)

        # 최대값이 나타난 연도 (index 위치를 찾아 visual_years에서 매핑)
        max_index = w.idxmax()
        max_year = visual_years[max_index]

    # annotation 추가
    fig.add_annotation(
        x=max_year,  # 최대값이 나타난 연도
        y=max_value,  # 최대값
        text=f"<b>Food is the best-selling daily necessities product every year,<br>with a total sales volume of {max_value} in {max_year}.</b>",
        showarrow=False,# 화살표 표시 여부 (True면 텍스트 박스와 타겟 위치를 연결하는 화살표가 표시됨)
        font=dict(
            size=15,
            color="#fc7507"
        ),
        align="center",
        xanchor="center",
        yanchor="top",
        xshift=-50,
        yshift=70,
        bordercolor="#0e28ea",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0e28ea",
        opacity=0.9
    )
    st.plotly_chart(fig, use_container_width=True,key="en_allPD_needs")

    st.markdown("""
    From the visual analysis, the top 3 items in terms of sales count were <span style='color:orange; font-weight:bold; font-size:20px;'>Alcohol, Meat, and Food</span>.
    Since the full item visualization includes many categories, making it harder to interpret, we reprocessed and re-visualized <span style='color:white; font-weight:bold; font-size:20px;'>only the Top 3 most-sold items</span> below.
    """, unsafe_allow_html=True)


    yearsCountTop3 = yearsCount[["Food", "Meat", "Alcohol"]]
    # -그래프 요소를 르트로 담음
    visual_count_top3 = list()

    for v in yearsCountTop3:
        pd_count = yearsCountTop3.loc[:,v]
        visual_count_top3.append(
            go.Bar(
                x=visual_years,
                y=pd_count,
                name=v,
                text=pd_count,
                textposition="inside",#inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig2 = go.Figure(data=visual_count_top3)

    fig2.update_layout(
        barmode="group",
        title=dict(
            text="<b>Number of pre-sale Top 3 items</b> by year",
            x=0.35,
            y=0.9,
            font={"size": 20,
                "color":"white"}
        ),
        xaxis=dict(title="Year"),
        yaxis_title="Number of purchases",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig2, use_container_width=True, key="en_top3PD_needs")


    st.markdown("""
    Next, we analyzed the <span style='color:white; font-weight:bold; font-size:20px;'>total sales amount by item category</span>.
    """, unsafe_allow_html=True)


    yearsPrice = pd.read_csv("./useData/finishPrepro/finish_prod_totalPrice.csv")
    yearsPrice = yearsPrice.iloc[:,1:]

    #영문 번역걸럼으로 대체
    new_yp_columns = ["Alcohol","Tobacco","Meat","Food","Electronics","Cookware","Ship Parts","Accessories","Fuel","Conditional Ship Stores","Ship Waste","Others"]
    yearsPrice.columns = [yearsPrice.columns[0]] + new_yp_columns

    # 시각화
    # -년도
    visual_years = yearsPrice["Years"].unique()
    visual_prod = yearsPrice.columns[1:]

    yearsPrice = yearsPrice.iloc[:,1:]

    # -그래프 요소를 르트로 담음
    visual_price = list()

    for v in visual_prod:
        pd_price = yearsPrice.loc[:,v]
        visual_price.append(
            go.Bar(
                x=visual_years,
                y=pd_price,
                name=v,
                text=pd_price,
                textposition="outside",#inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig_p = go.Figure(data=visual_price)

    fig_p.update_layout(
        barmode="group",
        title=dict(
            text="<b>Item Sales Amount</b> by Year",
            x=0.35,
            y=0.9,
            font={"size": 20,
                "color":"white"}
        ),
        xaxis=dict(title="Year"),
        yaxis_title="Sales amount",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )

    #최대값 추출
    max_count_list = list()
    for v in visual_prod:

        w = yearsPrice.loc[:, v]

        max_count_list.append(w.max())
        # 최대값
        max_value = max(max_count_list)

        # 최대값이 나타난 연도 (index 위치를 찾아 visual_years에서 매핑)
        max_index = w.idxmax()
        max_year = visual_years[max_index]

    # annotation 추가
    fig_p.add_annotation(
        x=max_year,  # 최대값이 나타난 연도
        y=max_value,  # 최대값
        text=f"Among the items sold each year,<br>the one with the highest sales amount was Fuel, which recorded a high of {max_value} in {max_year}.",

        showarrow=False,# 화살표 표시 여부 (True면 텍스트 박스와 타겟 위치를 연결하는 화살표가 표시됨)
        font=dict(
            size=12,
            color="#0e28ea"
        ),
        align="center",
        xanchor="center",
        yanchor="top",
        xshift=-100,
        yshift=60,
        bordercolor="#fc7507",
        borderwidth=1,
        borderpad=4,
        bgcolor="#fc7507",
        opacity=0.75
    )

    st.plotly_chart(fig_p, use_container_width=True, key="en_allPD_price_needs")

    st.markdown("""
    The top 3 items by sales amount were <span style='color:orange; font-weight:bold; font-size:20px;'>Fuel, Ship Parts, and Others</span>.
    To improve readability, we reprocessed and visualized only these top categories below.
    """, unsafe_allow_html=True)

    yearsPriceTop3 = yearsPrice[["Fuel", "Ship Parts", "Others"]]
    # -그래프 요소를 르트로 담음
    visual_price_top3 = list()

    for v in yearsPriceTop3:
        pd_price = yearsPriceTop3.loc[:,v]
        visual_price_top3.append(
            go.Bar(
                x=visual_years,
                y=pd_price,
                name=v,
                text=pd_price,
                textposition="inside",#inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig_p_2 = go.Figure(data=visual_price_top3)
    fig_p_2.update_layout(
        barmode="group",
        title=dict(
            text="<b>Top 3 Items Sales Amount</b> by Year",
            x=0.35,
            y=0.9,
            font={"size": 20,
                "color":"white"}
        ),
        xaxis=dict(title="Year"),
        yaxis_title="Number of purchases",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_p_2, use_container_width=True, key="en_top3PD_price_needs")

    st.markdown('''
    The top-selling items by sales count were <span style='color:white; font-weight:bold; font-size:20px;'>Meat, Alcohol, and Food</span>,
    while the top items by sales amount were <span style='color:white; font-weight:bold; font-size:20px;'>Fuel, Ship Parts, and Others</span>.
    However, we decided <span style='color:orange; font-weight:bold; font-size:20px;'>not to base sourcing decisions solely on volume or sales figures.
    Instead, we visualized monthly sales trends by item and analyzed the trendlines to select only items showing upward trends as final sourcing candidates</span>.
    Accordingly, we proceeded with the visual analysis as shown below.
    ''', unsafe_allow_html=True)

    # Food, Meat, Alcohol, ship parts 추세
    trend_data = pd.read_csv("./useData/finishPrepro/finish_prod_totalCountPrice_yearMonth.csv")
    trend_data = trend_data.iloc[:,1:]

    #식품
    trend_data_food = trend_data[["years", "months","count : 식품류"]]
    trend_data_food.columns = list(trend_data.columns[:2]) + ["Food"]
    #-25s년 절사
    trend_data_food = trend_data_food[trend_data_food["years"]!=2025]
    #-타입형변환
    trend_data_food[["years", "months"]] = trend_data_food[["years", "months"]].astype("str")
    trend_data_food["Date"] = pd.to_datetime(trend_data_food["years"] + "-" + trend_data_food["months"])

    # 그래프 그리기
    fig_f = px.scatter(
        trend_data_food,
        x="Date",
        y="Food",
        trendline="ols",
        title="Food Sales with Regression Trendline",
    )

    # 데이터 선 + 마커 + 값 표시
    fig_f.update_traces(
        line=dict(color="blue"),
        marker=dict(color="blue", size=6),
    )

    # 추세선 스타일 변경
    fig_f.update_traces(
        line=dict(color="red", width=3, dash="solid"),
        selector=dict(mode="lines")
    )

    # 레이아웃 설정
    fig_f.update_layout(
        xaxis=dict(
            title="Date",
            tickformat="%Y-%m",
            tickangle=20
        ),
        yaxis=dict(title="Count"),
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_f, use_container_width=True, key="en_trend_food_pd")

    #Alcohol
    trend_data_alcohol = trend_data[["years", "months","count : 주류"]]
    trend_data_alcohol.columns = list(trend_data.columns[:2]) + ["Alcohol"]
    #-25s년 절사
    trend_data_alcohol = trend_data_alcohol[trend_data_alcohol["years"]!=2025]
    #-타입형변환
    trend_data_alcohol[["years", "months"]] = trend_data_alcohol[["years", "months"]].astype("str")
    trend_data_alcohol[["years", "months"]] = trend_data_alcohol[["years", "months"]].astype("str")
    trend_data_alcohol["Date"] = pd.to_datetime(trend_data_alcohol["years"] + "-" + trend_data_alcohol["months"])
    trend_data_alcohol = trend_data_alcohol[["Date","Alcohol"]]

    # 그래프 그리기
    fig_a = px.scatter(
        trend_data_alcohol,
        x="Date",
        y="Alcohol",
        trendline="ols",
        title="Alcohol Sales with Regression Trendline",
    )

    # 데이터 선 + 마커 + 값 표시
    fig_a.update_traces(
        line=dict(color="blue"),
        marker=dict(color="blue", size=6),
    )

    # 추세선 스타일 변경-
    fig_a.update_traces(
        line=dict(color="red", width=3, dash="solid"),
        selector=dict(mode="lines")
    )

    # 레이아웃 설정
    fig_a.update_layout(
        xaxis=dict(
            title="Date",
            tickformat="%Y-%m",
            tickangle=20
        ),
        yaxis=dict(title="Count"),
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_a, use_container_width=True, key="en_trend_alcohol_pd")

    #Meat
    trend_data_meat = trend_data[["years", "months","count : 육류 "]]
    trend_data_meat.columns = list(trend_data.columns[:2]) + ["Meat"]
    #-25s년 절사
    trend_data_meat = trend_data_meat[trend_data_meat["years"]!=2025]
    #-타입형변환
    trend_data_meat[["years", "months"]] = trend_data_meat[["years", "months"]].astype("str")
    trend_data_meat[["years", "months"]] = trend_data_meat[["years", "months"]].astype("str")
    trend_data_meat["Date"] = pd.to_datetime(trend_data_meat["years"] + "-" + trend_data_meat["months"])
    trend_data_meat = trend_data_meat[["Date","Meat"]]

    # 그래프 그리기
    fig_m = px.scatter(
        trend_data_meat,
        x="Date",
        y="Meat",
        trendline="ols",
        title="Meat Sales with Regression Trendline",
    )

    # 데이터 선 + 마커 + 값 표시
    fig_m.update_traces(
        line=dict(color="blue"),
        marker=dict(color="blue", size=6),
    )

    # 추세선 스타일 변경
    fig_m.update_traces(
        line=dict(color="red", width=3, dash="solid"),
        selector=dict(mode="lines")
    )

    # 레이아웃 설정
    fig_m.update_layout(
        xaxis=dict(
            title="Date",
            tickformat="%Y-%m",
            tickangle=20
        ),
        yaxis=dict(title="Count"),
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_m, use_container_width=True, key="en_trend_meat_pd")


    #Ship Parts : 선박부품
    trend_data_shipparts = trend_data[["years", "months","count : 선박부품"]]
    trend_data_shipparts.columns = list(trend_data.columns[:2]) + ["Ship parts"]
    #-25s년 절사
    trend_data_shipparts = trend_data_shipparts[trend_data_shipparts["years"]!=2025]
    #-타입형변환
    trend_data_shipparts[["years", "months"]] = trend_data_shipparts[["years", "months"]].astype("str")
    trend_data_shipparts["Date"] = pd.to_datetime(trend_data_shipparts["years"] + "-" + trend_data_shipparts["months"])
    trend_data_shipparts = trend_data_shipparts[["Date","Ship parts"]]

    # 그래프 그리기
    fig_sp = px.scatter(
        trend_data_shipparts,
        x="Date",
        y="Ship parts",
        trendline="ols",
        title="Ship parts with Regression Trendline",
    )

    # 데이터 선 + 마커 + 값 표시
    fig_sp.update_traces(
        line=dict(color="blue"),
        marker=dict(color="blue", size=6),
    )

    # 추세선 스타일 변경
    fig_sp.update_traces(
        line=dict(color="red", width=3, dash="solid"),
        selector=dict(mode="lines")
    )

    # 레이아웃 설정
    fig_sp.update_layout(
        xaxis=dict(
            title="Date",
            tickformat="%Y-%m",
            tickangle=20
        ),
        yaxis=dict(title="Count"),
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_sp, use_container_width=True, key="en_trend_shippart_pd")

    st.subheader("Conclusion", anchor=False)
    st.markdown("""
    Based on the trend analysis, <span style='color:orange; font-weight:bold; font-size:20px;'>Food and Meat</span> showed a clear upward trend and were selected as final sourcing items.
    <span style='color:white; font-weight:bold; font-size:20px;'>Alcohol showed only a mild trend and was excluded.
    Ship Parts, while high in sales amount, showed a downward trend in transaction count and was excluded as well</span>.
    <span style='color:white; font-weight:bold; font-size:20px;'>Fuel was excluded due to its nature as direct fuel injection for vessels at ports,
    and Others was excluded because of the lack of detailed item classification</span>.
    Therefore, we collected and visualized data on companies that <span style='color:orange; font-weight:bold; font-size:20px;'>handle and distribute Food and Meat</span>.
    This visualization provides insight into <span style='color:orange; font-weight:bold; font-size:20px;'>company presence near Busan and can be used for sourcing and contact purposes</span>.
    """, unsafe_allow_html=True)


    #기업데이터 불러오기
    meatCompany_info = pd.read_csv("./useData/finishPrepro/meat_company_LaLo.csv", encoding="utf-8-sig")
    foodCompany_info = pd.read_csv("./useData/finishPrepro/food_company_LaLo.csv", encoding="utf-8-sig")

    meatCompany_info = meatCompany_info.iloc[:,1:]
    foodCompany_info = foodCompany_info.iloc[:,1:]
    mergeCompany_info = pd.concat(
        [meatCompany_info,
        foodCompany_info],
        axis=0,
        ignore_index=True
    )
    mergeCompany_info = mergeCompany_info.reset_index()
    mergeCompany_info = mergeCompany_info.iloc[:,1:]

    # attr option > "OpenStreetMap","Stamen Terrain","Stamen Toner","Stamen Watercolor","CartoDB positron","CartoDB dark_matter"
    #대한민국 : 36.554311389428506, 127.91990571290032
    targetArea = folium.Map(
        location=[36.19727816840753, 127.89219063707009],
        zoom_start=7,
        tiles="CartoDB positron",
        # width="100%",     # 또는 px 단위로: "800px"
        # height="500px"    # 문자열로 지정해야 함 (숫자 X)
    )

    busanGeo = "./useData/koreaBusan.geojson"

    with open(busanGeo, encoding="utf-8-sig") as f:
        myGeo = json.load(f)

    # Geo 스타일 함수
    def myGeo_style(x):
        return {
            "fillColor": "#11c511",   # 채우기 색 (파랑색)
            "color": "grey",         # 경계선 색
            "weight": 0.5,              # 선 굵기
            "fillOpacity": 1       # 투명도
        }

    folium.GeoJson(
        data=myGeo,
        name="Busan Metropolitan City, Republic of Korea",
        style_function=myGeo_style
    ).add_to(targetArea)

    # Set shared icon size and anchor point (공통 아이콘 크기 및 정렬 기준점 설정)
    icon_size = (21, 21)        # icon_size: (width, height) in pixels (아이콘의 가로, 세로 픽셀 크기)
    icon_anchor = (10, 10)      # icon_anchor: pixel offset from top-left to center (중앙 정렬: 좌측 상단 기준으로 (12, 12))

    # Iterate over each row in the company DataFrame
    # 회사 정보 데이터프레임의 각 행을 반복 처리함
    for i, v in mergeCompany_info.iterrows():

        # Extract latitude and longitude from last two columns
        # 위도, 경도 정보를 마지막 두 열에서 가져옴
        Latitude = v[-2]
        Longitude = v[-1]

        # Create HTML-formatted tooltip content
        # 마우스 오버 시 표시될 HTML 형식의 회사 정보 문자열 생성
        companyInfo = f"""
            {v[1]} Company Information<br>
            (1) Category : {v[0]}<br>
            (2) Owner : {v[1]}<br>
            (3) Address : {v[5]}<br>
            (4) Contact point : {v[6]}
        """

        # Generate tooltip for hover interaction
        # 마우스 오버 시 정보를 보여줄 Tooltip 객체 생성
        mytooltip = folium.Tooltip(companyInfo, sticky=True)

        # Check if company is meat-related and assign style accordingly
        # 회사가 "육류" 관련이면 해당 아이콘 및 색상 지정
        if "육류" in v[0]:

            # Define meat company icon (육류 회사 아이콘 설정)
            meat_icon_path = "./useData/myImage/meatCompany.png"  # 경로: meatCompany.png
            meat_icon = CustomIcon(
                icon_image=meat_icon_path,    # icon_image: 이미지 경로 (meat 아이콘)
                icon_size=icon_size,          # icon_size: 아이콘 크기 (25 x 25)
                icon_anchor=icon_anchor       # icon_anchor: 아이콘 내부의 중앙 좌표를 지도 위치에 정렬
            )

            # Add meat company marker to map
            # 육류 회사 위치에 마커(아이콘)를 지도에 추가함
            folium.Marker(
                location=[Latitude, Longitude],  # 마커가 표시될 지도상의 좌표
                icon=meat_icon,                  # 육류 회사 전용 커스텀 아이콘
                tooltip=mytooltip                # 마우스 오버 시 툴팁 표시
            ).add_to(targetArea)

            # Add circle around meat marker (for visual emphasis)
            # 육류 마커 주변에 반경 원 시각화 추가
            folium.CircleMarker(
                location=[Latitude, Longitude],  # 원의 중심 위치
                radius=30,                       # 반지름 (픽셀 단위)
                fill=True,                       # 내부 색상 채움
                color="none",                    # 외곽선 없음
                fill_color="#ff7f0e"             # 채우기 색상 (주황 계열)
            ).add_to(targetArea)

        else:
            # Non-meat companies (e.g., food companies) 처리
            # 육류 외 식품 관련 회사 처리
            # Define food company icon (식품 회사 아이콘 설정)
            food_icon_path = "./useData/myImage/foodCompany.png"  # 경로: foodCompany.png
            food_icon = CustomIcon(
                icon_image=food_icon_path,    # icon_image: 이미지 경로 (food 아이콘)
                icon_size=icon_size,          # 아이콘 크기 (25 x 25)
                icon_anchor=icon_anchor       # 아이콘 중앙을 지도 위치에 정렬
            )

            # Add food company marker to map
            # 식품 회사 위치에 마커(아이콘)를 지도에 추가함
            folium.Marker(
                location=[Latitude, Longitude],  # 지도상의 좌표
                icon=food_icon,                  # 식품 회사 전용 커스텀 아이콘
                tooltip=mytooltip                # 마우스 오버 시 툴팁 표시
            ).add_to(targetArea)

            # Add circle around food marker (for visual emphasis)
            # 식품 마커 주변에 반경 원 시각화 추가
            folium.CircleMarker(
                location=[Latitude, Longitude],  # 원의 중심 위치
                radius=30,                       # 반지름 (육류보다 크게 설정)
                fill=True,                       # 내부 채움
                color="none",                    # 테두리 없음
                fill_color="#65b2f5"             # 채우기 색상 (하늘색 계열)
            ).add_to(targetArea)

    # Display the map with all company markers and radius overlays
    # 모든 회사 위치 마커 및 시각적 원이 포함된 지도를 출력함
    st_folium(targetArea, width=1500, height=600, key="en_pdCompany_possition")

with tab_2:
    st.markdown("""
    온라인 선용품 플랫폼을 구축함에 있어, 고객 확보뿐만 아니라 <span style='color:orange; font-weight:bold; font-size:20px;'>판매 품목의 선별과 해당 품목을 취급 및 유통하는 기업의 소싱</span> 역시 중요한 요소입니다. 이를 위해 아래와 같이 연간 선용품 품목 데이터를 시각적으로 분석했습니다. 우선 <span style='color:white; font-weight:bold; font-size:20px;'>선용품 품목별 판매된 건수</span>에 대한 데이터를 전처리 후 시각화를 진행했습니다.
    """, unsafe_allow_html=True)


    yearsCount = pd.read_csv("./useData/finishPrepro/finish_prod_totalCount.csv")
    yearsCount = yearsCount.iloc[:,1:]
    # 컬럼명 변경 : count : 제외
    yc_columns = yearsCount.columns
    new_yc_columns = list()

    for v in yc_columns:
        if "count : " in v:
            v = v.replace("count : ", "")
            new_yc_columns.append(v)

    #영문 번역걸럼으로 대체
    new_yc_columns = ["Alcohol","Tobacco","Meat","Food","Electronics","Cookware","Ship Parts","Accessories","Fuel","Conditional Ship Stores","Ship Waste","Others"]
    yearsCount.columns = [yearsCount.columns[0]] + new_yc_columns

    # 시각화 : 전체품목
    # -년도
    visual_years = yearsCount["Years"].unique()
    visual_prod = yearsCount.columns[1:]
    yearsCount = yearsCount.iloc[:,1:]

    # -그래프 요소를 르트로 담음
    visual_count = list()

    for v in visual_prod:
        pd_count = yearsCount.loc[:,v]
        visual_count.append(
            go.Bar(
                x=visual_years,
                y=pd_count,
                name=v,
                text=pd_count,
                textposition="outside",#inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

        fig = go.Figure(data=visual_count)

        fig.update_layout(
            barmode="group",
            title=dict(
                text="<b>Number of pre-sale item</b> by year",
                x=0.35,
                y=0.9,
                font={"size": 20,
                    "color":"white"}
            ),
            xaxis=dict(title="Year"),
            yaxis_title="Number of purchases",
            legend=dict(
                bordercolor="grey",
                borderwidth=0.5
            )
        )

    #최대값 추출
    max_count_list = list()
    for v in visual_prod:

        w = yearsCount.loc[:, v]

        max_count_list.append(w.max())
        # 최대값
        max_value = max(max_count_list)

        # 최대값이 나타난 연도 (index 위치를 찾아 visual_years에서 매핑)
        max_index = w.idxmax()
        max_year = visual_years[max_index]

    # annotation 추가
    fig.add_annotation(
        x=max_year,  # 최대값이 나타난 연도
        y=max_value,  # 최대값
        text=f"<b>Food is the best-selling daily necessities product every year,<br>with a total sales volume of {max_value} in {max_year}.</b>",
        showarrow=False,# 화살표 표시 여부 (True면 텍스트 박스와 타겟 위치를 연결하는 화살표가 표시됨)
        font=dict(
            size=15,
            color="#fc7507"
        ),
        align="center",
        xanchor="center",
        yanchor="top",
        xshift=-50,
        yshift=70,
        bordercolor="#0e28ea",
        borderwidth=1,
        borderpad=4,
        bgcolor="#0e28ea",
        opacity=0.9
    )
    st.plotly_chart(fig, use_container_width=True,key="kr_allPD_needs")

    st.markdown("""
    시각화 분석결과 판매건수에 있어 많이 판매되는 3개 품목은 <span style='color:orange; font-weight:bold; font-size:20px;'>주류, 고기, 술</span> 이었습니다. 위 시각화 그래프는 품목이 너무 많아 정확한 수치를 파악하는 데 제한되어 <span style='color:white; font-weight:bold; font-size:20px;'>많이 판매된 Top3 품목만</span>을 전처리하여 아래와 같이 재시각화 하였습니다.
    """, unsafe_allow_html=True)

    yearsCountTop3 = yearsCount[["Food", "Meat", "Alcohol"]]
    # -그래프 요소를 르트로 담음
    visual_count_top3 = list()

    for v in yearsCountTop3:
        pd_count = yearsCountTop3.loc[:,v]
        visual_count_top3.append(
            go.Bar(
                x=visual_years,
                y=pd_count,
                name=v,
                text=pd_count,
                textposition="inside",#inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig2 = go.Figure(data=visual_count_top3)

    fig2.update_layout(
        barmode="group",
        title=dict(
            text="<b>Number of pre-sale Top 3 items</b> by year",
            x=0.35,
            y=0.9,
            font={"size": 20,
                "color":"white"}
        ),
        xaxis=dict(title="Year"),
        yaxis_title="Number of purchases",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig2, use_container_width=True, key="kr_top3PD_needs")


    st.markdown("""
    다음은 <span style='color:white; font-weight:bold; font-size:20px;'>선용품 품목별 총 판매금액</span>에 대한 시각화 분석을 진행했습니다.
    """, unsafe_allow_html=True)

    yearsPrice = pd.read_csv("./useData/finishPrepro/finish_prod_totalPrice.csv")
    yearsPrice = yearsPrice.iloc[:,1:]

    #영문 번역걸럼으로 대체
    new_yp_columns = ["Alcohol","Tobacco","Meat","Food","Electronics","Cookware","Ship Parts","Accessories","Fuel","Conditional Ship Stores","Ship Waste","Others"]
    yearsPrice.columns = [yearsPrice.columns[0]] + new_yp_columns

    # 시각화
    # -년도
    visual_years = yearsPrice["Years"].unique()
    visual_prod = yearsPrice.columns[1:]

    yearsPrice = yearsPrice.iloc[:,1:]

    # -그래프 요소를 르트로 담음
    visual_price = list()

    for v in visual_prod:
        pd_price = yearsPrice.loc[:,v]
        visual_price.append(
            go.Bar(
                x=visual_years,
                y=pd_price,
                name=v,
                text=pd_price,
                textposition="outside",#inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig_p = go.Figure(data=visual_price)

    fig_p.update_layout(
        barmode="group",
        title=dict(
            text="<b>Item Sales Amount</b> by Year",
            x=0.35,
            y=0.9,
            font={"size": 20,
                "color":"white"}
        ),
        xaxis=dict(title="Year"),
        yaxis_title="Sales amount",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )

    #최대값 추출
    max_count_list = list()
    for v in visual_prod:

        w = yearsPrice.loc[:, v]

        max_count_list.append(w.max())
        # 최대값
        max_value = max(max_count_list)

        # 최대값이 나타난 연도 (index 위치를 찾아 visual_years에서 매핑)
        max_index = w.idxmax()
        max_year = visual_years[max_index]

    # annotation 추가
    fig_p.add_annotation(
        x=max_year,  # 최대값이 나타난 연도
        y=max_value,  # 최대값
        text=f"Among the items sold each year,<br>the one with the highest sales amount was Fuel, which recorded a high of {max_value} in {max_year}.",

        showarrow=False,# 화살표 표시 여부 (True면 텍스트 박스와 타겟 위치를 연결하는 화살표가 표시됨)
        font=dict(
            size=12,
            color="#0e28ea"
        ),
        align="center",
        xanchor="center",
        yanchor="top",
        xshift=-100,
        yshift=60,
        bordercolor="#fc7507",
        borderwidth=1,
        borderpad=4,
        bgcolor="#fc7507",
        opacity=0.75
    )

    st.plotly_chart(fig_p, use_container_width=True, key="kr_allPD_price_needs")

    st.markdown("""
    년도별 판매금액이 높은 품목 3개는<span style='color:orange; font-weight:bold; font-size:20px;'>연료(Fuel), Ship parts, others</span>였으며, 이 또한 가시성을 위해 별도 전처리하여 아래와 같이 시각화로 구현했습니다.
    """, unsafe_allow_html=True)


    yearsPriceTop3 = yearsPrice[["Fuel", "Ship Parts", "Others"]]
    # -그래프 요소를 르트로 담음
    visual_price_top3 = list()

    for v in yearsPriceTop3:
        pd_price = yearsPriceTop3.loc[:,v]
        visual_price_top3.append(
            go.Bar(
                x=visual_years,
                y=pd_price,
                name=v,
                text=pd_price,
                textposition="inside",#inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig_p_2 = go.Figure(data=visual_price_top3)
    fig_p_2.update_layout(
        barmode="group",
        title=dict(
            text="<b>Top 3 Items Sales Amount</b> by Year",
            x=0.35,
            y=0.9,
            font={"size": 20,
                "color":"white"}
        ),
        xaxis=dict(title="Year"),
        yaxis_title="Number of purchases",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_p_2, use_container_width=True, key="kr_top3PD_price_needs")

    st.markdown('''
    년도별 판매 건수가 많은 주요 품목은 <span style='color:white; font-weight:bold; font-size:20px;'>Meat, Alcohol, Food</span>였으며,
    판매 금액 기준으로는 <span style='color:white; font-weight:bold; font-size:20px;'>Fuel, Ship Parts, Others</span>가 상위를 차지했습니다.
    하지만 우리는 <span style='color:orange; font-weight:bold; font-size:20px;'>단순히 판매 건수나 금액이 높다는 이유만으로 소싱 대상을 결정하지 않고,
    품목별 월별 판매 건수를 시각화한 뒤 추세선을 분석하여 상승 추세에 있는 품목만을 최종 소싱 대상으로 선정</span>하기로 하였습니다.
    이에 따라 아래와 같이 시각화 분석을 진행하였습니다.
    ''', unsafe_allow_html=True)

    # Food, Meat, Alcohol, ship parts 추세
    trend_data = pd.read_csv("./useData/finishPrepro/finish_prod_totalCountPrice_yearMonth.csv")
    trend_data = trend_data.iloc[:,1:]

    #식품
    trend_data_food = trend_data[["years", "months","count : 식품류"]]
    trend_data_food.columns = list(trend_data.columns[:2]) + ["Food"]
    #-25s년 절사
    trend_data_food = trend_data_food[trend_data_food["years"]!=2025]
    #-타입형변환
    trend_data_food[["years", "months"]] = trend_data_food[["years", "months"]].astype("str")
    trend_data_food["Date"] = pd.to_datetime(trend_data_food["years"] + "-" + trend_data_food["months"])

    # 그래프 그리기
    fig_f = px.scatter(
        trend_data_food,
        x="Date",
        y="Food",
        trendline="ols",
        title="Food Sales with Regression Trendline",
    )

    # 데이터 선 + 마커 + 값 표시
    fig_f.update_traces(
        line=dict(color="blue"),
        marker=dict(color="blue", size=6),
    )

    # 추세선 스타일 변경
    fig_f.update_traces(
        line=dict(color="red", width=3, dash="solid"),
        selector=dict(mode="lines")
    )

    # 레이아웃 설정
    fig_f.update_layout(
        xaxis=dict(
            title="Date",
            tickformat="%Y-%m",
            tickangle=20
        ),
        yaxis=dict(title="Count"),
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_f, use_container_width=True, key="trend_food_pd")

    #Alcohol
    trend_data_alcohol = trend_data[["years", "months","count : 주류"]]
    trend_data_alcohol.columns = list(trend_data.columns[:2]) + ["Alcohol"]
    #-25s년 절사
    trend_data_alcohol = trend_data_alcohol[trend_data_alcohol["years"]!=2025]
    #-타입형변환
    trend_data_alcohol[["years", "months"]] = trend_data_alcohol[["years", "months"]].astype("str")
    trend_data_alcohol[["years", "months"]] = trend_data_alcohol[["years", "months"]].astype("str")
    trend_data_alcohol["Date"] = pd.to_datetime(trend_data_alcohol["years"] + "-" + trend_data_alcohol["months"])
    trend_data_alcohol = trend_data_alcohol[["Date","Alcohol"]]

    # 그래프 그리기
    fig_a = px.scatter(
        trend_data_alcohol,
        x="Date",
        y="Alcohol",
        trendline="ols",
        title="Alcohol Sales with Regression Trendline",
    )

    # 데이터 선 + 마커 + 값 표시
    fig_a.update_traces(
        line=dict(color="blue"),
        marker=dict(color="blue", size=6),
    )

    # 추세선 스타일 변경-
    fig_a.update_traces(
        line=dict(color="red", width=3, dash="solid"),
        selector=dict(mode="lines")
    )

    # 레이아웃 설정
    fig_a.update_layout(
        xaxis=dict(
            title="Date",
            tickformat="%Y-%m",
            tickangle=20
        ),
        yaxis=dict(title="Count"),
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_a, use_container_width=True, key="trend_alcohol_pd")

    #Meat
    trend_data_meat = trend_data[["years", "months","count : 육류 "]]
    trend_data_meat.columns = list(trend_data.columns[:2]) + ["Meat"]
    #-25s년 절사
    trend_data_meat = trend_data_meat[trend_data_meat["years"]!=2025]
    #-타입형변환
    trend_data_meat[["years", "months"]] = trend_data_meat[["years", "months"]].astype("str")
    trend_data_meat[["years", "months"]] = trend_data_meat[["years", "months"]].astype("str")
    trend_data_meat["Date"] = pd.to_datetime(trend_data_meat["years"] + "-" + trend_data_meat["months"])
    trend_data_meat = trend_data_meat[["Date","Meat"]]

    # 그래프 그리기
    fig_m = px.scatter(
        trend_data_meat,
        x="Date",
        y="Meat",
        trendline="ols",
        title="Meat Sales with Regression Trendline",
    )

    # 데이터 선 + 마커 + 값 표시
    fig_m.update_traces(
        line=dict(color="blue"),
        marker=dict(color="blue", size=6),
    )

    # 추세선 스타일 변경
    fig_m.update_traces(
        line=dict(color="red", width=3, dash="solid"),
        selector=dict(mode="lines")
    )

    # 레이아웃 설정
    fig_m.update_layout(
        xaxis=dict(
            title="Date",
            tickformat="%Y-%m",
            tickangle=20
        ),
        yaxis=dict(title="Count"),
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_m, use_container_width=True, key="trend_meat_pd")


    #Ship Parts : 선박부품
    trend_data_shipparts = trend_data[["years", "months","count : 선박부품"]]
    trend_data_shipparts.columns = list(trend_data.columns[:2]) + ["Ship parts"]
    #-25s년 절사
    trend_data_shipparts = trend_data_shipparts[trend_data_shipparts["years"]!=2025]
    #-타입형변환
    trend_data_shipparts[["years", "months"]] = trend_data_shipparts[["years", "months"]].astype("str")
    trend_data_shipparts["Date"] = pd.to_datetime(trend_data_shipparts["years"] + "-" + trend_data_shipparts["months"])
    trend_data_shipparts = trend_data_shipparts[["Date","Ship parts"]]

    # 그래프 그리기
    fig_sp = px.scatter(
        trend_data_shipparts,
        x="Date",
        y="Ship parts",
        trendline="ols",
        title="Ship parts with Regression Trendline",
    )

    # 데이터 선 + 마커 + 값 표시
    fig_sp.update_traces(
        line=dict(color="blue"),
        marker=dict(color="blue", size=6),
    )

    # 추세선 스타일 변경
    fig_sp.update_traces(
        line=dict(color="red", width=3, dash="solid"),
        selector=dict(mode="lines")
    )

    # 레이아웃 설정
    fig_sp.update_layout(
        xaxis=dict(
            title="Date",
            tickformat="%Y-%m",
            tickangle=20
        ),
        yaxis=dict(title="Count"),
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_sp, use_container_width=True, key="trend_shippart_pd")

    st.subheader("결론", anchor=False)
    st.markdown("""
    추세 분석 결과, <span style='color:orange; font-weight:bold; font-size:20px;'>Food, Meat</span>는 뚜렷한 상승 추세를 보여 소싱 품목으로 선정되었으나, <span style='color:white; font-weight:bold; font-size:20px;'>Alcohol은 완만한 추세를 보여 최종 품목에서 제외하였습니다.
    또한, Ship Parts는 판매 금액은 높았지만 판매 건수 기준으로는 하락 추세를 보여 소싱 대상에서 제외</span>하였습니다.
    <span style='color:white; font-weight:bold; font-size:20px;'>Fuel의 경우, 높은 판매 금액을 기록하였으나 이는 선사에 직접 주입되는 연료로, 항구 내에서 주유되는 특수 환경을 고려해 품목 선정에서 제외하였으며,
    Others는 구성 품목의 세부 분류가 불명확하여 분석 및 소싱에서 제외</span>하였습니다.
    따라서, <span style='color:orange; font-weight:bold; font-size:20px;'>Food, Meat를 취급 및 유통하는 기업</span>을 대상으로 데이터 수집하여 그 위치와 정보를 아래와 같이 시각화했습니다.<br> 아래 데이터를 바탕으로 <span style='color:orange; font-weight:bold; font-size:20px;'>부산 인근의 기업현황을 파악 가능하고 컨택 및 소싱하는 데 활용</span> 할수 있습니다.
    """, unsafe_allow_html=True)

    #기업데이터 불러오기
    meatCompany_info = pd.read_csv("./useData/finishPrepro/meat_company_LaLo.csv", encoding="utf-8-sig")
    foodCompany_info = pd.read_csv("./useData/finishPrepro/food_company_LaLo.csv", encoding="utf-8-sig")

    meatCompany_info = meatCompany_info.iloc[:,1:]
    foodCompany_info = foodCompany_info.iloc[:,1:]
    mergeCompany_info = pd.concat(
        [meatCompany_info,
        foodCompany_info],
        axis=0,
        ignore_index=True
    )
    mergeCompany_info = mergeCompany_info.reset_index()
    mergeCompany_info = mergeCompany_info.iloc[:,1:]

    # attr option > "OpenStreetMap","Stamen Terrain","Stamen Toner","Stamen Watercolor","CartoDB positron","CartoDB dark_matter"
    #대한민국 : 36.554311389428506, 127.91990571290032
    targetArea = folium.Map(
        location=[36.19727816840753, 127.89219063707009],
        zoom_start=7,
        tiles="CartoDB positron",
        # width="100%",     # 또는 px 단위로: "800px"
        # height="500px"    # 문자열로 지정해야 함 (숫자 X)
    )

    busanGeo = "./useData/koreaBusan.geojson"

    with open(busanGeo, encoding="utf-8-sig") as f:
        myGeo = json.load(f)

    # Geo 스타일 함수
    def myGeo_style(x):
        return {
            "fillColor": "#11c511",   # 채우기 색 (파랑색)
            "color": "grey",         # 경계선 색
            "weight": 0.5,              # 선 굵기
            "fillOpacity": 1       # 투명도
        }

    folium.GeoJson(
        data=myGeo,
        name="Busan Metropolitan City, Republic of Korea",
        style_function=myGeo_style
    ).add_to(targetArea)

    # Set shared icon size and anchor point (공통 아이콘 크기 및 정렬 기준점 설정)
    icon_size = (21, 21)        # icon_size: (width, height) in pixels (아이콘의 가로, 세로 픽셀 크기)
    icon_anchor = (10, 10)      # icon_anchor: pixel offset from top-left to center (중앙 정렬: 좌측 상단 기준으로 (12, 12))

    # Iterate over each row in the company DataFrame
    # 회사 정보 데이터프레임의 각 행을 반복 처리함
    for i, v in mergeCompany_info.iterrows():

        # Extract latitude and longitude from last two columns
        # 위도, 경도 정보를 마지막 두 열에서 가져옴
        Latitude = v[-2]
        Longitude = v[-1]

        # Create HTML-formatted tooltip content
        # 마우스 오버 시 표시될 HTML 형식의 회사 정보 문자열 생성
        companyInfo = f"""
            {v[1]} Company Information<br>
            (1) Category : {v[0]}<br>
            (2) Owner : {v[1]}<br>
            (3) Address : {v[5]}<br>
            (4) Contact point : {v[6]}
        """

        # Generate tooltip for hover interaction
        # 마우스 오버 시 정보를 보여줄 Tooltip 객체 생성
        mytooltip = folium.Tooltip(companyInfo, sticky=True)

        # Check if company is meat-related and assign style accordingly
        # 회사가 "육류" 관련이면 해당 아이콘 및 색상 지정
        if "육류" in v[0]:

            # Define meat company icon (육류 회사 아이콘 설정)
            meat_icon_path = "./useData/myImage/meatCompany.png"  # 경로: meatCompany.png
            meat_icon = CustomIcon(
                icon_image=meat_icon_path,    # icon_image: 이미지 경로 (meat 아이콘)
                icon_size=icon_size,          # icon_size: 아이콘 크기 (25 x 25)
                icon_anchor=icon_anchor       # icon_anchor: 아이콘 내부의 중앙 좌표를 지도 위치에 정렬
            )

            # Add meat company marker to map
            # 육류 회사 위치에 마커(아이콘)를 지도에 추가함
            folium.Marker(
                location=[Latitude, Longitude],  # 마커가 표시될 지도상의 좌표
                icon=meat_icon,                  # 육류 회사 전용 커스텀 아이콘
                tooltip=mytooltip                # 마우스 오버 시 툴팁 표시
            ).add_to(targetArea)

            # Add circle around meat marker (for visual emphasis)
            # 육류 마커 주변에 반경 원 시각화 추가
            folium.CircleMarker(
                location=[Latitude, Longitude],  # 원의 중심 위치
                radius=30,                       # 반지름 (픽셀 단위)
                fill=True,                       # 내부 색상 채움
                color="none",                    # 외곽선 없음
                fill_color="#ff7f0e"             # 채우기 색상 (주황 계열)
            ).add_to(targetArea)

        else:
            # Non-meat companies (e.g., food companies) 처리
            # 육류 외 식품 관련 회사 처리
            # Define food company icon (식품 회사 아이콘 설정)
            food_icon_path = "./useData/myImage/foodCompany.png"  # 경로: foodCompany.png
            food_icon = CustomIcon(
                icon_image=food_icon_path,    # icon_image: 이미지 경로 (food 아이콘)
                icon_size=icon_size,          # 아이콘 크기 (25 x 25)
                icon_anchor=icon_anchor       # 아이콘 중앙을 지도 위치에 정렬
            )

            # Add food company marker to map
            # 식품 회사 위치에 마커(아이콘)를 지도에 추가함
            folium.Marker(
                location=[Latitude, Longitude],  # 지도상의 좌표
                icon=food_icon,                  # 식품 회사 전용 커스텀 아이콘
                tooltip=mytooltip                # 마우스 오버 시 툴팁 표시
            ).add_to(targetArea)

            # Add circle around food marker (for visual emphasis)
            # 식품 마커 주변에 반경 원 시각화 추가
            folium.CircleMarker(
                location=[Latitude, Longitude],  # 원의 중심 위치
                radius=30,                       # 반지름 (육류보다 크게 설정)
                fill=True,                       # 내부 채움
                color="none",                    # 테두리 없음
                fill_color="#65b2f5"             # 채우기 색상 (하늘색 계열)
            ).add_to(targetArea)

    # Display the map with all company markers and radius overlays
    # 모든 회사 위치 마커 및 시각적 원이 포함된 지도를 출력함
    st_folium(targetArea, width=1500, height=600, key="kr_pdCompany_possition")
