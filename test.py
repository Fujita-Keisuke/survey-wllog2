import streamlit as st
import time
button_css = f"""
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
st.markdown(button_css, unsafe_allow_html=True)
if st.button('このボタンを押してください'):
    st.write("aaaaa")


