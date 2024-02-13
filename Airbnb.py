import pandas as pd
import streamlit as st
import seaborn as sns
import numpy as np
from streamlit_option_menu import option_menu
import pymongo
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import altair as alt
import pymysql

client = pymongo.MongoClient("mongodb+srv://saranya:Kuttaiyur123!@cluster0.z8lhc9m.mongodb.net/")
db = client.sample_airbnb
details = db.listingsAndReviews

filepath = "C:\\Users\\psara\\Desktop\\SARANYA_VS\\cap4airbnb\\Airbnb.csv"
airbnb_df = pd.read_csv(filepath)

st.set_page_config(page_title = "Airbnb Data Visualization",
                   page_icon = None,
                   initial_sidebar_state="auto",
                   layout="wide",
                   )

with st.sidebar:
    select = option_menu("Menu", ["Home","Overview of Data","Explore"],
                         icons = ["house","graph-up-arrow","bar-chart-line"],
                         menu_icon="menu-button-wide",
                         default_index=0,
                         styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#009df9"}})
    

    
if select == "Home":
    st.header("Welcome to :blue[Airbnb Data Visualization]")
    with st.expander("About Airbnb"):
        st.subheader("Airbnb :blue[Bookings]")
        st.write("Airbnb features a review system in which guests and hosts can rate and review each other after a stay. Hosts and guests are unable to see reviews until both have submitted a review or until the time period to review has closed, a system that aims to improve accuracy and objectivity by removing fears that users will receive a negative review in retaliation if they write one. However, the truthfulness and impartiality of reviews may be adversely affected by concerns of future stays because prospective hosts may refuse to host a user who generally leaves negative reviews. The company's policy requires users to forego anonymity, which may also detract from users' willingness to leave negative reviews. These factors may damage the objectivity of the review system")
    with st.expander("Skills used"):
        st.subheader("Skills used in this :blue[Project]")
        st.write("Python :blue[Scripting]")
        st.write("Data :blue[Preprocessing]")
        st.write("Exploratory Data Analysis :blue[EDA]")
        st.write("Visualization")
        st.write("Stream:blue[lit]")
        st.write("Mongo:blue[DB]")
        st.write("PowerBI or :blue[Tableau]")
    st.markdown("Visualization by :blue[Saranya]")
    
    
    
if select == "Overview of Data":
    st.subheader("Overview of Airbnb Data")
    print(airbnb_df.columns)
    with st.expander("Overall Data of Airbnb"):
        st.write(airbnb_df)
    
    with st.expander("Room Type by Price"):    
        room_type_df = airbnb_df.groupby(by=["Room_type"], as_index=False)["Price"].sum()
        st.write(room_type_df.style.background_gradient(cmap="Greens"))
    
    with st.expander("Room Availability "):
        st.write(airbnb_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Blues"))
    
    with st.expander("Pie chart for Price by Country"):    
        fig = px.pie(airbnb_df,values = "Price", names = "Country", hole =0.5)
        st.plotly_chart(fig,use_container_width=True)
    
    with st.expander("Bar chart for Price by Room type"):
        fig = px.bar(room_type_df, x="Room_type", y="Price",template="seaborn")
        st.plotly_chart(fig,use_container_width=True)
        
    
    st.subheader("Airbnb Analysis in Map view")
    df = airbnb_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    st.map(df)
    
        
if select == "Explore":
    col1,col2,col3 = st.columns(3)
    with col1:
        country = st.selectbox("Select Country",airbnb_df["Country"].unique())
    with col2:
        property = st.selectbox("Select Property Type",airbnb_df["Property_type"].unique())
    with col3:
        room = st.selectbox("Select Room Type",airbnb_df["Room_type"].unique())

        
        
    select_data = airbnb_df[(airbnb_df["Country"] == country) & (airbnb_df["Property_type"] == property) & (airbnb_df["Room_type"] == room)]
    # st.subheader("")
    select_data = select_data.sort_values(by='Price')
    st.subheader("Your Selection of Airbnb Data for Bookings")
    st.write(select_data[['Name','Country','Property_type','Room_type','Price','Amenities','Host_name','Street','Review_scores','No_of_reviews','Min_nights','Max_nights']])
    
    with st.expander("Hotel Name by Price"):
        col1,col2 = st.columns([2,1])
        with col1:
            st.subheader("Bar Chart view")
            st.bar_chart(select_data.set_index('Name')['Price'])
        with col2:
            st.subheader("Table view")
            st.write(select_data[["Name","Price"]])
    
    with st.expander("Hotel Name by Review Scores"):
        col1,col2 = st.columns([2,1])
        with col1:
            st.subheader("Scatter Chart View")
            st.scatter_chart(select_data.set_index('Name')["Review_scores"])
        with col2:
            st.subheader("Table View")
            st.write(select_data[["Name","Review_scores"]])
            
    with st.expander("Number of Reviews by Price"):
        col1,col2 = st.columns([3,1])
        with col1:
            st.subheader("Pie Chart View")
            fig = px.pie(select_data,values = "Price", names = "No_of_reviews", hole =0.5)
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            st.subheader("Table View")
            st.write(select_data[["Price","No_of_reviews"]])
    
    with st.expander("Host Name by Price"):    
        col1,col2 = st.columns([3,1])
        with col1:
            st.subheader("Line Chart View")
            st.line_chart(data=select_data,x="Host_name",y="Price",color=None,width=0,height=0,use_container_width=True)
        with col2:
            st.subheader("Table View")
            st.write(select_data[["Host_name","Price"]])
        
    with st.expander("Total beds by Hotel Name"):    
        col1,col2 = st.columns([3,1])
        with col1:
            st.subheader("Bar Chart View")   
            fig1 = px.bar(select_data, x="Name", y="Total_beds",template="seaborn")
            st.plotly_chart(fig1,use_container_width=True)
        with col2:
            st.subheader("Table View")
            st.write(select_data[["Name","Total_beds"]])
    
    with st.expander("Accomodates, Bedrooms Availablity by Hotel Name"):
        col1,col2 = st.columns([2,1])  
        with col1:
            st.subheader("Altair Chart View")  
            chart = alt.Chart(select_data).mark_bar().encode(
            x='Name:N',  
            y='Price:Q',  
            color=alt.Color('Property_type:N', legend=None),
            column='Room_type:N',
            tooltip=['Name', 'Accomodates','Total_beds', 'Total_bedrooms']  
            ).properties(
                width=600,  
                height=400  # Adjust the height as needed
            ).configure_axis(
                labelAngle=45  # Rotate x-axis labels if needed
            )
            st.altair_chart(chart, use_container_width=True)
        with col2:
            st.subheader("Table View")
            st.write(select_data[["Name","Price","Accomodates","Total_beds","Total_bedrooms"]])
    
    with st.expander("Host by Number of Reviews"):
        col1,col2 = st.columns([3,1])
        with col1:
            st.subheader("Scatter Chart View")
            scatter_fig = px.scatter(
            select_data,
            x="Host_name",
            y="Price",
            size="No_of_reviews",
            color="No_of_reviews",  
            opacity=0.8,
            hover_name="Host_name",
            hover_data={"No_of_reviews": True},
            log_y=True,
            labels={"No_of_reviews": "Number of Reviews"},)
            scatter_fig.update_layout(width=500, height=500)
            st.plotly_chart(scatter_fig, use_container_width=True)
        with col2:
            st.subheader("Table View")
            st.write(select_data[["Host_name","Price","No_of_reviews"]])
    
   
            
    
    
    
    
    
    

    
        