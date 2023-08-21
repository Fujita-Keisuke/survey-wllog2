import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pytz
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from gspread_dataframe import set_with_dataframe
import time

flg_osiri_0 = 0
flg_osiri_1 = 0
flg_osiri_2 = 0
flg_bidet_0 = 0
flg_bidet_1 = 0
flg_bidet_2 = 0
#selected_small_amount = np.nan
#selected_big_bristol = np.nan
button_css_next = f"""
<style>
div.stButton > button:first-child  {{
    font-weight  : bold                ;/* 文字：太字                   */
    border       :  5px solid #f36     ;/* 枠線：ピンク色で5ピクセルの実線 */
    border-radius: 10px 10px 10px 10px ;/* 枠線：半径10ピクセルの角丸     */
    background   : #4CAF50             ;/* 背景色：            */
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
}}
</style>
"""
# button_css_back = f"""
# <style>
# div.stButton > button:first-child  {{
#     font-weight  : bold                ;/* 文字：太字                   */
#     border       :  5px solid #f36     ;/* 枠線：ピンク色で5ピクセルの実線 */
#     border-radius: 10px 10px 10px 10px ;/* 枠線：半径10ピクセルの角丸     */
#     background   : #3b50af             ;/* 背景色：            */
#     color: white;
#     padding: 14px 20px;
#     margin: 8px 0;
#     border: none;
#     cursor: pointer;
#     width: 100%;
# }}
# </style>
# """

st.markdown(button_css_next, unsafe_allow_html=True)
# st.markdown(button_css_back, unsafe_allow_html=True)

def click_1(user_id, selected_options, selected_wash, page):
    st.session_state.user_id = user_id
    st.session_state.selected_options = selected_options
    st.session_state.selected_wash = selected_wash
    st.session_state.page = page
def click_2(page):
    st.session_state.page = page
def click_3(user_id, selected_options, selected_wash, selected_mental, selected_physical, selected_menstruation, page):
##############データ処理
    if selected_mental == "雨":
        mental = 1
    elif selected_mental == "曇り":
        mental = 2
    else:
        mental = 3

    if selected_physical == "雨":
        physical = 1
    elif selected_physical == "曇り":
        physical = 2
    else:
        physical = 3

    if selected_menstruation == "いいえ":
        menstruation = 1
    elif selected_menstruation == "はい(1~3日目程度の多い日)":
        menstruation = 2
    elif selected_menstruation == "はい(4日目以降程度の少ない日)":
        menstruation = 3
    else:
        menstruation = 0

    if selected_options[0] == True:
        options_0 = 1
    else:
        options_0 = 0
    if selected_options[1] == True:
        options_1 = 1
    else:
        options_1 = 0
    if user_id > 200:
        if selected_options[2] == True:
            options_2 = 1
        else:
            options_2 = 0
        if selected_options[3] == True:
            options_3 = 1
        else:
            options_3 = 0
    else:
        options_2 = 0
        if selected_options[2] == True:
            options_3 = 1
        else:
            options_3 = 0

    if selected_wash[0] == True:
        wash_0 = 1
    else:
        wash_0 = 0
    if selected_wash[1] == True:
        wash_1 = 1
    else:
        wash_1 = 0
    if selected_wash[2] == True:
        wash_2 = 1
    else:
        wash_2 = 0

    if flg_osiri_0 == 1:
        selected_options_osiri = st.session_state.selected_options_osiri
        if selected_options_osiri[0] == True:
            osiri_0 = 1
        else:
            osiri_0 = 0
        if flg_osiri_1 == 1:
            if selected_options_osiri[1] == True:
                osiri_1 = 1
            else:
                osiri_1 = 0
            if flg_osiri_2 == 1:
                if selected_options_osiri[2] == True:
                    osiri_2 = 1
                else:
                    osiri_2 = 0
            else:
                osiri_2 = 0
        else:
            osiri_1 = 0
            if flg_osiri_2 == 1:
                if selected_options_osiri[1] == True:
                    osiri_2 = 1
                else:
                    osiri_2 = 0
            else:
                osiri_2 = 0
    else:
        osiri_0 = 0
        if flg_osiri_1 == 1:
            if selected_options_osiri[0] == True:
                osiri_1 = 1
            else:
                osiri_1 = 0
            if flg_osiri_2 == 1:
                if selected_options_osiri[1] == True:
                    osiri_2 = 1
                else:
                    osiri_2 = 0
            else:
                osiri_2 = 0
        else:
            osiri_1 = 0
            if flg_osiri_2 == 1:
                if selected_options_osiri[0] == True:
                    osiri_2 = 1
                else:
                    osiri_2 = 0
            else:
                osiri_2 = 0

    if flg_bidet_0 == 1:
        selected_options_bidet = st.session_state.selected_options_bidet
        if selected_options_bidet[0] == True:
            bidet_0 = 1
        else:
            bidet_0 = 0
        if flg_bidet_1 == 1:
            if selected_options_bidet[1] == True:
                bidet_1 = 1
            else:
                bidet_1 = 0
            if flg_bidet_2 == 1:
                if selected_options_bidet[2] == True:
                    bidet_2 = 1
                else:
                    bidet_2 = 0
            else:
                bidet_2 = 0
        else:
            bidet_1 = 0
            if flg_bidet_2 == 1:
                if selected_options_bidet[1] == True:
                    bidet_2 = 1
                else:
                    bidet_2 = 0
            else:
                bidet_2 = 0
    else:
        bidet_0 = 0
        if flg_bidet_1 == 1:
            if selected_options_bidet[0] == True:
                bidet_1 = 1
            else:
                bidet_1 = 0
            if flg_bidet_2 == 1:
                if selected_options_bidet[1] == True:
                    bidet_2 = 1
                else:
                    bidet_2 = 0
            else:
                bidet_2 = 0
        else:
            bidet_1 = 0
            if flg_bidet_2 == 1:
                if selected_options_bidet[0] == True:
                    bidet_2 = 1
                else:
                    bidet_2 = 0
            else:
                bidet_2 = 0

    if selected_options[0] == True:
        selected_small_amount = st.session_state.selected_small_amount
        if selected_small_amount == "いつもより多い":
            small_amount = 1
        elif selected_small_amount == "いつもと同じ":
            small_amount = 2
        elif selected_small_amount == "いつもより少ない":
            small_amount = 3
        else:
            small_amount = 0
    else:
        small_amount = 0

    if selected_options[1] == True:
        selected_big_bristol = st.session_state.selected_big_bristol
        if selected_big_bristol == "1.コロコロ便":
            bristol = 1
        elif selected_big_bristol == "2.硬い便":
            bristol = 2
        elif selected_big_bristol == "3.やや硬い便":
            bristol = 3
        elif selected_big_bristol == "4.普通便":
            bristol = 4
        elif selected_big_bristol == "5.やや柔らかい便":
            bristol = 5
        elif selected_big_bristol == "6.泥状便":
            bristol = 6
        elif selected_big_bristol == "7.水様便":
            bristol = 7
        else:
            bristol = 0
    else:
        bristol = 0

    if user_id > 200 and selected_options[2] == True:
        selected_women_sympt = st.session_state.selected_women_sympt
        if selected_women_sympt[0] == True:
            women_sympt_0 = 1
        else:
            women_sympt_0 = 0
        if selected_women_sympt[1] == True:
            women_sympt_1 = 1
        else:
            women_sympt_1 = 0
        if selected_women_sympt[2] == True:
            women_sympt_2 = 1
        else:
            women_sympt_2 = 0
        if selected_women_sympt[3] == True:
            women_sympt_3 = 1
        else:
            women_sympt_3 = 0
        if len(selected_women_sympt) > 4:
            women_sympt_4 = selected_women_sympt[4]
        else:
            women_sympt_4 = 0
    else:
        women_amount = 0
        women_sympt_0 = 0
        women_sympt_1 = 0
        women_sympt_2 = 0
        women_sympt_3 = 0
        women_sympt_4 = 0

    now = now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))#datetime.datetime.today()
    _data = {
        "日時": [now],
        "ユーザーID": [user_id],
        "ココロの状態": [mental],
        "カラダの状態": [physical],
        "月経期間": [menstruation],
        "排尿": [options_0],
        "排便": [options_1],
        "デリケートゾーンのケア": [options_2],
        "当てはまる行動はない": [options_3],
        "おしり洗浄": [wash_0],
        "ビデ洗浄": [wash_1],
        "ウォシュレット洗浄していない": [wash_2],
        "おしり洗浄を排尿に使用": [osiri_0],
        "おしり洗浄を排便に使用": [osiri_1],
        "おしり洗浄をデリケートゾーンのケアに使用": [osiri_2],
        "ビデ洗浄を排尿に使用": [bidet_0],
        "ビデ洗浄を排便に使用": [bidet_1],
        "ビデ洗浄をデリケートゾーンのケアに使用": [bidet_2],
        "尿量": [small_amount],
        "ブリストルスケール": [bristol],
        "生理用品の交換": [women_sympt_0],
        "おりものシートの交換": [women_sympt_1],
        "ウェットティッシュでの拭き取り": [women_sympt_2],
        "スプレーやクリームの使用": [women_sympt_3],
        "その他": [women_sympt_4]
    }
    _df = pd.DataFrame(data = _data)
    #st.dataframe(_df)
    SP_SHEET_KEY = st.secrets.SP_SHEET_KEY.key
    SP_SHEET = "db_survey"
    data = gspread_read(SP_SHEET_KEY, SP_SHEET)
    df = pd.concat([data, _df], ignore_index=True)
    gspread_write(SP_SHEET_KEY, SP_SHEET, df)
    st.session_state.page = 4
def click_4(selected_mental, selected_physical, selected_menstruation, page):
    st.session_state.selected_mental = selected_mental
    st.session_state.selected_physical = selected_physical
    st.session_state.selected_menstruation = selected_menstruation
    st.session_state.page = page
def gspread_read(SP_SHEET_KEY, SP_SHEET):
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SP_SHEET_KEY)
    worksheet = sh.worksheet(SP_SHEET)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def gspread_write(SP_SHEET_KEY, SP_SHEET, data):
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SP_SHEET_KEY)
    worksheet = sh.worksheet(SP_SHEET)
    df = pd.DataFrame(data)
    set_with_dataframe(worksheet, df, row=1, col=1)
    return "end"

if 'page' not in st.session_state:
    st.session_state.selected_options = []
    st.session_state.user_id = []
    st.session_state.selected_wash = []
    st.session_state.selected_options_osiri = []
    st.session_state.selected_options_bidet = []
    st.session_state.selected_small_amount = []
    st.session_state.selected_big_bristol = []
    st.session_state.selected_women_sympt = []
    st.session_state.selected_mental = []
    st.session_state.selected_physical = []
    st.session_state.selected_menstruation = []
    st.session_state.page = 1

if st.session_state.page == 1:
    st.title("トイレ利用に関するアンケート")
##############ユーザーID入力
    users_id_men = list(range(101,111))
    users_id_women = list(range(201,211))
    users_id = users_id_men + users_id_women
    st.write("##### あなたのユーザーIDを入力してください")
    _user_id = st.session_state.user_id
    user_index=0
    _selected_options = st.session_state.selected_options
    value_options_1 = False
    value_options_2 = False
    value_options_3 = False
    value_options_4 = False
    value_options_5 = False
    _selected_wash = st.session_state.selected_wash
    value_wash_1 = False
    value_wash_2 = False
    value_wash_3 = False
    _selected_options_osiri = st.session_state.selected_options_osiri
    value_options_osiri_1 = False
    value_options_osiri_2 = False
    value_options_osiri_3 = False
    _selected_options_bidet = st.session_state.selected_options_bidet
    value_options_bidet_1 = False
    value_options_bidet_2 = False
    value_options_bidet_3 = False
    if _user_id:
        user_index = users_id.index(_user_id)
    user_id = st.selectbox("",users_id, label_visibility="collapsed", index=user_index)

##############男女分岐
    st.write("##### Q.今回トイレで実施した行動をすべて選択してください")
    if user_id < 200:
        options_action = [
            "排尿", "排便", "当てはまる行動はない"
        ]
        col1, col2, col3 = st.columns(3)
        selected_options = []
        if _selected_options:
            if _selected_options[0] == True:
                value_options_1 = True
            if _selected_options[1] == True:
                value_options_2 = True
            if _selected_options[2] == True:
                value_options_3 = True
        selected_options.append(col1.checkbox(options_action[0], key="options_1_1", value=value_options_1))
        selected_options.append(col2.checkbox(options_action[1], key="options_2_1", value=value_options_2))
        selected_options.append(col3.checkbox(options_action[2], key="options_3_1", value=value_options_3))
    elif user_id >= 201:
        options_action = [
            "排尿", "排便", "デリケートゾーンのケア", "当てはまる行動はない"
        ]
        col1, col2, col3, col4 = st.columns(4)
        selected_options = []
        if _selected_options:
            if _selected_options[0] == True:
                value_options_1 = True
            if _selected_options[1] == True:
                value_options_2 = True
            if _selected_options[2] == True:
                value_options_3 = True
            if _selected_options[3] == True:
                value_options_4 = True
        selected_options.append(col1.checkbox(options_action[0], key="options_1_2", value=value_options_1))
        selected_options.append(col2.checkbox(options_action[1], key="options_2_2", value=value_options_2))
        selected_options.append(col3.checkbox(options_action[2], key="options_3_2", value=value_options_3))
        selected_options.append(col4.checkbox(options_action[3], key="options_4_2", value=value_options_4))

    ##############洗浄選択
    st.write("##### Q.今回使ったウォシュレット洗浄をすべて選択してください")
    options_wash = [
        "おしり洗浄",
        "ビデ洗浄",
        "ウォシュレット洗浄していない",
    ]
    col1, col2, col3 = st.columns(3)
    selected_wash = []
    if _selected_wash:
        if _selected_wash[0] == True:
            value_wash_1 = True
        if _selected_wash[1] == True:
            value_wash_2 = True
        if _selected_wash[2] == True:
            value_wash_3 = True
    selected_wash.append(col1.checkbox(options_wash[0], key="wash_1", value=value_wash_1))
    selected_wash.append(col2.checkbox(options_wash[1], key="wash_2", value=value_wash_2))
    selected_wash.append(col3.checkbox(options_wash[2], key="wash_3", value=value_wash_3))

##############マトリックス質問
    options_osiri = []
    options_bidet = []
    if selected_options[-1] == False:
        if (selected_wash[0] == True) or (selected_wash[1] == True):
            st.write("##### Q.今回使ったウォシュレット洗浄の目的をすべて選択してください")
            if selected_wash[0] == True:
                if selected_options[0] == True:
                    options_osiri.append(f"{options_wash[0]}を{options_action[0]}のケアに使った")
                if selected_options[1] == True:
                    options_osiri.append(f"{options_wash[0]}を{options_action[1]}のケアに使った")
                if user_id > 200:
                    if selected_options[2] == True:
                        options_osiri.append(f"{options_wash[0]}を{options_action[2]}のケアに使った")

            if selected_wash[1] == True:
                if selected_options[0] == True:
                    options_bidet.append(f"{options_wash[1]}を{options_action[0]}のケアに使った")
                if selected_options[1] == True:
                    options_bidet.append(f"{options_wash[1]}を{options_action[1]}のケアに使った")
                if user_id > 200:
                    if selected_options[2] == True:
                        options_bidet.append(f"{options_wash[1]}を{options_action[2]}のケアに使った")

        if len(options_osiri) > 0:
            if len(options_bidet) > 0:
                selected_options_osiri = []
                selected_options_bidet = []
                if _selected_options_osiri:
                    if _selected_options_osiri[0] == True:
                        value_options_osiri_1 = True
                if _selected_options_bidet:
                    if _selected_options_bidet[0] == True:
                        value_options_bidet_1 = True
                col1, col2 = st.columns(2)
                selected_options_osiri.append(col1.checkbox(options_osiri[0], key="options_wash_1", value=value_options_osiri_1))
                selected_options_bidet.append(col2.checkbox(options_bidet[0], key="options_wash_2", value=value_options_bidet_1))
                flg_osiri_0 = 1
                flg_bidet_0 = 1
                if len(options_osiri) > 1:
                    col3, col4 = st.columns(2)
                    if _selected_options_osiri:
                        if _selected_options_osiri[1] == True:
                            value_options_osiri_2 = True
                    if _selected_options_bidet:
                        if _selected_options_bidet[1] == True:
                            value_options_bidet_2 = True
                    selected_options_osiri.append(col3.checkbox(options_osiri[1], key="options_wash_3", value=value_options_osiri_2))
                    selected_options_bidet.append(col4.checkbox(options_bidet[1], key="options_wash_4", value=value_options_bidet_2))
                    flg_osiri_1 = 1
                    flg_bidet_1 = 1
                    if len(options_osiri) > 2:
                        col5, col6 = st.columns(2)
                        if _selected_options_osiri:
                            if _selected_options_osiri[2] == True:
                                value_options_osiri_3 = True
                        if _selected_options_bidet:
                            if _selected_options_bidet[2] == True:
                                value_options_bidet_3 = True
                        selected_options_osiri.append(col5.checkbox(options_osiri[2], key="options_wash_5", value=value_options_osiri_3))
                        selected_options_bidet.append(col6.checkbox(options_bidet[2], key="options_wash_6", value=value_options_bidet_3))
                        flg_osiri_2 = 1
                        flg_bidet_2 = 1
                st.session_state.selected_options_osiri = selected_options_osiri
                st.session_state.selected_options_bidet = selected_options_bidet
            elif len(options_bidet) == 0:
                selected_options_osiri = []
                if _selected_options_osiri:
                    if _selected_options_osiri[0] == True:
                        value_options_osiri_1 = True
                selected_options_osiri.append(st.checkbox(options_osiri[0], key="options_wash_7", value=value_options_osiri_1))
                flg_osiri_0 = 1
                flg_bidet_0 = 0
                if len(options_osiri) > 1:
                    if _selected_options_osiri:
                        if _selected_options_osiri[1] == True:
                            value_options_osiri_2 = True
                    selected_options_osiri.append(st.checkbox(options_osiri[1], key="options_wash_8", value=value_options_osiri_2))
                    flg_osiri_1 = 1
                    flg_bidet_1 = 0
                    if len(options_osiri) > 2:
                        if _selected_options_osiri:
                            if _selected_options_osiri[2] == True:
                                value_options_osiri_3 = True
                        selected_options_osiri.append(st.checkbox(options_osiri[2], key="options_wash_9", value=value_options_osiri_3))
                        flg_osiri_2 = 1
                        flg_bidet_2 = 0
                st.session_state.selected_options_osiri = selected_options_osiri
        else:
            if len(options_bidet) > 0:
                selected_options_bidet = []
                if _selected_options_bidet:
                    if _selected_options_bidet[0] == True:
                        value_options_bidet_1 = True
                selected_options_bidet.append(st.checkbox(options_bidet[0], key="options_wash_10", value=value_options_bidet_1))
                flg_osiri_0 = 0
                flg_bidet_0 = 1
                if len(options_bidet) > 1:
                    if _selected_options_bidet:
                        if _selected_options_bidet[1] == True:
                            value_options_bidet_2 = True
                    selected_options_bidet.append(st.checkbox(options_bidet[1], key="options_wash_11", value=value_options_bidet_2))
                    flg_osiri_1 = 0
                    flg_bidet_1 = 1
                    if len(options_bidet) > 2:
                        if _selected_options_bidet:
                            if _selected_options_bidet[2] == True:
                                value_options_bidet_3 = True
                        selected_options_bidet.append(st.checkbox(options_bidet[2], key="options_wash_12", value=value_options_bidet_3))
                        flg_osiri_2 = 0
                        flg_bidet_2 = 1
                st.session_state.selected_options_bidet = selected_options_bidet
    if len(selected_options_osiri) > 0:
        st.session_state.selected_options_osiri = selected_options_osiri
    if len(selected_options_bidet) > 0:
        st.session_state.selected_options_bidet = selected_options_bidet
    if not any(selected_options):
        if st.button("次へ", key="error1_1"):
            st.error('トイレで実施した行動を入力してください:e1-1')
    elif selected_options[0] or selected_options[1] or selected_options[-2] == True:
        if selected_options[-1] == True:
            if st.button("次へ", key="error1_2"):
                st.error('トイレで実施した行動について、「何もしていない」とその他を同時に入力しないでください:e1-2')
        else:
            if not any(selected_wash):
                if st.button("次へ", key="error1_3"):
                    st.error('今回使った洗浄を入力してください:e1-3')
            elif selected_wash[0] or selected_wash[1] == True:
                if selected_wash[2] == True:
                    if st.button("次へ", key="error1_4"):
                        st.error('今回使った洗浄について、「洗浄していない」とその他を同時に入力しないでください:e1-4')
                else:
                    if selected_wash[0] == True and selected_wash[1] == False:
                        if not any(selected_options_osiri):
                            if st.button("次へ", key="error1_5"):
                                st.error('おしり洗浄を使った目的を入力してください:e1-5')
                        else:
                            st.button("次へ", key="page1to2_1", on_click = lambda:click_1(user_id, selected_options, selected_wash, 2))
                    elif selected_wash[1] == True and selected_wash[0] == False:
                        if not any(selected_options_bidet):
                            if st.button("次へ", key="error1_6"):
                                st.error('ビデ洗浄を使った目的を入力してください:e1-6')
                        else:
                            st.button("次へ", key="page1to2_2", on_click = lambda:click_1(user_id, selected_options, selected_wash, 2))
                    elif selected_wash[0] == True and selected_wash[1] == True:
                        text_osiri = ""
                        text_bidet = ""
                        if not any(selected_options_osiri):
                            text_osiri = 'おしり洗浄を使った目的を入力してください:e1-7'
                        if not any(selected_options_bidet):
                            text_bidet = 'ビデ洗浄を使った目的を入力してください:e1-7'
                        if len(text_osiri) > 0 or len(text_bidet) > 0:
                            if st.button("次へ", key="error1_7"):
                                if len(text_osiri)>0:
                                    st.error(text_osiri)
                                if len(text_bidet)>0:
                                    st.error(text_bidet)
                        else:
                            st.button("次へ", key="page1to2_3", on_click = lambda:click_1(user_id, selected_options, selected_wash, 2))
            else:
                st.button("次へ", key="page1to2_4", on_click = lambda:click_1(user_id, selected_options, selected_wash, 2))
    else:
        if not any(selected_wash):
            if st.button("次へ", key="error1_8"):
                    st.error('今回使った洗浄を入力してください:e1-8')
        elif selected_wash[0] or selected_wash[1] == True:
            if selected_wash[2] == True:
                if st.button("次へ", key="error1_9"):
                    st.error('今回使った洗浄について、「洗浄していない」とその他を同時に入力しないでください:e1-9')
            else:
                st.button("次へ", key="page1to3_1",on_click = lambda:click_1(user_id, selected_options, selected_wash, 3))
        else:
            st.button("次へ", key="page1to3_2", on_click = lambda:click_1(user_id, selected_options, selected_wash, 3))

##############個別質問
elif st.session_state.page == 2:
    selected_options = st.session_state.selected_options
    st.title("トイレで実施した行動に関する質問")
    if selected_options[0] == True:
        _selected_small_amount = st.session_state.selected_small_amount
        if _selected_small_amount == "いつもより多い":
            value_small = 0
        elif _selected_small_amount == "いつもと同じ":
            value_small = 1
        elif _selected_small_amount == "いつもより少ない":
            value_small = 2
        else:
            value_small = 0
        st.write("#### ■排尿に関する質問")
        st.write("##### Q.今回の排尿の量についてどのように感じましたか？")
        selected_small_amount = st.radio("", ("いつもより多い", "いつもと同じ", "いつもより少ない"), horizontal=True,label_visibility="collapsed", index = value_small)
        st.session_state.selected_small_amount = selected_small_amount
    if selected_options[1] == True:
        _selected_big_bristol = st.session_state.selected_big_bristol
        if _selected_big_bristol == "1.コロコロ便":
            value_big = 0
        elif _selected_big_bristol == "2.硬い便":
            value_big = 1
        elif _selected_big_bristol == "3.やや硬い便":
            value_big = 2
        elif _selected_big_bristol == "4.普通便":
            value_big = 3
        elif _selected_big_bristol == "5.やや柔らかい便":
            value_big = 4
        elif _selected_big_bristol == "6.泥状便":
            value_big = 5
        elif _selected_big_bristol == "7.水様便":
            value_big = 6
        else:
            value_big = 0
        st.write("#### ■排便に関する質問")
        st.write("##### Q.今回の便で最も近いものをお選びください")
        selected_big_bristol = st.radio("", ("1.コロコロ便", "2.硬い便", "3.やや硬い便", "4.普通便", "5.やや柔らかい便", "6.泥状便", "7.水様便"), horizontal=True,label_visibility="collapsed", index = value_big)
        st.image("bristol_stool.png", width = 500)
        st.session_state.selected_big_bristol = selected_big_bristol
    if selected_options[2] == True:
        st.write("#### ■デリケートゾーンのケアに関する質問")
        options_women = [
            "生理用品の交換",
            "おりものシートの交換",
            "ウェットティッシュで拭き取る",
            "スプレーやクリームを使う",
            "その他"
        ]
        st.write("##### Q.実施したケア内容をすべて選択してください")
        selected_women_sympt = []
        _selected_women_sympt = st.session_state.selected_women_sympt
        value_women_1 = False
        value_women_2 = False
        value_women_3 = False
        value_women_4 = False
        value_women_5 = False
        if _selected_women_sympt:
            if _selected_women_sympt[0] == True:
                value_women_1 = True
            if _selected_women_sympt[1] == True:
                value_women_2 = True
            if _selected_women_sympt[2] == True:
                value_women_3 = True
            if _selected_women_sympt[3] == True:
                value_women_4 = True
            if len(_selected_women_sympt) > 4:
                value_women_5 = True
                value_women_text = _selected_women_sympt[4]
        selected_women_sympt.append(st.checkbox(options_women[0], key="women_sympt_1", value = value_women_1))
        selected_women_sympt.append(st.checkbox(options_women[1], key="women_sympt_2", value = value_women_2))
        selected_women_sympt.append(st.checkbox(options_women[2], key="women_sympt_3", value = value_women_3))
        selected_women_sympt.append(st.checkbox(options_women[3], key="women_sympt_4", value = value_women_4))
        free_text_input = st.checkbox(options_women[4], key="women_sympt_5", value = value_women_5)
        if free_text_input:
            if _selected_women_sympt:
                if len(_selected_women_sympt) > 4:
                    free_text = st.text_input("その他のケア内容を入力してください", key="free_text_input_1", value=value_women_text)
                    selected_women_sympt.append(free_text)
                else:
                    free_text = st.text_input("その他のケア内容を入力してください", key="free_text_input_2")
                    selected_women_sympt.append(free_text)
            else:
                    free_text = st.text_input("その他のケア内容を入力してください", key="free_text_input_3")
                    selected_women_sympt.append(free_text)
        #st.image("dcare.jpg", width = 500)
        st.session_state.selected_women_sympt = selected_women_sympt
        if not any(selected_women_sympt):
            if st.button("次へ",key="error2-1"):
                st.error("デリケートゾーンのケアの内容について入力してください:e2-1")
        else:
            st.button("次へ",key="page2to3_1", on_click = lambda:click_2(3))
    if selected_options[2] == False:
        st.button("次へ",key="page2to3_2", on_click = lambda:click_2(3))
    st.button("前へ",key="page2to1", on_click = lambda:click_2(1))

##############共通質問
elif st.session_state.page == 3:
    user_id = st.session_state.user_id
    selected_options = st.session_state.selected_options
    selected_wash = st.session_state.selected_wash
    st.title("その他質問")
    _selected_mental = st.session_state.selected_mental
    if _selected_mental == "晴れ":
        value_mental = 0
    elif _selected_mental == "曇り":
        value_mental = 1
    elif _selected_mental == "雨":
        value_mental = 2
    else:
        value_mental = 0
    _selected_physical = st.session_state.selected_physical
    if _selected_physical == "晴れ":
        value_physical = 0
    elif _selected_physical == "曇り":
        value_physical = 1
    elif _selected_physical == "雨":
        value_physical = 2
    else:
        value_physical = 0
    st.write("##### Q.あなたの現在のココロの状態を教えてください")
    st.write("###### ココロの状態：ストレスを感じている、不安があるなど")
    selected_mental = st.radio("", ("晴れ", "曇り", "雨"), horizontal=True, key="selected_mental", label_visibility="collapsed", index = value_mental)
    #st.session_state.selected_mental = selected_mental
    st.write("##### Q.あなたの現在のカラダの状態を教えてください")
    st.write("###### カラダの状態：カラダがだるい・重い、頭痛や肩こりが辛いなど")
    selected_physical = st.radio("", ("晴れ", "曇り", "雨"), horizontal=True, key="selected_physical",label_visibility="collapsed", index = value_physical)
    #st.session_state.selected_physical = selected_physical
    selected_menstruation = np.nan
    #selected_options_osiri =  np.nan
    #selected_options_bidet = np.nan
    ##############女性のみ
    if user_id >= 201:
        _selected_menstruation = st.session_state.selected_menstruation
        if _selected_menstruation == "いいえ":
            value_menstruation = 0
        elif _selected_menstruation == "はい(1~3日目程度の多い日)":
            value_menstruation = 1
        elif _selected_menstruation == "はい(4日目以降程度の少ない日)":
            value_menstruation = 2
        else:
            value_menstruation = 0
        st.write("##### Q.あなたは現在、月経期間中ですか？")
        selected_menstruation = st.radio("", ("いいえ", "はい(1~3日目程度の多い日)", "はい(4日目以降程度の少ない日)"), horizontal=True,label_visibility="collapsed", index = value_menstruation)
        st.session_state.selected_menstruation = selected_menstruation
    st.button("結果を送信",key="result", on_click=lambda:click_3(user_id, selected_options, selected_wash, selected_mental, selected_physical, selected_menstruation, 4))
    if selected_options[0] or selected_options[1] or selected_options[-2] == True:
        st.button("戻る",key="page3to2", on_click=lambda:click_4(selected_mental, selected_physical, selected_menstruation, 2))
    else:
        st.button("戻る",key="page3to1", on_click=lambda:click_4(selected_mental, selected_physical, selected_menstruation, 1))
elif st.session_state.page == 4:
    st.title("アンケートはこれで終了です。")
    if st.button("戻る",key="back"):
        del st.session_state.page
    # if any(selected_options) == True:
    #     if st.button("前へ", key="page3to2"):
    #         st.session_state.page = 2
    # else:
    #     if st.button("前へ", key="page3to1"):
    #         st.session_state.page = 1