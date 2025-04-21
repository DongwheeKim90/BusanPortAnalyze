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
                년도별 대한민국 항구에 대한 입항되는 외국선사의 수, 물동량에서 제일 높은 항구는 부산항이었습니다. 사실 부산은 3개로  <span style='color:orange; font-weight:bold; font-size:20px;'>신항, 북항, 감천항</span>이 주요 항구이며 대게, 이를 부산항이라고 부릅니다. 따라서 우리는 부산 3개 항구에 대한 입항 건수와 GT:Gross Tonge(선박부피+물동량인 선박 총 부피) 대하여 데이터 수집 후 시각화 분석을 진행했습니다.
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
            text="<b>Annual GT(Gross Tonge) volume</b> of Busan's three major ports",
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
                시각화 분석결과 년간 입항 배의 수가 많은 항구는 <span style='color:orange; font-weight:bold; font-size:20px;'>감천항</span>, 물동량이 많은 항구는 <span style='color:orange; font-weight:bold; font-size:20px;'>신항</span>이 1위를 차지했습니다. 우리는 이어서 3개 항구를 합친 부산항 전체에 대한 입항되는 배의 수와 GT:Gross Tonge(선박부피+물동량으로 선박 총 부피)  상관관계 및 추세를 파악할 수 있는 시각화 분석작업을 진행 했습니다.
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
        title="<b>Analyzing the Annual GT(Gross Tonge) Volume Trend Entering</b> Busan Port",
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
    부산의 3개 항구를 기준으로 분석한 결과, <span style='color:white; font-weight:bold; font-size:20px;'>입항하는 선박 수는 감소 추세인 반면, 입항 GT:Gross Tonge(선박부피+물동량으로 선박 총 부피)는 오히려 증가하는 추세</span>를 보였습니다. 이는 <span style='color:orange; font-weight:bold; font-size:20px;'>해운 기반 유통의 특성상, 선사들이 운송 효율성을 높이기 위해 더 큰 규모의 카고선으로 교체 운영</span>했기 때문으로 해석할 수 있습니다.
    ''', unsafe_allow_html=True)

with tab_3:
    st.markdown('''
    (1) Data Source : https://www.chainportal.co.kr/nexacro/index.html?screenid=screen_main <br>
    (2) Collected Data : Data collection of annual vessel calls and cargo throughput for the entire Port of Busan and its three major sub-ports(부산항 전체 및 3대 부산항구의 연간 입항 배 건수와 물동량 데이터 수집)<br>
    (3) Data Type : Structured Data(정형 데이터)<br>
    (4) Technologies Used : Selenium, BeautifulSoup(bs4), Pandas, Plotly Express & Plotly Graph Objects<br>
    (5) Data Collection and Preprocessing Process
    ''',unsafe_allow_html=True)
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Collection (데이터 수집)</span>", unsafe_allow_html=True)
    st.video("./useData/busanports.mp4")
    st.code('''
    # ------------------------------------------------------------------------------
    # Author: DongWhee Kim
    # Date: 2025-04-10
    # Description: Collect annual vessel calls and cargo throughput data from
    #              ChainPortal for Busan Port (전체, 신항, 북항, 감천항) using Selenium.
    # ------------------------------------------------------------------------------

    # Selenium for web automation
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Standard modules
    import time  # for sleep/delay
    import re    # for dynamic ID extraction

    # Data handling
    import pandas as pd

    # ------------------------------------------------------------------------------
    # Step 1: Chrome WebDriver 설정
    # ------------------------------------------------------------------------------
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("no-sandbox")  # Sandbox 모드 비활성화

    chrome_service = Service("../autoDriver/chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    action = ActionChains(driver)
    driver.maximize_window()

    # 명시적 대기 설정 (3초)
    wait = WebDriverWait(driver, 3)

    # ------------------------------------------------------------------------------
    # Step 2: BeautifulSoup을 위한 find 함수 정의
    # ------------------------------------------------------------------------------
    def bs4_find(value):
        return mysoup.select_one(value)

    def bs4_finds(value):
        return mysoup.select(value)

    def selenium_find(css_selector):
        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    def selenium_finds(css_selector):
        return wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    # ------------------------------------------------------------------------------
    # Step 3: 사이트 접속 및 로그인 처리
    # ------------------------------------------------------------------------------
    target_url = "https://www.chainportal.co.kr/portstat/nexacro/index.html?screenid=screen_stat"
    driver.get(target_url)
    time.sleep(50)
    print(f"사이트 접속 완료 : {target_url}")

    input_fields = selenium_finds("input.nexainput")
    for field in input_fields:
        field_value = field.get_attribute("value")
        if field_value == "":
            field.click()
            field.send_keys("romangrism")
        elif field_value == "패스워드를 입력해 주세요":
            field.click()
            field.send_keys("xhdtls723186!@\n")
    print("아이디 비밀번호 기입 완료")
    print("로그인 성공")
    time.sleep(10)

    # 메뉴 클릭
    selenium_find("div#mainframe\\.frameIndex\\.form\\.divFrameLeft\\.form\\.divLeft\\.form\\.grdTree\\.body\\.gridrow_0\\.cell_0_1\\:text").click()
    print("선박메뉴 클릭 완료")
    selenium_find("div#mainframe\\.frameIndex\\.form\\.divFrameLeft\\.form\\.divLeft\\.form\\.grdTree\\.body\\.gridrow_1\\.cell_1_1\\:text").click()
    print("연도별 입출항 통계 클릭 완료")
    time.sleep(5)

    # ------------------------------------------------------------------------------
    # Step 4: 검색 초기화 및 입력
    # ------------------------------------------------------------------------------
    year_input_selector = "input[aria-labelledby$='edtYYYYFrom']"
    selenium_find(year_input_selector).click()
    time.sleep(1)
    selenium_find(year_input_selector).clear()
    time.sleep(1)
    selenium_find(year_input_selector).send_keys("2013")
    time.sleep(1)
    print("시작년도 초기화 및 값 입력 완료")

    # 입항 클릭
    selenium_find("img[alt=' 입항']").click()

    # ------------------------------------------------------------------------------
    # Step 5: 항구 및 연도 정의
    # ------------------------------------------------------------------------------
    harbor_list = ["부산항(전체)", "신항", "북항", "감천항"]
    year_range = list(range(2013, 2026))

    # ------------------------------------------------------------------------------
    # Step 6: 항구별 반복 수집
    # ------------------------------------------------------------------------------
    for harbor_name in harbor_list:
        # 동적 ID 추출
        page_html = driver.page_source
        match = re.search(r"win80050100_0_\d+", page_html)
        win_id = match.group()
        print(f"현재 추출된 win_id: {win_id}")

        # 드롭다운에서 항구 선택
        harbor_dropdown = driver.find_element(
            By.XPATH,
            f"//*[@id='mainframe.frameIndex.form.divMain.form.{win_id}.form.divWork.form.Div00.form.cboPrtAtCode.comboedit:input']"
        )
        harbor_dropdown.click()
        time.sleep(2)

        selected_option = driver.find_element(By.XPATH, f"//div[text()='{harbor_name}']")
        selected_option.click()
        print(f"{harbor_name} 선택 완료")
        time.sleep(3)

        # 검색 버튼 클릭
        search_button = driver.find_element(
            By.XPATH,
            f"//*[@id='mainframe.frameIndex.form.divMain.form.{win_id}.form.divWork.form.Div00.form.Button05_00:icontext']/div"
        )
        search_button.click()
        print("검색버튼 클릭")
        time.sleep(5)

        # 다시 win_id 추출
        page_html = driver.page_source
        match = re.search(r"win80050100_0_\d+", page_html)
        win_id = match.group()
        print(f"검색 후 추출된 win_id: {win_id}")

        # 데이터 수집 리스트 초기화
        collected_years = []
        ship_counts = []
        gross_tonnages = []

        # 연도별 데이터 수집
        for idx, year in enumerate(year_range):
            year_text = driver.find_element(
                By.XPATH,
                f"//*[@id='mainframe.frameIndex.form.divMain.form.{win_id}.form.divWork.form.grdMain.body.gridrow_{idx}.cell_{idx}_0:text']"
            ).text
            collected_years.append(year_text)

            count_text = driver.find_element(
                By.XPATH,
                f"//*[@id='mainframe.frameIndex.form.divMain.form.{win_id}.form.divWork.form.grdMain.body.gridrow_{idx}.cell_{idx}_5:text']"
            ).text
            ship_counts.append(count_text)

            gt_text = driver.find_element(
                By.XPATH,
                f"//*[@id='mainframe.frameIndex.form.divMain.form.{win_id}.form.divWork.form.grdMain.body.gridrow_{idx}.cell_{idx}_6:text']"
            ).text
            gross_tonnages.append(gt_text)

            time.sleep(1)

        # DataFrame 저장
        harbor_df = pd.DataFrame({
            "Harbor Name": [harbor_name] * len(year_range),
            "Year": collected_years,
            "Ship Count": ship_counts,
            "GT(Gross Tonnage)": gross_tonnages
        })

        # CSV 저장
        output_path = f"../useData/busan_{harbor_name}_rawData.csv"
        harbor_df.to_csv(output_path, encoding="utf-8-sig", index=False)
        print(f"{harbor_name} 데이터 저장 완료: {output_path}")

            ''')
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Preprocessing (데이터 가공)</span>", unsafe_allow_html=True)
    st.code('''
    # ------------------------------------------------------------------------------
    # Author: DongWhee Kim
    # Date: 2025-04-10
    # Description: Data preprocessing and visualization for annual ship traffic and
    #              cargo throughput at Busan Port and its three major sub-ports
    # ------------------------------------------------------------------------------

    import pandas as pd                        # For data handling and analysis (데이터 처리 및 분석)
    import plotly.graph_objects as go          # For bar and combined visualizations (막대 및 혼합 시각화)
    import plotly.express as px                # For scatter plots and trend lines (산점도 및 추세선)
    import scipy.stats as stats                # For correlation and p-value (상관계수 및 p-value 분석)
    import folium                              # For map visualization (지도 시각화)
    from folium.features import CustomIcon     # For custom icons on folium map (지도 아이콘 커스터마이징)
    from sklearn.preprocessing import MinMaxScaler  # For data normalization (데이터 정규화)
    import os                                  # For file and folder handling (파일 및 폴더 제어)
    import json                                # For reading GeoJSON files (GeoJSON 파일 읽기)

    # ------------------------------------------------------------------------------
    # Load all CSV files from folder except total Busan port (전체)
    # ("부산항(전체)" 제외하고 개별 항만 파일 읽기)
    # ------------------------------------------------------------------------------
    port_folder = "../useData/busanport/"
    file_list = os.listdir(port_folder)

    read_files = []

    for file_name in file_list:
        if "부산항(전체)" not in file_name:
            df = pd.read_csv(os.path.join(port_folder, file_name))
            read_files.append(df)
        else:
            total_busan_df = pd.read_csv(os.path.join(port_folder, file_name))

    # ------------------------------------------------------------------------------
    # Concatenate individual port data (개별 항만 데이터 통합)
    # ------------------------------------------------------------------------------
    individual_port = pd.concat(read_files, axis=0, ignore_index=False)

    # ------------------------------------------------------------------------------
    # Clean and convert text numbers (콤마 제거 및 숫자형으로 변환)
    # ------------------------------------------------------------------------------
    def remove_comma(x):
        return x.replace(",", "")

    individual_port["Year"] = individual_port["Year"].astype("object")
    individual_port["Ship Count"] = individual_port["Ship Count"].apply(remove_comma).astype("int64")
    individual_port["GT(Gross Tonnage)"] = individual_port["GT(Gross Tonnage)"].apply(remove_comma).astype("int64")

    # ------------------------------------------------------------------------------
    # Save cleaned dataset (전처리된 데이터 저장)
    # ------------------------------------------------------------------------------
    individual_port.to_csv("../useData/finishPrepro/busanAllPorts_GTCount.csv", encoding="utf-8-sig", index=False)

    # ------------------------------------------------------------------------------
    # Remove 2025 (incomplete year) from analysis (2025년 데이터 제외)
    # ------------------------------------------------------------------------------
    individual_port = individual_port[individual_port["Year"] != 2025]

    # ------------------------------------------------------------------------------
    # Bar chart - Ship Count by Port and Year (항구별 연도별 입항 선박수 시각화)
    # ------------------------------------------------------------------------------
    port_names = individual_port["Harbor Name"].unique()
    data_ship_counts = []

    for port in port_names:
        port_data = individual_port[individual_port["Harbor Name"] == port].sort_values("Year")
        data_ship_counts.append(
            go.Bar(
                x=port_data["Year"],
                y=port_data["Ship Count"],
                name=port,
                text=port_data["Ship Count"],
                textposition="inside",
                texttemplate="%{text:,}"
            )
        )

    fig = go.Figure(data=data_ship_counts)
    fig.update_layout(
        barmode="group",
        title=dict(text="<b>Number of ships</b> entering Busan's three major ports by year", x=0.5),
        xaxis=dict(title="Year", dtick=1),
        yaxis_title="Number of ships",
        legend=dict(bordercolor="grey", borderwidth=0.5)
    )
    fig.show()

    # ------------------------------------------------------------------------------
    # Bar chart - Cargo Volume (GT) by Port and Year (항구별 연도별 물동량 시각화)
    # ------------------------------------------------------------------------------
    data_cargo_volumes = []

    for port in port_names:
        port_data = individual_port[individual_port["Harbor Name"] == port].sort_values("Year")
        data_cargo_volumes.append(
            go.Bar(
                x=port_data["Year"],
                y=port_data["GT(Gross Tonnage)"],
                name=port,
                text=port_data["GT(Gross Tonnage)"],
                textposition="inside",
                texttemplate="%{text:,}"
            )
        )

    fig = go.Figure(data=data_cargo_volumes)
    fig.update_layout(
        barmode="group",
        title=dict(text="<b>Annual cargo volume</b> of Busan's three major ports", x=0.5),
        xaxis=dict(title="Year", dtick=1),
        yaxis_title="GT(Gross Tonnage)",
        legend=dict(bordercolor="grey", borderwidth=0.5)
    )
    fig.show()

    # ------------------------------------------------------------------------------
    # Process total Busan port data (부산항 전체 데이터 전처리)
    # ------------------------------------------------------------------------------
    total_busan_df[["Ship Count", "GT(Gross Tonnage)"]] = total_busan_df[["Ship Count", "GT(Gross Tonnage)"]].applymap(remove_comma).astype("int64")
    total_busan_df["Year"] = total_busan_df["Year"].astype("object")

    total_busan_df = total_busan_df.iloc[:-1, :]  # Drop last row if necessary (마지막 행 제거)
    total_visual_df = total_busan_df[["Year", "Ship Count", "GT(Gross Tonnage)"]].copy()

    # ------------------------------------------------------------------------------
    # Visualization: Combined chart (bar for ships, line for GT) (입항 건수 + 물동량 이중 축 시각화)
    # ------------------------------------------------------------------------------
    fig = go.Figure()

    # Bar: Ship Count
    fig.add_trace(
        go.Bar(
            x=total_visual_df["Year"],
            y=total_visual_df["Ship Count"],
            name="Ships",
            textposition="auto",
            marker=dict(color="blue")
        )
    )

    # Line: Cargo Volume
    fig.add_trace(
        go.Scatter(
            x=total_visual_df["Year"],
            y=total_visual_df["GT(Gross Tonnage)"],
            name="GT (Gross Tonnage)",
            mode="lines+markers",
            marker=dict(color="red"),
            yaxis="y2"
        )
    )

    fig.update_layout(
        title={
            "text": "<b>Annual ships and cargo volume</b> entering Busan Port",
            "x": 0.45,
            "font": {"size": 20, "color": "black"}
        },
        xaxis={"title": "Years", "dtick": 1},
        yaxis={"title": "Ship Count"},
        yaxis2={"title": "GT", "overlaying": "y", "side": "right"},
        showlegend=True,
        autosize=False,
        width=900,
        height=450,
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0)",
            bordercolor="gray",
            borderwidth=1
        )
    )
    fig.show()

    # ------------------------------------------------------------------------------
    # Correlation analysis (상관계수 및 P-value 분석)
    # ------------------------------------------------------------------------------
    corr_value, p_value = stats.pearsonr(total_visual_df['Ship Count'], total_visual_df['GT(Gross Tonnage)'])
    print(f"상관계수 : {round(corr_value, 3)}")
    print(f"P-value : {round(p_value, 5)}")

    # ------------------------------------------------------------------------------
    # Folium Map Visualization - Ports in Busan (Folium을 활용한 항만 지도 시각화)
    # ------------------------------------------------------------------------------
    busan_geo_path = "../useData/koreaBusan.geojson"
    with open(busan_geo_path, encoding="utf-8-sig") as f:
        busan_geo = json.load(f)

    def geo_style(feature):
        return {
            "fillColor": "#05d06b",
            "color": "grey",
            "weight": 0.5,
            "fillOpacity": 0.2
        }

    # Create base map (기본 지도 생성)
    busan_map = folium.Map(
        location=[35.18397316013664, 129.07057865661844],
        zoom_start=11,
        tiles="CartoDB positron"
    )

    # Add GeoJSON overlay (부산시 영역 표시)
    folium.GeoJson(
        data=busan_geo,
        name="Busan Metropolitan City",
        style_function=geo_style
    ).add_to(busan_map)

    # Load port location CSV (항만 위치 파일 로드)
    port_pos_df = pd.read_csv("../useData/busanThreeport_position.csv")

    # Add markers to map (지도에 항만 마커 추가)
    for _, row in port_pos_df.iterrows():
        lat, lon = row["Latitude"], row["Longitude"]
        port_html = f"- Port Name : {row[0]}<br>- Port Address : {row[1]}"
        popup = folium.Popup(port_html, max_width=300, show=True)

        # Custom icon
        icon_path = "../useData/myImage/shipping.png"
        custom_icon = CustomIcon(icon_image=icon_path, icon_size=(35, 35), icon_anchor=(10, 10))

        # Add marker and circle
        folium.Marker(location=[lat, lon], icon=custom_icon).add_child(popup).add_to(busan_map)
        folium.CircleMarker(
            location=[lat, lon],
            radius=60,
            fill=True,
            color="#1f77b4",
            fill_color="#ff7f0e"
        ).add_to(busan_map)

    # Display map object (지도 객체 반환)
    busan_map
    ''')
