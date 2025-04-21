import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from tmapAPI.tmapAPI import *
import nbformat
from analyzer.dwellTimeAnalyzer import *

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
    Draws route segments on a folium map from tour course DataFrame and calculates total distance and total time.
    
    Parameters:
        df (DataFrame): Tour spots DataFrame with columns such as 'lat', 'lng', 'name', etc.
        tmap: Tmap API instance.
        mode (str): "car" for driving mode or "peds" for pedestrian mode.
    
    Returns:
        tuple: (folium Map object, total_distance (km), total_time (min))
    """
    # 지도 중심을 생성할 좌표: DataFrame에 있는 모든 'lat'와 'lng'의 중앙값(중위수)를 사용
    center_lat = df['lat'].median()
    center_lng = df['lng'].median()
    map_center = [center_lat, center_lng]
    m = folium.Map(location=map_center, zoom_start=15)

    # Total distance and time accumulate
    total_distance = 0  # in km
    total_time = 0      # in minutes

    # Add markers for each tour spot
    for idx, row in df.iterrows():
        if idx == 0:
            color = 'green'
        elif idx == len(df) - 1:
            color = 'red'
        else:
            color = 'blue'

        popup_html = f"""
        <b>{idx+1}. {row['name']}</b><br>
        Rating: {row['rating']}<br>
        Category (KR): {row['category2']}<br>
        Category (EN): {row['category2_en']}<br>
        Address: {row['address']}
        """
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=popup_html,
            icon=folium.Icon(color=color)
        ).add_to(m)

    # Draw route segments between consecutive spots and accumulate distance/time
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

        total_distance += segment['distance']
        total_time += segment['time']

        # Convert coordinates for folium (latitude, longitude)
        coordinates = [(pt[1], pt[0]) for pt in segment['path']]
        folium.PolyLine(locations=coordinates, color=color, weight=3.5, opacity=0.9).add_to(m)

        # Place segment info (distance/time) at the midpoint
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
                </div>
                """)
        ).add_to(m)

    return m, total_distance, total_time

# 탭 생성
tab1, tab2, tab3 = st.tabs(["Analysis Proccess(EN)", "Analysis Proccess(KR)", "Data Preprocessing"])

with tab1:
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>Overview of Suggested Travel Courses for Long-Stay Shipping Lines at Busan Port</span><br>
    On the (7) Dwell Time Analysis page, we analyzed the stay durations of incoming cargo ships. Based on this, we aim to provide <span style='font-weight:bold; font-size:20px;'>time-based customized information</span> to help <span style='font-weight:bold; font-size:20px;'>shipping companies and their crew members</span> make more <span style='font-weight:bold; font-size:20px;'>efficient use of their time</span> during their stay in Busan. This serves as a strategic approach by Busan Port Authority to <span style='font-weight:bold; font-size:20px;color:orange;'>enhance satisfaction and offer welfare benefits to foreign shipping companies, its key clientele</span>. To achieve this, we collected data on nearby restaurants, accommodations, and major tourist spots with Google ratings of 4.0 or higher. Then, we <span style='font-weight:bold; font-size:20px; color:orange;'>categorized the stays into three groups and created optimized travel courses</span> for each group as shown below.<br>
    """, unsafe_allow_html=True)

    dataArea_en, plotArea_en = st.columns(2)
    with st.container():
        with dataArea_en:
            with st.container():
                # Dwell time quantile analysis for long-staying shipping companies
                st.dataframe(shipsDuration_10['Total duration(Hours)'].describe(), row_height=52, height=450)
        with plotArea_en:
            with st.container():
                dwellTA = dwellTimeAnalyzer(shipsDuration_10, 'Total duration(Hours)', 'Ship Company', marker_color='red')
                boxPlot = dwellTA.draw_boxplot('Residence Time by Shipping Company')
                st.plotly_chart(boxPlot, use_container_width=True)

    st.markdown("""
    From the quantile analysis of stay durations, the top 10 shipping companies stay between <span style='font-weight:bold;font-size:20px;'>a minimum of 24 hours and a maximum of 58 hours</span>. The <span style='font-weight:bold; font-size:20px;'>gap between quantiles is relatively small</span>, which suggests that a grouping approach based solely on duration may be insufficient. Instead, we propose to categorize them based on <span style='color:orange; font-weight:bold;font-size:20px;'>the purpose and behavior patterns</span> of the shipping companies during their stay.<br>
    In particular, the gap between the <span style='font-weight:bold;font-size:20px;'>1st quartile (42 hours) and 3rd quartile (45 hours)</span> is quite narrow. Thus, the <span style='color:orange; font-weight:bold;font-size:20px;'>mid-stay group</span> targets companies with shorter stays but some spare time, while <span style='color:orange; font-weight:bold;font-size:20px;'>short and long stay groups</span> are more clearly differentiated based on time characteristics and usage patterns.
    """, unsafe_allow_html=True)

    with st.container():
        short_col_en, mid_col_en, long_col_en = st.columns(3)
        with short_col_en:
            st.markdown("""
            <span style='font-weight:bold; font-size:20px;'>Short Stay Group</span><br>
            Time Range: <span style='font-weight:bold; font-size:20px;'>24 to 42 hours</span> (0% ~ 25%)<br>
            Characteristics: Mainly focused on port-related tasks, with limited time for outside activities.<br>
            Recommendation: <span style='color:orange; font-weight:bold; font-size:20px;'>Short itineraries</span> focusing on <span style='color:orange; font-weight:bold; font-size:20px;'>nearby attractions</span> and <span style='color:orange; font-weight:bold; font-size:20px;'>meals</span><br><br>
            """, unsafe_allow_html=True)
        with mid_col_en:
            st.markdown("""
            <span style='font-weight:bold; font-size:20px;'>Mid Stay Group</span><br>
            Time Range: <span style='font-weight:bold; font-size:20px;'>43 to 44 hours</span> (25% ~ 50%)<br>
            Characteristics: Relatively short stays with time for light outings or local sightseeing.<br>
            Recommendation: Travel courses including <span style='color:orange; font-weight:bold; font-size:20px;'>meals</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>simple tourist spots</span>, and <span style='color:orange; font-weight:bold; font-size:20px;'>resting places</span> (e.g., cafes, observatories)<br><br>
            """, unsafe_allow_html=True)
        with long_col_en:
            st.markdown("""
            <span style='font-weight:bold; font-size:20px;'>Long Stay Group</span> (50% and above)<br>
            Time Range: <span style='font-weight:bold; font-size:20px;'>45 hours or more</span><br>
            Characteristics: Suitable for overnight stays with time for full outdoor activities and relaxation.<br>
            Recommendation: <span style='color:orange; font-weight:bold; font-size:20px;'>1-night, 2-day itineraries</span> including <span style='color:orange; font-weight:bold; font-size:20px;'>tourist attractions</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>local meals</span>, and <span style='color:orange; font-weight:bold; font-size:20px;'>accommodations</span>
            """, unsafe_allow_html=True)


    # ------------- Row 1: Enter Stay Duration | Select Transportation Mode -------------
    col_input_en, col_transport_en = st.columns(2)
    with col_input_en:
        stay_time = st.number_input("Enter your stay duration (in hours)", min_value=0)
    with col_transport_en:
        transport_mode = st.selectbox("Select your mode of transport", options=["Choose an option", "Car", "Walking"])

    # ------------- Row 2: Determine Group & Display Comment -------------
    if stay_time < 24:
        group = None
        st.warning("Travel recommendations are available only for stays of 24 hours or more.")
        st.stop()
    else:
        if 24 <= stay_time <= 42:
            group = "short"
            comment = f"Your stay duration is {stay_time} hours. You belong to the Short Stay Group."
        elif 43 <= stay_time <= 44:
            group = "mid"
            comment = f"Your stay duration is {stay_time} hours. You belong to the Mid Stay Group."
        elif stay_time >= 45:
            group = "long"
            comment = f"Your stay duration is {stay_time} hours. You belong to the Long Stay Group."

    # ------------- Row 3: Left Column - Course Generation & DataFrame / Right Column - Map Output -------------
    if group is not None:
        left_col_en, right_col_en = st.columns(2)
        
        with left_col_en:
            st.subheader(f":rainbow[{comment}]", anchor=False)
            if transport_mode == "Choose an option":
                st.info("Please select a mode of transport first.")
            else:
                if st.button("Generate Travel Course"):
                    tourCourse = get_stay_group_course(busanSpots, group).fillna('-')
                    st.session_state.tourCourse = tourCourse
                    mode = "car" if transport_mode == "Car" else "peds"
                    st.session_state.mode = mode
                    st.session_state.route_map, st.session_state.total_distance, st.session_state.total_time = \
                        draw_route_from_tourCourse(tourCourse, tmap, mode=mode)
                    st.session_state.map_generated = True

            if "tourCourse" in st.session_state:
                tour_df = st.session_state.tourCourse.rename(columns={
                    'name': 'Place',
                    'rating': 'Rating',
                    'category1': 'Category',
                    'category2_en': 'Subcategory',
                    'address': 'Address'
                })
                st.dataframe(tour_df[['Place', 'Rating', 'Category', 'Subcategory', 'Address']], hide_index=True)

        with right_col_en:
            if "map_generated" in st.session_state and st.session_state.map_generated:
                st.subheader(f":rainbow[Distance: {round(st.session_state.total_distance, 1)} km / Duration: {st.session_state.total_time} minutes]", anchor=False)
                st.components.v1.html(st.session_state.route_map._repr_html_(), height=600)

with tab2:
    st.markdown("""
    <span style='font-weight:bold; font-size:20px;'>부산항 장기체류 선사 여행코스 제안 개요</span><br>
    (7)Dwell Time Analysis 페이지에서 우리는 입항 카고선들에 대한 체류 시간을 분석했고, <span style='font-weight:bold; font-size:20px;'>선사 및 선원들</span>이 부산에 입항했을 때 <span style='font-weight:bold; font-size:20px;'>체류하는 시간을 보다 효율적으로 사용</span>할 수 있도록 주어진 <span style='font-weight:bold; font-size:20px;color:orange;'>시간별 맞춤형 정보를 제공</span>하고자 아래와 같이 데이터를 가공/시각화 했습니다. 이는 부산항만공사가 <span style='font-weight:bold; font-size:20px;color:orange;'>주고객인 외국 선사들에게 높은 만족도와 복지혜택을 줄 수 있는 수단으로 작용할 것</span>입니다. 이를 위해 우리는 부산항 인근의 Google 평점 4.0 이상의 식당, 숙박업소, 주요 관광지 정보를 크롤링하여 아래와 같이 
    <span style='font-weight:bold; font-size:20px; color:orange;'>선사들의 체류 시간을 세 그룹으로 나누어 적합한 맞춤형 여행 코스를 체계적으로 구성</span>하여 제공했습니다.<br>
    """, unsafe_allow_html=True)

    dataArea_kr, plotArea_kr = st.columns(2)
    with st.container():
        with dataArea_kr:
            with st.container():
                # 장기체류 선사들의 체류시간 분위수 분석
                st.dataframe(shipsDuration_10['Total duration(Hours)'].describe(), row_height=52, height=450)
        with plotArea_kr:
            with st.container():
                dwellTA = dwellTimeAnalyzer(shipsDuration_10, 'Total duration(Hours)', 'Ship Company', marker_color='red')
                boxPlot = dwellTA.draw_boxplot('Residence Time by Shipping Company')
                st.plotly_chart(boxPlot, use_container_width=True, key='boxplot')


    st.markdown("""
    체류 시간 분위수 분석 결과, 상위 10개 선사의 체류 시간은 <span style='font-weight:bold;font-size:20px;'>최소 24시간에서 최대 58시간</span> 사이로 분포하고 있으며, <span style='font-weight:bold; font-size:20px;'>분위수 간의 격차가 크지 않은 것으로 나타났습니다.</span> 따라서 단순한 시간 기준으로 그룹을 나누기보다는, <span style='color:orange; font-weight:bold;font-size:20px;'>선사의 체류 목적과 행동 패턴</span>을 고려한 실용적인 기준에 따라 그룹을 구분하는 것이 더 효과적인 접근으로 판단됩니다.<br>
    특히, <span style='font-weight:bold;font-size:20px;'>1분위(42시간)와 3분위(45시간)</span> 사이의 간격이 매우 좁기 때문에, <span style='color:orange; font-weight:bold;font-size:20px;'>중간 체류 그룹</span>은 상대적으로 체류 시간은 짧지만 일정 여유가 있는 선사들을 위한 타겟팅 기준으로 설정하였고, <span style='color:orange; font-weight:bold;font-size:20px;'>단기 및 장기 체류 그룹</span>은 보다 명확한 시간 특성과 이용 행태를 기반으로 구분하였습니다.
    """, unsafe_allow_html=True)

    with st.container():
        short_col_kr, mid_col_kr, long_col_kr = st.columns(3)
        with short_col_kr:
            st.markdown("""
            <span style='font-weight:bold; font-size:20px;'>단기 체류 그룹 (Short Stay)</span><br>
            시간 기준: <span style='font-weight:bold; font-size:20px;'>24시간 이상 ~ 42시간 이하</span> (0% ~ 25%)<br>
            특징: 항만 업무 중심의 체류가 주를 이루며, 외부 활동 여유가 적은 그룹입니다.<br>
            추천 방향: <span style='color:orange; font-weight:bold; font-size:20px;'>항만 인근</span>의 <span style='color:orange; font-weight:bold; font-size:20px;'>근거리 관광지</span> 방문 및 <span style='color:orange; font-weight:bold; font-size:20px;'>식사 위주</span>의 짧은 일정 추천<br><br>
            """, unsafe_allow_html=True)
        with mid_col_kr:
            st.markdown("""
            <span style='font-weight:bold; font-size:20px;'>중기 체류 그룹 (Mid Stay)</span><br>
            시간 기준: <span style='font-weight:bold; font-size:20px;'>43시간 ~ 44시간</span> (25% ~ 50%)<br>
            특징: 비교적 짧지만 소규모 외출이나 관광이 가능한 여유가 있는 체류입니다.<br>
            추천 방향: <span style='color:orange; font-weight:bold; font-size:20px;'>식사</span>와 <span style='color:orange; font-weight:bold; font-size:20px;'>간단한 관광지</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>휴식 공간</span>(카페, 전망대 등) 중심의 코스 제안<br><br>
            """, unsafe_allow_html=True)
        with long_col_kr:
            st.markdown("""
            <span style='font-weight:bold; font-size:20px;'>장기 체류 그룹 (Long Stay)</span> (50% ~ )<br>
            시간 기준: <span style='font-weight:bold; font-size:20px;'>45시간 이상</span><br>
            특징: 1박 이상의 일정이 가능하며, 본격적인 외부 활동 및 휴식을 고려할 수 있는 체류입니다.<br>
            추천 방향: <span style='color:orange; font-weight:bold; font-size:20px;'>관광지 탐방</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>지역 식사</span>, <span style='color:orange; font-weight:bold; font-size:20px;'>숙박</span>이 포함된 <span style='font-weight:bold;'>1박 2일형 일정</span> 제안
            """, unsafe_allow_html=True)


    # ------------- Row 1: 체류 시간 입력 | 이동 수단 선택 -------------
    col_input_kr, col_transport_kr = st.columns(2)
    with col_input_kr:
        stay_time = st.number_input("체류 시간을 입력하세요 (단위: 시간)", min_value=0)
    with col_transport_kr:
        transport_mode = st.selectbox("이동 수단을 선택하세요", options=["선택하세요", "차량", "보행자"])

    # ------------- Row 2: 그룹 결정 및 코멘트 출력 -------------
    if stay_time < 24:
        group = None
        st.warning("체류 시간이 24시간 이상일 때만 추천 코스를 제공해 드립니다.")
        st.stop()  # 체류 시간이 부족하면 이후 코드를 실행하지 않음
    else:
        if 24 <= stay_time <= 42:
            group = "short"
            comment = f"당신의 체류 시간은 {stay_time}시간입니다. 단기 체류 그룹에 속합니다."
        elif 43 <= stay_time <= 44:
            group = "mid"
            comment = f"당신의 체류 시간은 {stay_time}시간입니다. 중기 체류 그룹에 속합니다."
        elif stay_time >= 45:
            group = "long"
            comment = f"당신의 체류 시간은 {stay_time}시간입니다. 장기 체류 그룹에 속합니다."

    # ------------- Row 3: 왼쪽 컬럼 - 코스 생성 버튼 및 데이터프레임 / 오른쪽 컬럼 - 지도 출력 -------------
    if group is not None:
        left_col_kr, right_col_kr = st.columns(2)
        
        # 왼쪽 컬럼: 코멘트는 위쪽에 이미 출력되었으므로 코스 생성 버튼과 투어 코스 데이터프레임 출력
        with left_col_kr:
            st.subheader(f":rainbow[{comment}]", anchor=False)
            if transport_mode == "선택하세요":
                st.info("먼저 이동 수단을 선택해 주세요.")
            else:
                if st.button("여행 코스 생성하기"):
                    # 투어 코스 생성 및 세션에 저장
                    tourCourse = get_stay_group_course(busanSpots, group).fillna('-')
                    st.session_state.tourCourse = tourCourse
                    mode = "car" if transport_mode == "차량" else "peds"
                    st.session_state.mode = mode
                    st.session_state.route_map, st.session_state.total_distance, st.session_state.total_time = \
                        draw_route_from_tourCourse(tourCourse, tmap, mode=mode)
                    st.session_state.map_generated = True

            if "tourCourse" in st.session_state:
                tour_df = st.session_state.tourCourse.rename(columns={
                    'name': '장소',
                    'rating': '별점',
                    'category1': '대분류',
                    'category2': '중분류',
                    'address': '주소'
                })
                st.dataframe(tour_df[['장소', '별점', '대분류', '중분류', '주소']], hide_index=True)

        # 오른쪽 컬럼: 지도를 출력 (총 이동거리 및 시간 정보 포함)
        with right_col_kr:
            if "map_generated" in st.session_state and st.session_state.map_generated:
                st.subheader(f":rainbow[거리: {round(st.session_state.total_distance, 1)} km / 시간: {st.session_state.total_time} 분]", anchor=False)
                st.components.v1.html(st.session_state.route_map._repr_html_(), height=600)

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