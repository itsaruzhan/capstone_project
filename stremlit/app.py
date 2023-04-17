import streamlit as st
import pandas as pd
import joblib
from streamlit_option_menu import option_menu
import time

if 'num' not in st.session_state:
    st.session_state.num = 1
if 'data' not in st.session_state:
    st.session_state.data = []
st.write("""
    # BBC NEWS Classification 
    """)
filename = "stremlit/nlp-model.joblib"

model = joblib.load(filename)

with st.sidebar:
    selected = option_menu("Main Menu", ["Add News", "News"], 
        icons=['cloud-upload', 'house'], menu_icon="cast", default_index=0)
    selected

  
class News:
    def __init__(self, page_id):
        st.title(f"BBC NEWS N°{page_id}")
        self.text = st.text_area("Add News")
        predictions = model.predict([self.text])
        predictions = pd.Series(predictions)
        predictions = predictions.replace([1, 2,3,4,5], ["Sport", "Business", "Politics","Entertainment","Tech"])
        self.category = predictions[0]

def main():
    placeholder = st.empty()
    placeholder2 = st.empty()
    
    while True:    
        num = st.session_state.num

        if placeholder2.button('End', key=num):
            selected == "News"
            placeholder2.empty()
            df = pd.DataFrame(st.session_state.data)
            st.dataframe(df)
            break
        else:        
            with placeholder.form(key=str(num)):

                new_comment = News(page_id=num)        

                if st.form_submit_button('Submit'):                
                    st.session_state.data.append({
                        'id': num, 'new': new_comment.text, 'category': new_comment.category})
                    st.session_state.num += 1
                    with st.spinner('Wait for it...'):
                        time.sleep(3)
                        st.success("Done! News' category is " +  new_comment.category)
                    placeholder.empty()
                    placeholder2.empty()
                else:
                    st.stop()


if selected == "Add News":
    main()


if selected == "News":
    if len(st.session_state.data)>0:
        df = pd.DataFrame(st.session_state.data)  

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sport", "Business", "Politics","Entertainment","Tech"])

        with tab1:
            st.header("Sport News")
            for index, new in enumerate(df[df['category']== "Sport"]["new"]):
                st.title(f"Sport NEWS N°{index+1}")
                st.write(new)
            

        with tab2:
            st.header("Business News")
            for index, new in enumerate(df[df['category']== "Business"]["new"]):
                st.title(f"Business NEWS N°{index+1}")
                st.write(new)
        with tab3:
            st.header("Politics News")
            for index, new in enumerate(df[df['category']== "Politics"]["new"]):
                st.title(f"Politics NEWS N°{index+1}")
                st.write(new)

        with tab4:
            st.header("Entertainment News")
            for index, new in enumerate(df[df['category']== "Entertainment"]["new"]):
                st.title(f"Entertainment NEWS N°{index+1}")
                st.write(new)

        with tab5:
            st.header("Tech News")
            for index, new in enumerate(df[df['category']== "Tech"]["new"]):
                st.title(f"Tech NEWS N°{index+1}")
                st.write(new)                        
        

        

    