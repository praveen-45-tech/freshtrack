import streamlit as st
import pandas as pd
from database import *

create_table()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="FreshTrack",
    page_icon="🥗",
    layout="wide"
)

# ---------------- STYLE ----------------

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

# ---------------- DASHBOARD ----------------

def show_dashboard(username):

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header(f"🍎 Welcome {username}")

    mode = st.sidebar.radio(
        "Select Mode",
        [
            "🏠 Home",
            "➕ Add Food",
            "📊 Dashboard",
            "🤖 AI Prediction",
            "⚠ Expiry Alerts",
            "🍲 Recipe Suggestions",
            "📈 Analytics",
            "🌍 Sustainability"
        ]
    )

    # HOME

    if mode == "🏠 Home":

        st.success(
            "Welcome to FreshTrack AI Food Waste Reduction System"
        )

    # ADD FOOD

    elif mode == "➕ Add Food":

        food = st.text_input("Food Name")

        added_date = st.date_input(
            "Added Date"
        )

        expiry_date = st.date_input(
            "Expiry Date"
        )

        if st.button("Save Food"):

            days_left = (
                expiry_date - added_date
            ).days

            try:
                df = pd.read_csv(
                    "user_foods.csv"
                )
            except:
                df = pd.DataFrame(
                    columns=[
                        "Food_Name",
                        "Time_To_Expiry"
                    ]
                )

            new_row = {
                "Food_Name": food,
                "Time_To_Expiry": days_left
            }

            df.loc[len(df)] = new_row

            df.to_csv(
                "user_foods.csv",
                index=False
            )

            st.success(
                "Food Added Successfully"
            )

    # DASHBOARD

    elif mode == "📊 Dashboard":

        try:
            df = pd.read_csv(
                "user_foods.csv"
            )
        except:
            df = pd.DataFrame(
                columns=[
                    "Food_Name",
                    "Time_To_Expiry"
                ]
            )

        st.subheader(
            "📊 User Added Foods"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    # AI PREDICTION

    elif mode == "🤖 AI Prediction":

        try:
            df = pd.read_csv(
                "user_foods.csv"
            )
        except:
            df = pd.DataFrame(
                columns=[
                    "Food_Name",
                    "Time_To_Expiry"
                ]
            )

        if len(df) > 0:

            food = st.selectbox(
                "Select Food",
                df["Food_Name"]
            )

            days_left = int(
                df[df["Food_Name"] == food]
                ["Time_To_Expiry"]
                .values[0]
            )

            score = min(
                100,
                int((days_left / 30) * 100)
            )

            st.progress(
                score / 100
            )

            st.metric(
                "Freshness Score",
                f"{score}%"
            )

            if score >= 70:
                st.success(
                    "Food is Fresh ✅"
                )

            elif score >= 40:
                st.warning(
                    "Consume Soon ⚠️"
                )

            else:
                st.error(
                    "Food Spoiled ❌"
                )

    # EXPIRY ALERTS

        # EXPIRY ALERTS

        # EXPIRY ALERTS

    elif mode == "⚠ Expiry Alerts":

        st.subheader("📱 FreshTrack Expiry Notification Center")

        try:
            df = pd.read_csv("user_foods.csv")
        except:
            df = pd.DataFrame(
                columns=["Food_Name", "Time_To_Expiry"]
            )

        alerts_found = False

        for _, row in df.iterrows():

            if row["Time_To_Expiry"] <= 1:

                alerts_found = True

                st.error(
                    f"🚨 ALERT: {row['Food_Name']} expires tomorrow!"
                )

            elif row["Time_To_Expiry"] <= 3:

                alerts_found = True

                st.warning(
                    f"⚠ {row['Food_Name']} expires in {row['Time_To_Expiry']} days."
                )

        if not alerts_found:

            st.success(
                "✅ No foods are close to expiry."
            )

    # RECIPE

    elif mode == "🍲 Recipe Suggestions":

        food = st.text_input(
            "Enter Food Name"
        )

        recipes = {
            "Milk": "Milkshake",
            "Apple": "Apple Pie",
            "Banana": "Banana Smoothie",
            "Egg": "Omelette",
            "Bread": "Sandwich"
        }

        if food in recipes:

            st.success(
                recipes[food]
            )

    # ANALYTICS

    elif mode == "📈 Analytics":

        try:
            df = pd.read_csv(
                "user_foods.csv"
            )
        except:
            df = pd.DataFrame(
                columns=[
                    "Food_Name",
                    "Time_To_Expiry"
                ]
            )

        if len(df) > 0:

            st.bar_chart(
                df.set_index(
                    "Food_Name"
                )["Time_To_Expiry"]
            )

    # SUSTAINABILITY

    elif mode == "🌍 Sustainability":

        try:
            df = pd.read_csv(
                "user_foods.csv"
            )
        except:
            df = pd.DataFrame(
                columns=[
                    "Food_Name",
                    "Time_To_Expiry"
                ]
            )

        foods_saved = len(df)

        money_saved = foods_saved * 50

        co2_saved = foods_saved * 0.5

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Foods Saved",
            foods_saved
        )

        c2.metric(
            "Money Saved",
            f"₹{money_saved}"
        )

        c3.metric(
            "CO₂ Reduced",
            f"{co2_saved} kg"
        )
# ---------------- LOGIN REGISTER ----------------

menu = ["Login", "Register"]

choice = st.sidebar.selectbox(
    "Menu",
    menu
)

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
                "Account created successfully"
            )

        else:

            st.error(
                "Username already exists"
            )

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
                f"Welcome {username}"
            )

            st.balloons()

        else:

            st.error(
                "Invalid username or password"
            )

    if st.session_state.logged_in:

        show_dashboard(
            st.session_state.username
        )
            
