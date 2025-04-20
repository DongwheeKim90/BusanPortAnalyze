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

# ================= EN Tab =================
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

    vacancyData_en = pd.read_csv("./useData/finishPrepro/vacancy_locationLaLo.csv", encoding="utf-8-sig")
    vacancyData_en["FloorType"] = ["지하" if "B" in v else "지상" for v in vacancyData_en["Floor"]]
    vacancyData_en["Floor"] = vacancyData_en["Floor"].str.replace(" Floor", "").str.replace("B", "").astype("int64")

    renameColumns = ['FloorType', 'Address', 'Size', 'Floor', 'Month Price', 'Depossit Price', 'Latitude', 'Longitude']
    vacancyData_en = vacancyData_en[renameColumns]

    cntType_en = vacancyData_en.groupby(["Address", "FloorType"])["FloorType"].count()
    group_countType_en = pd.DataFrame({
        "Address": [v[0] for v in cntType_en.index],
        "FloorType": [v[1] for v in cntType_en.index],
        "Type": cntType_en.values
    })

    groupPriceMean_en = vacancyData_en.groupby("Address")[["Month Price", "Depossit Price"]].mean()
    groupPriceMeanResult_en = pd.DataFrame({
        "Address": groupPriceMean_en.index,
        "Month Price(AVG)": groupPriceMean_en["Month Price"].astype(int),
        "Depossit Price(AVG)": groupPriceMean_en["Depossit Price"].astype(int)
    }).reset_index(drop=True)

    groupSizeMean_en = vacancyData_en.groupby("Address")["Size"].mean()
    groupFloorMean_en = vacancyData_en.groupby("Address")["Floor"].mean()

    groupMerge_en = (
        groupPriceMeanResult_en
        .merge(groupFloorMean_en, on="Address")
        .merge(groupSizeMean_en, on="Address")
    )

    targetArea_en = folium.Map(location=[35.125135, 128.962119], zoom_start=11, tiles="CartoDB positron")

    with open("./useData/koreaBusan.geojson", encoding="utf-8-sig") as f:
        myGeo_en = json.load(f)

    def myGeo_style(x):
        return {"fillColor": "#dae080", "color": "", "weight": 0.5, "fillOpacity": 0.2}

    folium.GeoJson(data=myGeo_en, style_function=myGeo_style).add_to(targetArea_en)

    for _, v in vacancyData_en.iterrows():
        lat, lon, address = v["Latitude"], v["Longitude"], v["Address"]

        if (address in groupMerge_en.index) and (address in group_countType_en["Address"].values):
            avg_floor = int(groupMerge_en.loc[address]["Floor"])
            avg_size = int(groupMerge_en.loc[address]["Size"])
            avg_month = groupMerge_en.loc[address]["Month Price(AVG)"]
            avg_deposit = groupMerge_en.loc[address]["Depossit Price(AVG)"]

            formatted_month = f"{avg_month:,}"
            formatted_deposit = f"{avg_deposit:,}"
            formatted_size = f"{avg_size:,}"

            floor_info_rows = group_countType_en[group_countType_en["Address"] == address]
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

            myIcon_en = "./useData/myImage/vacancyMan.png"
            myIcon_edit_en = CustomIcon(icon_image=myIcon_en, icon_size=(31, 31), icon_anchor=(15, 15))

            folium.Marker(location=[lat, lon], icon=myIcon_edit_en, popup=folium.Popup(noticeInfo, show=True)).add_to(targetArea_en)

        folium.CircleMarker(location=[lat, lon], radius=60, fill=True, fill_color="#e7ede3", color="#ee928c", fill_opacity=0.1).add_to(targetArea_en)

    st_folium(targetArea_en, use_container_width=True, key="vacancy_map_en")

    st.subheader("Conclusion", anchor=False)
    st.markdown('''
    Through the above vacancy data visualization, we can <span style='color:orange; font-weight:bold; font-size:20px;'>secure optimal geographic logistics hubs near each port</span>,
    which can also serve as a valuable reference for <span style='color:orange; font-weight:bold; font-size:20px;'>budget estimation and allocation for the online ship supply platform</span>.
    ''', unsafe_allow_html=True)
