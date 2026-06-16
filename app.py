import streamlit as st
import pandas as pd
from database import *

create_table()


st.set_page_config(
    page_title="FreshTrack",
    page_icon="🥗",
    layout="wide"
)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #FFF8E7, #E8F5E9);
}

.main-title {
    font-size: 45px;
    font-weight: bold;
    color: #2E7D32;
    text-align: center;
}

.subtitle {
    font-size: 22px;
    color: #FF6F00;
    text-align: center;
}

.food-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    border-left: 8px solid #4CAF50;
}

.metric-box {
    background-color: #FFF3E0;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="main-title">🥗 FreshTrack</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">AI Smart Food Waste Reduction System</p>',
    unsafe_allow_html=True
)
from datetime import date, datetime

def show_dashboard(username):

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header(f"Welcome {username} 👋")

    mode = st.sidebar.radio(
        "Select Mode",
        ["Add Food", "Dashboard"]
    )

    if mode == "Add Food":

        food = st.text_input("Food Name")

        category = st.selectbox(
            "Category",
            ["Dairy","Fruit","Vegetable",
             "Meat","Protein","Bakery"]
        )

        temperature = st.number_input(
            "Temperature (°C)",
            0, 50, 25
        )

        humidity = st.number_input(
            "Humidity (%)",
            0, 100, 50
        )

        quantity = st.text_input("Quantity")

        added_date = st.date_input(
            "Added Date"
        )

        expiry_date = st.date_input(
            "Expiry Date"
        )

        if st.button("Add Food"):

            score = 100

            if temperature > 25:
                score -= 20

            if humidity > 70:
                score -= 10

            score = max(0, score)

            if score >= 70:
                status = "Fresh"
            elif score >= 40:
                status = "Expiring"
            else:
                status = "Spoiled"

            df = pd.read_csv("projcsv.csv")

            new_row = {
                "Food_Name": food,
                "Category": category,
                "Temperature": temperature,
                "Humidity": humidity,
                "Quantity": quantity,
                "Purchase_Date": str(added_date),
                "Expiry_Date": str(expiry_date),
                "Freshness_Score": score,
                "Status": status
            }

            df.loc[len(df)] = new_row

            df.to_csv(
                "projcsv.csv",
                index=False
            )

            st.success(
                "Food Added Successfully!"
            )

    else:

        df = pd.read_csv(
            "projcsv.csv"
        )

        st.subheader(
            "📊 Stored Food Data"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

menu = ["Login", "Register"]

choice = st.sidebar.selectbox(
    "Menu",
    menu
)

# ---------------- REGISTER ----------------

if choice == "Register":

    st.header("Create Account")

    new_user = st.text_input(
        "Username"
    )

    new_password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        success = add_user(
            new_user,
            new_password
        )

        if success:

            st.success(
                "Account created successfully!"
            )

        else:

            st.error(
                "Username already exists!"
            )

# ---------------- LOGIN ----------------

else:

    st.header("Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if st.button("Login"):

        result = login_user(
            username,
            password
        )

        if result:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success(
                f"Welcome {username}!"
            )

            st.balloons()

        else:

            st.error(
                "Invalid username or password."
            )

    if st.session_state.logged_in:
        show_dashboard(
            st.session_state.username
        )
            
