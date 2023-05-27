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
    # Загружай новости NUR.KZ и узнай категорию!
    """)
filename = "streamlit/nlp-model-ru.joblib"

model = joblib.load(filename)

with st.sidebar:
    selected = option_menu("Главное", ["Добавить", "Новости"], 
        icons=['cloud-upload', 'house'], menu_icon="cast", default_index=0)
    selected

  
class News:
    def __init__(self, page_id):
        st.title(f"NUR.KZ NEWS N°{page_id}")
        self.text = st.text_area("Добавить")
        st.form_submit_button("Отправить")
        predictions = model.predict([self.text])
        predictions = pd.Series(predictions)
        predictions = predictions.replace([1,2,3,4], ["Политика", "Финансы", "Общество","Мир"])
        self.category = predictions[0]

def main():
    placeholder = st.empty()
    placeholder2 = st.empty()
    
    while True:    
        num = st.session_state.num
     
        with placeholder.form(key=str(num)):

            new_comment = News(page_id=num)        
            
            if st.form_submit_button("Отправить"):                
                st.session_state.data.append({
                        'id': num, 'new': new_comment.text, 'category': new_comment.category})
                st.session_state.num += 1
                with st.spinner('Загружаем...'):
                    time.sleep(3)
                    st.success("Сделано! Категория - " +  new_comment.category)
                placeholder.empty()
                placeholder2.empty()
            else:
                st.stop()

def show_news():
    
    if len(st.session_state.data)>0:
            df = pd.DataFrame(st.session_state.data)  

            tab1, tab2, tab3, tab4 = st.tabs( ["Политика", "Финансы", "Общество","Мир"])

            with tab1:
                st.header("Политика")
                for index, new in enumerate(df[df['category']== "Политика"]["new"]):
                    st.title(f"Политические Новости N°{index+1}")
                    st.write(new)
                

            with tab2:
                st.header("Финансы")
                for index, new in enumerate(df[df['category']== "Финансы"]["new"]):
                    st.title(f"Финансовые Новости N°{index+1}")
                    st.write(new)
            with tab3:
                st.header("Общество")
                for index, new in enumerate(df[df['category']== "Общество"]["new"]):
                    st.title(f"Общественные Новости N°{index+1}")
                    st.write(new)

            with tab4:
                st.header("Мир")
                for index, new in enumerate(df[df['category']== "Мир"]["new"]):
                    st.title(f"Новости Мира N°{index+1}")
                    st.write(new)

if selected == "Добавить":
    main()


if selected == "Новости":
    show_news()                
        

        

    