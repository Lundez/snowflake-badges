import streamlit as st
import pandas as pd

def main():
    st.title("My Parents New Healthy Diner")

    st.header("Breakfast Favorites")
    st.text("🥣 Omega 3 & Blueberry Oatmeal")
    st.text("🥗 Kale, Spinach & Rocket Smoothie")
    st.text("🐔 Hard-Boiled Free-Range Egg")
    st.text("🥑🍞 Avocado Toast")

    st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

    my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
    streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

    st.dataframe(my_fruit_list)

if __name__ == '__main__':
    main()