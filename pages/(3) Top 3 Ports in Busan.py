import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import folium
from folium.features import CustomIcon
from streamlit_folium import st_folium
import scipy.stats as stats
from sklearn.preprocessing import MinMaxScaler
import json

st.set_page_config(layout="wide")

st.title("Data Analysis for Sourcing Item-Related Companies for an Online Ship Supply Platform", anchor=False)

tab_1, tab_2, tab_3 = st.tabs(["Analysis Process(EN)", "Analysis Process(KR)", "Data Preprocessing"])

with tab_1:
    st.subheader("Busan Ports", anchor=False)

    st.markdown('''
    Among all ports in South Korea, Busan Port recorded the highest number of foreign vessel arrivals and cargo volume over the years.
    In fact, Busan Port consists of three main ports: <span style='color:orange; font-weight:bold; font-size:20px;'>New Port, North Port, and Gamcheon Port</span>, which are generally referred to collectively as "Busan Port".
    Accordingly, we collected and visualized data related to the number of ship arrivals and cargo volume across these three ports.
    ''', unsafe_allow_html=True)


    # Define map tile options
    tile_option = "CartoDB positron"

    # Define Busan center coordinates
    busan_center = [35.18397316013664, 129.07057865661844]

    # Define color settings
    circle_fill_color = "#ff7f0e"
    circle_border_color = "#1f77b4"
    geo_fill_color = "#05d06b"

    # Create base map
    targetArea = folium.Map(
        location=busan_center,
        zoom_start=11,
        tiles=tile_option
    )

    # Load GeoJSON (Busan boundary)
    busanGeo = "./useData/koreaBusan.geojson"
    with open(busanGeo, encoding="utf-8-sig") as f:
        myGeo = json.load(f)

    # Style for Busan region
    def myGeo_style(x):
        return {
            "fillColor": geo_fill_color,
            "color": "grey",
            "weight": 0.5,
            "fillOpacity": 0.2
        }

    # Add Busan boundary to map
    folium.GeoJson(
        data=myGeo,
        name="Busan Metropolitan City, Republic of Korea",
        style_function=myGeo_style
    ).add_to(targetArea)

    # Load port data
    portPosition = pd.read_csv("./useData/busanThreeport_position.csv")

    # Iterate through port data
    for i, v in portPosition.iterrows():
        lat = v["Latitude"]
        lon = v["Longitude"]

        # Popup content
        portNames = f"- Port Name : {v[0]}<br>- Port Address : {v[1]}"
        popup = folium.Popup(
            portNames,
            max_width=300,
            min_width=30,
            max_height=300
        )

        # Custom port icon
        myIcon = "./useData/myImage/shipping.png"
        myIcon_edit = CustomIcon(
            icon_image=myIcon,
            icon_size=(47, 47),
            icon_anchor=(23, 23)
        )

        # Add marker
        folium.Marker(
            location=[lat, lon],
            icon=myIcon_edit
        ).add_child(popup).add_to(targetArea)

        # Add circular highlight around port
        folium.CircleMarker(
            location=[lat, lon],
            radius=60,
            fill=True,
            color=circle_border_color,
            fill_color=circle_fill_color
        ).add_to(targetArea)

    # Display the map once after all markers are added
    st_folium(targetArea, width=1500, height=600, key="en_pdCompany_possition")


    myfolders = os.listdir("./useData/busanport/")

    readFile_list = list()

    for v in range(len(myfolders)):
        if "부산항(전체)" not in myfolders[v]:
            open_data = pd.read_csv(f"./useData/busanport/{myfolders[v]}")
            readFile_list.append(open_data)
        else:
            totalBusanWeight = pd.read_csv(f"./useData/busanport/{myfolders[v]}")

    individual_port = pd.concat(readFile_list, axis=0, ignore_index=False)

    # 타입변경
    # individual_port[["Ship Count", "GT(Gross Tonnage)"]].astype("int64") > ","로 인해 변환 불가

    # , 제거 함수 정의
    def notComma(x):
        return x.replace(",", "")

    individual_port["Year"] = individual_port["Year"].astype("object")
    individual_port["Ship Count"] = individual_port["Ship Count"].apply(notComma).astype("int64")
    individual_port["GT(Gross Tonnage)"] = individual_port["GT(Gross Tonnage)"].apply(notComma).astype("int64")

    individual_port.to_csv("./useData/finishPrepro/busanAllPorts_GTCount.csv", encoding="utf-8-sig")

    # 25년도는 절사
    individual_port = individual_port[individual_port["Year"] != 2025]

    #연도 리스트
    threeport_year = individual_port["Year"].unique()
    #항구 리스트
    threeport_name = individual_port["Harbor Name"].unique()

    #년도별 항구마다의 입항 개수를 그래프 요소들을 리스트로 담음
    dataList_count = list()

    # 각 항구별로 배 입항 건수 데이터리스트에 담음
    for v in threeport_name:
        port_weight = individual_port[individual_port["Harbor Name"]==v].sort_values("Year")
        dataList_count.append(
            go.Bar(
                x = port_weight["Year"],
                y = port_weight["Ship Count"],
                name = v,
                text=individual_port["Ship Count"],
                textposition="inside", #inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig_1 = go.Figure(data= dataList_count)

    fig_1.update_layout(
        barmode="group", #항구별 막대를 표시화기위해 그룹화
        title=dict(
            text="<b>Number of ships</b> entering Busan's three major ports by year",
            x=0.3,
            y=0.9,
            font={
                "size":20,
                "color":"white"
            }),
        xaxis=dict(
            title="Year",  # x축 제목
            dtick=1        # x축 눈금 간격 1년 단위
        ),
        yaxis_title="Number of ship",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_1, key="en_3busan_shipcount")

    # 25년도는 절사
    individual_port = individual_port[individual_port["Year"] != 2025]

    #연도 리스트
    threeport_year = individual_port["Year"].unique()
    #항구 리스트
    threeport_name = individual_port["Harbor Name"].unique()

    #년도별 항구마다의 입항 개수를 그래프 요소들을 리스트로 담음
    dataList_count = list()

    # 각 항구별로 배 입항 건수 데이터리스트에 담음
    for v in threeport_name:
        port_weight = individual_port[individual_port["Harbor Name"]==v].sort_values("Year")
        dataList_count.append(
            go.Bar(
                x = port_weight["Year"],
                y = port_weight["GT(Gross Tonnage)"],
                name = v,
                text=individual_port["GT(Gross Tonnage)"],
                textposition="inside", #inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig_2 = go.Figure(data= dataList_count)

    fig_2.update_layout(
        barmode="group", #항구별 막대를 표시화기위해 그룹화
        title=dict(
            text="<b>Annual cargo volume</b> of Busan's three major ports",
            x=0.3,
            y=0.9,
            font={
                "size":20,
                "color":"white"
            }),
        xaxis=dict(
            title="Year",  # x축 제목
            dtick=1        # x축 눈금 간격 1년 단위
        ),
        yaxis_title="GT(Gross Tonnage)",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_2, key="en_3busan_weight")

    st.markdown('''
    According to the visual analysis, <span style='color:orange; font-weight:bold; font-size:20px;'>Gamcheon Port</span> recorded the highest number of annual ship arrivals,
    while <span style='color:orange; font-weight:bold; font-size:20px;'>New Port</span> ranked first in terms of cargo volume.
    Following this, we conducted a visual analysis to explore the correlation and trends between ship arrivals and cargo volume for the overall Busan Port, which combines all three ports.
    ''', unsafe_allow_html=True)


    totalBusan_visual = totalBusanWeight[["Year", "Ship Count", "GT(Gross Tonnage)"]].copy()
    totalBusan_visual = totalBusan_visual.iloc[:-1,:]

    fig_3 = go.Figure()

    # 막대그래프: Ship Count
    fig_3.add_trace(
        go.Bar(
            x=totalBusan_visual["Year"],
            y=totalBusan_visual["Ship Count"],
            name="Ships",
            textposition="auto",
            marker=dict(color="blue")
        )
    )
    # 선그래프: GT(Gross Tonnage)
    fig_3.add_trace(
        go.Scatter(
            x=totalBusan_visual["Year"],
            y=totalBusan_visual["GT(Gross Tonnage)"],
            name="GT (Gross Tonnage)",
            mode="lines+markers",
            marker=dict(color="red"),
            yaxis="y2"  # 보조 y축 사용
        )
    )
    # 전체 레이아웃 설정
    fig_3.update_layout(
        title={
            "text": "<b>Annual ships and cargo volume</b> entering Busan Port",
            "x": 0.45,
            "y": 0.9,
            "font": {"size": 20, "color": "white"},
            "xanchor": "center",
            "yanchor": "top"
        },
        xaxis={
            "title": "Years",
            "showticklabels": True,
            "dtick": 1
        },
        yaxis={
            "title": "Ship Count"
        },
        yaxis2={
            "title": "GT",
            "overlaying": "y",
            "side": "right"
        },
        showlegend=True,
        autosize=False,
        width=900,
        height=450,
            legend=dict(
            x=4,
            y=6,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0)",
            bordercolor="gray",
            borderwidth=1
        )
    )

    st.plotly_chart(fig_3, key="busan_Alldata_en")



    # "," 제거 후 숫자형으로 변환
    totalBusan_visual["Ship Count"] = totalBusan_visual["Ship Count"].astype(str).str.replace(",", "")
    totalBusan_visual["GT(Gross Tonnage)"] = totalBusan_visual["GT(Gross Tonnage)"].astype(str).str.replace(",", "")

    # 숫자형으로 안전하게 변환 (NaN 처리 포함)
    totalBusan_visual["Ship Count"] = pd.to_numeric(totalBusan_visual["Ship Count"], errors="coerce")
    totalBusan_visual["GT(Gross Tonnage)"] = pd.to_numeric(totalBusan_visual["GT(Gross Tonnage)"], errors="coerce")

    # NaN 값 제거
    totalBusan_visual = totalBusan_visual.dropna(subset=["Ship Count", "GT(Gross Tonnage)"])

    #년도별 부산 입항 배 개수 : 추세선
    df_busanShip = px.scatter(
        totalBusan_visual,
        x=totalBusan_visual["Year"],
        y=totalBusan_visual["Ship Count"],
        trendline="ols",
        title="<b>Identifying the Annual Number of Ships Entering</b> Busan Port",
        labels={
            "Year": "Year",
            "Ship Count": "Number of Ships"
        },
        template="plotly_white",  # 배경 흰색 테마
        width=900,
        height=500,
    )

    # 추세선 색상 설정
    df_busanShip.update_traces(
        line=dict(color="red", dash="solid"), #solid, dot, dash, longdash
        selector=dict(mode="lines")  # 추세선만 선택
    )

    # Layout 꾸미기
    df_busanShip.update_layout(
        title=dict(
            x=0.3,
            y=0.95,
            font=dict(size=22, color="white")
        ),
        xaxis=dict(
            dtick=1,              # 1년 단위 눈금
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0)",
        bordercolor="lightgray",
        borderwidth=1
    )
    )

    st.plotly_chart(df_busanShip, key="trend_shipCount_en")


    #년도별 부산 입항 배 개수 : 추세선
    df_busanWeight = px.scatter(
        totalBusan_visual,
        x=totalBusan_visual["Year"],
        y=totalBusan_visual["GT(Gross Tonnage)"],
        trendline="ols",
        title="<b>Analyzing the Annual Cargo Volume Trend Entering</b> Busan Port",
        labels={
            "Year": "Year",
            "GT": "GT(Gross Tonnage)"
        },
        template="plotly_white",  # 배경 흰색 테마
        width=900,
        height=500,
    )

    # 추세선 색상 설정 (선택)
    df_busanWeight.update_traces(
        line=dict(color="red", dash="solid"), #solid, dot, dash, longdash
        selector=dict(mode="lines")  # 추세선만 선택
    )

    # Layout 꾸미기
    df_busanWeight.update_layout(
        title=dict(
            x=0.3,
            y=0.95,
            font=dict(size=22, color="white")
        ),
        xaxis=dict(
            dtick=1,              # 1년 단위 눈금
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0)",
            bordercolor="lightgray",
            borderwidth=1
        )
    )

    st.plotly_chart(df_busanWeight, key="trend_shipWeight_en")

    st.markdown('''
    Based on the analysis of the three ports in Busan, <span style='color:white; font-weight:bold; font-size:20px;'>the number of arriving vessels has shown a decreasing trend, while the volume of cargo handled has been increasing</span>. This can be interpreted as a result of <span style='color:orange; font-weight:bold; font-size:20px;'>shipping companies replacing their vessels with larger cargo ships to improve transport efficiency</span>, which is a typical characteristic of maritime logistics.
    ''', unsafe_allow_html=True)

with tab_2:
    st.subheader("부산 항구", anchor=False)
    st.markdown('''
                년도별 대한민국 항구에 대한 입항되는 외국선사의 수, 물동량에서 제일 높은 항구는 부산항이었습니다. 사실 부산은 3개로  <span style='color:orange; font-weight:bold; font-size:20px;'>신항, 북항, 감천항</span>이 주요 항구이며 대게, 이를 부산항이라고 부릅니다. 따라서 우리는 부산 3개 항구에 대한 입항 건수와 물동량에 대하여 데이터 수집 후 시각화 분석을 진행했습니다.
                ''', unsafe_allow_html=True)

    # Define map tile options
    tile_option = "CartoDB positron"

    # Define Busan center coordinates
    busan_center = [35.18397316013664, 129.07057865661844]

    # Define color settings
    circle_fill_color = "#ff7f0e"
    circle_border_color = "#1f77b4"
    geo_fill_color = "#05d06b"

    # Create base map
    targetArea = folium.Map(
        location=busan_center,
        zoom_start=11,
        tiles=tile_option
    )

    # Load GeoJSON (Busan boundary)
    busanGeo = "./useData/koreaBusan.geojson"
    with open(busanGeo, encoding="utf-8-sig") as f:
        myGeo = json.load(f)

    # Style for Busan region
    def myGeo_style(x):
        return {
            "fillColor": geo_fill_color,
            "color": "grey",
            "weight": 0.5,
            "fillOpacity": 0.2
        }

    # Add Busan boundary to map
    folium.GeoJson(
        data=myGeo,
        name="Busan Metropolitan City, Republic of Korea",
        style_function=myGeo_style
    ).add_to(targetArea)

    # Load port data
    portPosition = pd.read_csv("./useData/busanThreeport_position.csv")

    # Iterate through port data
    for i, v in portPosition.iterrows():
        lat = v["Latitude"]
        lon = v["Longitude"]

        # Popup content
        portNames = f"- Port Name : {v[0]}<br>- Port Address : {v[1]}"
        popup = folium.Popup(
            portNames,
            max_width=300,
            min_width=30,
            max_height=300
        )

        # Custom port icon
        myIcon = "./useData/myImage/shipping.png"
        myIcon_edit = CustomIcon(
            icon_image=myIcon,
            icon_size=(47, 47),
            icon_anchor=(23, 23)
        )

        # Add marker
        folium.Marker(
            location=[lat, lon],
            icon=myIcon_edit
        ).add_child(popup).add_to(targetArea)

        # Add circular highlight around port
        folium.CircleMarker(
            location=[lat, lon],
            radius=60,
            fill=True,
            color=circle_border_color,
            fill_color=circle_fill_color
        ).add_to(targetArea)

    # Display the map once after all markers are added
    st_folium(targetArea, width=1500, height=600, key="kr_pdCompany_possition")


    myfolders = os.listdir("./useData/busanport/")

    readFile_list = list()

    for v in range(len(myfolders)):
        if "부산항(전체)" not in myfolders[v]:
            open_data = pd.read_csv(f"./useData/busanport/{myfolders[v]}")
            readFile_list.append(open_data)
        else:
            totalBusanWeight = pd.read_csv(f"./useData/busanport/{myfolders[v]}")

    individual_port = pd.concat(readFile_list, axis=0, ignore_index=False)

    # 타입변경
    # individual_port[["Ship Count", "GT(Gross Tonnage)"]].astype("int64") > ","로 인해 변환 불가

    # , 제거 함수 정의
    def notComma(x):
        return x.replace(",", "")

    individual_port["Year"] = individual_port["Year"].astype("object")
    individual_port["Ship Count"] = individual_port["Ship Count"].apply(notComma).astype("int64")
    individual_port["GT(Gross Tonnage)"] = individual_port["GT(Gross Tonnage)"].apply(notComma).astype("int64")

    individual_port.to_csv("./useData/finishPrepro/busanAllPorts_GTCount.csv", encoding="utf-8-sig")

    # 25년도는 절사
    individual_port = individual_port[individual_port["Year"] != 2025]

    #연도 리스트
    threeport_year = individual_port["Year"].unique()
    #항구 리스트
    threeport_name = individual_port["Harbor Name"].unique()

    #년도별 항구마다의 입항 개수를 그래프 요소들을 리스트로 담음
    dataList_count = list()

    # 각 항구별로 배 입항 건수 데이터리스트에 담음
    for v in threeport_name:
        port_weight = individual_port[individual_port["Harbor Name"]==v].sort_values("Year")
        dataList_count.append(
            go.Bar(
                x = port_weight["Year"],
                y = port_weight["Ship Count"],
                name = v,
                text=individual_port["Ship Count"],
                textposition="inside", #inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig_1 = go.Figure(data= dataList_count)

    fig_1.update_layout(
        barmode="group", #항구별 막대를 표시화기위해 그룹화
        title=dict(
            text="<b>Number of ships</b> entering Busan's three major ports by year",
            x=0.3,
            y=0.9,
            font={
                "size":20,
                "color":"white"
            }),
        xaxis=dict(
            title="Year",  # x축 제목
            dtick=1        # x축 눈금 간격 1년 단위
        ),
        yaxis_title="Number of ship",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_1, key="kr_3busan_shipcount")

    # 25년도는 절사
    individual_port = individual_port[individual_port["Year"] != 2025]

    #연도 리스트
    threeport_year = individual_port["Year"].unique()
    #항구 리스트
    threeport_name = individual_port["Harbor Name"].unique()

    #년도별 항구마다의 입항 개수를 그래프 요소들을 리스트로 담음
    dataList_count = list()

    # 각 항구별로 배 입항 건수 데이터리스트에 담음
    for v in threeport_name:
        port_weight = individual_port[individual_port["Harbor Name"]==v].sort_values("Year")
        dataList_count.append(
            go.Bar(
                x = port_weight["Year"],
                y = port_weight["GT(Gross Tonnage)"],
                name = v,
                text=individual_port["GT(Gross Tonnage)"],
                textposition="inside", #inside, outside, asuto, name
                texttemplate="%{text:,}"
            )
        )

    fig_2 = go.Figure(data= dataList_count)

    fig_2.update_layout(
        barmode="group", #항구별 막대를 표시화기위해 그룹화
        title=dict(
            text="<b>Annual cargo volume</b> of Busan's three major ports",
            x=0.3,
            y=0.9,
            font={
                "size":20,
                "color":"white"
            }),
        xaxis=dict(
            title="Year",  # x축 제목
            dtick=1        # x축 눈금 간격 1년 단위
        ),
        yaxis_title="GT(Gross Tonnage)",
        legend=dict(
            bordercolor="grey",
            borderwidth=0.5
        )
    )
    st.plotly_chart(fig_2, key="kr_3busan_weight")

    st.markdown('''
                시각화 분석결과 년간 입항 배의 수가 많은 항구는 <span style='color:orange; font-weight:bold; font-size:20px;'>감천항</span>, 물동량이 많은 항구는 <span style='color:orange; font-weight:bold; font-size:20px;'>신항</span>이 1위를 차지했습니다. 우리는 이어서 3개 항구를 합친 부산항 전체에 대한 입항되는 배의 수와 물동량의 상관관계 및 추세를 파악할 수 있는 시각화 분석작업을 진행 했습니다.
                ''', unsafe_allow_html=True)

    totalBusan_visual = totalBusanWeight[["Year", "Ship Count", "GT(Gross Tonnage)"]].copy()
    totalBusan_visual = totalBusan_visual.iloc[:-1,:]

    fig_3 = go.Figure()

    # 막대그래프: Ship Count
    fig_3.add_trace(
        go.Bar(
            x=totalBusan_visual["Year"],
            y=totalBusan_visual["Ship Count"],
            name="Ships",
            textposition="auto",
            marker=dict(color="blue")
        )
    )
    # 선그래프: GT(Gross Tonnage)
    fig_3.add_trace(
        go.Scatter(
            x=totalBusan_visual["Year"],
            y=totalBusan_visual["GT(Gross Tonnage)"],
            name="GT (Gross Tonnage)",
            mode="lines+markers",
            marker=dict(color="red"),
            yaxis="y2"  # 보조 y축 사용
        )
    )
    # 전체 레이아웃 설정
    fig_3.update_layout(
        title={
            "text": "<b>Annual ships and cargo volume</b> entering Busan Port",
            "x": 0.45,
            "y": 0.9,
            "font": {"size": 20, "color": "white"},
            "xanchor": "center",
            "yanchor": "top"
        },
        xaxis={
            "title": "Years",
            "showticklabels": True,
            "dtick": 1
        },
        yaxis={
            "title": "Ship Count"
        },
        yaxis2={
            "title": "GT",
            "overlaying": "y",
            "side": "right"
        },
        showlegend=True,
        autosize=False,
        width=900,
        height=450,
            legend=dict(
            x=4,
            y=6,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0)",
            bordercolor="gray",
            borderwidth=1
        )
    )

    st.plotly_chart(fig_3, key="busan_Alldata_kr")



    # "," 제거 후 숫자형으로 변환
    totalBusan_visual["Ship Count"] = totalBusan_visual["Ship Count"].astype(str).str.replace(",", "")
    totalBusan_visual["GT(Gross Tonnage)"] = totalBusan_visual["GT(Gross Tonnage)"].astype(str).str.replace(",", "")

    # 숫자형으로 안전하게 변환 (NaN 처리 포함)
    totalBusan_visual["Ship Count"] = pd.to_numeric(totalBusan_visual["Ship Count"], errors="coerce")
    totalBusan_visual["GT(Gross Tonnage)"] = pd.to_numeric(totalBusan_visual["GT(Gross Tonnage)"], errors="coerce")

    # NaN 값 제거
    totalBusan_visual = totalBusan_visual.dropna(subset=["Ship Count", "GT(Gross Tonnage)"])

    #년도별 부산 입항 배 개수 : 추세선
    df_busanShip = px.scatter(
        totalBusan_visual,
        x=totalBusan_visual["Year"],
        y=totalBusan_visual["Ship Count"],
        trendline="ols",
        title="<b>Identifying the Annual Number of Ships Entering</b> Busan Port",
        labels={
            "Year": "Year",
            "Ship Count": "Number of Ships"
        },
        template="plotly_white",  # 배경 흰색 테마
        width=900,
        height=500,
    )

    # 추세선 색상 설정
    df_busanShip.update_traces(
        line=dict(color="red", dash="solid"), #solid, dot, dash, longdash
        selector=dict(mode="lines")  # 추세선만 선택
    )

    # Layout 꾸미기
    df_busanShip.update_layout(
        title=dict(
            x=0.3,
            y=0.95,
            font=dict(size=22, color="white")
        ),
        xaxis=dict(
            dtick=1,              # 1년 단위 눈금
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0)",
        bordercolor="lightgray",
        borderwidth=1
    )
    )

    st.plotly_chart(df_busanShip, key="trend_shipCount_kr")


    #년도별 부산 입항 배 개수 : 추세선
    df_busanWeight = px.scatter(
        totalBusan_visual,
        x=totalBusan_visual["Year"],
        y=totalBusan_visual["GT(Gross Tonnage)"],
        trendline="ols",
        title="<b>Analyzing the Annual Cargo Volume Trend Entering</b> Busan Port",
        labels={
            "Year": "Year",
            "GT": "GT(Gross Tonnage)"
        },
        template="plotly_white",  # 배경 흰색 테마
        width=900,
        height=500,
    )

    # 추세선 색상 설정 (선택)
    df_busanWeight.update_traces(
        line=dict(color="red", dash="solid"), #solid, dot, dash, longdash
        selector=dict(mode="lines")  # 추세선만 선택
    )

    # Layout 꾸미기
    df_busanWeight.update_layout(
        title=dict(
            x=0.3,
            y=0.95,
            font=dict(size=22, color="white")
        ),
        xaxis=dict(
            dtick=1,              # 1년 단위 눈금
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0)",
            bordercolor="lightgray",
            borderwidth=1
        )
    )
    st.plotly_chart(df_busanWeight, key="trend_shipWeight_kr")

    st.markdown('''
    부산의 3개 항구를 기준으로 분석한 결과, <span style='color:white; font-weight:bold; font-size:20px;'>입항하는 선박 수는 감소 추세인 반면, 입항 물동량은 오히려 증가하는 추세</span>를 보였습니다. 이는 <span style='color:orange; font-weight:bold; font-size:20px;'>해운 기반 유통의 특성상, 선사들이 운송 효율성을 높이기 위해 더 큰 규모의 카고선으로 교체 운영</span>했기 때문으로 해석할 수 있습니다.
    ''', unsafe_allow_html=True)
