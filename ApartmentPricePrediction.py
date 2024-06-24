import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, OrdinalEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle
import streamlit as st

# Initialize session state
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
    
# Main Page
if not st.session_state.show_form:
    st.title("Apartment Price Estimator")
    st.image("https://arbor.com/wp-content/uploads/2017/12/How-do-small-building-renters-find-apartments.jpg")
    st.write("Estimate apartment costs across India with ease using our Apartment Price Estimator. Whether you're a buyer, seller, or simply researching the market, our tool simplifies the process with approximate predictions.")
    
    
    if st.button("Click here to estimate"):
        st.session_state.show_form = True
        st.experimental_rerun()
             
else:
    # Asssigning default values to the categories.
    location_categories=['agra','ahmadnagar','ahmedabad','allahabad','aurangabad','badlapur','bangalore','belgaum','bhiwadi','bhiwandi','bhopal','bhubaneswar','chandigarh',
    'chennai','coimbatore', 'dehradun','durgapur','ernakulam','faridabad','ghaziabad','goa','greater-noida','guntur','gurgaon','guwahati','gwalior','haridwar','hyderabad',
    'indore','jabalpur','jaipur','jamshedpur','jodhpur','kalyan','kanpur','kochi','kolkata','kozhikode','lucknow','ludhiana','madurai','mangalore','mohali','mumbai',
    'mysore','nagpur','nashik','navi-mumbai','navsari','nellore','new-delhi','noida','palakkad','palghar','panchkula','patna','pondicherry','pune','raipur','rajahmundry',
    'ranchi','satara','shimla','siliguri','solapur','sonipat','surat','thane','thrissur','tirupati','trichy','trivandrum','udaipur','udupi','vadodara','vapi','varanasi',
    'vijayawada','visakhapatnam','vrindavan','zirakpur']

    transaction_categories=['New Property','Resale','Other']

    furnishing_categories=['Furnished', 'Semi-Furnished', 'Unfurnished']
    facing_categories=['East','West','North','South','North - East','North - West','South - East','South -West']

    overlooking_categories=['Garden/Park','Garden/Park, Main Road','Garden/Park, Pool','Garden/Park, Pool, Main Road','Main Road','Main Road, Pool','Pool','Not Available']

    ownership_categories=['Freehold','Leasehold','Co-operative Society','Power Of Attorney','Unknown']

    type_of_car_parking_categories=['Covered', 'Open', 'Not Available']

    floor_categories = ["Lower Basement","Upper Basement","Ground"]+[i for i in range(1,301)]

    st.subheader("Fill to Estimate")

    # Assigning the input values.
    location=st.selectbox("Location",location_categories)
    facing=st.selectbox("Facing",facing_categories)
    bhk=st.number_input("Number of BHK",1,step=1)
    bathroom=st.number_input("Number of Bathrooms",0,step=1)
    balcony=st.number_input("Number of Balconies",0,step=1)
    overlooking=st.selectbox("Overlooking",overlooking_categories)

    type_of_car_parking=st.radio("Type of Parking",type_of_car_parking_categories)
    noOfCarParking=st.number_input("Number of Parking Spots",0,step=1)

    saleFloor=st.selectbox("Floor no.",floor_categories)
    totalFloors=st.selectbox("Total Floors",floor_categories)
    area=st.number_input("Area (Square Feet)")

    furnishing=st.radio("Furnishing",furnishing_categories)
    transaction=st.radio("Transaction",transaction_categories)
    ownership=st.radio("Ownership",ownership_categories)

    #Assigning values to the original data values
    if type_of_car_parking=="Not Available":
        type_of_car_parking="Not_Available"

    if saleFloor=="Lower Basement":
        saleFloor=-2
    elif saleFloor=="Upper Basement":
        saleFloor=-1
    elif saleFloor=="Ground":
        saleFloor=0

    if totalFloors=="Lower Basement":
        totalFloors=-2
    elif "Upper Basement":
        totalFloors=-1
    elif totalFloors=="Ground":
        totalFloors=0

    if ownership=="Unknown":
        ownership='Not Mentioned'

    #Pridiction
    model=pickle.load(open(r"..\apartment_price_predictor.pkl","rb"))

    if st.button("Estimate"):

        data=[location, transaction, furnishing, facing, overlooking, bathroom, balcony, ownership, bhk, area, type_of_car_parking, noOfCarParking, saleFloor, totalFloors]
        column=['Location', 'Transaction', 'Furnishing', 'Facing','Overlooking', 'Bathroom', 'Balcony', 'Ownership', 'BHK','Area', 'Type of Car Parking', 'No of Car Parking', 'Sale Floor', 'Total Floors']

        price=model.predict(pd.DataFrame([data],columns=column))

        st.write(f"The approximate price is {round(price[0],2)} lakh.")
