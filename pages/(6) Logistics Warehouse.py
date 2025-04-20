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

tab_1, tab_2, tab_3 = st.tabs(["Analysis Process(EN)", "Analysis Process(KR)", "Data Prep&EDA"])

# ======================= 공통 함수 =======================
def load_vacancy_data():
    df = pd.read_csv("./useData/finishPrepro/vacancy_locationLaLo.csv", encoding="utf-8-sig")
    df["FloorType"] = ["지하" if "B" in v else "지상" for v in df["Floor"]]
    df["Floor"] = df["Floor"].str.replace(" Floor", "").str.replace("B", "").astype("int64")
    cols = ['FloorType', 'Address', 'Size', 'Floor', 'Month Price', 'Depossit Price', 'Latitude', 'Longitude']
    return df[cols]

def summarize_vacancy_data(df):
    cnt_type = df.groupby(["Address", "FloorType"])["FloorType"].count()
    group_count = pd.DataFrame({
        "Address": [v[0] for v in cnt_type.index],
        "FloorType": [v[1] for v in cnt_type.index],
        "Type": cnt_type.values
    })
    
    price_mean = df.groupby("Address")[["Month Price", "Depossit Price"]].mean().astype(int)
    price_df = price_mean.rename(columns={"Month Price": "Month Price(AVG)", "Depossit Price": "Depossit Price(AVG)"}).reset_index()

    size_mean = df.groupby("Address")["Size"].mean().astype(int).reset_index(name="Size")
    floor_mean = df.groupby("Address")["Floor"].mean().astype(int).reset_index(name="Floor")

    merge_df = price_df.merge(size_mean, on="Address").merge(floor_mean, on="Address")
    return group_count, merge_df

def draw_map(df, group_count, merge_df, key):
    target_map = folium.Map(location=[35.1251, 128.9621], zoom_start=11, tiles="CartoDB positron")

    with open("./useData/koreaBusan.geojson", encoding="utf-8-sig") as f:
        geo_data = json.load(f)

    folium.GeoJson(geo_data, style_function=lambda x: {
        "fillColor": "#dae080", "color": "", "weight": 0.5, "fillOpacity": 0.2
    }).add_to(target_map)

    for _, row in df.iterrows():
        lat, lon, address = row["Latitude"], row["Longitude"], row["Address"]

        if address in merge_df["Address"].values and address in group_count["Address"].values:
            avg_row = merge_df[merge_df["Address"] == address].iloc[0]
            formatted = {
                "month": f"{avg_row['Month Price(AVG)']:,}",
                "deposit": f"{avg_row['Depossit Price(AVG)']:,}",
                "size": f"{avg_row['Size']:,}",
                "floor": avg_row['Floor']
            }
            types = group_count[group_count["Address"] == address]
            type_str = ", ".join([f"{r['FloorType']} (count: {r['Type']})" for _, r in types.iterrows()])

            popup_html = f"""
                <div style='background-color:#f9f9f9; padding:10px; border-radius:8px; font-size:13px; line-height:1.6'>
                <b>(1) Area Name</b>: {address}<br>
                <b>(2) Vacancy Type</b>: {type_str}<br>
                <b>(3) Average Floor</b>: {formatted['floor']}<br>
                <b>(4) Average Size</b>: {formatted['size']}㎡<br>
                <b>(5) Average Monthly Price (KRW)</b>: {formatted['month']}<br>
                <b>(6) Average Monthly Deposit (KRW)</b>: {formatted['deposit']}
                </div>
            """
            popup = folium.Popup(popup_html, max_width=400)

            icon = CustomIcon("./useData/myImage/vacancyMan.png", icon_size=(31, 31), icon_anchor=(15, 15))
            folium.Marker(location=[lat, lon], icon=icon).add_child(popup).add_to(target_map)

        folium.CircleMarker(
            location=[lat, lon], radius=60, fill=True,
            fill_color="#e7ede3", color="#ee928c", fill_opacity=0.1
        ).add_to(target_map)

    st_folium(target_map, use_container_width=True, key=key)

# ======================= EN 탭 =======================
with tab_1:
    st.markdown("""
    Previously, we conducted an analysis covering <span style='color:orange; font-weight:bold; font-size:20px;'>correlation with potential customers, product selection based on annual ship supply demand, and the identification of companies dealing with those products</span> for building an online ship supply platform.
    In this section, we performed a <span style='color:white; font-weight:bold; font-size:20px;'>visual analysis of vacancy data</span>.
    But why did we collect and analyze vacancy data in the first place?
    We assumed that if an online ship supply platform is launched, it would be important for foreign crew members to be able to <span style='color:white; font-weight:bold; font-size:20px;'>pick up their ordered products near the port during embarkation or disembarkation</span>.
    This would help <span style='color:orange; font-weight:bold; font-size:20px;'>crew members plan their time more efficiently and make the most of their stay</span>.
    Based on this rationale, we collected and visualized vacancy data around <span style='color:orange; font-weight:bold; font-size:20px;'>the three major ports of Busan (New Port, North Port, and Gamcheon Port)</span>.
    <br><span style='color:red; font-weight:bold; font-size:15px;'>* Due to confidentiality policies of real estate agencies, detailed vacancy addresses and building names were not publicly available. Therefore, we gathered, processed, and visualized data by searching areas near the three major port addresses.</span>
    """, unsafe_allow_html=True)

    df_en = load_vacancy_data()
    count_en, merge_en = summarize_vacancy_data(df_en)
    draw_map(df_en, count_en, merge_en, key="vacancy_map_en")

    st.subheader("Conclusion", anchor=False)
    st.markdown('''
    Through the above vacancy data visualization, we can <span style='color:orange; font-weight:bold; font-size:20px;'>secure optimal geographic logistics hubs near each port</span>, which can also serve as a valuable reference for <span style='color:orange; font-weight:bold; font-size:20px;'>budget estimation and allocation for the online ship supply platform</span>.
    ''', unsafe_allow_html=True)

# ======================= KR 탭 =======================
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

    df_kr = load_vacancy_data()
    count_kr, merge_kr = summarize_vacancy_data(df_kr)
    draw_map(df_kr, count_kr, merge_kr, key="vacancy_map_kr")

    st.subheader("결론", anchor=False)
    st.markdown('''
    위의 공실 시각화 데이터를 통해 <span style='color:orange; font-weight:bold; font-size:20px;'>항구별 최적의 지리적 유통 거점을 선점할 수 있고</span>, 오름라인 선용품 쇼핑몰 예산 산정 및 배분에 참고할 수 있습니다.
    ''', unsafe_allow_html=True)
    st.dataframe(merge_kr, hide_index=True)
