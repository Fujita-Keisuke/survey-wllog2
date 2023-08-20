import streamlit as st

def main():
    st.title("Colored 'Buttons' with Streamlit")

    button_styles = {
        '次へ': 'background-color: #FF5733; color: white;',
        '前へ': 'background-color: #337DFF; color: white;'
    }

    # ボタンにスタイルを適用して表示
    for button_label, style in button_styles.items():
        st.markdown(f'<button style="{style}"</button>', unsafe_allow_html=True)
        #if st.session_state.get(button_label, False):
            #st.markdown(f"You clicked **{button_label}**!")

if __name__ == "__main__":
    main()
