import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Number of foreign ships entering and cargo volume by port in Korea.", anchor=False)

tab_1, tab_2, tab_3 = st.tabs(["Analysis Process(EN)", "Analysis Process(KR)", "Data Prep&EDA"])

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

    st.markdown("""
    Although the <span style='font-weight:bold; font-size:20px;'>number of foreign ships entering annually is decreasing</span>,
    cargo volume shows a trend of increasing.<br>
    To provide objective judgment and clear analysis, we conducted a <span style='color:orange; font-weight:bold; font-size:20px;'>correlation analysis</span> and visualized it as a heatmap.
    """, unsafe_allow_html=True)

    # 상관관계 계산
    corr_matrix = koreaPorts_busan_countWeight[["Ship count", "Weight"]].corr()

    # 히트맵 생성
    fig = go.Figure()

    # Heatmap 본체
    fig.add_trace(go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        colorbar=dict(title="Correlation"),
        showscale=True
    ))

    # 셀 안에 수치 텍스트 표시용 annotation 추가
    for i in range(len(corr_matrix.index)):
        for j in range(len(corr_matrix.columns)):
            value = corr_matrix.values[i][j]
            fig.add_annotation(
                x=corr_matrix.columns[j],
                y=corr_matrix.index[i],
                text=f"{value:.4f}",  # 소수점 4자리
                showarrow=False,
                font=dict(color="#f03a3a", size=14)  # 수치 색상과 크기
            )

    # 레이아웃 설정: 배경 검정 + 폰트 흰색
    fig.update_layout(
        title=dict(
            text="Correlation Heatmap: Ship Count vs Weight",  # 제목 내용
            x=0.35,                # x=0.0 → 왼쪽 정렬, x=0.5 → 가운데, x=1.0 → 오른쪽
            xanchor="left",       # 왼쪽 기준 정렬
            y=0.95,               # y 위치 (0~1, 1은 top)
            yanchor="top",        # 위쪽 기준 정렬
            font=dict(size=20, color="white")  # 제목 폰트 스타일
        ),
        xaxis=dict(title="", tickangle=0),
        yaxis=dict(title=""),
        width=500,
        height=400,
        plot_bgcolor='black',     # 플롯 영역 배경
        paper_bgcolor='black',    # 전체 배경
        font=dict(color='white')  # 전체 폰트 색상
    )

    # Streamlit에서 출력 (Jupyter이면 fig.show() 사용)
    st.plotly_chart(fig, use_container_width=True, key="en_busan_correlation")

    st.markdown("""
    The correlation analysis showed a <span style='color:orange; font-weight:bold; font-size:20px;'>correlation coefficient of 0.0184</span>,
    indicating a very weak positive relationship. Therefore, it can be concluded that <span style='color:white; font-weight:bold; font-size:20px;'>there is almost no correlation between the number of arriving ships and total cargo volume</span>.
    """, unsafe_allow_html=True)

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

    st.markdown("""
    년도별 입항된 <span style='font-weight:bold; font-size:20px;'>외국선은 감소하는 추세임에도 불구하고 물동량은 점차 증가</span>하는 것으로 보여졌습니다.<br>객관적인 판단과 명확한 분석을 위해 <span style='color:orange; font-weight:bold; font-size:20px;'>상관관계 분석</span>을 진행하였고 이를 히트맵으로 구현했습니다.
    """, unsafe_allow_html=True)

    # 상관관계 계산
    corr_matrix = koreaPorts_busan_countWeight[["Ship count", "Weight"]].corr()

    # 히트맵 생성
    fig = go.Figure()

    # Heatmap 본체
    fig.add_trace(go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        colorbar=dict(title="Correlation"),
        showscale=True
    ))

    # 셀 안에 수치 텍스트 표시용 annotation 추가
    for i in range(len(corr_matrix.index)):
        for j in range(len(corr_matrix.columns)):
            value = corr_matrix.values[i][j]
            fig.add_annotation(
                x=corr_matrix.columns[j],
                y=corr_matrix.index[i],
                text=f"{value:.4f}",  # 소수점 4자리
                showarrow=False,
                font=dict(color="#f03a3a", size=14)  # 수치 색상과 크기
            )

    # 레이아웃 설정: 배경 검정 + 폰트 흰색
    fig.update_layout(
        title=dict(
            text="Correlation Heatmap: Ship Count vs Weight",  # 제목 내용
            x=0.35,                # x=0.0 → 왼쪽 정렬, x=0.5 → 가운데, x=1.0 → 오른쪽
            xanchor="left",       # 왼쪽 기준 정렬
            y=0.95,               # y 위치 (0~1, 1은 top)
            yanchor="top",        # 위쪽 기준 정렬
            font=dict(size=20, color="white")  # 제목 폰트 스타일
        ),
        xaxis=dict(title="", tickangle=0),
        yaxis=dict(title=""),
        width=500,
        height=400,
        plot_bgcolor='black',     # 플롯 영역 배경
        paper_bgcolor='black',    # 전체 배경
        font=dict(color='white')  # 전체 폰트 색상
    )

    # Streamlit에서 출력 (Jupyter이면 fig.show() 사용)
    st.plotly_chart(fig, use_container_width=True, key="kr_busan_correlation")

    st.markdown("""
    상관분석결과 <span style='color:orange; font-weight:bold; font-size:20px;'>상관계수값은 0.0184</span>로 매우 약한 양의 상관관계를 띄고 있는 것 파악하였고, <span style='color:white; font-weight:bold; font-size:20px;'>입항 선박 수와 총 물동량은 거의 무관</span>하다고 판단했습니다.
    """, unsafe_allow_html=True)
