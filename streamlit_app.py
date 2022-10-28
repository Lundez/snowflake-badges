import streamlit as st
import requests
import pandas as pd
import snowflake.connector

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

    fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
    st.write('The user entered ', fruit_choice)

    st.header("Fruityvice Fruit Advice!")
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")

    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    st.dataframe(fruityvice_normalized)

    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    my_data_row = my_cur.fetchone()
    st.text("Hello from Snowflake:")
    st.text(my_data_row)

if __name__ == '__main__':
    main()