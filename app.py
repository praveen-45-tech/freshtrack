import streamlit as st
import pandas as pd
import os

try:
    import plotly.express as px
except ModuleNotFoundError:
    px = None

st.write("DEBUG users.db path =", os.path.abspath("users.db"))
from database import *

create_table()

st.set_page_config(
    page_title="FreshTrack",
    page_icon="🥗",
    layout="wide"
)

# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "active_menu" not in st.session_state:
    st.session_state.active_menu = "🏠 Home"

# PAGE HEADER
st.markdown("""
<div style="text-align:center; padding:20px;">
<h1 style="color:#2E7D32; font-size:60px; font-weight:bold;">🥗 FreshTrack</h1>
<h3 style="color:#FF6F00;">AI Smart Food Waste Reduction System</h3>
<p style="font-size:18px; color:gray;">Track • Save • Sustain • Earn Rewards</p>
</div>
""", unsafe_allow_html=True)

# STYLE
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
* { font-family: 'Poppins', sans-serif !important; }
.stApp{ background: linear-gradient(135deg, #F4FFF4, #E8F5E9) !important; }
[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 50%, #1B5E20 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0px 20px rgba(0,0,0,0.25) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label { color: white !important; }

.user-card{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    padding: 20px 15px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.20);
    margin-bottom: 12px;
    text-align: center;
}

.menu-section-title{
    color: rgba(255,255,255,0.65) !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    margin: 12px 0px 6px 0px !important;
    padding-left: 8px !important;
}

.menu-divider{
    height: 1px;
    background: rgba(255,255,255,0.15);
    margin: 10px 10px;
    border-radius: 5px;
}

.stButton button{
    width: 100%;
    border-radius: 16px !important;
    height: 48px !important;
    border: none !important;
    background: transparent !important;
    color: rgba(255,255,255,0.88) !important;
    font-weight: 650 !important;
    font-size: 15px !important;
    padding: 0px 14px !important;
    text-align: left !important;
    transition: all 0.25s ease !important;
    box-shadow: none !important;
}

.stButton button:hover{
    background: rgba(255,255,255,0.18) !important;
    color: white !important;
    transform: translateX(5px);
}

.active-menu button{
    background: linear-gradient(135deg, rgba(255,255,255,0.30), rgba(255,255,255,0.10)) !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
    color: white !important;
    font-weight: 800 !important;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.18) !important;
    transform: translateX(5px);
}

.logout-btn button{
    background: linear-gradient(135deg, #FF5252, #D32F2F) !important;
    color: white !important;
    font-weight: 800 !important;
    box-shadow: 0px 10px 25px rgba(255,82,82,0.25) !important;
    border: none !important;
}

.logout-btn button:hover{
    background: linear-gradient(135deg, #FF6B6B, #C62828) !important;
    transform: scale(1.01);
}

.banner{
    background: linear-gradient(135deg, #00C853, #64DD17);
    padding: 35px;
    border-radius: 25px;
    color: white;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

.stTextInput input,
.stSelectbox select{ border-radius: 15px !important; border: 2px solid #E8F5E9 !important; }
[data-testid="stDataFrame"]{ border-radius: 15px !important; }
.stButton button:focus{ box-shadow: none !important; }
</style>
""", unsafe_allow_html=True)

# DATA
def load_data():
    try:
        return pd.read_csv("user_foods.csv")
    except Exception:
        return pd.DataFrame(columns=["Food_Name", "Category", "Time_To_Expiry"])

def save_data(df):
    df.to_csv("user_foods.csv", index=False)

# SIDEBAR MENU
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

    logout_wrap = st.sidebar.container()
    with logout_wrap:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.active_menu = "🏠 Home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# DASHBOARD CONTENT
def show_dashboard(username):
    df = load_data()
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

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🍎 Total Foods", len(df))
        c2.metric("📂 Categories", df["Category"].nunique() if len(df) > 0 else 0)
        c3.metric("⚠ Expiring Soon", len(df[df["Time_To_Expiry"] <= 3]) if len(df) > 0 else 0)
        c4.metric("✅ Fresh Foods", len(df[df["Time_To_Expiry"] > 3]) if len(df) > 0 else 0)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📂 Quick Categories")

        cats = ["Dairy", "Fruit", "Vegetable", "Bakery"]
        cols = st.columns(4)
        for i, cat in enumerate(cats):
            if cols[i].button(cat, key=f"cat_{cat}"):
                st.dataframe(df[df["Category"] == cat], use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
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

        food_option = st.selectbox(
            "Select Food",
            ["Milk", "Apple", "Banana", "Bread", "Egg", "Tomato", "Others"]
        )
        food = st.text_input("Enter Food Name") if food_option == "Others" else food_option

        category_option = st.selectbox(
            "Select Category",
            ["Dairy", "Fruit", "Vegetable", "Bakery", "Protein", "Beverage", "Others"]
        )
        Category = st.text_input("Enter Category Name") if category_option == "Others" else category_option

        added_date = st.date_input("📅 Added Date")
        expiry_date = st.date_input("📅 Expiry Date")

        if st.button("💾 Save Food"):
            days = (expiry_date - added_date).days
            df.loc[len(df)] = {
                "Food_Name": food,
                "Category": Category,
                "Time_To_Expiry": days
            }
            save_data(df)
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
            score = min(100, int((days / 30) * 100))
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
                st.error(f"🚨 {row['Food_Name']} expires tomorrow")
            elif row["Time_To_Expiry"] <= 3:
                found = True
                st.warning(f"⚠ {row['Food_Name']} expires soon")
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
                return

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
        rewards = len(df) * 10
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

# MAIN APP
# MAIN APP
if st.session_state.logged_in:
    show_dashboard(st.session_state.username)
else:
    choice = st.sidebar.selectbox("Menu", ["Login", "Register"])

    st.markdown("### ")

    if choice == "Register":
        st.markdown("""
        <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 5px 15px rgba(0,0,0,0.1);
        text-align:center;
        ">
        <h2>📝 Create FreshTrack Account</h2>
        <p>Start saving food and earn rewards</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("register_form"):
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Register")

            if submitted:
                if add_user(new_user, new_password):
                    st.success("Account Created")
                    st.session_state.logged_in = True
                    st.session_state.username = new_user
                    st.rerun()
                else:
                    st.error("Username Already Exists")

    else:
        st.markdown("""
        <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 5px 15px rgba(0,0,0,0.1);
        text-align:center;
        ">
        <h2>🔐 Login to FreshTrack</h2>
        <p>Manage your foods and reduce waste smartly</p>
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
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
