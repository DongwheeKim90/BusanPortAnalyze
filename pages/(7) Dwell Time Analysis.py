import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Vessel Dwell Time Analysis by Shipping Company", anchor=False)

tab_1, tab_2, tab_3 = st.tabs(["Analysis Process(EN)", "Analysis Process(KR)", "Data Preprocessing"])

with tab_1:
    st.markdown('''
    In this section, we <span style='color:orange; font-weight:bold; font-size:20px;'>analyze the average vessel stay duration by shipping company</span>.
    The goal of this analysis is to <span style='color:orange; font-weight:bold; font-size:20px;'>understand the distribution of vessel stay durations and use this data to recommend travel courses in Busan</span>, linking with local attractions such as restaurants, tourist spots, and accommodations.

    According to the results of the previous analysis in ‘(4) Top 3 Ports in Busan’, North Port had the highest number of vessel calls, while New Port handled the largest cargo volume.
    Although it might be reasonable to focus on North Port for analysis, in this project we chose to focus on <span style='color:orange; font-weight:bold; font-size:20px;'>New Port</span> instead.

    The reasons are as follows:

    - New Port primarily serves <span style='color:white; font-weight:bold; font-size:20px;'>large international container vessels</span>, whereas <span style='color:white; font-weight:bold; font-size:20px;'>North Port handles a higher proportion of small domestic vessels and passenger ships</span>, which differ in characteristics.
    - Among the three major ports in Busan, <span style='color:white; font-weight:bold; font-size:20px;'>only New Port is equipped with advanced logistics infrastructure</span>, such as automated terminals, large-scale warehouses, and a Free Trade Zone (FTZ).

    Accordingly, we collected and visualized data on the shipping companies and their stay durations by year/month/day for vessels entering New Port.
    ''', unsafe_allow_html=True)

    schedule = pd.read_csv("./useData/SinhangSchedule_rawData.csv", encoding="utf-8-sig")
    schedule = schedule.iloc[:,1:]
    #형변환 : Date_time
    #-함수 정의
    def changeDateType(x):
        changeDate = pd.to_datetime(x)
        return changeDate

    #-형변환
    schedule["Enter Time"] = changeDateType(schedule["Enter Time"])
    schedule["Out Time"] = changeDateType(schedule["Out Time"])
    schedule["Day difference"] = schedule["Enter Time"] - schedule["Out Time"]

    #-체류기간(일,시간) : Duration of stay (days, hours)
    Dd_list = list(schedule["Day difference"])
    Duration_days_list = list()
    Duration_hourss_list = list()

    for v in Dd_list:
        v = str(v)
        v_edit = v.replace(" ","").replace("days","").replace("-","").split("+")
        Duration_days_list.append(v_edit[0])
        Duration_hourss_list.append(v_edit[1])

    schedule["Duration days"] = Duration_days_list
    schedule["Duration hours"] = Duration_hourss_list

    #-체류기간 총 시간
    calculate_hour_list = list()
    for v in schedule["Duration days"]:
        v = int(v)
        change_hour = v*24
        calculate_hour_list.append(change_hour)

    hourToInt = [v.split(":")[0] for v in schedule["Duration hours"]]

    sumHour_list = [int(i) + int(v) for i,v in zip(calculate_hour_list, hourToInt)]

    schedule["Total duration(Hours)"] = sumHour_list

    schedule_duration = schedule[["Ship Company", "Total duration(Hours)"]].copy()

    # 평균 계산
    schedule_duration = schedule.groupby("Ship Company")["Total duration(Hours)"].mean()

    # 리스트로 분리 저장
    avg_shipName_list = list(schedule_duration.index)
    avgTime_list = list(schedule_duration.values)

    # 데이터프레임 생성
    avgDuration_ships = pd.DataFrame({
        "Ship name": avg_shipName_list,
        "Avg time": avgTime_list
    })

    avgDuration_ships = avgDuration_ships.sort_values(["Avg time"],ascending=False).reset_index().iloc[:,1:]

    #평균시간이 긴 10개 선사
    avgDuration_ships_top10 = avgDuration_ships.iloc[:9,:]

    duration_fig = px.box(
        schedule,
        y="Total duration(Hours)",
        title="Residence Time by Shipping Company",
    )

    duration_fig.update_layout(
        title=dict(
            text="<b>Residence Time by Shipping Company</b>",
            x=0.5,
            xanchor='center',
            font=dict(color="white")  # ✅ 제목 색상
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(
            title=dict(text="Ship Company", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title=dict(text="Total Duration (Hours)", font=dict(color="white")),
            tickfont=dict(color="white"),
            gridcolor="gray"
        )
    )
    duration_fig.update_traces(
        marker_color="orange",
        boxmean=True
    )
    st.plotly_chart(duration_fig, key="kr_duration_en")

    st.markdown('''
    Typically, the <span style='color:white; font-weight:bold; font-size:20px;'>average stay duration by ship type</span> is shown in the table below.
    However, based on our actual data analysis, there were cases where <span style='color:orange; font-weight:bold; font-size:20px;'>the average stay duration by shipping company reached up to 59 hours</span>.
    We considered such values as outliers, excluded them, and re-visualized the data.
    ''', unsafe_allow_html=True)

    new_time_df = pd.DataFrame({
        "Ship Type": ["Container Ship", "Bulk Carrier (grain, coal, etc.)", "Oil Tanker", "Cruise Ship"],
        "Average Stay Duration (Approx.)": ["About 24–36 hours", "Possibly over 48 hours", "Around 36 hours", "8–12 hours (short)"]
    })

    st.dataframe(new_time_df, hide_index=True, use_container_width=True)

    schedule_removeAnomaly = schedule[schedule["Total duration(Hours)"] <=59]
    schedule_removeAnomaly[["Ship Company","Enter Time", "Out Time", "Duration days", "Duration hours", "Total duration(Hours)"]].to_csv("./useData/finishPrepro/shipsDuration.csv")

    duration_fig_1 = px.box(
    schedule_removeAnomaly,
    y="Total duration(Hours)",
    title="Residence Time by Shipping Company",
    )

    duration_fig_1.update_layout(
        title=dict(
            text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
            x=0.5,
            xanchor='center',
            font=dict(color="white")  # ✅ 제목 색상
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(
            title=dict(text="Ship Company", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title=dict(text="Total Duration (Hours)", font=dict(color="white")),
            tickfont=dict(color="white"),
            gridcolor="gray"
        )
    )

    duration_fig_1.update_traces(
        marker_color="red",
        boxmean=True
    )
    st.plotly_chart(duration_fig_1, use_container_width=True, key="kr_duration_anomaly_en")

    st.markdown('''
    From the graph above, we confirmed that <span style='color:orange; font-weight:bold; font-size:20px;'>the maximum stay duration for large cargo ships was 59 hours, the average and median were 37 hours, and the minimum was 24 hours</span>.
    By analyzing the <span style='color:white; font-weight:bold; font-size:20px;'>quartiles of the box plot, we were able to understand the distribution of stay durations</span>, and based on this, we plan to <span style='color:white; font-weight:bold; font-size:20px;'>design and recommend tourist courses in Busan</span>.
    Below is the analysis of the average stay duration by shipping company.
    ''', unsafe_allow_html=True)


    top10_ship = [v for v in avgDuration_ships_top10["Ship name"]]

    index_list = list()

    for i, v in enumerate(schedule["Ship Company"]):
        if v in top10_ship:
            index_list.append(i)

    schedule_10 = schedule.iloc[index_list].reset_index().iloc[:,1:]

    duration_fig_10 = px.box(
        schedule_10,
        x="Ship Company",
        y="Total duration(Hours)",
        title="Residence Time by Shipping Company",
    )

    duration_fig_10.update_layout(
        title=dict(
            text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
            x=0.5,
            xanchor='center',
            font=dict(color="white")  # ✅ 제목 색상
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(
            title=dict(text="Ship Company", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title=dict(text="Total Duration (Hours)", font=dict(color="white")),
            tickfont=dict(color="white"),
            gridcolor="gray"
        )
    )

    duration_fig_10.update_traces(
        marker_color="red",
        boxmean=True
    )

    st.plotly_chart(duration_fig_10, use_container_width=True, key="ship10_duration_en")

    aew_df = pd.DataFrame(schedule_10[schedule_10["Ship Company"]=="AEW"])
    st.dataframe(aew_df, use_container_width=True, hide_index=True)

    st.markdown('''
    According to the analysis, <span style='color:orange; font-weight:bold; font-size:20px;'>AEW entered the port only once</span>, with a stay duration of 58 hours, which placed it high in the average stay time rankings.
    Therefore, <span style='color:white; font-weight:bold; font-size:20px;'>AEW was excluded</span>, and the Top 10 shipping companies were reselected and visualized using a box plot.
    ''', unsafe_allow_html=True)

    avgDuration_ships_top10 = avgDuration_ships.iloc[:11,:]
    avgDuration_ships_top10 = avgDuration_ships_top10[avgDuration_ships_top10["Ship name"]!="AEW"]
    new_avgDuration_ships = avgDuration_ships.iloc[:11,:]
    new_avgDuration_ships = new_avgDuration_ships[new_avgDuration_ships["Ship name"]!="AEW"]


    new_top10_ship = [v for v in new_avgDuration_ships["Ship name"]]

    index_list = list()

    for i, v in enumerate(schedule["Ship Company"]):
        if v in new_top10_ship:
            index_list.append(i)

    new_schedule_10 = schedule.iloc[index_list].reset_index().iloc[:,1:]


    duration_fig_10_edit = px.box(
        new_schedule_10,
        x="Ship Company",
        y="Total duration(Hours)",
        title="Residence Time by Shipping Company",
    )

    duration_fig_10_edit.update_layout(
        title=dict(
            text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
            x=0.5,
            xanchor='center',
            font=dict(color="white")  # ✅ 제목 색상
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(
            title=dict(text="Ship Company", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title=dict(text="Total Duration (Hours)", font=dict(color="white")),
            tickfont=dict(color="white"),
            gridcolor="gray"
        )
    )

    duration_fig_10_edit.update_traces(
        marker_color="red",
        boxmean=True
    )
    st.plotly_chart(duration_fig_10_edit, use_container_width=True, key="ship10_duration_edit_en")

    st.markdown('''
    The analysis revealed that <span style='color:orange; font-weight:bold; font-size:20px;'>10 shipping companies, including MSC</span>, tend to have long port stays.
    Based on this data, Busan Port Authority can <span style='color:orange; font-weight:bold; font-size:20px;'>identify long-stay carriers and organize welfare or benefit events</span>, which can be used to <span style='color:orange; font-weight:bold; font-size:20px;'>effectively manage and retain their clients</span>.
    ''', unsafe_allow_html=True)


with tab_2:
    st.markdown('''
    이번 페이지에서는 <span style='color:orange; font-weight:bold; font-size:20px;'>선사별 체류시간 분석을 수행</span>합니다.
    해당 분석의 목적은 <span style='color:orange; font-weight:bold; font-size:20px;'>선박의 체류시간 분포를 파악하고, 이를 기반으로 부산 내 관광 정보(맛집, 관광명소, 숙박업소 등)를 연계한 추천 코스를 제시</span>하기 위함입니다.
    앞서 ‘(4) Top 3 Ports in Busan’ 분석 결과에 따르면, 입항 건수가 가장 많은 항구는 북항, 물동량이 가장 많은 항구는 신항으로 나타났습니다.
    일반적으로는 북항을 중심으로 분석하는 것이 타당해 보일 수 있으나, 본 프로젝트에서는 <span style='color:orange; font-weight:bold; font-size:20px;'>신항</span>에 초점을 맞추어 분석을 진행하였습니다.
    그 이유는 다음과 같습니다.

    - 신항은 <span style='color:white; font-weight:bold; font-size:20px;'>대형 컨테이너선 등 국제 화물선 중심의 항만</span>인 반면, <span style='color:white; font-weight:bold; font-size:20px;'>북항은 소형 선박, 국내선, 여객선 비중이 높은 항구</span>로, 선박 유형의 특성이 다릅니다.<br>
    - 부산 내 3개 항구 중 <span style='color:white; font-weight:bold; font-size:20px;'>유일하게 자동화 터미널, 대형 물류창고, 자유무역지역(FTZ) 등 첨단 물류 인프라를 갖춘 항만</span>이 신항이기 때문입니다.<br>

    이에 따라, 신항에 입항한 선박의 연도/월/일별 선사 및 체류시간 데이터를 수집·분석하여 시각화하였습니다.
    ''',unsafe_allow_html=True)

    schedule = pd.read_csv("./useData/SinhangSchedule_rawData.csv", encoding="utf-8-sig")
    schedule = schedule.iloc[:,1:]
    #형변환 : Date_time
    #-함수 정의
    def changeDateType(x):
        changeDate = pd.to_datetime(x)
        return changeDate

    #-형변환
    schedule["Enter Time"] = changeDateType(schedule["Enter Time"])
    schedule["Out Time"] = changeDateType(schedule["Out Time"])
    schedule["Day difference"] = schedule["Enter Time"] - schedule["Out Time"]

    #-체류기간(일,시간) : Duration of stay (days, hours)
    Dd_list = list(schedule["Day difference"])
    Duration_days_list = list()
    Duration_hourss_list = list()

    for v in Dd_list:
        v = str(v)
        v_edit = v.replace(" ","").replace("days","").replace("-","").split("+")
        Duration_days_list.append(v_edit[0])
        Duration_hourss_list.append(v_edit[1])

    schedule["Duration days"] = Duration_days_list
    schedule["Duration hours"] = Duration_hourss_list

    #-체류기간 총 시간
    calculate_hour_list = list()
    for v in schedule["Duration days"]:
        v = int(v)
        change_hour = v*24
        calculate_hour_list.append(change_hour)

    hourToInt = [v.split(":")[0] for v in schedule["Duration hours"]]

    sumHour_list = [int(i) + int(v) for i,v in zip(calculate_hour_list, hourToInt)]

    schedule["Total duration(Hours)"] = sumHour_list

    schedule_duration = schedule[["Ship Company", "Total duration(Hours)"]].copy()

    # 평균 계산
    schedule_duration = schedule.groupby("Ship Company")["Total duration(Hours)"].mean()

    # 리스트로 분리 저장
    avg_shipName_list = list(schedule_duration.index)
    avgTime_list = list(schedule_duration.values)

    # 데이터프레임 생성
    avgDuration_ships = pd.DataFrame({
        "Ship name": avg_shipName_list,
        "Avg time": avgTime_list
    })

    avgDuration_ships = avgDuration_ships.sort_values(["Avg time"],ascending=False).reset_index().iloc[:,1:]

    #평균시간이 긴 10개 선사
    avgDuration_ships_top10 = avgDuration_ships.iloc[:9,:]

    duration_fig = px.box(
        schedule,
        y="Total duration(Hours)",
        title="Residence Time by Shipping Company",
    )

    duration_fig.update_layout(
        title=dict(
            text="<b>Residence Time by Shipping Company</b>",
            x=0.5,
            xanchor='center',
            font=dict(color="white")  # ✅ 제목 색상
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(
            title=dict(text="Ship Company", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title=dict(text="Total Duration (Hours)", font=dict(color="white")),
            tickfont=dict(color="white"),
            gridcolor="gray"
        )
    )
    duration_fig.update_traces(
        marker_color="orange",
        boxmean=True
    )
    st.plotly_chart(duration_fig, key="kr_duration")

    st.markdown('''
    대개 <span style='color:white; font-weight:bold; font-size:20px;'>선박 유형별 평균 체류 시간</span>은 아래 표와 같습니다. 그러나 실제 데이터 분석 결과, <span style='color:orange; font-weight:bold; font-size:20px;'>선사별 평균 체류 시간이 최대 59시간에 달하는 경우</span>도 있어, 이를 초과하는 데이터는 이상치로 간주하여 제거한 후 시각화를 다시 진행하였습니다.
    ''', unsafe_allow_html=True)

    new_time_df = pd.DataFrame({
        "선박 유형" : ["컨테이너선","벌크선(곡물, 석탄 등)","유조선","크루즈선"],
        "평균 체류시간 (대략)" : ["약 24시간 ~ 36시간", "48시간 이상도 가능", "36시간 내외", "8~12시간 (짧음)"]
    })
    st.dataframe(new_time_df, hide_index=True, use_container_width=True)

    schedule_removeAnomaly = schedule[schedule["Total duration(Hours)"] <=59]
    schedule_removeAnomaly[["Ship Company","Enter Time", "Out Time", "Duration days", "Duration hours", "Total duration(Hours)"]].to_csv("./useData/finishPrepro/shipsDuration.csv")

    duration_fig_1 = px.box(
    schedule_removeAnomaly,
    y="Total duration(Hours)",
    title="Residence Time by Shipping Company",
    )

    duration_fig_1.update_layout(
        title=dict(
            text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
            x=0.5,
            xanchor='center',
            font=dict(color="white")  # ✅ 제목 색상
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(
            title=dict(text="Ship Company", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title=dict(text="Total Duration (Hours)", font=dict(color="white")),
            tickfont=dict(color="white"),
            gridcolor="gray"
        )
    )

    duration_fig_1.update_traces(
        marker_color="red",
        boxmean=True
    )
    st.plotly_chart(duration_fig_1, use_container_width=True, key="kr_duration_anomaly")

    st.markdown('''
    위 그래프를 통해 대형 카고선의 <span style='color:orange; font-weight:bold; font-size:20px;'>체류 시간은 최대 59시간, 평균 및 중앙값은 37시간, 최소는 24시간</span>임을 확인할 수 있었습니다.
    <span style='color:white; font-weight:bold; font-size:20px;'>박스플롯의 4분위수를 통해 체류 시간의 분포를 파악</span>하였고, 이를 바탕으로 <span style='color:white; font-weight:bold; font-size:20px;'>부산에서의 관광 코스를 설계하고 추천</span>할 예정입니다. 아래는 선사별 평균 체류시간을 분석 결과입니다.
    ''', unsafe_allow_html=True)

    top10_ship = [v for v in avgDuration_ships_top10["Ship name"]]

    index_list = list()

    for i, v in enumerate(schedule["Ship Company"]):
        if v in top10_ship:
            index_list.append(i)

    schedule_10 = schedule.iloc[index_list].reset_index().iloc[:,1:]

    duration_fig_10 = px.box(
        schedule_10,
        x="Ship Company",
        y="Total duration(Hours)",
        title="Residence Time by Shipping Company",
    )

    duration_fig_10.update_layout(
        title=dict(
            text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
            x=0.5,
            xanchor='center',
            font=dict(color="white")  # ✅ 제목 색상
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(
            title=dict(text="Ship Company", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title=dict(text="Total Duration (Hours)", font=dict(color="white")),
            tickfont=dict(color="white"),
            gridcolor="gray"
        )
    )

    duration_fig_10.update_traces(
        marker_color="red",
        boxmean=True
    )

    st.plotly_chart(duration_fig_10, use_container_width=True, key="ship10_duration")

    aew_df = pd.DataFrame(schedule_10[schedule_10["Ship Company"]=="AEW"])
    st.dataframe(aew_df, use_container_width=True, hide_index=True)

    st.markdown('''
    분석 결과, <span style='color:orange; font-weight:bold; font-size:20px;'>AEW는 단 1회 입항</span>했으며 체류 시간이 58시간으로 나타나 평균 체류 시간 집계 시 상위 순위에 포함되었습니다.
    이에 따라 <span style='color:white; font-weight:bold; font-size:20px;'>AEW를 제외한 후, 다시 Top 10 선사를 선정</span>하고 박스플롯 시각화를 진행하였습니다.
    ''', unsafe_allow_html=True)

    avgDuration_ships_top10 = avgDuration_ships.iloc[:11,:]
    avgDuration_ships_top10 = avgDuration_ships_top10[avgDuration_ships_top10["Ship name"]!="AEW"]
    new_avgDuration_ships = avgDuration_ships.iloc[:11,:]
    new_avgDuration_ships = new_avgDuration_ships[new_avgDuration_ships["Ship name"]!="AEW"]


    new_top10_ship = [v for v in new_avgDuration_ships["Ship name"]]

    index_list = list()

    for i, v in enumerate(schedule["Ship Company"]):
        if v in new_top10_ship:
            index_list.append(i)

    new_schedule_10 = schedule.iloc[index_list].reset_index().iloc[:,1:]


    duration_fig_10_edit = px.box(
        new_schedule_10,
        x="Ship Company",
        y="Total duration(Hours)",
        title="Residence Time by Shipping Company",
    )

    duration_fig_10_edit.update_layout(
        title=dict(
            text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
            x=0.5,
            xanchor='center',
            font=dict(color="white")  # ✅ 제목 색상
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(
            title=dict(text="Ship Company", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title=dict(text="Total Duration (Hours)", font=dict(color="white")),
            tickfont=dict(color="white"),
            gridcolor="gray"
        )
    )

    duration_fig_10_edit.update_traces(
        marker_color="red",
        boxmean=True
    )
    st.plotly_chart(duration_fig_10_edit, use_container_width=True, key="ship10_duration_edit")

    st.markdown('''
    분석 결과, <span style='color:orange; font-weight:bold; font-size:20px;'>MSC를 포함한 10개 선사</span>가 장기 체류하는 경향이 있음을 확인할 수 있었습니다.
    이 데이터를 바탕으로 부산항만공사는 <span style='color:orange; font-weight:bold; font-size:20px;'>장기 체류 선사를 선별하여 복지 및 혜택 제공 이벤트를 기획하고, 이를 통해 자사 고객을 효과적으로 관리하고 유지</span>하는 데 활용할 수 있을 것입니다.
    ''', unsafe_allow_html=True)
