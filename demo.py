import streamlit as st

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Energy Consumption Estimator",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- App Title and Description ---
st.title("⚡ Home Energy Consumption Estimator ⚡")
st.markdown(
    """
    Welcome! This simple app helps you estimate your home's energy consumption
    based on your living situation and appliance usage.
    """
)

st.divider()

# --- User Input Section ---
st.header("🏡 Your Living Situation")

# Input for name
name = st.text_input("What is your name?", placeholder="John Doe")

# Input for age with validation
age = st.number_input(
    "What is your age?",
    min_value=1,
    max_value=120,
    value=30, # Default value
    step=1
)

# Input for city and area
city = st.text_input("Which city do you live in?", placeholder="Mumbai")
area = st.text_input("What is your area name?", placeholder="Bandra")

# Input for flat or tenement
flat_tenament = st.radio(
    "Are you living in a Flat or a Tenament?",
    ("Flat", "Tenament"),
    index=0 # Default to Flat
)

# Input for BHK type
facility = st.radio(
    "What type of home do you live in?",
    ("1BHK", "2BHK", "3BHK"),
    index=1 # Default to 2BHK
)

st.header("🔌 Your Appliance Usage")

# Checkboxes for appliance usage
ac_usage = st.checkbox("Are you using an AC?")
fridge_usage = st.checkbox("Are you using a Fridge?")
wm_usage = st.checkbox("Are you using a Washing Machine?")

st.divider()

# --- Energy Calculation Logic ---
cal_energy = 0 # Initialize energy calculation

# Base energy calculation based on BHK type
# These values are illustrative; adjust them based on real-world data or your specific metric.
if facility == "1BHK":
    cal_energy += 5  # Example base energy for 1BHK
elif facility == "2BHK":
    cal_energy += 8  # Example base energy for 2BHK
elif facility == "3BHK":
    cal_energy += 12 # Example base energy for 3BHK

# Add energy for appliances if used
if ac_usage:
    cal_energy += 3  # Example energy for AC
if fridge_usage:
    cal_energy += 2  # Example energy for Fridge
if wm_usage:
    cal_energy += 1.5 # Example energy for Washing Machine

# --- Display Results ---
st.header("📊 Your Estimated Energy Consumption")

if st.button("Calculate Energy"):
    if not name or not city or not area:
        st.warning("Please fill in all the required personal information.")
    else:
        st.subheader("Summary of Your Inputs:")
        st.write(f"**Name:** {name}")
        st.write(f"**Age:** {age}")
        st.write(f"**City:** {city}")
        st.write(f"**Area:** {area}")
        st.write(f"**Living in:** {flat_tenament}")
        st.write(f"**Home Type:** {facility}")
        st.write(f"**Using AC:** {'Yes' if ac_usage else 'No'}")
        st.write(f"**Using Fridge:** {'Yes' if fridge_usage else 'No'}")
        st.write(f"**Using Washing Machine:** {'Yes' if wm_usage else 'No'}")

        st.markdown("---")
        st.success(f"**Your Estimated Energy Consumption: {cal_energy:.2f} units**")
        st.info("*(Note: These 'units' are illustrative and represent a simplified energy metric. For actual consumption, consult your utility bill or energy audit.)*")

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)
