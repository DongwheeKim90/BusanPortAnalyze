import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Number of foreign ships entering and cargo volume by port in Korea.", anchor=False)

tab_1, tab_2, tab_3 = st.tabs(["Analysis Process(EN)", "Analysis Process(KR)", "Data Preprocessing"])

with tab_1:
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>South Korea</span> has an industrial structure centered on processing trade, where it imports raw materials and components, processes and assembles them, and then re-exports high value-added products.
    <span style='color:orange; font-weight:bold; font-size:20px;'>It is the 9th largest importer in the world as of 2023</span>. In particular, <span style='color:orange; font-weight:bold; font-size:20px;'>Busan, Incheon, Gwangyang, and Ulsan</span> are Korea's major ports and serve as logistics hubs for actual imports and exports.
    """, unsafe_allow_html=True)


    #시각화 데이터
    koreaPorts = pd.read_csv("./useData/raw_koreaAllHarbors.csv")
    koreaPorts = koreaPorts.iloc[:, 1:]
    koreaPorts = koreaPorts[koreaPorts["Harbor name"]!="항만명"]
    # 건수와 중량 0인것 절사
    koreaPorts = koreaPorts[koreaPorts["Ship count"] != "0"]
    koreaPorts = koreaPorts[koreaPorts["Ship count"] != "0"]

    def notComma(x):
        return x.replace(",","")

    koreaPorts_counts = koreaPorts[["Year", "Harbor name", "Ship count"]]
    koreaPorts_counts["Ship count"] = koreaPorts_counts["Ship count"].apply(notComma)
    koreaPorts_counts["Ship count"] = koreaPorts_counts["Ship count"].astype("int32")
    koreaPorts_counts["Year"] = koreaPorts_counts["Year"].astype("str")
    koreaPorts_counts = koreaPorts_counts[koreaPorts_counts["Year"] != "2025"]

    # 항구 이름 고유값 추출
    harbors = koreaPorts_counts["Harbor name"].unique()
    # 연도는 문자열로 정렬
    years = sorted(koreaPorts_counts["Year"].unique())

    # Figure 초기화
    fig = go.Figure()


    # 항구별 입항 외국선 개수 시각화
    for harbor in harbors:
        subset = koreaPorts_counts[koreaPorts_counts["Harbor name"] == harbor]
        subset = subset.groupby("Year")["Ship count"].sum().reindex(years, fill_value=0)  # 누락 연도는 0으로 채움

        fig.add_trace(go.Bar(
            x=years,
            y=subset.values,
            name=harbor
        ))

    # 레이아웃 설정
    fig.update_layout(
        template = "plotly_dark",
        title=dict(
        text="<b>Number of foreign ships entering port by year</b>",
        x=0.35,
        y=0.9,
        font={"size": 20,
                "color":"white"}
        ),
        xaxis_title="Year",
        yaxis_title="Number of foreign ships",
        barmode="group",  # 'stack'으로 바꾸면 누적형
        xaxis=dict(type='category', categoryorder='category ascending'),
        font=dict(family="Malgun Gothic"),  # 한글 깨짐 방지
        legend_title="Kinds of harbor"
    )

    # Streamlit에 시각화 출력
    st.plotly_chart(fig, use_container_width=True, key="en_foreign_ship_count")


    # 필요한 열 선택 후 쉼표 제거 및 int 변환
    koreaPorts_weights = koreaPorts[["Year", "Harbor name", "Weight"]]
    koreaPorts_weights["Weight"] = koreaPorts_weights["Weight"].apply(notComma)
    koreaPorts_weights["Weight"] = koreaPorts_weights["Weight"].astype("int32")
    koreaPorts_weights["Year"] = koreaPorts_weights["Year"].astype("str")
    koreaPorts_weights = koreaPorts_weights[koreaPorts_weights["Year"] != "2025"]

    # 항구 이름 고유값 추출
    harbors = koreaPorts_weights["Harbor name"].unique()

    # 연도는 문자열로 정렬
    years = sorted(koreaPorts_weights["Year"].unique())

    # Figure 초기화
    fig_w = go.Figure()

    # 항구별 입항 외국선 기준 물동량 시각화
    for harbor in harbors:
        subset = koreaPorts_weights[koreaPorts_weights["Harbor name"] == harbor]
        subset = subset.groupby("Year")["Weight"].sum().reindex(years, fill_value=0)  # 누락 연도는 0으로 채움

        fig_w.add_trace(go.Bar(
            x=years,
            y=subset.values,
            name=harbor
        ))

    # 레이아웃 설정
    # 레이아웃 설정 (중량 단위로 수정)
    fig_w.update_layout(
        template="plotly_dark",
        title=dict(
            text="<b>Total cargo weight by year and harbor</b>",
            x=0.35,
            y=0.9,
            font={"size": 20, "color": "white"}
        ),
        xaxis_title="Year",
        yaxis_title="Cargo Weight (tons)",
        barmode="group",
        xaxis=dict(type='category', categoryorder='category ascending'),
        font=dict(family="Malgun Gothic"),
        legend_title="Kinds of harbor"
    )

    # Streamlit에 시각화 출력
    st.plotly_chart(fig_w, use_container_width=True, key="en_cargo_weight_by_port")

    st.markdown("""
    From the visualization above, we can clearly see that <span style='font-weight:bold; font-size:20px;'>Busan, Ulsan, Incheon, and Gwangyang</span> handle the highest number of foreign ship entries and cargo volumes annually.
    <br>Among them, <span style='color:orange; font-weight:bold; font-size:20px;'>Busan ranks first</span> in both ship entries and cargo volume, so we extracted and re-visualized its data separately.
    """, unsafe_allow_html=True)

    # 부산 시각화 년도 월별
    koreaPorts_busan_countWeight = koreaPorts[koreaPorts["Harbor name"]=="부산"]

    # 입항건수 : 필요한 열 선택 후 쉼표 제거 및 int 변환
    koreaPorts_busan_countWeight["Ship count"] = koreaPorts_busan_countWeight["Ship count"].apply(notComma)
    koreaPorts_busan_countWeight["Ship count"] = koreaPorts_busan_countWeight["Ship count"].astype("int32")
    koreaPorts_busan_countWeight["Year"] = koreaPorts_busan_countWeight["Year"].astype("str")
    koreaPorts_busan_countWeight = koreaPorts_busan_countWeight[koreaPorts_busan_countWeight["Year"] != "2025"]

    # 부산 항만 데이터만 필터링
    # Filter data for the port of 'Busan' only
    koreaPorts_busan_countWeight = koreaPorts[koreaPorts["Harbor name"] == "부산"].copy()

    # 1. Remove commas from 'Ship count' column and convert to integer
    #    'Ship count' 열의 쉼표 제거 후 정수형으로 변환합니다.
    koreaPorts_busan_countWeight["Ship count"] = koreaPorts_busan_countWeight["Ship count"].apply(notComma)
    koreaPorts_busan_countWeight["Ship count"] = koreaPorts_busan_countWeight["Ship count"].astype("int32")

    # 2. Remove commas from 'Weight' column and convert to integer
    #    'Weight' 열의 쉼표 제거 후 정수형으로 변환합니다.
    #    예: "30,727,140" → 30727140 (수치 계산 가능하게 변환)
    koreaPorts_busan_countWeight["Weight"] = koreaPorts_busan_countWeight["Weight"].str.replace(",", "").astype(int)

    # 3. Convert 'Year' to string and filter out the year 2025
    koreaPorts_busan_countWeight["Year"] = koreaPorts_busan_countWeight["Year"].astype("str")
    koreaPorts_busan_countWeight = koreaPorts_busan_countWeight[koreaPorts_busan_countWeight["Year"] != "2025"]

    # 4. Create 'Year-Month' column as datetime
    koreaPorts_busan_countWeight["Year-Month"] = pd.to_datetime(
        koreaPorts_busan_countWeight["Year"] + "-" + koreaPorts_busan_countWeight["Month"].astype(str).str.zfill(2)
    )

    # 5. Sort the data by 'Year-Month' for time-series visualization
    koreaPorts_busan_countWeight = koreaPorts_busan_countWeight.sort_values(by="Year-Month")


    # Initialize the figure
    # 그래프 Figure 객체 생성함
    fig_busan = go.Figure()

    # Add Bar Chart (Ship Count - left Y axis)
    # 입항 건수 데이터를 막대그래프로 추가함 (왼쪽 y축 기준)
    fig_busan.add_trace(go.Bar(
        x=koreaPorts_busan_countWeight["Year-Month"],  # Set x-axis to Year-Month datetime values
        # x축을 연-월(datetime) 값으로 설정함
        y=koreaPorts_busan_countWeight["Ship count"],  # Set y-axis to ship count values
        # y축을 선박 입항 건수로 설정함
        name="Ship count",  # Name shown in legend
        # 범례에 표시될 이름 설정함
        yaxis="y1",  # Use left y-axis
        # 왼쪽 y축에 매핑함
        marker_color="#c2baba"  # Set bar color to light green
    ))

    # Add Line Chart (Weight - right Y axis)
    # 화물 중량 데이터를 선 그래프로 추가함 (오른쪽 y축 기준)
    fig_busan.add_trace(go.Scatter(
        x=koreaPorts_busan_countWeight["Year-Month"],  # Set x-axis to Year-Month datetime values
        # x축을 연-월(datetime) 값으로 설정함
        y=koreaPorts_busan_countWeight["Weight"],  # Set y-axis to cargo weight values
        # y축을 화물 중량 값으로 설정함
        name="Weight (tons)",  # Name shown in legend
        # 범례에 표시될 이름 설정함
        yaxis="y2",  # Use right y-axis
        # 오른쪽 y축에 매핑함
        mode="lines",  # Show only lines (no markers)
        # 마커 없이 선만 표시되도록 설정함
        line=dict(color="#fa0714", width=3)  # Set line color to red and thickness to 3
        # 선 색상을 빨간색으로, 두께는 3으로 설정함
    ))

    # Set Layout for the figure
    # 그래프 전체 레이아웃을 설정함
    fig_busan.update_layout(
        template="plotly_dark",  # Apply dark theme
        # 다크 테마 적용함 (배경 어두움)

        title=dict(
            text="<b>Monthly Ship Count and Cargo Weight (Busan)</b>",  # Set the chart title
            # 그래프 제목을 설정함
            x=0.35,  # Center the title horizontally
            # 제목을 수평 중앙에 배치함
            font=dict(size=20, color="white")  # Set title font size and color
            # 제목 폰트 크기를 20, 색상을 흰색으로 설정함
        ),

        xaxis=dict(
            title="Year-Month",  # Set x-axis title
            # x축 제목을 설정함
            tickangle=-45,  # Rotate tick labels for better readability
            # 눈금 라벨을 45도 기울여 가독성을 높임
            dtick="M12"  # Show tick every 12 months (1 year)
            # 12개월(1년)마다 눈금이 표시되도록 설정함
        ),

        yaxis=dict(
            title="Ship Count",  # Title for the left y-axis
            # 왼쪽 y축 제목을 설정함
            side="left"  # Position on the left
            # 왼쪽에 위치하도록 설정함
        ),

        yaxis2=dict(
            title="Weight (tons)",  # Title for the right y-axis
            # 오른쪽 y축 제목을 설정함
            overlaying="y",  # Overlay on top of the left y-axis
            # 왼쪽 y축 위에 겹쳐서 표시되도록 설정함
            side="right",  # Position on the right
            # 오른쪽에 위치하도록 설정함
            showgrid=False  # Hide grid lines for the secondary y-axis
            # 보조 y축의 그리드 라인을 숨김
        ),

        legend=dict(
            x=1,  # Position legend on the far right
            # 범례를 그래프 오른쪽 끝에 배치함
            y=5,  # Position at the top
            # 범례를 그래프 상단에 배치함
            xanchor="right",  # Anchor legend box from the right
            # x 기준 오른쪽 정렬되도록 설정함
            yanchor="top"  # Anchor from the top
            # y 기준 위쪽 정렬되도록 설정함
        ),

        font=dict(family="Malgun Gothic")  # Set font to support Korean characters
        # 한글 폰트 깨짐 방지를 위해 'Malgun Gothic' 폰트 사용함
    )

    # Streamlit에 시각화 출력
    st.plotly_chart(fig_busan, use_container_width=True, key="en_busan_monthly")

with tab_2:
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>대한민국</span>은 원자재와 부품을 수입해 조립·가공한 뒤 고부가가치 제품으로 재수출하는 가공무역 중심의 산업 구조를 갖추고 있으며
    <span style='color:orange; font-weight:bold; font-size:20px;'>세계에서 9번째로 큰 수입국</span>입니다.
    <br>특히, <span style='color:orange; font-weight:bold; font-size:20px;'>부산항, 인천항, 광양항, 울산항</span>은 대한민국의 주요 항구이자 수출입을 실질적으로 수행하는 물류 허브입니다.
    """, unsafe_allow_html=True)

    #시각화 데이터
    koreaPorts = pd.read_csv("./useData/raw_koreaAllHarbors.csv")
    koreaPorts = koreaPorts.iloc[:, 1:]
    koreaPorts = koreaPorts[koreaPorts["Harbor name"]!="항만명"]
    # 건수와 중량 0인것 절사
    koreaPorts = koreaPorts[koreaPorts["Ship count"] != "0"]
    koreaPorts = koreaPorts[koreaPorts["Ship count"] != "0"]

    def notComma(x):
        return x.replace(",","")

    koreaPorts_counts = koreaPorts[["Year", "Harbor name", "Ship count"]]
    koreaPorts_counts["Ship count"] = koreaPorts_counts["Ship count"].apply(notComma)
    koreaPorts_counts["Ship count"] = koreaPorts_counts["Ship count"].astype("int32")
    koreaPorts_counts["Year"] = koreaPorts_counts["Year"].astype("str")
    koreaPorts_counts = koreaPorts_counts[koreaPorts_counts["Year"] != "2025"]

    # 항구 이름 고유값 추출
    harbors = koreaPorts_counts["Harbor name"].unique()
    # 연도는 문자열로 정렬
    years = sorted(koreaPorts_counts["Year"].unique())

    # Figure 초기화
    fig = go.Figure()


    # 항구별 입항 외국선 개수 시각화
    for harbor in harbors:
        subset = koreaPorts_counts[koreaPorts_counts["Harbor name"] == harbor]
        subset = subset.groupby("Year")["Ship count"].sum().reindex(years, fill_value=0)  # 누락 연도는 0으로 채움

        fig.add_trace(go.Bar(
            x=years,
            y=subset.values,
            name=harbor
        ))

    # 레이아웃 설정
    fig.update_layout(
        template = "plotly_dark",
        title=dict(
        text="<b>Number of foreign ships entering port by year</b>",
        x=0.35,
        y=0.9,
        font={"size": 20,
                "color":"white"}
        ),
        xaxis_title="Year",
        yaxis_title="Number of foreign ships",
        barmode="group",  # 'stack'으로 바꾸면 누적형
        xaxis=dict(type='category', categoryorder='category ascending'),
        font=dict(family="Malgun Gothic"),  # 한글 깨짐 방지
        legend_title="Kinds of harbor"
    )

    # Streamlit에 시각화 출력
    st.plotly_chart(fig, use_container_width=True, key="kr_foreign_ship_count")


    # 필요한 열 선택 후 쉼표 제거 및 int 변환
    koreaPorts_weights = koreaPorts[["Year", "Harbor name", "Weight"]]
    koreaPorts_weights["Weight"] = koreaPorts_weights["Weight"].apply(notComma)
    koreaPorts_weights["Weight"] = koreaPorts_weights["Weight"].astype("int32")
    koreaPorts_weights["Year"] = koreaPorts_weights["Year"].astype("str")
    koreaPorts_weights = koreaPorts_weights[koreaPorts_weights["Year"] != "2025"]

    # 항구 이름 고유값 추출
    harbors = koreaPorts_weights["Harbor name"].unique()

    # 연도는 문자열로 정렬
    years = sorted(koreaPorts_weights["Year"].unique())

    # Figure 초기화
    fig_w = go.Figure()

    # 항구별 입항 외국선 기준 물동량 시각화
    for harbor in harbors:
        subset = koreaPorts_weights[koreaPorts_weights["Harbor name"] == harbor]
        subset = subset.groupby("Year")["Weight"].sum().reindex(years, fill_value=0)  # 누락 연도는 0으로 채움

        fig_w.add_trace(go.Bar(
            x=years,
            y=subset.values,
            name=harbor
        ))

    # 레이아웃 설정
    # 레이아웃 설정 (중량 단위로 수정)
    fig_w.update_layout(
        template="plotly_dark",
        title=dict(
            text="<b>Total cargo weight by year and harbor</b>",
            x=0.35,
            y=0.9,
            font={"size": 20, "color": "white"}
        ),
        xaxis_title="Year",
        yaxis_title="Cargo Weight (tons)",
        barmode="group",
        xaxis=dict(type='category', categoryorder='category ascending'),
        font=dict(family="Malgun Gothic"),
        legend_title="Kinds of harbor"
    )

    # Streamlit에 시각화 출력
    st.plotly_chart(fig_w, use_container_width=True, key="kr_cargo_weight_by_port")

    st.markdown("""
    위 시각화 그래프를 통해서 <span style='font-weight:bold; font-size:20px;'>년간 입항된 외국선 수, 외국선의 물동량 모두 </span><span style='color:white; font-weight:bold; font-size:20px;'>부산, 울산, 인천, 광양</span> 항구가 제일 높은 것을 확인 할 수 있습니다.
    <br>그 중 <span style='color:orange; font-weight:bold; font-size:20px;'>부산 항구가 외국선 수와 물동량 모두 1위</span>를 차지하여 별도 데이터를 추출하여 시각화 그래프로 재구현했습니다.
    """, unsafe_allow_html=True)

    # 부산 시각화 년도 월별
    koreaPorts_busan_countWeight = koreaPorts[koreaPorts["Harbor name"]=="부산"]

    # 입항건수 : 필요한 열 선택 후 쉼표 제거 및 int 변환
    koreaPorts_busan_countWeight["Ship count"] = koreaPorts_busan_countWeight["Ship count"].apply(notComma)
    koreaPorts_busan_countWeight["Ship count"] = koreaPorts_busan_countWeight["Ship count"].astype("int32")
    koreaPorts_busan_countWeight["Year"] = koreaPorts_busan_countWeight["Year"].astype("str")
    koreaPorts_busan_countWeight = koreaPorts_busan_countWeight[koreaPorts_busan_countWeight["Year"] != "2025"]

    # 부산 항만 데이터만 필터링
    # Filter data for the port of 'Busan' only
    koreaPorts_busan_countWeight = koreaPorts[koreaPorts["Harbor name"] == "부산"].copy()

    # 1. Remove commas from 'Ship count' column and convert to integer
    #    'Ship count' 열의 쉼표 제거 후 정수형으로 변환합니다.
    koreaPorts_busan_countWeight["Ship count"] = koreaPorts_busan_countWeight["Ship count"].apply(notComma)
    koreaPorts_busan_countWeight["Ship count"] = koreaPorts_busan_countWeight["Ship count"].astype("int32")

    # 2. Remove commas from 'Weight' column and convert to integer
    #    'Weight' 열의 쉼표 제거 후 정수형으로 변환합니다.
    #    예: "30,727,140" → 30727140 (수치 계산 가능하게 변환)
    koreaPorts_busan_countWeight["Weight"] = koreaPorts_busan_countWeight["Weight"].str.replace(",", "").astype(int)

    # 3. Convert 'Year' to string and filter out the year 2025
    koreaPorts_busan_countWeight["Year"] = koreaPorts_busan_countWeight["Year"].astype("str")
    koreaPorts_busan_countWeight = koreaPorts_busan_countWeight[koreaPorts_busan_countWeight["Year"] != "2025"]

    # 4. Create 'Year-Month' column as datetime
    koreaPorts_busan_countWeight["Year-Month"] = pd.to_datetime(
        koreaPorts_busan_countWeight["Year"] + "-" + koreaPorts_busan_countWeight["Month"].astype(str).str.zfill(2)
    )

    # 5. Sort the data by 'Year-Month' for time-series visualization
    koreaPorts_busan_countWeight = koreaPorts_busan_countWeight.sort_values(by="Year-Month")


    # Initialize the figure
    # 그래프 Figure 객체 생성함
    fig_busan = go.Figure()

    # Add Bar Chart (Ship Count - left Y axis)
    # 입항 건수 데이터를 막대그래프로 추가함 (왼쪽 y축 기준)
    fig_busan.add_trace(go.Bar(
        x=koreaPorts_busan_countWeight["Year-Month"],  # Set x-axis to Year-Month datetime values
        # x축을 연-월(datetime) 값으로 설정함
        y=koreaPorts_busan_countWeight["Ship count"],  # Set y-axis to ship count values
        # y축을 선박 입항 건수로 설정함
        name="Ship count",  # Name shown in legend
        # 범례에 표시될 이름 설정함
        yaxis="y1",  # Use left y-axis
        # 왼쪽 y축에 매핑함
        marker_color="#c2baba"  # Set bar color to light green
    ))

    # Add Line Chart (Weight - right Y axis)
    # 화물 중량 데이터를 선 그래프로 추가함 (오른쪽 y축 기준)
    fig_busan.add_trace(go.Scatter(
        x=koreaPorts_busan_countWeight["Year-Month"],  # Set x-axis to Year-Month datetime values
        # x축을 연-월(datetime) 값으로 설정함
        y=koreaPorts_busan_countWeight["Weight"],  # Set y-axis to cargo weight values
        # y축을 화물 중량 값으로 설정함
        name="Weight (tons)",  # Name shown in legend
        # 범례에 표시될 이름 설정함
        yaxis="y2",  # Use right y-axis
        # 오른쪽 y축에 매핑함
        mode="lines",  # Show only lines (no markers)
        # 마커 없이 선만 표시되도록 설정함
        line=dict(color="#fa0714", width=3)  # Set line color to red and thickness to 3
        # 선 색상을 빨간색으로, 두께는 3으로 설정함
    ))

    # Set Layout for the figure
    # 그래프 전체 레이아웃을 설정함
    fig_busan.update_layout(
        template="plotly_dark",  # Apply dark theme
        # 다크 테마 적용함 (배경 어두움)

        title=dict(
            text="<b>Monthly Ship Count and Cargo Weight (Busan)</b>",  # Set the chart title
            # 그래프 제목을 설정함
            x=0.35,  # Center the title horizontally
            # 제목을 수평 중앙에 배치함
            font=dict(size=20, color="white")  # Set title font size and color
            # 제목 폰트 크기를 20, 색상을 흰색으로 설정함
        ),

        xaxis=dict(
            title="Year-Month",  # Set x-axis title
            # x축 제목을 설정함
            tickangle=-45,  # Rotate tick labels for better readability
            # 눈금 라벨을 45도 기울여 가독성을 높임
            dtick="M12"  # Show tick every 12 months (1 year)
            # 12개월(1년)마다 눈금이 표시되도록 설정함
        ),

        yaxis=dict(
            title="Ship Count",  # Title for the left y-axis
            # 왼쪽 y축 제목을 설정함
            side="left"  # Position on the left
            # 왼쪽에 위치하도록 설정함
        ),

        yaxis2=dict(
            title="Weight (tons)",  # Title for the right y-axis
            # 오른쪽 y축 제목을 설정함
            overlaying="y",  # Overlay on top of the left y-axis
            # 왼쪽 y축 위에 겹쳐서 표시되도록 설정함
            side="right",  # Position on the right
            # 오른쪽에 위치하도록 설정함
            showgrid=False  # Hide grid lines for the secondary y-axis
            # 보조 y축의 그리드 라인을 숨김
        ),

        legend=dict(
            x=1,  # Position legend on the far right
            # 범례를 그래프 오른쪽 끝에 배치함
            y=5,  # Position at the top
            # 범례를 그래프 상단에 배치함
            xanchor="right",  # Anchor legend box from the right
            # x 기준 오른쪽 정렬되도록 설정함
            yanchor="top"  # Anchor from the top
            # y 기준 위쪽 정렬되도록 설정함
        ),

        font=dict(family="Malgun Gothic")  # Set font to support Korean characters
        # 한글 폰트 깨짐 방지를 위해 'Malgun Gothic' 폰트 사용함
    )

    # Streamlit에 시각화 출력
    st.plotly_chart(fig_busan, use_container_width=True, key="kr_busan_monthly")

with tab_3:
    st.markdown('''
    (1) Data Source : https://www.nlic.go.kr/nlic/seaShipEtrypt.action <br>
    (2) Collected Data : Collected data to assess foreign vessel cargo volume arriving in South Korea (2010–Feb 2025).(대한민국에 입항한 외국선의 물동량을 파악하기 위해 2010년부터 2025년 2월까지의 데이터를 수집함.)<br>
    (3) Data Type : Structured Data(정형 데이터)<br>
    (4) Technologies Used : Selenium, BeautifulSoup(bs4), Pandas, Plotly Express & Plotly Graph Objects<br>
    (5) Data Collection and Preprocessing Process
    ''',unsafe_allow_html=True)
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Collection (데이터 수집)</span>", unsafe_allow_html=True)
    st.video("./useData/koreaAllports.mp4")
    st.code('''
    # Author : DongWheeKIM
    # Date Written : 2025-04-09
    # Description  : Crawls the Korean National Logistics portal to collect vessel entry data by year/month/port and exports it to CSV format.
    # (한국 해양물류정보시스템에서 연도/월/항구별 입항 선박 및 물동량 데이터를 수집하여 CSV로 저장)

    # Import libraries with purpose comments (라이브러리 목적별 주석)
    from bs4 import BeautifulSoup  # for parsing HTML content (HTML 콘텐츠 파싱용)
    import pandas as pd  # for data storage and analysis (데이터 저장 및 분석용)
    import requests as req  # for sending HTTP requests (HTTP 요청 전송용)

    # Selenium WebDriver modules for browser automation (웹 브라우저 자동화를 위한 Selenium 모듈)
    from selenium import webdriver  # Web browser controller (웹 브라우저 제어)
    from selenium.webdriver.support.select import Select  # for interacting with dropdown menus (드롭다운 메뉴 조작)
    from selenium.webdriver.chrome.service import Service  # Chrome driver service manager (크롬 드라이버 서비스 관리)
    from selenium.webdriver.common.by import By  # for selecting HTML elements (HTML 요소 탐색)
    from selenium.webdriver.support.ui import WebDriverWait  # for explicit wait handling (명시적 대기 설정)
    from selenium.webdriver.support import expected_conditions as EC  # for wait conditions (기대 조건 설정)
    from selenium.webdriver.common.keys import Keys  # for keyboard input (키보드 입력 제어)
    import time  # for execution delays (지연 실행을 위한 time 모듈)

    # Set Chrome browser options (크롬 브라우저 옵션 설정)
    optionSet = webdriver.ChromeOptions()
    optionSet.add_argument("no-sandbox")  # Disable sandbox mode for compatibility (샌드박스 모드 비활성화로 호환성 확보)

    # Start Chrome browser with defined service and options (설정된 서비스 및 옵션으로 브라우저 실행)
    chromeService = Service("../autoDriver/chromedriver.exe")
    chromeDriver = webdriver.Chrome(service=chromeService, options=optionSet)
    chromeDriver.maximize_window()  # Maximize browser window (브라우저 창 최대화)

    # Set explicit wait object with 3 seconds timeout (3초 명시적 대기 객체 설정)
    waitObject = WebDriverWait(chromeDriver, 3)

    # Define utility functions for element selection (요소 탐색을 위한 유틸 함수 정의)

    def bs4_find(css_selector):
        # Find a single element using BeautifulSoup (BeautifulSoup로 단일 요소 탐색)
        return soupObject.select_one(css_selector)

    def bs4_finds(css_selector):
        # Find multiple elements using BeautifulSoup (BeautifulSoup로 다중 요소 탐색)
        return soupObject.select(css_selector)

    def selenium_find(css_selector):
        # Wait for an element to be present and return it (요소가 로드될 때까지 대기 후 반환)
        return waitObject.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    # Target URL for vessel entry portal (입항 통계 사이트 URL 설정)
    targetUrl = "https://www.nlic.go.kr/nlic/seaShipEtrypt.action"
    chromeDriver.get(targetUrl)  # Open the URL in the browser (브라우저에서 URL 열기)
    time.sleep(5)  # Wait for initial page load (초기 페이지 로딩 대기)
    print("✅ Site loaded")

    # Setup BeautifulSoup for parsing static HTML (정적 HTML 파싱을 위한 BeautifulSoup 설정)
    headersInfo = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = req.get(targetUrl, headers=headersInfo)  # Send GET request (GET 요청 전송)
    soupObject = BeautifulSoup(response.text, "html.parser")  # Parse the response text (응답 HTML 파싱)

    # Initialize lists for collected data (수집할 데이터를 담을 리스트 초기화)
    HarborNameList = list()  # 항구명 리스트
    ShipCountList = list()  # 선박 수 리스트
    WeightList = list()  # 물동량 리스트
    YearList = list()  # 연도 리스트
    MonthList = list()  # 월 리스트

    # Extract available years from dropdown (연도 선택 드롭다운에서 연도 추출)
    yearText = bs4_find("select#S_YEAR").get_text(strip=True)
    YearOptions = [yearText[i:i+4] for i in range(0, len(yearText), 4)]  # 4글자 단위로 자르기
    YearOptions.sort()  # 연도 정렬

    # Loop through years and months (연도 및 월별 반복)
    for year in YearOptions:
        yearDropdown = Select(selenium_find("select#S_YEAR"))  # 연도 드롭다운 객체
        yearDropdown.select_by_value(year)  # 연도 선택
        print(f"\n====================\nYear: {year}")

        selenium_find("button.btn-md").click()  # 조회 버튼 클릭
        time.sleep(5)  # 결과 로딩 대기

        # Get available months (해당 연도에서 선택 가능한 월 추출)
        monthOptions = [
            option.get_attribute("value")
            for option in Select(selenium_find("select#S_MONTH")).options
            if option.get_attribute("value")
        ]
        monthOptions.sort()

        for month in monthOptions:
            monthDropdown = Select(selenium_find("select#S_MONTH"))  # 월 드롭다운 객체
            monthDropdown.select_by_value(month)  # 월 선택

            selenium_find("button.btn-md").click()  # 다시 조회 버튼 클릭
            print(f"📅 Month {month}: Search initiated")
            time.sleep(5)

            soup = BeautifulSoup(chromeDriver.page_source, "html.parser")  # 현재 페이지 HTML 파싱

            # Scrape harbor name, ship count, and weight (항구명, 선박 수, 물동량 추출)
            harborElements = soup.select("ul.frist_b.W_100px")
            tempHarborNames = [el.get_text(strip=True) for el in harborElements if el.get_text(strip=True) != "합계"]

            shipCountElements = soup.select("ul.etc_b.W_64px")
            tempShipCounts = [shipCountElements[i].get_text(strip=True) for i in range(2, len(shipCountElements), 6)]

            weightElements = soup.select("ul.etc_b.W_96px")
            tempWeights = [weightElements[i].get_text(strip=True) for i in range(2, len(weightElements), 5)]

            # Append to main list (리스트에 각 데이터 추가)
            for idx in range(len(tempHarborNames)):
                HarborNameList.append(tempHarborNames[idx])
                ShipCountList.append(tempShipCounts[idx] if idx < len(tempShipCounts) else "")
                WeightList.append(tempWeights[idx] if idx < len(tempWeights) else "")
                YearList.append(year)
                MonthList.append(month)

    # Create and export DataFrame (데이터프레임 생성 및 CSV 저장)
    KoreaHarborsData = pd.DataFrame({
        "Year": YearList,
        "Month": MonthList,
        "HarborName": HarborNameList,
        "ShipCount": ShipCountList,
        "Weight": WeightList
    })

    KoreaHarborsData.to_csv("useData/koreaHarbors_rawData.csv", encoding="utf-8-sig", index=False)  # CSV로 저장
    print("✅ Data saved to useData/koreaHarbors_rawData.csv")  # 완료 메시지 출력
            ''')
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Preprocessing (데이터 가공)</span>", unsafe_allow_html=True)
    st.code('''
    # Author : DongWheeKIM
    # Date Written : 2025-04-09
    # Description  : Load, clean, and visualize vessel entry and cargo weight data from Korean ports,
    #                with a focus on Busan. Outputs include bar charts, line plots, and correlation analysis.

    # Import libraries for data processing and visualization (데이터 처리 및 시각화를 위한 라이브러리)
    import pandas as pd  # for data manipulation (데이터 조작)
    import plotly.express as px  # for simple visualizations (간단한 시각화)
    import plotly.graph_objects as go  # for advanced visualizations (고급 시각화)
    from scipy.stats import pearsonr  # for calculating Pearson correlation (피어슨 상관계수 계산용)

    # Load and clean raw data (원시 데이터 불러오고 전처리)
    koreaPorts = pd.read_csv("../useData/raw_koreaAllHarbors.csv")  # Load CSV file (CSV 파일 불러오기)
    koreaPorts = koreaPorts.iloc[:, 1:]  # Drop index column if present (불필요한 인덱스 컬럼 제거)
    koreaPorts = koreaPorts[koreaPorts["Harbor name"] != "항만명"]  # Remove header row if duplicated (중복된 헤더 제거)
    koreaPorts = koreaPorts[koreaPorts["Ship count"] != "0"]  # Filter out zero ship count (선박 수 0 제외)

    print(koreaPorts.info())  # Print data info (데이터 요약 출력)
    koreaPorts.head()  # Show first few rows (처음 몇 줄 출력)

    # Define function to remove commas (숫자 쉼표 제거 함수 정의)
    def not_comma(x):
        return x.replace(",", "")

    # ===============================
    # 1. Ship Count by Year & Harbor
    # ===============================

    # Select relevant columns and convert data types (필요한 열 선택 및 자료형 변환)
    koreaPortsCounts = koreaPorts[["Year", "Harbor name", "Ship count"]].copy()
    koreaPortsCounts["Ship count"] = koreaPortsCounts["Ship count"].apply(not_comma).astype("int32")
    koreaPortsCounts["Year"] = koreaPortsCounts["Year"].astype("str")
    koreaPortsCounts = koreaPortsCounts[koreaPortsCounts["Year"] != "2025"]  # Exclude incomplete year (2025년 제외)

    # Extract unique values for plotting (그래프용 고유값 추출)
    harbors = koreaPortsCounts["Harbor name"].unique()  # Unique harbor names (항구명)
    years = sorted(koreaPortsCounts["Year"].unique())  # Sorted year list (연도 정렬)

    # Initialize Plotly figure (그래프 객체 초기화)
    fig = go.Figure()

    # Add bar trace for each harbor (항구별 막대그래프 트레이스 추가)
    for harbor in harbors:
        subset = koreaPortsCounts[koreaPortsCounts["Harbor name"] == harbor]
        subset = subset.groupby("Year")["Ship count"].sum().reindex(years, fill_value=0)
        fig.add_trace(go.Bar(x=years, y=subset.values, name=harbor))

    # Update layout and show figure (레이아웃 설정 및 그래프 출력)
    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text="<b>Number of foreign ships entering port by year</b>",
            x=0.5, y=0.9,
            font={"size": 20, "color": "white"}
        ),
        xaxis_title="Year",
        yaxis_title="Number of foreign ships",
        barmode="group",
        xaxis=dict(type='category', categoryorder='category ascending'),
        font=dict(family="Malgun Gothic"),
        legend_title="Kinds of harbor"
    )
    fig.show()

    # ===============================
    # 2. Cargo Weight by Year & Harbor
    # ===============================
    koreaPortsWeights = koreaPorts[["Year", "Harbor name", "Weight"]].copy()
    koreaPortsWeights["Weight"] = koreaPortsWeights["Weight"].apply(not_comma).astype("int32")
    koreaPortsWeights["Year"] = koreaPortsWeights["Year"].astype("str")
    koreaPortsWeights = koreaPortsWeights[koreaPortsWeights["Year"] != "2025"]

    harbors = koreaPortsWeights["Harbor name"].unique()
    years = sorted(koreaPortsWeights["Year"].unique())

    fig_w = go.Figure()
    for harbor in harbors:
        subset = koreaPortsWeights[koreaPortsWeights["Harbor name"] == harbor]
        subset = subset.groupby("Year")["Weight"].sum().reindex(years, fill_value=0)
        fig_w.add_trace(go.Bar(x=years, y=subset.values, name=harbor))

    fig_w.update_layout(
        template="plotly_dark",
        title=dict(
            text="<b>Total cargo weight by year and harbor</b>",
            x=0.5, y=0.9,
            font={"size": 20, "color": "white"}
        ),
        xaxis_title="Year",
        yaxis_title="Cargo Weight (tons)",
        barmode="group",
        xaxis=dict(type='category', categoryorder='category ascending'),
        font=dict(family="Malgun Gothic"),
        legend_title="Kinds of harbor"
    )
    fig_w.show()

    # ===============================
    # 3. Busan Monthly Trends (Ship Count & Weight)
    # ===============================
    busanData = koreaPorts[koreaPorts["Harbor name"] == "부산"].copy()
    busanData["Ship count"] = busanData["Ship count"].apply(not_comma).astype("int32")
    busanData["Weight"] = busanData["Weight"].str.replace(",", "").astype(int)
    busanData["Year"] = busanData["Year"].astype("str")
    busanData = busanData[busanData["Year"] != "2025"]
    busanData["Year-Month"] = pd.to_datetime(busanData["Year"] + "-" + busanData["Month"].astype(str).str.zfill(2))
    busanData = busanData.sort_values(by="Year-Month")
    busanData.to_csv("../useData/finishPrepro/koreaAllharbors_countWeight.csv", encoding="utf-8-sig")

    # Initialize dual-axis plot (이중 y축 그래프 생성)
    fig_busan = go.Figure()
    fig_busan.add_trace(go.Bar(
        x=busanData["Year-Month"],
        y=busanData["Ship count"],
        name="Ship count",
        yaxis="y1",
        marker_color="lightgreen"
    ))
    fig_busan.add_trace(go.Scatter(
        x=busanData["Year-Month"],
        y=busanData["Weight"],
        name="Weight (tons)",
        yaxis="y2",
        mode="lines",
        line=dict(color="red", width=3)
    ))
    fig_busan.update_layout(
        template="plotly_dark",
        title=dict(
            text="<b>Monthly Ship Count and Cargo Weight (Busan)</b>",
            x=0.5, font=dict(size=20, color="white")
        ),
        xaxis=dict(title="Year-Month", tickangle=-45, dtick="M12"),
        yaxis=dict(title="Ship Count", side="left"),
        yaxis2=dict(title="Weight (tons)", overlaying="y", side="right", showgrid=False),
        legend=dict(x=1, y=1, xanchor="right", yanchor="top"),
        font=dict(family="Malgun Gothic")
    )
    fig_busan.show()

    # ===============================
    # 4. Correlation Heatmap (상관관계 분석)
    # ===============================
    corrMatrix = busanData[["Ship count", "Weight"]].corr()  # Compute correlation matrix (상관행렬 계산)
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=corrMatrix.values,
        x=corrMatrix.columns,
        y=corrMatrix.index,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        colorbar=dict(title="Correlation"),
        showscale=True
    ))
    # Add annotation for each cell (셀마다 수치 표시)
    for i in range(len(corrMatrix.index)):
        for j in range(len(corrMatrix.columns)):
            value = corrMatrix.values[i][j]
            fig.add_annotation(
                x=corrMatrix.columns[j],
                y=corrMatrix.index[i],
                text=f"{value:.4f}",
                showarrow=False,
                font=dict(color="#f03a3a", size=14)
            )
    fig.update_layout(
        title="Correlation Heatmap: Ship Count vs Weight",
        xaxis=dict(title="", tickangle=0),
        yaxis=dict(title=""),
        width=500,
        height=400,
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
    fig.show()

    # ===============================
    # 5. Pearson Correlation Coefficient (피어슨 상관계수 계산)
    # ===============================
    x = busanData["Ship count"]  # X variable (입항 건수)
    y = busanData["Weight"]      # Y variable (화물 중량)
    corrCoef, pValue = pearsonr(x, y)  # Pearson correlation (피어슨 상관계수와 유의확률 계산)
    print(f"Pearson correlation coefficient: {corrCoef:.4f}")
    print(f"P-value: {pValue:.4f}")
    ''')
