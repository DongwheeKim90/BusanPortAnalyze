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

tab_1, tab_2, tab_3 = st.tabs(["Analysis Process(EN)", "Analysis Process(KR)", "Data Preprocessing"])

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

    st.subheader("Marketing Demand Research for Sourcing Items", anchor=False)
    st.markdown("Based on the annual ship supply data and item-specific trends above, we have finalized <span style='color:orange; font-weight:bold; font-size:20px;'>‘Meat’ and ‘Food’</span> as the final sourcing items. Furthermore, we conducted a <span style='color:orange; font-weight:bold; font-size:20px;'>word cloud analysis for detailed sub-item decisions</span> as part of our marketing research.<br>(The word cloud was generated by <span style='color:white; font-weight:bold; font-size:20px;'>crawling content related to Korean meat and food from overseas social media and blogs</span>, as shown below.)", unsafe_allow_html=True)
    # Create two columns
    img_col_1, img_col_2 = st.columns(2)
    # Column 1 with container
    with img_col_1:
        with st.container():
            st.image("./useData/myImage/Meat_wordCloud.png")
    # Column 2 with container
    with img_col_2:
        with st.container():
            st.image("./useData/myImage/Food_wordCloud.png")
    st.markdown('''
    According to the word cloud results, <span style='color:orange; font-weight:bold; font-size:20px;'>keywords like Bulgogi, Ogyeopsal, Samgyeopsal, Chicken, and Galbi</span> appeared most frequently for meat items, while <span style='color:orange; font-weight:bold; font-size:20px;'>Fish, Kimchi, Gukbap, Noodles, and Pajeon</span> stood out in food-related content. Based on this, we can utilize the keywords that appeared in the word cloud to source companies that deal with these specific products.
    ''', unsafe_allow_html=True)


    st.subheader("Conclusion", anchor=False)
    st.markdown("""
    Based on the trend analysis, <span style='color:orange; font-weight:bold; font-size:20px;'>Food and Meat</span> showed a clear upward trend and were selected as sourcing items. In contrast, <span style='color:white; font-weight:bold; font-size:20px;'>Alcohol showed only a mild trend and was excluded from the final selection.
    Although Ship Parts recorded high sales in terms of revenue, they showed a declining trend in the number of transactions and were therefore excluded from sourcing.
    Fuel, despite recording high sales, was excluded due to its unique nature of being directly refueled into ships at ports.
    Others were excluded due to unclear classification of the items within that category.</span>
    <br>Therefore, we collected data on companies that <span style='color:orange; font-weight:bold; font-size:20px;'>distribute and handle Food and Meat</span>, and visualized their locations and information as shown below. Based on this data, we can <span style='color:orange; font-weight:bold; font-size:20px;'>understand the status of companies near Busan and use it for outreach and sourcing purposes</span>.
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
    st_folium(targetArea, width=1500, height=600, key="kr_pdCompany_position_")

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

    st.subheader("소싱품목에 대한 마케팅 수요조사", anchor=False)
    st.markdown("우리는 위에서 년도별 선용품 데이터와 품목별 추세를 바탕으로 <span style='color:orange; font-weight:bold; font-size:20px;'>'고기', '음식'</span>을 최종 소싱품목으로 결정했습니다. 그리고 더 나아가  <span style='color:orange; font-weight:bold; font-size:20px;'>품목별 구체적인 하위 제품 결정을 위한 마케팅 조사로 워드 크라우드</span>를 진행했습니다.<br>(워드 크라우드는 <span style='color:white; font-weight:bold; font-size:20px;'>해외 SNS 및 블로그 등에서 대한민국 육류, 음식에 대한 콘텐츠를 대상으로 데이터 크롤링</span> 후 아래와 같이 진행 했습니다.)", unsafe_allow_html=True)
    # Create two columns
    img_col_1, img_col_2 = st.columns(2)
    # Column 1 with container
    with img_col_1:
        with st.container():
            st.image("./useData/myImage/Meat_wordCloud.png")
    # Column 2 with container
    with img_col_2:
        with st.container():
            st.image("./useData/myImage/Food_wordCloud.png")
    st.markdown('''
        워드 크라우드 결과 <span style='color:orange; font-weight:bold; font-size:20px;'>고기 품목에서는 Bulgogo, Ogyeopsal, Samgeopsal, Chikin, Galbi</span> 등이 제일 많이 출현하였고, <span style='color:orange; font-weight:bold; font-size:20px;'>음식 품목에서는 Fish, Kimchi,Gukbap, Noodles, Pajeon</span> 등이 출현한 것을 파악할 수 있습니다. 이에 따라 우리는 워드 크라우드에 출현한 키워드 들을 바탕으로 해당 제품을 취급하는 기업을 소싱하는 데 해당 데이터를 활용 할 수 있습니다.
    ''', unsafe_allow_html=True)

    st.subheader("결론", anchor=False)
    st.markdown("""
    추세 분석 결과, <span style='color:orange; font-weight:bold; font-size:20px;'>Food, Meat</span>는 뚜렷한 상승 추세를 보여 소싱 품목으로 선정되었으나, <span style='color:white; font-weight:bold; font-size:20px;'>Alcohol은 완만한 추세를 보여 최종 품목에서 제외하였습니다.
    또한, Ship Parts는 판매 금액은 높았지만 판매 건수 기준으로는 하락 추세를 보여 소싱 대상에서 제외</span>하였습니다.
    <span style='color:white; font-weight:bold; font-size:20px;'>Fuel의 경우, 높은 판매 금액을 기록하였으나 이는 배에 직접 주입되는 연료로, 항구 내에서 주유되는 특수 환경을 고려해 품목 선정에서 제외하였으며,
    Others는 구성 품목의 세부 분류가 불명확하여 분석 및 소싱에서 제외</span>하였습니다.
    <br>따라서, <span style='color:orange; font-weight:bold; font-size:20px;'>Food, Meat를 취급 및 유통하는 기업</span>을 대상으로 데이터 수집하여 그 위치와 정보를 아래와 같이 시각화했습니다. 아래 데이터를 바탕으로 <span style='color:orange; font-weight:bold; font-size:20px;'>부산 인근의 기업현황을 파악 가능하고 컨택 및 소싱하는 데 활용</span> 할수 있습니다.
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
    st_folium(targetArea, width=1500, height=600, key="kr_pdCompany_position")

with tab_3:
    st.markdown('''
    (1) Data Source : "https://dart.fss.or.kr/dsae001/main.do#none" <br>
    (2) Collected Data : Collect corporate data related to ship supplies, especially companies dealing with meat and food.(선용품 품목 관련, 특히 육류 및 식품을 취급하는 기업 정보 데이터 수집)<br>
    (3) Data Type : Structured Data(정형 데이터)<br>
    (4) Technologies Used : Selenium, BeautifulSoup(bs4), Pandas<br>
    (5) Data Collection and Preprocessing Process
    ''',unsafe_allow_html=True)
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Collection (데이터 수집)</span>", unsafe_allow_html=True)
    st.video("./useData/prodcompany.mp4")
    st.code('''
    # Author: Dongwhee Kim
    # Date: 2025-04-12
    # Description: Selenium-based scraper for extracting meat and food distribution company information from the DART system.

    from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing (HTML 파싱을 위한 BeautifulSoup 임포트)
    import pandas as pd  # Import pandas for data analysis (데이터 분석을 위한 pandas 임포트)
    import requests as req  # Import requests for HTTP requests (HTTP 요청을 위한 requests 임포트)

    from selenium import webdriver  # Import the Selenium WebDriver module (Selenium WebDriver 모듈 임포트)
    from selenium.webdriver.chrome.service import Service  # Import the Chrome driver service manager (Chrome 드라이버 서비스 매니저 임포트)
    from selenium.webdriver.common.by import By  # Import locator strategies (요소 탐색 전략 클래스 임포트)
    from selenium.webdriver.support.ui import WebDriverWait  # Import explicit wait utility (명시적 대기를 위한 WebDriverWait 임포트)
    from selenium.webdriver.support import expected_conditions as EC  # Import expected conditions (기대 조건 클래스 임포트)
    from selenium.webdriver.common.keys import Keys  # Import keyboard key constants (키보드 키 입력 상수 임포트)
    from selenium.webdriver import ActionChains  # Import for advanced user interactions (고급 사용자 동작을 위한 ActionChains 임포트)

    import time  # Import time module for delays (지연을 위한 time 모듈 임포트)
    import re  # Import regular expressions for text processing (정규표현식 처리를 위한 re 모듈 임포트)

    # Set Chrome options (크롬 옵션 설정)
    myOption = webdriver.ChromeOptions()
    myOption.add_argument("no-sandbox")  # Disable sandbox mode for Linux environments (리눅스 환경 등에서 샌드박스 비활성화)

    # Set path to Chrome driver (크롬 드라이버 경로 지정)
    myChrome = Service("../autoDriver/chromedriver.exe")

    # Launch Chrome browser (크롬 브라우저 실행)
    myChrome = webdriver.Chrome(service=myChrome, options=myOption)

    # Maximize browser window (브라우저 창 최대화)
    myChrome.maximize_window()

    # Set explicit wait of 3 seconds (3초 명시적 대기 설정)
    waitTime = WebDriverWait(myChrome, 3)

    # Define BS4 single selector function (BS4 단일 선택자 함수 정의)
    def bs4_find(value):
        return mysoup.select_one(value)  # Return first matched element (첫 번째 일치하는 요소 반환)

    # Define BS4 multiple selector function (BS4 다중 선택자 함수 정의)
    def bs4_finds(value):
        return mysoup.select(value)  # Return all matched elements (모든 일치하는 요소 반환)

    # Define Selenium single element find function (Selenium 단일 요소 탐색 함수 정의)
    def selenium_find(value):
        return waitTime.until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))  # CSS 셀렉터로 단일 요소 대기 후 반환

    # Define Selenium multiple element find function (Selenium 다중 요소 탐색 함수 정의)
    def selenium_finds(value):
        return waitTime.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, value)))  # CSS 셀렉터로 다중 요소 대기 후 반환

    # Access the DART business info page (DART 업종정보 페이지 접속)
    myUrl = "https://dart.fss.or.kr/dsae001/main.do#none"
    myChrome.get(myUrl)  # Load the URL (URL 로드)
    time.sleep(10)  # Wait for the page to load completely (페이지 완전히 로드되도록 대기)
    print(f"{myUrl} 접속완료")  # Print confirmation (접속 확인 출력)

    # Step 1: Select 'Business Category' tab (1단계: 업종별 탭 클릭)
    selenium_find("li#businessTab").click()  # Click '업종별' 탭
    print("업종별 클릭")
    time.sleep(3)  # Wait for the category tree to appear (카테고리 트리 표시될 때까지 대기)

    # Click tree icons to expand category (업종별 항목 펼치기)
    selenium_finds("i.jstree-icon.jstree-ocl")[7].click()  # Click 8th node (8번째 노드 클릭)
    time.sleep(2)
    selenium_finds("i.jstree-icon.jstree-ocl")[9].click()  # Click 10th node (10번째 노드 클릭)
    time.sleep(2)
    selenium_finds("i.jstree-icon.jstree-ocl")[12].click()  # Click 13th node (13번째 노드 클릭)
    time.sleep(2)
    selenium_finds("i.jstree-icon.jstree-ocl")[14].click()  # Click 15th node (15번째 노드 클릭)
    time.sleep(2)

    # Click specific industry: '육류 가공식품 도매업' (해당 업종 클릭)
    myChrome.find_element(By.XPATH, "//a[contains(., '육류 가공식품 도매업')]").click()
    time.sleep(2)  # Wait after selection (선택 후 대기)

    # Lists for storing company info (기업 정보 저장용 리스트 선언)
    info_list = list()
    category_list = list()
    companyNM_list = list()
    companyOwner_list = list()
    corporate_Registration_list = list()
    business_Registration_list = list()
    companyAddress_list = list()
    companyCP_list = list()

    # Start pagination and data scraping (페이지 순회 및 데이터 수집 시작)
    page_button_len = myChrome.find_elements(By.XPATH, '//*[@id="listContents"]/div[2]/div[2]/ul/li/a')  # Find page buttons (페이지 버튼 찾기)

    if page_button_len:
        for v in range(len(page_button_len)):
            v += 1
            page_button = myChrome.find_element(By.XPATH, f'//*[@id="listContents"]/div[2]/div[2]/ul/li[{v}]/a')
            page_button.click()
            print(f"{v} 페이지 클릭")
            time.sleep(10)

            meat_company_list = selenium_finds("span.nobr1")
            for v in meat_company_list:
                v.click()
                time.sleep(5)

                for v in range(0, 16):
                    v += 1
                    if v == 14:
                        category = myChrome.find_element(By.XPATH , f"//*[@id='corpDetailTabel']/tbody/tr[{v}]/td").text
                        category_list.append(category)
                    elif v == 1:
                        name = myChrome.find_element(By.XPATH , f"//*[@id='corpDetailTabel']/tbody/tr[{v}]/td").text
                        companyNM_list.append(name)
                    elif v == 5:
                        owner = myChrome.find_element(By.XPATH , f"//*[@id='corpDetailTabel']/tbody/tr[{v}]/td").text
                        companyOwner_list.append(owner)
                    elif v == 7:
                        crNum = myChrome.find_element(By.XPATH , f"//*[@id='corpDetailTabel']/tbody/tr[{v}]/td").text
                        corporate_Registration_list.append(crNum)
                    elif v == 8:
                        brNum = myChrome.find_element(By.XPATH , f"//*[@id='corpDetailTabel']/tbody/tr[{v}]/td").text
                        business_Registration_list.append(brNum)
                    elif v == 9:
                        address = myChrome.find_element(By.XPATH , f"//*[@id='corpDetailTabel']/tbody/tr[{v}]/td").text
                        companyAddress_list.append(address)
                    elif v == 12:
                        contact = myChrome.find_element(By.XPATH , f"//*[@id='corpDetailTabel']/tbody/tr[{v}]/td").text
                        companyCP_list.append(contact)
                    time.sleep(5)

    # Collapse current category and go to next (현재 업종 닫고 다음 업종으로 이동)
    selenium_finds("i.jstree-icon.jstree-ocl")[14].click()
    time.sleep(2)
    selenium_finds("i.jstree-icon.jstree-ocl")[13].click()
    time.sleep(2)
    myChrome.find_element(By.XPATH, "//a[contains(., '육류 도매업')]").click()
    time.sleep(2)

    # After scraping, create final DataFrame for meat companies (육류 도매업 최종 데이터프레임 생성)
    meat_companyKR = pd.DataFrame({
        "Company category" : category_list,
        "Comapany name" : companyNM_list,
        "CEO" : companyOwner_list,
        "Corporate registration number" : corporate_Registration_list,
        "Business registration number" : business_Registration_list,
        "Address" : companyAddress_list,
        "Contact point" : companyCP_list
    })

    meat_companyKR.head()
    print(meat_companyKR.shape)
    meat_companyKR.to_csv("../useData/raw_meat_companyKR.csv", encoding="utf-8-sig", index=False)

    # food_companyKR = pd.DataFrame({...}) # 동일 방식으로 생성 가능

    meat_companyKR = pd.read_csv("../useData/raw_meat_companyKR.csv", encoding="utf-8-sig")
    meat_companyKR.to_csv("../useData/raw_meat_companyKR.csv", encoding="utf-8-sig", index=False)

    print("크롤링 및 저장 완료")
            ''')
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Preprocessing (데이터 가공)</span>", unsafe_allow_html=True)
    st.code('''
    # ------------------------------------------------------------------------------
    # Author: DongWhee Kim
    # Date: 2025-04-12
    # Description: Preprocessing and visualization of monthly product needs data
    #              including total counts, prices, and trend analysis of major items.
    # ------------------------------------------------------------------------------

    import pandas as pd                      # For data manipulation (데이터 처리용)
    import plotly.express as px              # For scatter plots and regression lines (산점도 및 추세선)
    import plotly.graph_objects as go        # For grouped bar charts (그룹형 막대그래프)
    import os                                # For file handling (파일 읽기)

    # Define month and field combinations for renaming columns (월 + 필드명 조합 정의)
    field_list = [" : total count", ": total price"]
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']

    combined_field_list = [month + field for month in month_list for field in field_list]

    # Function to clean strings and convert to int (쉼표, 공백 제거 후 정수형 변환)
    def clean_and_convert_to_int(x):
        return (
            x.replace(r"[,　\s]", "", regex=True)  # Remove comma, full-width space, normal space
            .fillna("0")                               # Fill NaN with 0
            .astype(str)                               # Convert to string
            .replace("", "0")                         # Replace empty strings with 0
            .astype("int32")                          # Convert to int
        )

    # Function to build bar traces for a given dataframe and column list (막대그래프 요소 생성 함수)
    def build_bar_traces(df, x_data, columns):
        traces = []
        for col in columns:
            traces.append(
                go.Bar(
                    x=x_data,
                    y=df[col],
                    name=col,
                    text=df[col],
                    textposition="inside",
                    texttemplate="%{text:,}"
                )
            )
        return traces

    # Function to create a trend scatter plot with regression line (회귀선 포함 산점도 생성 함수)
    def create_trend_scatter(df, date_col, value_col, title, y_title):
        fig = px.scatter(
            df,
            x=date_col,
            y=value_col,
            trendline="ols",
            title=title
        )
        fig.update_traces(
            line=dict(color="red", width=3, dash="solid"),
            marker=dict(color="blue", size=6),
            selector=dict(mode="lines")
        )
        fig.update_layout(
            xaxis=dict(title="Date", tickformat="%Y-%m", tickangle=20),
            yaxis=dict(title=y_title),
            legend=dict(bordercolor="grey", borderwidth=0.5)
        )
        return fig

    # Function to process trend data and return cleaned DataFrame with datetime (월별 추세용 데이터프레임 생성 함수)
    def prepare_trend_data(df, year_col, month_col, value_col, new_col_name):
        trend_df = df[[year_col, month_col, value_col]].copy()
        trend_df.columns = ["year", "month", new_col_name]
        trend_df = trend_df[trend_df["year"] != "2025"]  # Ensure year is string for comparison
        trend_df[["year", "month"]] = trend_df[["year", "month"]].astype(str)
        trend_df["date"] = pd.to_datetime(trend_df["year"] + "-" + trend_df["month"])
        return trend_df[["date", new_col_name]]

    # Function to annotate highest value in a bar chart (막대그래프에서 최고값에 주석 추가)
    def add_max_annotation(fig, x_data, y_data, label_prefix):
        max_index = y_data.idxmax()
        max_value = y_data[max_index]
        max_year = x_data[max_index]
        fig.add_annotation(
            x=max_year,
            y=max_value,
            text=f"{label_prefix} {max_value:,} in {max_year}",
            showarrow=False,
            font=dict(size=10, color="#fc7507"),
            xanchor="center",
            yanchor="top",
            xshift=-50,
            yshift=45,
            bordercolor="#0e28ea",
            borderwidth=1,
            borderpad=4,
            bgcolor="#0e28ea",
            opacity=0.9
        )
        return fig

    # Function to generate and show a bar chart for top N items (상위 N개 항목에 대한 막대그래프 시각화 함수)
    def visualize_top_items(df, x_col, y_cols, title, y_title):
        traces = build_bar_traces(df, df[x_col], y_cols)
        fig = go.Figure(data=traces)
        fig.update_layout(
            barmode="group",
            title=dict(text=title, x=0.5),
            xaxis=dict(title=x_col),
            yaxis_title=y_title,
            legend=dict(bordercolor="grey", borderwidth=0.5)
        )
        return fig

    # Trendline Visualization for Monthly Product Sales (월별 품목별 추세선 시각화 예시)
    if __name__ == "__main__":
        trend_data = pd.read_csv("../useData/finishPrepro/finish_prod_totalCountPrice_yearMonth.csv")

        # Count Trends
        trend_food = prepare_trend_data(trend_data, "years", "months", "count : 식품류", "Food")
        trend_meat = prepare_trend_data(trend_data, "years", "months", "count : 육류 ", "Meat")
        trend_alcohol = prepare_trend_data(trend_data, "years", "months", "count : 주류", "Alcohol")
        trend_parts = prepare_trend_data(trend_data, "years", "months", "count : 선박부품", "Ship Parts")

        fig_trend_food = create_trend_scatter(trend_food, "date", "Food", "Food Sales with Regression Trendline", "Count")
        fig_trend_meat = create_trend_scatter(trend_meat, "date", "Meat", "Meat Sales with Regression Trendline", "Count")
        fig_trend_alcohol = create_trend_scatter(trend_alcohol, "date", "Alcohol", "Alcohol Sales with Regression Trendline", "Count")
        fig_trend_parts = create_trend_scatter(trend_parts, "date", "Ship Parts", "Ship Parts Sales with Regression Trendline", "Count")

        fig_trend_food.show()
        fig_trend_meat.show()
        fig_trend_alcohol.show()
        fig_trend_parts.show()

        # Price Trends
        trend_price_food = prepare_trend_data(trend_data, "years", "months", "price(KR) : 식품류", "Food")
        trend_price_meat = prepare_trend_data(trend_data, "years", "months", "price(KR) : 육류 ", "Meat")
        trend_price_alcohol = prepare_trend_data(trend_data, "years", "months", "price(KR) : 주류", "Alcohol")
        trend_price_parts = prepare_trend_data(trend_data, "years", "months", "price(KR) : 선박부품", "Ship Parts")

        fig_price_food = create_trend_scatter(trend_price_food, "date", "Food", "Food Sales Amount with Regression Trendline", "KRW")
        fig_price_meat = create_trend_scatter(trend_price_meat, "date", "Meat", "Meat Sales Amount with Regression Trendline", "KRW")
        fig_price_alcohol = create_trend_scatter(trend_price_alcohol, "date", "Alcohol", "Alcohol Sales Amount with Regression Trendline", "KRW")
        fig_price_parts = create_trend_scatter(trend_price_parts, "date", "Ship Parts", "Ship Parts Sales Amount with Regression Trendline", "KRW")

        fig_price_food.show()
        fig_price_meat.show()
        fig_price_alcohol.show()
        fig_price_parts.show()
    ''')
