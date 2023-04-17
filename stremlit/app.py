import streamlit as st
import pandas as pd
import joblib
from streamlit_option_menu import option_menu

if 'num' not in st.session_state:
    st.session_state.num = 1
if 'data' not in st.session_state:
    st.session_state.data = []
st.write("""
    # Analyzing comments app
    Streamlit App
    """)
filename = "nlp-model.joblib"

model = joblib.load(filename)

with st.sidebar:
    selected = option_menu("Main Menu", ["Add news", "News"], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected

  
class News:
    def __init__(self, page_id):
        st.title(f"BBC NEWS N°{page_id}")
        self.text = st.text_input("New")
        predictions = model.predict([self.text])
        predictions = pd.Series(predictions)
        predictions = predictions.replace([1, 2,3,4,5], ["Sport", "Business", "Politics","Entertainment","Tech"])
        self.category = predictions

def main():
    placeholder = st.empty()
    placeholder2 = st.empty()

    while True:    
        num = st.session_state.num

        if placeholder2.button('end', key=num):
            selected == "News"
            placeholder2.empty()
            df = pd.DataFrame(st.session_state.data)
            st.dataframe(df)
            break
        else:        
            with placeholder.form(key=str(num)):
                new_comment = News(page_id=num)        

                if st.form_submit_button('submit'):                
                    st.session_state.data.append({
                        'id': num, 'new': new_comment.text, 'category': new_comment.category})
                    st.session_state.num += 1
                    placeholder.empty()
                    placeholder2.empty()
                else:
                    st.stop()


if selected == "Add News":
    main()


if selected == "News":
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)   


 