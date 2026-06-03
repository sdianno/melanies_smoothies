# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  

# Name box
name_on_order = st.text_input("Name on order:")
st.write("The name on your order will be", name_on_order)

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!")
st.write(
  """Choose the fruits you want in your custom smoothie  """
)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients?",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string=''

    for smoothie_ingredient in ingredients_list:
         ingredients_string+=smoothie_ingredient + ' '
         st.subheader(smoothie_ingredient + ' Nutrition information')
         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + smoothie_ingredient)  
         st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','"""+ name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order + '!', icon="✅")
       
               

