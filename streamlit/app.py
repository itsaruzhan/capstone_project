import streamlit as st
import pandas as pd
import joblib
from streamlit_option_menu import option_menu
import time
from sklearn.base import BaseEstimator, TransformerMixin
import string

from nltk.corpus import stopwords
import re

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
    selected = option_menu("Главное", ["Добавить Новости", "Читать Новости"], 
        icons=['cloud-upload', 'house'], menu_icon="cast", default_index=0)
    selected


class CustomTextPrep(BaseEstimator, TransformerMixin):
    """My custom description
    Args:
        delete_stopwords (bool): True if I want to delete most popular russian words 
    Returns:

    """
    def __init__(self, delete_stopwords=True):
        self.delete_stopwords = delete_stopwords
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        def text_clean(text):        
            text = text.lower() 
            text = re.sub('https?://\S+|www\.\S+', '', text) 
            text = re.sub(r"\b\d+\b", "", text) 
            text = re.sub('<.*?>+', '', text) 
            text = re.sub('[%s]' % re.escape(string.punctuation), '', text) 
            text = re.sub('\n', '', text)
            text = re.sub('[’“”…]', '', text)

            return text

        def delete_stopwords(text):
            stop_words = set(stopwords.words('russian'))
            return ' '.join([word for word in text.split() if word not in (stop_words)])
        
        X_copy = X.copy()
        X_copy = X_copy.apply(lambda text: text_clean(str(text)))
        if delete_stopwords:
            X_copy= X_copy.apply(lambda text: delete_stopwords(str(text)))
        
        X_copy = X_copy.apply(lambda text: stemming(str(text)))
        
        return X_copy
        

    
  
class News:
    def __init__(self, page_id):
        st.title(f"NUR.KZ NEWS N°{page_id}")
        self.text = st.text_area("Добавить Новости")
        predictions = model.predict(pd.Series([self.text]))
        predictions = pd.Series(predictions)
        predictions = predictions.replace([1,2,3,4,5], ["Политика", "Финансы", "Общество","Новости мира"])
        self.category = predictions[0]

def main():
    placeholder = st.empty()
    placeholder2 = st.empty()
    
    while True:    
        num = st.session_state.num
     
        with placeholder.form(key=str(num)):

            new_comment = News(page_id=num)        

            if st.form_submit_button('Отправить'):                
                st.session_state.data.append({
                        'id': num, 'new': new_comment.text, 'category': new_comment.category})
                st.session_state.num += 1
                with st.spinner('Загружаем...'):
                    time.sleep(3)
                    st.success("Сделано! Категория новостей - " +  new_comment.category)
                placeholder.empty()
                placeholder2.empty()
            else:
                st.stop()

def show_news():
    
    if len(st.session_state.data)>0:
            df = pd.DataFrame(st.session_state.data)  

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Политика", "Финансы", "Общество","Новости мира"])

            with tab1:
                st.header("Политические Новости")
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
                st.header("Новости мира")
                for index, new in enumerate(df[df['category']== "Новости мира"]["new"]):
                    st.title(f"Новости мира N°{index+1}")
                    st.write(new)

if selected == "Добавить Новости":
    main()


if selected == "Читать Новости":
    show_news()                
        
