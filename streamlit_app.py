import streamlit as st
import requests
import pandas as pd
import snowflake.connector
from urllib.error import URLError


def get_fruity_data(fruit: str) -> pd.DataFrame:
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit}")
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

def get_fruit_list(my_cnx) -> pd.DataFrame:
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()

def main():
    st.title("My Parents New Healthy Diner")

    st.header("Breakfast Favorites")
    st.text("🥣 Omega 3 & Blueberry Oatmeal")
    st.text("🥗 Kale, Spinach & Rocket Smoothie")
    st.text("🐔 Hard-Boiled Free-Range Egg")
    st.text("🥑🍞 Avocado Toast")

    st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

    my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
    my_fruit_list = my_fruit_list.set_index('Fruit')
    
    fruit_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"])
    fruits_to_show = my_fruit_list.loc[fruit_selected]
    
    st.dataframe(fruits_to_show)

    st.header("Fruityvice Fruit Advice!")
    try:
        fruit_choice = st.text_input('What fruit would you like information about?')
        if not fruit_choice:
            st.error("Please select a fruit")
        else:
            st.dataframe(get_fruity_data(fruit_choice))
    except URLError as e:
        st.error()

    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    st.header("The fruit list contains: ")
    if st.button("Show Fruit List"):
        
        st.dataframe(get_fruit_list(my_cnx))

    add_fruit = st.text_input("Add a fruit")
    if len(add_fruit):
        st.write(f"Thanks for adding fruit ({add_fruit})")
        st.stop()
        my_cur.execute(f"insert into pc_rivery_db.public.fruit_load_list values ('{add_fruit}');")

if __name__ == '__main__':
    main()