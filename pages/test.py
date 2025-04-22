import matplotlib.pyplot as plt # Import matplotlib (used for plotting; we re-import pyplot later) (시각화를 위한 matplotlib 전체 임포트)
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np
import streamlit as st
import os
font_dirs = 'Fonts/MALGUN.TTF'
font_prop = fm.FontProperties(fname=font_dirs)
st.subheader(font_prop.get_name())



def unique(list):
    x = np.array(list)
    return np.unique(x)

@st.cache_data
def fontRegistered():
    font_dirs = '../Fonts/MALGUN.TTF'
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)
    

def main():
    
    # fontRegistered()
    fontNames = [f.name for f in fm.fontManager.ttflist]
    fontname = st.selectbox("폰트 선택", unique(fontNames))

    plt.rc('font', family=fontname)
    tips = sns.load_dataset("tips")
    fig, ax = plt.subplots()
    sns.scatterplot(data=tips, x = 'total_bill', y = 'tip', hue='day')
    ax.set_title("한글 테스트")
    st.pyplot(fig)
    
    st.dataframe(tips)

main()