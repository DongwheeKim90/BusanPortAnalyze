import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from tmapAPI.tmapAPI import *
import nbformat

st.set_page_config(layout='wide')

st.title('Tourist Information by Dwell Time',anchor=False)

# 환경 변수 로딩 및 객체 초기화
load_dotenv()
apikey = os.getenv('TMAP_API_KEY')
tmap = tmapAPI(apikey)

# 부산항 장기체류 top 10 선사 체류시간 데이터 로드
shipsDuration_10 = pd.read_csv('./useData/shipsDuration_10.csv',index_col=0)

# 부산 여행 스팟 데이터 로드
busanSpots = pd.read_csv('./useData/busanSpotsCategorized.csv',index_col=0,encoding='utf-8-sig')

def get_stay_group_course(df, group: str):
    # 공백 제거 혹시 모르니
    df["category2_en"] = df["category2_en"].str.strip()

    if group == "short":
        # 단기 체류: restaurant 2곳
        return df[df["category1"] == "restaurant"].sample(2).reset_index(drop=True)

    elif group == "mid":
        # 중기 체류: restaurant 1곳, 일반 관광지 1곳, 전망대/공원 1곳
        mid_restaurant = df[df["category1"] == "restaurant"].sample(1)
        mid_tour_general = df[
            (df["category1"] == "tour attraction") &
            (~df["category2_en"].isin(["Observatory", "Park"]))
        ].sample(1)
        mid_tour_rest = df[
            (df["category1"] == "tour attraction") &
            (df["category2_en"].isin(["Observatory", "Park"]))
        ].sample(1)
        return pd.concat([mid_restaurant, mid_tour_general, mid_tour_rest]).reset_index(drop=True)

    elif group == "long":
        # 장기 체류: restaurant 2곳, tour attraction 1곳, hotel 1곳
        long_restaurants = df[df["category1"] == "restaurant"].sample(2)
        long_tour = df[df["category1"] == "tour attraction"].sample(1)
        long_hotel = df[df["category1"] == "hotel"].sample(1)
        return pd.concat([long_restaurants, long_tour, long_hotel]).reset_index(drop=True)

    else:
        raise ValueError("그룹 이름은 'short', 'mid', 'long' 중 하나여야 합니다.")

def draw_route_from_tourCourse(df, tmap, mode="car"):
    """
    df: 관광지 DataFrame
    tmap: tmap API 인스턴스
    mode: "car" 또는 "peds"
    
    각 구간별 경로를 folium 지도에 그리면서, 총 이동거리(킬로미터)와 총 소요시간(분)을 합산하여 반환
    """
    # 시작점과 끝점 중심으로 지도 초기화
    start = df.iloc[0]
    end = df.iloc[-1]
    map_center = [(start['lat'] + end['lat']) / 2, (start['lng'] + end['lng']) / 2]
    m = folium.Map(location=map_center, zoom_start=13)

    # 총 합산을 위한 변수 초기화
    total_distance = 0    # km 단위
    total_time = 0        # 분 단위

    # 각 투어 장소에 마커 추가
    for idx, row in df.iterrows():
        if idx == 0:
            color = 'green'
        elif idx == len(df) - 1:
            color = 'red'
        else:
            color = 'blue'

        popup_html = f"""
        <b>{idx+1}. {row['name']}</b><br>
        평점: {row['rating']}<br>
        카테고리(KR): {row['category2']}<br>
        Category(EN): {row['category2_en']}<br>
        주소: {row['address']}
        """

        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=popup_html,
            icon=folium.Icon(color=color)
        ).add_to(m)

    # 연속된 지점 사이의 경로 그리기 및 총합 계산
    for i in range(len(df) - 1):
        start = df.iloc[i]
        end = df.iloc[i + 1]

        if i == 0:
            color = 'green'
        elif i == len(df) - 2:
            color = 'red'
        else:
            color = 'blue'

        start_info = {
            'name': start['name'],
            'lat': start['lat'],
            'lng': start['lng']
        }
        end_info = {
            'name': end['name'],
            'lat': end['lat'],
            'lng': end['lng']
        }

        routes = tmap.get_route_raw(start_info, end_info)
        route_data = tmap.get_route(routes)
        segment = route_data[mode]

        # 각 구간의 이동거리와 소요시간 누적
        total_distance += segment['distance']
        total_time += segment['time']

        # 경로 좌표 리스트 처리(Folium 좌표 순서: [위도, 경도])
        coordinates = [(pt[1], pt[0]) for pt in segment['path']]
        folium.PolyLine(locations=coordinates, color=color, weight=3.5, opacity=0.9).add_to(m)

        # 각 구간의 중간에 구간 정보(거리/시간) 마커 추가
        midpoint_idx = len(coordinates) // 2
        midpoint = coordinates[midpoint_idx]
        folium.Marker(
            location=midpoint,
            icon=folium.DivIcon(html=f"""
                <div style='font-size: 11px; color: black; background: white;
                    padding: 4px 8px; border-radius: 5px; border: 1px solid #888;
                    white-space: nowrap; text-align: center;
                    display: inline-block; min-width: 80px;'>
                    {segment['distance']} km / {segment['time']} min
                </div>""")
        ).add_to(m)

    return m, total_distance, total_time

# 탭 생성
tab1, tab2, tab3 = st.tabs(["Analysis Proccess(EN)", "Analysis Proccess(KR)", "Data Prep&EDA"])

with tab1:
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>Overview: Travel Course Proposal for Long-Stay Shipping Lines at Busan Port</span><br>
    An analysis of the top 10 shipping lines with the longest average port stays at Busan Port revealed that these companies tend to remain in port for extended periods. As a result, they are likely to be more sensitive to service satisfaction and crew welfare benefits. Therefore, to foster loyalty among these long-stay shipping lines, Busan Port Authority should consider offering <span style='font-weight:bold; font-size:20px;color:orange;'>customized benefits and targeted information</span>.<br>
    Based on this, the port aims to <span style='font-weight:bold; font-size:20px;'>enhance the stay experience</span> for crew members by providing structured information on <span style='color:orange; font-weight:bold; font-size:20px;'>major attractions</span> near the port, as well as <span style='color:orange; font-weight:bold; font-size:20px;'>restaurants and accommodations with Google ratings of 4.0 or higher</span>.
    To achieve this, shipping lines will be categorized into <span style='font-weight:bold; font-size:20px;'>three quantile-based groups</span> based on their average port stay durations, and <span style='font-weight:bold; font-size:20px;color:orange;'>tailored travel itineraries</span> will be proposed for each group according to their available time.
    """, unsafe_allow_html=True)

    st.dataframe(shipsDuration_10['Total duration(Hours)'].describe())

    st.markdown("""
    An analysis of quantiles for the top 10 shipping lines' port stay durations at Busan Port shows a distribution ranging from <span style='font-weight:bold; font-size:20px;'>a minimum of 24 hours to a maximum of 58 hours</span>, with relatively small gaps between quantile values. As a result, instead of dividing groups purely based on time brackets, it was deemed more effective to use <span style='color:orange; font-weight:bold; font-size:20px;'>practical criteria that reflect the purpose and behavioral patterns</span> of the shipping lines.<br>
    In particular, the <span style='font-weight:bold; font-size:20px;'>gap between the 1st quantile (42 hours) and the 3rd quantile (45 hours)</span> is minimal. Therefore, the <span style='color:orange; font-weight:bold; font-size:20px;'>mid-stay group</span> was defined to target shipping lines with relatively short stays but some available leisure time, while the <span style='color:orange; font-weight:bold; font-size:20px;'>short-stay and long-stay groups</span> were clearly differentiated based on distinct time characteristics and usage patterns.
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("""
        <span style='font-weight:bold; font-size:20px;'>1. Short Stay Group</span><br>
        Time Range: <span style='font-weight:bold; font-size:20px;'>24 to 42 hours</span><br>
        Characteristics: Mainly focused on port-related tasks with limited time for outside activities.<br>
        Recommendation: Suggest brief itineraries centered on <span style='color:orange; font-weight:bold; font-size:20px;'>nearby attractions</span> around the <span style='color:orange; font-weight:bold; font-size:20px;'>port</span> and focused on <span style='color:orange; font-weight:bold; font-size:20px;'>meals</span>.<br><br>

        <span style='font-weight:bold; font-size:20px;'>2. Mid Stay Group</span><br>
        Time Range: <span style='font-weight:bold; font-size:20px;'>43 to 44 hours</span><br>
        Characteristics: Relatively short stays but allow for small excursions or light sightseeing.<br>
        Recommendation: Propose courses featuring <span style='color:orange; font-weight:bold; font-size:20px;'>meals</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>simple attractions</span>, and <span style='color:orange; font-weight:bold; font-size:20px;'>relaxing spaces</span> such as cafes or observatories.<br><br>

        <span style='font-weight:bold; font-size:20px;'>3. Long Stay Group</span><br>
        Time Range: <span style='font-weight:bold; font-size:20px;'>45 hours or more</span><br>
        Characteristics: Suitable for overnight stays and offers the opportunity for substantial outdoor activities and rest.<br>
        Recommendation: Recommend <span style='color:orange; font-weight:bold; font-size:20px;'>sightseeing tours</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>local cuisine</span>, and <span style='color:orange; font-weight:bold; font-size:20px;'>accommodation</span> as part of a <span style='font-weight:bold;'>2-day itinerary</span>.
        """, unsafe_allow_html=True)

    stay_time = st.number_input("Enter your stay time (in hours)", min_value=0)

    if stay_time >= 24 and stay_time <= 42:
        group = "short"
        comment = "You seem to have limited time. We recommend a short itinerary focusing on nearby attractions and dining."
    elif stay_time >= 43 and stay_time <= 44:
        group = "mid"
        comment = "You have moderate time. We recommend an itinerary including dining, simple attractions, and a relaxing spot such as an observatory or park."
    elif stay_time >= 45:
        group = "long"
        comment = "You have plenty of time. We recommend a 1-night, 2-day itinerary including attractions, dining, and accommodation."
    else:
        group = None

    if group:
        st.markdown(f"### {comment}")

        # Generate tour course and store in session_state
        if st.button("Generate Tour Course"):
            st.session_state.tourCourse = get_stay_group_course(busanSpots, group)

        # Display generated tour course DataFrame
        if "tourCourse" in st.session_state:
            tour_df = st.session_state.tourCourse
            st.dataframe(tour_df)

            # Mode of travel selection using radio button
            transport_mode = st.radio("Select your mode of travel", options=["Car", "Pedestrian"])
            mode = "car" if transport_mode == "Car" else "peds"

            # Button to display the travel route map along with total distance and time
            if st.button("View Travel Route Map"):
                route_map, total_distance, total_time = draw_route_from_tourCourse(tour_df, tmap, mode=mode)
                st.markdown(f"### Total Distance: **{total_distance} km**, Total Time: **{total_time} min**")
                st.components.v1.html(route_map._repr_html_(), height=600)
        else:
            st.warning("Please click the 'Generate Tour Course' button first to create a tour course.")
    else:
        st.warning("Recommended course is only available if the stay time is 24 hours or more.")

with tab2:
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>부산항 장기체류 선사 여행코스 제안 개요</span><br>
    부산항에 입항하는 화물선 중 <span style='font-weight:bold; font-size:20px;'>체류 시간이 긴 상위 10개 선사</span>를 분석한 결과, 이들 선사들은 항만 내에서 머무는 시간이 상대적으로 길기 때문에, <span style='font-weight:bold; font-size:20px;'>서비스 만족도와 복지 혜택에 민감</span>할 가능성이 높습니다.
    따라서 부산항만공사에서는 이들 선사들을 <span style='font-weight:bold; font-size:20px;'>충성 고객</span>으로 관리하기 위해, <span style='color:orange; font-weight:bold; font-size:20px;'>차별화된 혜택과 맞춤형 정보</span>를 제공할 필요가 있습니다.<br>
    위와 같은 이유로, 부산항에 장기 체류하는 선사 직원들의 <span style='font-weight:bold; font-size:20px;'>체류 경험을 향상</span>시키기 위해, <span style='color:orange; font-weight:bold; font-size:20px;'>부산항 인근의 주요 관광지</span>와 <span style='color:orange; font-weight:bold; font-size:20px;'>Google 평점 4.0 이상</span>의 식당 및 숙박업소 정보를 체계적으로 제공합니다.
    이를 위해, 선사들의 평균 체류 시간을 기준으로 <span style='font-weight:bold; font-size:20px;'>3개의 분위수 그룹</span>으로 나누고, <span style='font-weight:bold; font-size:20px;color:orange;'>각 그룹별 체류 시간에 적합한 맞춤형 여행 코스</span>를 구성할 계획입니다.
    """, unsafe_allow_html=True)

    # 장기체류 선사들의 체류시간 분위수 분석
    st.dataframe(shipsDuration_10['Total duration(Hours)'].describe())
    st.markdown("""
    체류 시간 분위수 분석 결과, 상위 10개 선사의 체류 시간은 <span style='font-weight:bold;font-size:20px;'>최소 24시간에서 최대 58시간</span> 사이로 분포하고 있으며, 분위수 간의 격차가 크지 않은 것으로 나타났습니다. 따라서 단순한 시간 기준으로 그룹을 나누기보다는, <span style='color:orange; font-weight:bold;font-size:20px;'>선사의 체류 목적과 행동 패턴</span>을 고려한 실용적인 기준에 따라 그룹을 구분하는 것이 더 효과적인 접근으로 판단됩니다.<br>
    특히, <span style='font-weight:bold;font-size:20px;'>1분위(42시간)와 3분위(45시간)</span> 사이의 간격이 매우 좁기 때문에, <span style='color:orange; font-weight:bold;font-size:20px;'>중간 체류 그룹</span>은 상대적으로 체류 시간은 짧지만 일정 여유가 있는 선사들을 위한 타겟팅 기준으로 설정하였고, <span style='color:orange; font-weight:bold;font-size:20px;'>단기 및 장기 체류 그룹</span>은 보다 명확한 시간 특성과 이용 행태를 기반으로 구분하였습니다.
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("""
        <span style='font-weight:bold; font-size:20px;'>1. 단기 체류 그룹 (Short Stay)</span><br>
        시간 기준: <span style='font-weight:bold; font-size:20px;'>24시간 이상 ~ 42시간 이하</span><br>
        특징: 항만 업무 중심의 체류가 주를 이루며, 외부 활동 여유가 적은 그룹입니다.<br>
        추천 방향: <span style='color:orange; font-weight:bold; font-size:20px;'>항만 인근</span>의 <span style='color:orange; font-weight:bold; font-size:20px;'>근거리 관광지</span> 방문 및 <span style='color:orange; font-weight:bold; font-size:20px;'>식사 위주</span>의 짧은 일정 추천<br><br>

        <span style='font-weight:bold; font-size:20px;'>2. 중기 체류 그룹 (Mid Stay)</span><br>
        시간 기준: <span style='font-weight:bold; font-size:20px;'>43시간 ~ 44시간</span><br>
        특징: 비교적 짧지만 소규모 외출이나 관광이 가능한 여유가 있는 체류입니다.<br>
        추천 방향: <span style='color:orange; font-weight:bold; font-size:20px;'>식사</span>와 <span style='color:orange; font-weight:bold; font-size:20px;'>간단한 관광지</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>휴식 공간</span>(카페, 전망대 등) 중심의 코스 제안<br><br>

        <span style='font-weight:bold; font-size:20px;'>3. 장기 체류 그룹 (Long Stay)</span><br>
        시간 기준: <span style='font-weight:bold; font-size:20px;'>45시간 이상</span><br>
        특징: 1박 이상의 일정이 가능하며, 본격적인 외부 활동 및 휴식을 고려할 수 있는 체류입니다.<br>
        추천 방향: <span style='color:orange; font-weight:bold; font-size:20px;'>관광지 탐방</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>지역 식사</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>숙박</span>이 포함된 <span style='font-weight:bold;'>1박 2일형 일정</span> 제안
        """, unsafe_allow_html=True)
    # 체류 시간 입력
    stay_time = st.number_input("체류 시간을 입력하세요 (단위: 시간)", min_value=0)

    if stay_time >= 24 and stay_time <= 42:
        group = "short"
        comment = "활동 여유가 많지는 않으시군요! 인근 관광지 방문 및 식사 위주의 짧은 일정을 추천드려요!"
    elif stay_time >= 43 and stay_time <= 44:
        group = "mid"
        comment = "어느 정도 여유가 있으시군요! 식사와 간단한 관광지, 그리고 전망대/공원 같은 휴식 공간 중심의 일정을 추천드려요!"
    elif stay_time >= 45:
        group = "long"
        comment = "오래 머무시는군요! 관광지, 식사, 숙박이 포함된 1박 2일의 일정을 제안드려요!"
    else:
        group = None

    if group:

        st.markdown(f"### {comment}")
        # 투어 코스를 생성하고 session_state에 저장
        if st.button("여행 코스 생성하기"):
            st.session_state.tourCourse = get_stay_group_course(busanSpots, group)

        # 생성된 투어 코스가 session_state에 저장돼 있으면 데이터프레임으로 출력
        if "tourCourse" in st.session_state:
            tour_df = st.session_state.tourCourse
            st.dataframe(tour_df)

            # 이동 수단 선택 (st.radio를 활용한 옵션 선택)
            transport_mode = st.radio("이동 수단을 선택하세요", options=["차량", "보행자"])
            mode = "car" if transport_mode == "차량" else "peds"

            # 지도 출력 버튼: 선택된 이동 수단(mode)에 따라 경로 및 소요시간 정보 반영
            if st.button("여행 경로 지도 보기"):
                # draw_route_from_tourCourse 함수 내부에서는 지정된 mode에 따라 T맵 API를
                # 호출하여 차량 경로 또는 보행자 경로 데이터를 가져옵니다.
                route_map, total_distance, total_time = draw_route_from_tourCourse(tour_df, tmap, mode=mode)
                st.markdown(f"### 총 이동거리: **{total_distance} km**, 총 이동시간: **{total_time} 분**")
                st.components.v1.html(route_map._repr_html_(), height=600)
        else:
            st.warning("먼저 '여행 코스 생성하기' 버튼을 눌러 코스를 생성해주세요.")
    else:
        st.warning("체류 시간이 24시간 이상일 때만 추천 코스를 제공해 드립니다.")

with tab3:
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Preprocessing (데이터 가공)</span>", unsafe_allow_html=True)
    def jupyter_reader(path:str):
        # 노트북 파일 열기
        with open(path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # 코드 셀만 추출
        code_cells = [cell['source'] for cell in notebook.cells if cell['cell_type'] == 'code']
        code_content = '\n\n'.join(code_cells)
        return code_content
    codeSpots = jupyter_reader('./sourceCode/tourCourse.ipynb')
    st.code(codeSpots)
    st.code('''
        # Author: DongWhee Kim
        # Date: 2025-04-14
        # Description: Quartile-Based Visualization of Vessel Dwell Time by Shipping Company (선사별 체류시간의 사분위 기반 시각화 작업)
        # Import necessary libraries (필요한 라이브러리 임포트)
        import pandas as pd  # DataFrame handling (데이터프레임 처리)
        import plotly.express as px  # Interactive visualizations (인터랙티브 시각화)

        # Load raw ship schedule data and remove index column (데이터 로드 및 인덱스 제거)
        schedule = pd.read_csv("../useData/SinhangSchedule_rawData.csv", encoding="utf-8-sig")
        schedule = schedule.iloc[:,1:]
        schedule.head(5)

        # Check data types and structure (데이터 타입 및 구조 확인)
        schedule.info()
        schedule.shape

        # Define and apply datetime conversion function (형변환 함수 정의 및 적용)
        def changeDateType(x):
            changeDate = pd.to_datetime(x)
            return changeDate

        # Convert string columns to datetime (문자열 날짜 → datetime 형식)
        schedule["Enter Time"] = changeDateType(schedule["Enter Time"])
        schedule["Out Time"] = changeDateType(schedule["Out Time"])
        schedule.info()

        # Calculate time difference (날짜 차이 계산)
        schedule["Day difference"] = schedule["Enter Time"] - schedule["Out Time"]
        schedule.head()

        # Split into days and hours (체류기간을 일과 시간으로 분리)
        Dd_list = list(schedule["Day difference"])
        Duration_days_list = list()
        Duration_hourss_list = list()

        for v in Dd_list:
            v = str(v)
            v_edit = v.replace(" ","").replace("days","").replace("-","").split("+")
            Duration_days_list.append(v_edit[0])
            Duration_hourss_list.append(v_edit[1])

        # Add duration columns to DataFrame (체류기간 열 추가)
        schedule["Duration days"] = Duration_days_list
        schedule["Duration hours"] = Duration_hourss_list

        # Calculate total stay duration in hours (총 체류시간 계산)
        calculate_hour_list = list()
        for v in schedule["Duration days"]:
            v = int(v)
            change_hour = v*24
            calculate_hour_list.append(change_hour)

        # Extract hours only from "Duration hours" (시간만 추출)
        hourToInt = [v.split(":")[0] for v in schedule["Duration hours"]]

        # Sum day-hours and hour-only to get total duration (총 시간 계산)
        sumHour_list = [int(i) + int(v) for i,v in zip(calculate_hour_list, hourToInt)]
        schedule["Total duration(Hours)"] = sumHour_list

        # Print dataset summary (데이터셋 요약 출력)
        print("==================================================")
        print(schedule.info())
        print("==================================================")
        schedule.head()

        # Create reduced DataFrame for analysis (분석용 컬럼만 선택)
        schedule_duration = schedule[["Ship Company", "Total duration(Hours)"]].copy()
        print(schedule_duration.info())

        # Calculate average stay by shipping company (선사별 평균 체류시간 계산)
        schedule_duration = schedule.groupby("Ship Company")["Total duration(Hours)"].mean()

        # Separate values into lists (리스트로 분리 저장)
        avg_shipName_list = list(schedule_duration.index)
        avgTime_list = list(schedule_duration.values)

        # Create summary DataFrame (요약 데이터프레임 생성)
        avgDuration_ships = pd.DataFrame({
            "Ship name": avg_shipName_list,
            "Avg time": avgTime_list
        })

        # Sort descending and reset index (내림차순 정렬 및 인덱스 초기화)
        avgDuration_ships = avgDuration_ships.sort_values(["Avg time"],ascending=False).reset_index().iloc[:,1:]
        avgDuration_ships

        # Select top 10 shipping companies by avg stay (평균 체류시간 상위 10개 선사)
        avgDuration_ships_top10 = avgDuration_ships.iloc[:9,:]
        avgDuration_ships_top10

        # Summary statistics (요약 통계 확인)
        schedule["Total duration(Hours)"].describe()

        # Draw box plot (박스 플롯 시각화)
        duration_fig = px.box(
            schedule,
            y="Total duration(Hours)",
            title="Residence Time by Shipping Company",
        )

        # Layout customization (레이아웃 설정)
        duration_fig.update_layout(
            title=dict(
                text="<b>Residence Time by Shipping Company</b>",
                x=0.5,
                xanchor='center',
                font=dict(color="white")
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
        duration_fig.show()

        # Remove anomalies over 59 hours (59시간 초과 이상치 제거)
        schedule_removeAnomaly = schedule[schedule["Total duration(Hours)"] <=59]
        schedule_removeAnomaly[["Ship Company","Enter Time", "Out Time", "Duration days", "Duration hours", "Total duration(Hours)"]].to_csv("../useData/finishPrepro/shipsDuration.csv")
        schedule_removeAnomaly.head()

        # Redraw box plot after anomaly removal (이상치 제거 후 시각화)
        duration_fig = px.box(
            schedule_removeAnomaly,
            y="Total duration(Hours)",
            title="Residence Time by Shipping Company",
        )

        duration_fig.update_layout(
            title=dict(
                text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
                x=0.5,
                xanchor='center',
                font=dict(color="white")
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
            marker_color="red",
            boxmean=True
        )
        duration_fig.show()

        # Extract top 10 ship names (상위 10개 선사 추출)
        top10_ship = [v for v in avgDuration_ships_top10["Ship name"]]

        index_list = list()
        for i, v in enumerate(schedule["Ship Company"]):
            if v in top10_ship:
                index_list.append(i)
        print(index_list)

        # Extract data for top 10 ships (상위 10개 선사 데이터 추출)
        schedule_10 = schedule.iloc[index_list].reset_index().iloc[:,1:]
        schedule_10

        # Draw filtered box plot (선택 선사만 시각화)
        duration_fig = px.box(
            schedule_10,
            x="Ship Company",
            y="Total duration(Hours)",
            title="Residence Time by Shipping Company",
        )

        duration_fig.update_layout(
            title=dict(
                text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
                x=0.5,
                xanchor='center',
                font=dict(color="white")
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
            marker_color="red",
            boxmean=True
        )
        duration_fig.show()

        # Check anomaly ship (이상치 포함 선사 확인)
        schedule_10[schedule_10["Ship Company"]=="AEW"]

        # Remove anomaly ship "AEW" and recreate top 10 (AEW 제거 후 top10 재구성)
        avgDuration_ships_top10 = avgDuration_ships.iloc[:11,:]
        avgDuration_ships_top10 = avgDuration_ships_top10[avgDuration_ships_top10["Ship name"]!="AEW"]
        avgDuration_ships_top10

        new_avgDuration_ships = avgDuration_ships.iloc[:11,:]
        new_avgDuration_ships = new_avgDuration_ships[new_avgDuration_ships["Ship name"]!="AEW"]

        # Re-filter with updated top 10 list (재필터링)
        new_top10_ship = [v for v in new_avgDuration_ships["Ship name"]]
        index_list = list()
        for i, v in enumerate(schedule["Ship Company"]):
            if v in new_top10_ship:
                index_list.append(i)

        new_schedule_10 = schedule.iloc[index_list].reset_index().iloc[:,1:]
        new_schedule_10

        # Final plot for top 10 excluding AEW (AEW 제외 최종 상위 선사 박스플롯)
        duration_fig = px.box(
            new_schedule_10,
            x="Ship Company",
            y="Total duration(Hours)",
            title="Residence Time by Shipping Company",
        )

        duration_fig.update_layout(
            title=dict(
                text="<b>Residence Time by Shipping Company<br>(Remove outliers)</b>",
                x=0.5,
                xanchor='center',
                font=dict(color="white")
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
            marker_color="red",
            boxmean=True
        )
        duration_fig.show()
        ''')