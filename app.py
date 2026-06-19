import streamlit as st
import pandas as pd
import os
import yagmail
import json


def send_expiry_email(receiver_email, food_name, days):

    try:
        sender_email = st.secrets.get("FRESHTRACK_EMAIL", os.environ.get("FRESHTRACK_EMAIL"))
        sender_app_password = st.secrets.get("FRESHTRACK_APP_PASSWORD", os.environ.get("FRESHTRACK_APP_PASSWORD"))

        if not sender_email or not sender_app_password:
            print("Email credentials not set. Set FRESHTRACK_EMAIL and FRESHTRACK_APP_PASSWORD environment variables.")
            return False

        yag = yagmail.SMTP(
            sender_email,
            sender_app_password
        )

        subject = "FreshTrack Expiry Alert"

        body = f"""
Hello,

Your food item "{food_name}" will expire in {days} day(s).

Please consume it soon to reduce food waste.

FreshTrack Team 🌱
"""

        yag.send(
            to=receiver_email,
            subject=subject,
            contents=body
        )

        return True

    except Exception as e:
        print(e)
        return False


try:
    import plotly.express as px
except ModuleNotFoundError:
    px = None

st.set_page_config(
    page_title="FreshTrack",
    page_icon="🥗",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, .stApp {
    font-family: 'Poppins', sans-serif !important;
    background: #F7F9FC !important;
    color: #111827 !important;
}

h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: #111827 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F3D1E 0%, #1B5E20 50%, #0F3D1E 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0px 20px rgba(0,0,0,0.25) !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6 {
    color: white !important;
}

.user-card {
    background: rgba(255,255,255,0.14);
    backdrop-filter: blur(10px);
    padding: 20px 15px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.20);
    margin-bottom: 12px;
    text-align: center;
}

.menu-section-title {
    color: rgba(255,255,255,0.75) !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    margin: 12px 0px 6px 0px !important;
    padding-left: 8px !important;
}

.menu-divider {
    height: 1px;
    background: rgba(255,255,255,0.18);
    margin: 10px 10px;
    border-radius: 5px;
}

.stButton button {
    width: 100%;
    border-radius: 16px !important;
    height: 48px !important;
    border: none !important;
    background: transparent !important;
    color: rgba(255,255,255,0.95) !important;
    font-weight: 650 !important;
    font-size: 15px !important;
    padding: 0px 14px !important;
    text-align: left !important;
    transition: all 0.25s ease !important;
    box-shadow: none !important;
}

.stButton button:hover {
    background: rgba(255,255,255,0.18) !important;
    color: white !important;
    transform: translateX(5px);
}

.active-menu button {
    background: linear-gradient(135deg, rgba(255,255,255,0.30), rgba(255,255,255,0.10)) !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
    color: white !important;
    font-weight: 800 !important;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.18) !important;
    transform: translateX(5px);
}

.logout-btn button {
    background: linear-gradient(135deg, #FF5252, #D32F2F) !important;
    color: white !important;
    font-weight: 800 !important;
    box-shadow: 0px 10px 25px rgba(255,82,82,0.25) !important;
    border: none !important;
}

.logout-btn button:hover {
    background: linear-gradient(135deg, #FF6B6B, #C62828) !important;
    transform: scale(1.01);
}

.banner {
    background: linear-gradient(135deg, #00C853, #64DD17);
    padding: 35px;
    border-radius: 25px;
    color: white !important;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

.banner h1, .banner p {
    color: white !important;
}

.stTextInput input,
.stSelectbox div,
.stDateInput input,
textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 15px !important;
}

.stTextInput label,
.stSelectbox label,
.stDateInput label {
    color: #111827 !important;
    font-weight: 600 !important;
}

[data-testid="stDataFrame"] {
    border-radius: 15px !important;
}

.stForm {
    background: #FFFFFF !important;
    padding: 18px !important;
    border-radius: 18px !important;
    border: 1px solid #E5E7EB !important;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.06) !important;
}
</style>
""", unsafe_allow_html=True)

from database import *

create_table()

LOGIN_FILE = "login.json"

if os.path.exists(LOGIN_FILE):
    try:
        with open(LOGIN_FILE, "r") as f:
            data = json.load(f)
            st.session_state.logged_in = True
            st.session_state.username = data["username"]
    except:
        pass

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "active_menu" not in st.session_state:
    st.session_state.active_menu = "🏠 Home"


def get_user_file(username):
    return f"{username}_foods.csv"


def load_data(username):
    file_name = get_user_file(username)
    try:
        return pd.read_csv(file_name)
    except:
        return pd.DataFrame(
            columns=["Food_Name", "Category", "Time_To_Expiry"]
        )


def save_data(df, username):
    file_name = get_user_file(username)
    df.to_csv(file_name, index=False)


def render_sidebar_menu(username: str):
    st.sidebar.markdown(f"""
    <div class="user-card">
        <div style="font-size:44px; margin-bottom:8px;">👨‍🍳</div>
        <div style="font-size:17px; font-weight:800;">{username}</div>
        <div style="font-size:12px; opacity:0.85; margin-top:4px;">⭐ Premium Member</div>
        <div style="display:inline-block; margin-top:10px; background:rgba(255,255,255,0.2); padding:4px 12px; border-radius:999px; font-size:11px;">
            🟢 Active
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="menu-section-title">📱 Navigation</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True)

    menu_top = [
        ("🏠", "Home", "🏠 Home"),
        ("➕", "Add Food", "➕ Add Food"),
        ("📂", "Categories", "📂 Categories"),
        ("📊", "Dashboard", "📊 Dashboard"),
        ("🤖", "AI Prediction", "🤖 AI Prediction"),
        ("⚠️", "Expiry Alerts", "⚠️ Expiry Alerts"),
        ("🍲", "Recipe Suggestions", "🍲 Recipe Suggestions"),
        ("📈", "Analytics", "📈 Analytics"),
        ("🌍", "Sustainability", "🌍 Sustainability"),
        ("🏆", "Rewards", "🏆 Rewards"),
        ("👤", "Profile", "👤 Profile"),
    ]

    for icon, label, key in menu_top:
        is_active = st.session_state.active_menu == key
        wrapper_cls = "active-menu" if is_active else ""
        st.sidebar.markdown(f'<div class="{wrapper_cls}">', unsafe_allow_html=True)
        if st.sidebar.button(f"{icon}  {label}", key=f"menu_{key}", use_container_width=True):
            st.session_state.active_menu = key
            st.rerun()
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="logout-btn">', unsafe_allow_html=True)

    if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.active_menu = "🏠 Home"
        if os.path.exists(LOGIN_FILE):
            os.remove(LOGIN_FILE)
        st.rerun()

    st.sidebar.markdown('</div>', unsafe_allow_html=True)


def show_dashboard(username):
    df = load_data(username)
    render_sidebar_menu(username)
    mode = st.session_state.active_menu

    if mode == "🏠 Home":
        st.markdown("""
        <div class="banner">
            <h1 style="font-size:48px; margin-bottom:8px;">🥗 FreshTrack</h1>
            <p style="font-size:20px; opacity:0.92;">Track • Save • Sustain • Earn Rewards</p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🔎 Search Food")
        search = st.text_input("Search by Food Name")

        if search:
            result = df[df["Food_Name"].str.contains(search, case=False, na=False)]
            if len(result) > 0:
                st.success("✅ Food Found")
                st.dataframe(result, use_container_width=True)
            else:
                st.error("❌ Food Not Found")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🍎 Total Foods", len(df))
        c2.metric("📂 Categories", df["Category"].nunique() if len(df) > 0 else 0)
        c3.metric("⚠ Expiring Soon", len(df[df["Time_To_Expiry"] <= 3]) if len(df) > 0 else 0)
        c4.metric("✅ Fresh Foods", len(df[df["Time_To_Expiry"] > 3]) if len(df) > 0 else 0)

        st.subheader("📂 Quick Categories")
        cats = ["Dairy", "Fruit", "Vegetable", "Bakery"]
        cols = st.columns(4)
        for i, cat in enumerate(cats):
            if cols[i].button(cat, key=f"cat_{cat}"):
                st.dataframe(df[df["Category"] == cat], use_container_width=True)

        st.subheader("🔥 All Foods")
        for i, row in df.iterrows():
            if st.button(f"🍽 {row['Food_Name']}", key=f"food_{i}"):
                st.info(
                    f"**Food:** {row['Food_Name']}\n\n"
                    f"**Category:** {row['Category']}\n\n"
                    f"**Days Left:** {row['Time_To_Expiry']}"
                )

    elif mode == "➕ Add Food":
        st.subheader("➕ Add New Food")
        food_option = st.selectbox("Select Food", ["Milk", "Apple", "Banana", "Bread", "Egg", "Tomato", "Others"])
        food = st.text_input("Enter Food Name") if food_option == "Others" else food_option
        category_option = st.selectbox("Select Category", ["Dairy", "Fruit", "Vegetable", "Bakery", "Protein", "Beverage", "Others"])
        category = st.text_input("Enter Category Name") if category_option == "Others" else category_option
        added_date = st.date_input("📅 Added Date")
        expiry_date = st.date_input("📅 Expiry Date")

        if st.button("💾 Save Food"):
            days = (expiry_date - added_date).days
            duplicate = df[df["Food_Name"].str.lower() == food.lower()]

            if len(duplicate) > 0:
                st.error("❌ Food already exists! Please enter a different food.")
            else:
                df.loc[len(df)] = {
                    "Food_Name": food,
                    "Category": category,
                    "Time_To_Expiry": days
                }
                save_data(df, username)
                st.success("✅ Food Added Successfully!")
                st.balloons()

    elif mode == "📂 Categories":
        st.subheader("📂 Food Categories")
        st.dataframe(df[["Food_Name", "Category"]], use_container_width=True)

    elif mode == "📊 Dashboard":
        st.subheader("📊 Full Food Dashboard")
        st.dataframe(df, use_container_width=True)

    elif mode == "🤖 AI Prediction":
        st.subheader("🤖 AI Freshness Prediction")
        if len(df) > 0:
            food = st.selectbox("Select Food", df["Food_Name"])
            days = int(df[df["Food_Name"] == food]["Time_To_Expiry"].values[0])
            score = min(100, max(0, int((days / 30) * 100)))
            st.metric("Freshness Score", f"{score}%")
            st.progress(score / 100)
        else:
            st.info("No data available. Add food first.")

    elif mode == "⚠️ Expiry Alerts":
        st.subheader("⚠ Expiry Alerts")
        found = False
        for _, row in df.iterrows():
            if row["Time_To_Expiry"] <= 1:
                found = True
                st.toast(f"🚨 {row['Food_Name']} expires tomorrow")
            elif row["Time_To_Expiry"] <= 3:
                found = True
                email = get_email(username)

                if email:
                    send_expiry_email(
                        email,
                        row["Food_Name"],
                        row["Time_To_Expiry"]
                    )

                st.warning(
                    f"{row['Food_Name']} expires soon"
                )

        if not found:
            st.success("✅ No expiry alerts")

    elif mode == "🍲 Recipe Suggestions":
        st.subheader("🍲 Recipe Suggestions")
        st.info("""
🥛 Milk → Milkshake
🍎 Apple → Apple Pie
🍞 Bread → Sandwich
🥚 Egg → Omelette
""")

    elif mode == "📈 Analytics":
        st.subheader("📈 Food Analytics Dashboard")
        if len(df) > 0:
            if px is None:
                st.error("plotly is not available. Add it to requirements.txt and redeploy.")
            else:
                fig = px.bar(
                    df,
                    x="Food_Name",
                    y="Time_To_Expiry",
                    color="Category",
                    title="Food Expiry Analysis"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig2 = px.pie(
                    df,
                    names="Category",
                    title="Food Category Distribution"
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data available")

    elif mode == "🌍 Sustainability":
        st.subheader("🌍 FreshTrack Sustainability Score")
        foods_saved = len(df)
        fresh_foods = len(df[df["Time_To_Expiry"] > 3])
        points = foods_saved * 5 + fresh_foods * 10

        c1, c2, c3 = st.columns(3)
        c1.metric("🥗 Foods Saved", foods_saved)
        c2.metric("💰 Money Saved", f"₹{foods_saved * 50}")
        c3.metric("🌍 CO₂ Reduced", f"{foods_saved * 0.5} kg")

        st.markdown("---")
        st.subheader("🏆 FreshTrack Reward Points")
        st.metric("⭐ Total Points", points)

        progress = min(points / 100, 1.0)
        st.progress(progress)

        if points >= 100:
            st.success("🏅 Green Hero Badge Unlocked!")
        elif points >= 50:
            st.info("🌱 Eco Saver Badge Unlocked!")
        else:
            st.warning(f"Earn {100 - points} more points to unlock Green Hero Badge")

    elif mode == "🏆 Rewards":
        st.subheader("🏆 FreshTrack Rewards")
        fresh_foods = len(df[df["Time_To_Expiry"] > 3])
        rewards = fresh_foods * 20

        st.metric("FreshTrack Points", rewards)
        st.success(f"You earned {rewards} points for saving food!")
        st.progress(min(rewards / 500, 1.0))
        st.info("🎁 500 Points = Premium Badge")

    elif mode == "👤 Profile":
        st.subheader("👤 User Profile")
        st.write("Username:", username)
        st.write("Foods Added:", len(df))
        st.write("Categories Used:", df["Category"].nunique() if len(df) > 0 else 0)
        st.write("FreshTrack Points:", len(df) * 10)


if st.session_state.logged_in:
    show_dashboard(st.session_state.username)
else:
    choice = st.sidebar.selectbox("Menu", ["Login", "Register"])

    if choice == "Register":
        st.markdown("""
        <div style="
        background:#FFFFFF;
        color:#111827;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 5px 15px rgba(0,0,0,0.08);
        text-align:center;
        border:1px solid #E5E7EB;
        ">
        <h2 style="color:#111827;">📝 Create FreshTrack Account</h2>
        <p style="color:#374151;">Start saving food and earn rewards</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("register_form"):
            new_user = st.text_input("Username")
            email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Register")

            if submitted:
                if add_user(new_user, new_password, email):
                    st.success("✅ Account Created Successfully!")
                    st.session_state.logged_in = True
                    st.session_state.username = new_user

                    with open(LOGIN_FILE, "w") as f:
                        json.dump({"username": new_user}, f)

                    st.rerun()
                else:
                    st.error("❌ Username Already Exists")

    else:
        st.markdown("""
        <div style="
        background:#FFFFFF;
        color:#111827;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 5px 15px rgba(0,0,0,0.08);
        text-align:center;
        border:1px solid #E5E7EB;
        ">
        <h2 style="color:#111827;">🔐 Login to FreshTrack</h2>
        <p style="color:#374151;">Manage your foods and reduce waste smartly</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                ok = login_user(username, password)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.username = username

                    with open(LOGIN_FILE, "w") as f:
                        json.dump({"username": username}, f)

                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password")
