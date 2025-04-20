import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.features import CustomIcon
from streamlit_folium import st_folium
import json

st.set_page_config(layout="wide")

st.title("Vacancy data analysis for ship supplies storage", anchor=False)

tab_1, tab_2, tab_3 = st.tabs(["Analysis Process(EN)", "Analysis Process(KR)", "Data Preprocessing"])

with tab_1:
    st.markdown("""
    Previously, we conducted an analysis covering <span style='color:orange; font-weight:bold; font-size:20px;'>correlation with potential customers, product selection based on annual ship supply demand, and the identification of companies dealing with those products</span> for building an online ship supply platform.
    In this section, we performed a <span style='color:white; font-weight:bold; font-size:20px;'>visual analysis of vacancy data</span>.
    But why did we collect and analyze vacancy data in the first place?
    We assumed that if an online ship supply platform is launched, it would be important for foreign crew members to be able to <span style='color:white; font-weight:bold; font-size:20px;'>pick up their ordered products near the port during embarkation or disembarkation</span>.
    This would help <span style='color:orange; font-weight:bold; font-size:20px;'>crew members plan their time more efficiently and make the most of their stay</span>.
    Based on this rationale, we collected and visualized vacancy data around <span style='color:orange; font-weight:bold; font-size:20px;'>the three major ports of Busan (New Port, North Port, and Gamcheon Port)</span>.
    <br><span style='color:red; font-weight:bold; font-size:15px;'>(* Due to confidentiality policies of real estate agencies, detailed vacancy addresses and building names were not publicly available. Therefore, we gathered, processed, and visualized data by searching areas near the three major port addresses.)</span>
    """, unsafe_allow_html=True)

    vacancyData = pd.read_csv("./useData/finishPrepro/vacancy_locationLaLo.csv", encoding="utf-8-sig")
    vacancyData["FloorType"] = ["지하" if "B" in v else "지상" for v in vacancyData["Floor"]]

   # 예시 전처리 함수
    def deleteFloor(x):
        x = x.replace(" Floor", "").replace("B","")
        return x

    vacancyData["Floor"] = vacancyData["Floor"].apply(deleteFloor)
    vacancyData["Floor"] = vacancyData["Floor"].astype("int64")

    # 열 정리
    renameColumns = ['FloorType', 'Address', 'Size', 'Floor', 'Month Price', 'Depossit Price', 'Latitude', 'Longitude']
    vacancyData = vacancyData[renameColumns]

    # 그룹별 정보 정리
    cntType = vacancyData.groupby(["Address", "FloorType"])["FloorType"].count()

    group_countType = pd.DataFrame({
        "Address": [v[0] for v in cntType.index],
        "FloorType": [v[1] for v in cntType.index],
        "Type": cntType.values
    })

    groupPriceMean = vacancyData.groupby("Address")[["Month Price", "Depossit Price"]].mean()
    groupPriceMeanResult = pd.DataFrame({
        "Address": groupPriceMean.index,
        "Month Price(AVG)": groupPriceMean["Month Price"].astype(int),
        "Depossit Price(AVG)": groupPriceMean["Depossit Price"].astype(int)
    }).reset_index(drop=True)

    groupSizeMean = vacancyData.groupby("Address")["Size"].mean()
    groupFloorMean = vacancyData.groupby("Address")["Floor"].mean()

    groupMerge = (
        groupPriceMeanResult
        .merge(groupFloorMean, on="Address")
        .merge(groupSizeMean, on="Address")
    )

    # 지도 생성
    targetArea = folium.Map(
        location=[35.125135443661655, 128.96211911293543],
        zoom_start=11,
        tiles="CartoDB positron"
    )

    # 부산 geojson 적용
    busanGeo = "./useData/koreaBusan.geojson"
    with open(busanGeo, encoding="utf-8-sig") as f:
        myGeo = json.load(f)

    def myGeo_style(x):
        return {
            "fillColor": "#dae080",
            "color": "",
            "weight": 0.5,
            "fillOpacity": 0.2
        }

    folium.GeoJson(data=myGeo, style_function=myGeo_style).add_to(targetArea)

    # 지도에 마커 추가
    for i, v in vacancyData.iterrows():
        lat = v["Latitude"]
        lon = v["Longitude"]
        address = v["Address"]

        if (address in groupMerge["Address"].values) and (address in group_countType["Address"].values):
            avg_floor = int(groupMerge[groupMerge["Address"] == address]["Floor"].values[0])
            avg_size = int(groupMerge[groupMerge["Address"] == address]["Size"].values[0])
            avg_month = groupMerge[groupMerge["Address"] == address]["Month Price(AVG)"].values[0]
            avg_deposit = groupMerge[groupMerge["Address"] == address]["Depossit Price(AVG)"].values[0]

            formatted_month = f"{avg_month:,}"
            formatted_deposit = f"{avg_deposit:,}"
            formatted_size = f"{avg_size:,}"

            floor_info_rows = group_countType[group_countType["Address"] == address]
            floor_type_strs = [f"{row['FloorType']} (count: {row['Type']})" for _, row in floor_info_rows.iterrows()]
            floor_type_combined = ", ".join(floor_type_strs)

            noticeInfo = (
                f"<div style='background-color:#f9f9f9; padding:10px; border-radius:8px; font-size:13px; line-height:1.6'>"
                f"<b>(1) Area Name</b>: {address}<br>"
                f"<b>(2) Vacancy Type</b>: {floor_type_combined}<br>"
                f"<b>(3) Average Floor</b>: {avg_floor}<br>"
                f"<b>(4) Average Size</b>: {formatted_size}㎡<br>"
                f"<b>(5) Average Monthly Price (KRW)</b>: {formatted_month}<br>"
                f"<b>(6) Average Monthly Deposit (KRW)</b>: {formatted_deposit}"
                f"</div>"
            )

            popup = folium.Popup(noticeInfo, max_width=400, min_width=30, max_height=300, show=True)

            myIcon = "./useData/myImage/vacancyMan.png"
            myIcon_edit = CustomIcon(
                icon_image=myIcon,
                icon_size=(31, 31),
                icon_anchor=(15, 15)
            )

            folium.Marker(
                location=[lat, lon],
                icon=myIcon_edit
            ).add_child(popup).add_to(targetArea)

        # 원형 마커는 모든 공실에 추가
        folium.CircleMarker(
            location=[lat, lon],
            radius=60,
            fill=True,
            fill_color="#e7ede3",
            color="#ee928c",
            fill_opacity=0.1
        ).add_to(targetArea)

    # ✅ 지도 출력은 for문 바깥에서 단 1번만 실행
    st_folium(targetArea, use_container_width=True, key="vacancy_en")

    st.subheader("Conclusion", anchor=False)

    st.markdown('''
    Through the above vacancy data visualization, we can <span style='color:orange; font-weight:bold; font-size:20px;'>secure optimal geographic logistics hubs near each port</span>,
    which can also serve as a valuable reference for <span style='color:orange; font-weight:bold; font-size:20px;'>budget estimation and allocation for the online ship supply platform</span>.
    ''', unsafe_allow_html=True)
    st.dataframe(groupMerge, hide_index=True)


with tab_2:
    st.markdown("""
    앞서 우리는 온라인 선용품 쇼핑몰 구축을 위한 <span style='color:orange; font-weight:bold; font-size:20px;'>잠재 고객을 위한 상관관계 분석, 연도별 선용품 수요 조사를 통한 품목 선정, 해당 품목을 취급하는 기업에 대한 분석</span>을 진행했습니다.
    이번 페이지에서는 <span style='color:white; font-weight:bold; font-size:20px;'>공실 데이터에 대한 시각화 분석</span>을 수행했습니다.
    그렇다면, 왜 공실 데이터를 수집하고 분석했을까요?
    온라인 선용품 쇼핑몰이 운영된다면, 외국 선원들이 <span style='color:white; font-weight:bold; font-size:20px;'>승선 또는 하선 시 항구 인근에서 제품을 직접 수령</span>할 수 있도록 하는 것이 중요하다고 판단했습니다.
    이는 <span style='color:orange; font-weight:bold; font-size:20px;'>선원들이 보다 효율적으로 시간 계획을 세우고, 체류 중 다양한 활동을 하는 데 도움</span>이 될 수 있습니다.
    이에 따라, 우리는 <span style='color:orange; font-weight:bold; font-size:20px;'>부산의 3대 항구(신항, 북항, 감천항)</span>를 중심으로 인근 지역의 공실 데이터를 수집하고, 아래와 같이 시각화하였습니다.
    <br><span style='color:red; font-weight:bold; font-size:15px;'>(데이터 출처에서 부동산 중개소의 영업관련 기밀로 공실관련 빌딩명, 공실 세부주소를 공개하지 않아, 3대 항구별 주소 입력 후 그 인근에 검색되는 데이터를 수집/가공/시각화 했습니다.)</span>
    """, unsafe_allow_html=True)

    vacancyData_2 = pd.read_csv("./useData/finishPrepro/vacancy_locationLaLo.csv", encoding="utf-8-sig")
    vacancyData_2["FloorType"] = ["지하" if "B" in v else "지상" for v in vacancyData_2["Floor"]]

   # 예시 전처리 함수
    def deleteFloor(x):
        x = x.replace(" Floor", "").replace("B","")
        return x

    vacancyData_2["Floor"] = vacancyData_2["Floor"].apply(deleteFloor)
    vacancyData_2["Floor"] = vacancyData_2["Floor"].astype("int64")

    # 열 정리
    renameColumns = ['FloorType', 'Address', 'Size', 'Floor', 'Month Price', 'Depossit Price', 'Latitude', 'Longitude']
    vacancyData_2 = vacancyData_2[renameColumns]

    # 그룹별 정보 정리
    cntType_2 = vacancyData_2.groupby(["Address", "FloorType"])["FloorType"].count()

    group_countType_2 = pd.DataFrame({
        "Address": [v[0] for v in cntType_2.index],
        "FloorType": [v[1] for v in cntType_2.index],
        "Type": cntType_2.values
    })

    groupPriceMean_2 = vacancyData_2.groupby("Address")[["Month Price", "Depossit Price"]].mean()
    groupPriceMeanResult_2 = pd.DataFrame({
        "Address": groupPriceMean_2.index,
        "Month Price(AVG)": groupPriceMean_2["Month Price"].astype(int),
        "Depossit Price(AVG)": groupPriceMean_2["Depossit Price"].astype(int)
    }).reset_index(drop=True)

    groupSizeMean_2 = vacancyData_2.groupby("Address")["Size"].mean()
    groupFloorMean_2 = vacancyData_2.groupby("Address")["Floor"].mean()

    groupMerge_2 = (
        groupPriceMeanResult
        .merge(groupFloorMean, on="Address")
        .merge(groupSizeMean, on="Address")
    )

    # 지도 생성
    targetArea_2 = folium.Map(
        location=[35.125135443661655, 128.96211911293543],
        zoom_start=11,
        tiles="CartoDB positron"
    )

    # 부산 geojson 적용
    busanGeo_2 = "./useData/koreaBusan.geojson"
    with open(busanGeo_2, encoding="utf-8-sig") as f:
        myGeo = json.load(f)

    def myGeo_style(x):
        return {
            "fillColor": "#dae080",
            "color": "",
            "weight": 0.5,
            "fillOpacity": 0.2
        }

    folium.GeoJson(data=myGeo, style_function=myGeo_style).add_to(targetArea_2)

    # 지도에 마커 추가
    for i, v in vacancyData.iterrows():
        lat = v["Latitude"]
        lon = v["Longitude"]
        address = v["Address"]

        if (address in groupMerge["Address"].values) and (address in group_countType["Address"].values):
            avg_floor = int(groupMerge[groupMerge["Address"] == address]["Floor"].values[0])
            avg_size = int(groupMerge[groupMerge["Address"] == address]["Size"].values[0])
            avg_month = groupMerge[groupMerge["Address"] == address]["Month Price(AVG)"].values[0]
            avg_deposit = groupMerge[groupMerge["Address"] == address]["Depossit Price(AVG)"].values[0]

            formatted_month = f"{avg_month:,}"
            formatted_deposit = f"{avg_deposit:,}"
            formatted_size = f"{avg_size:,}"

            floor_info_rows = group_countType[group_countType["Address"] == address]
            floor_type_strs = [f"{row['FloorType']} (count: {row['Type']})" for _, row in floor_info_rows.iterrows()]
            floor_type_combined = ", ".join(floor_type_strs)

            noticeInfo = (
                f"<div style='background-color:#f9f9f9; padding:10px; border-radius:8px; font-size:13px; line-height:1.6'>"
                f"<b>(1) Area Name</b>: {address}<br>"
                f"<b>(2) Vacancy Type</b>: {floor_type_combined}<br>"
                f"<b>(3) Average Floor</b>: {avg_floor}<br>"
                f"<b>(4) Average Size</b>: {formatted_size}㎡<br>"
                f"<b>(5) Average Monthly Price (KRW)</b>: {formatted_month}<br>"
                f"<b>(6) Average Monthly Deposit (KRW)</b>: {formatted_deposit}"
                f"</div>"
            )

            popup_2 = folium.Popup(noticeInfo, max_width=400, min_width=30, max_height=300, show=True)

            myIcon_2 = "./useData/myImage/vacancyMan.png"
            myIcon_edit_2 = CustomIcon(
                icon_image=myIcon_2,
                icon_size=(31, 31),
                icon_anchor=(15, 15)
            )

            folium.Marker(
                location=[lat, lon],
                icon=myIcon_edit_2
            ).add_child(popup_2).add_to(targetArea_2)

        # 원형 마커는 모든 공실에 추가
        folium.CircleMarker(
            location=[lat, lon],
            radius=60,
            fill=True,
            fill_color="#e7ede3",
            color="#ee928c",
            fill_opacity=0.1
        ).add_to(targetArea_2)

    # ✅ 지도 출력은 for문 바깥에서 단 1번만 실행
    st_folium(targetArea_2, use_container_width=True, key="vacancy_kr")

    st.subheader("결론", anchor=False)
    st.markdown('''
        위의 공실 시각화 데이터를 통하여 <span style='color:orange; font-weight:bold; font-size:20px;'>항구별 최적의 지리적 유통 거점을 선점할 수 있으며, 온라인 선용품 쇼핑몰 예산 산정 및 배분에 참고</span> 할 수 있습니다.

with tab_3:
    st.markdown('''
    (1) Data Source : "https://new.land.naver.com/offices?ms=35.087642,128.8114855,16&a=SG&e=RETAIL&ad=true", "https://new.land.naver.com/offices?ms=35.094507,128.835046,16&a=SG&e=RETAIL&ad=true", "https://new.land.naver.com/offices?ms=35.120913,129.0412781,17&a=SG&e=RETAIL&ad=true", "https://new.land.naver.com/offices?ms=35.081925,128.987775,16&a=SG&e=RETAIL&ad=true" <br>
    (2) Collected Data : To collect vacancy data of warehouses used for storing ship stores and supplies.(선용품 및 선박용 물품 보관을 위한 창고의 공실 데이터를 수집하기 위함.)<br>
    (3) Data Type : Structured Data(정형 데이터)<br>
    (4) Technologies Used : Selenium, BeautifulSoup(bs4), Pandas<br>
    (5) Data Collection and Preprocessing Process
    ''',unsafe_allow_html=True)
    st.markdown("<span style='color:orange; font-weight:bold; font-size:20px;'>Data Collection (데이터 수집)</span>", unsafe_allow_html=True)
    st.video("./useData/vacancyData.mp4")
    st.code('''
    # Author: DongWhee Kim
    # Date: 2025-04-20
    # Description: Visualize processed warehouse vacancy data on an interactive map using Folium. (가공된 공실 데이터를 folium 기반의 인터랙티브 지도에 시각화)

    import warnings  # Suppress warning messages (경고 메시지 출력 방지)
    warnings.simplefilter(action='ignore', category=FutureWarning)

    import pandas as pd  # Data manipulation (데이터 조작을 위한 pandas 임포트)
    import re  # Regular expressions (정규표현식)
    from geopy.geocoders import Nominatim  # Geocoding API (주소 → 위도/경도 변환)
    from tqdm import tqdm  # Progress bar for loops (루프 진행 표시)
    import os  # Operating system interactions (환경변수 접근 등 시스템 연동)
    import json  # JSON parsing (JSON 파싱)
    import requests  # HTTP requests (HTTP 요청)
    from dotenv import load_dotenv  # Load environment variables (.env 환경변수 로드)
    import folium  # Map rendering (지도 시각화)
    from folium.features import CustomIcon  # Custom icon for map markers (지도 마커 커스텀 아이콘)
    import plotly.express as px  # Interactive charting (인터랙티브 차트용 plotly)

    # Load vacancy data from preprocessing output (전처리된 공실 데이터 로드)
    vacancyData = pd.read_csv("../useData/finishPrepro/vacancy_location.csv")
    vacancyData["Address"].value_counts()
    vacancyData = vacancyData.iloc[:,1:]  # Remove unnecessary index column (불필요한 인덱스 제거)

    vacancyData.head()

    # Convert price columns to integers (가격 컬럼 정수형 변환)
    vacancyData["Month Price"] = vacancyData["Month Price"].astype("int64")
    processed_DepositPrice = [
        v.replace(",", "").replace("억", "00000000")
        for v in vacancyData["Depossit Price"]
    ]
    vacancyData["Depossit Price"] = processed_DepositPrice
    vacancyData["Depossit Price"] = vacancyData["Depossit Price"].astype("int64")

    # Adjust units to KRW (단위 보정: 천원 → 원)
    vacancyData["Depossit Price"] = vacancyData["Depossit Price"] * 1000
    vacancyData["Month Price"] = vacancyData["Month Price"] * 1000
    vacancyData.iloc[3,-1] = vacancyData.iloc[3,-1]/1000  # 특정 행의 값 수동 보정

    # Initialize lists to store geolocation (위도/경도 저장 리스트)
    lat_list = list()
    lng_list = list()

    # Load Google API Key from environment variables (.env 파일에서 API 키 로딩)
    load_dotenv()
    myGoogleAPI = os.environ.get("googleAPI")

    # Geocode each address (주소 → 위도/경도 변환)
    for v in vacancyData["Address"]:
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={v}&key={myGoogleAPI}'
        response = json.loads(requests.post(url).text)
        print(response)

        location = response["results"][0]['geometry']['location']
        lat = round(location['lat'], 2)
        lat_list.append(lat)
        lng = round(location['lng'], 2)
        lng_list.append(lng)

    print(len(lat_list))
    print(len(lng_list))

    # Store geolocation back to DataFrame (위경도 데이터 프레임에 저장)
    vacancyData["Latitude"] = lat_list
    vacancyData["Longitude"] = lng_list
    vacancyData

    # Save with coordinates (위경도 포함 데이터 저장)
    vacancyData.to_csv("../useData/finishPrepro/vacancy_locationLaLo.csv", encoding="utf-8-sig")

    # Add new column to distinguish floor type (층수 유형 구분 컬럼 추가)
    vacancyData["FloorType"] = ["지하" if "B" in v else "지상" for v in vacancyData["Floor"]]

    # Remove ' Floor' and 'B' from floor string (층수 문자열 정제)
    def deleteFloor(x):
        x = x.replace(" Floor", "").replace("B", "")
        return x

    vacancyData["Floor"] = vacancyData["Floor"].apply(deleteFloor)
    vacancyData["Floor"] = vacancyData["Floor"].astype("int64")
    vacancyData.head(5)

    vacancyData.columns

    # Rearranging columns for clarity (컬럼 순서 정렬)
    renameColumns = ['FloorType', 'Address', 'Size', 'Floor', 'Month Price', 'Depossit Price', 'Latitude', 'Longitude']
    vacancyData = vacancyData[renameColumns]
    vacancyData.head()

    vacancyData.info()

    # Count listings by FloorType per address (주소별 지상/지하 건수 집계)
    cntType = vacancyData.groupby(["Address", "FloorType"])["FloorType"].count()

    # Convert to DataFrame (집계 결과를 데이터프레임으로 변환)
    group_countType = pd.DataFrame(
        {
            "Address": [v[0] for v in cntType.index],
            "FloorType": [v[1] for v in cntType.index],
            "Type": cntType.values
        }
    )

    group_countType

    # Group and calculate average price per address (주소별 평균 가격 계산)
    groupPriceMean = vacancyData.groupby(["Address"])[["Month Price", "Depossit Price"]].mean()

    groupPriceMeanResult = pd.DataFrame(
        {
            "Address": groupPriceMean.index,
            "Month Price(AVG)": groupPriceMean["Month Price"].astype(int),
            "Depossit Price(AVG)": groupPriceMean["Depossit Price"].astype(int)
        }
    ).reset_index(drop=True)

    groupPriceMeanResult

    # Group and calculate average size (주소별 평균 면적 계산)
    groupSizeMean = vacancyData.groupby(["Address"])["Size"].mean()
    groupSizeMeanResult = pd.DataFrame(
        {
            "Address": groupSizeMean.index,
            "Size(AVG ㎡)": groupSizeMean.values.astype(int)
        }
    )

    groupSizeMeanResult

    # Group and calculate average floor (주소별 평균 층수 계산)
    groupFloorMean = vacancyData.groupby(["Address"])["Floor"].mean()
    groupFloorMeanResult = pd.DataFrame(
        {
            "Address": groupFloorMean.index,
            "Floor(AVG)": groupFloorMean.values.astype(int)
        }
    )

    groupFloorMeanResult

    # Merge all group results into one DataFrame (모든 요약 데이터 병합)
    groupMerge = (
        groupPriceMeanResult
        .merge(groupFloorMean, on="Address")
        .merge(groupSizeMean, on="Address")
    )
    groupMerge

    # Create base folium map centered on Busan (부산 중심 좌표 기준 베이스 맵 생성)
    targetArea = folium.Map(
        location=[35.125135443661655, 128.96211911293543],
        zoom_start=11,
        tiles="CartoDB positron"
    )

    # Load GeoJSON data for Busan boundary (부산시 경계 GeoJSON 로딩)
    busanGeo = "../useData/koreaBusan.geojson"
    with open(busanGeo, encoding="utf-8-sig") as f:
        myGeo = json.load(f)

    # Style function for GeoJSON rendering (GeoJSON 스타일 함수 정의)
    def myGeo_style(x):
        return {
            "fillColor": "#dae080",
            "color": "",
            "weight": 0.5,
            "fillOpacity": 0.2
        }

    # Add boundary overlay to map (지도에 경계선 오버레이 추가)
    folium.GeoJson(
        data=myGeo,
        name="Busan Metropolitan City, Republic of Korea",
        style_function=myGeo_style
    ).add_to(targetArea)

    # Add each vacancy marker to map (각 공실에 대한 마커 추가)
    for i, v in vacancyData.iterrows():
        lat = v["Latitude"]
        lon = v["Longitude"]
        address = v["Address"]

        if (address in groupMerge["Address"].values) and (address in group_countType["Address"].values):
            avg_floor = int(groupMerge[groupMerge["Address"] == address]["Floor"].values[0])
            avg_size = int(groupMerge[groupMerge["Address"] == address]["Size"].values[0])
            avg_month = groupMerge[groupMerge["Address"] == address]["Month Price(AVG)"].values[0]
            avg_deposit = groupMerge[groupMerge["Address"] == address]["Depossit Price(AVG)"].values[0]

            formatted_month = f"{avg_month:,}"
            formatted_deposit = f"{avg_deposit:,}"
            formatted_size = f"{avg_size:,}"

            floor_info_rows = group_countType[group_countType["Address"] == address]
            floor_type_strs = [
                f"{row['FloorType']} (count: {row['Type']})"
                for _, row in floor_info_rows.iterrows()
            ]
            floor_type_combined = ", ".join(floor_type_strs)

            noticeInfo = (
                f"<div style='background-color:#f9f9f9; padding:10px; border-radius:8px; font-size:13px; line-height:1.6'>"
                f"<b>(1) Area Name</b>: {address}<br>"
                f"<b>(2) Vacancy Type</b>: {floor_type_combined}<br>"
                f"<b>(3) Average Floor</b>: {avg_floor}<br>"
                f"<b>(4) Average Size</b>: {formatted_size}㎡<br>"
                f"<b>(5) Average Monthly Price (KRW)</b>: {formatted_month}<br>"
                f"<b>(6) Average Monthly Deposit (KRW)</b>: {formatted_deposit}"
                f"</div>"
            )

            popup = folium.Popup(
                noticeInfo,
                max_width=400,
                min_width=30,
                max_height=300,
                show=True
            )

            myIcon = "../useData/myImage/vacancyMan.png"
            myIcon_edit = CustomIcon(
                icon_image=myIcon,
                icon_size=(31, 31),
                icon_anchor=(15, 15)
            )

            folium.Marker(
                location=[lat, lon],
                icon=myIcon_edit
            ).add_child(popup).add_to(targetArea)

        folium.CircleMarker(
            location=[lat, lon],
            radius=60,
            fill=True,
            fill_color="#e7ede3",
            color="#ee928c",
            fill_opacity=0.1
        ).add_to(targetArea)

    # Final interactive map result (최종 지도 결과)
    targetArea
    ''')
