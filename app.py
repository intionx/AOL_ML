import streamlit as st
import numpy as np
import joblib

model = joblib.load("air_quality_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

st.set_page_config(
    page_title="Air Quality Predictor",
    page_icon="wind.png",                        
    layout="centered",                  
    initial_sidebar_state="auto"
)

st.title("Air Quality Index (AQI) Prediction")
st.markdown("Enter environmental conditions to predict the air quality.")

region_defaults = {
    "Central Jakarta": {"pop_density": 23000, "industrial_proximity": 3.0},
    "West Jakarta": {"pop_density": 20000, "industrial_proximity": 6.0},
    "East Jakarta": {"pop_density": 11000, "industrial_proximity": 7.5},
    "North Jakarta": {"pop_density": 12000, "industrial_proximity": 4.0},
    "South Jakarta": {"pop_density": 15000, "industrial_proximity": 8.0},
}


col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Location")
    region = st.selectbox(
        "Which part of Jakarta are you in?",
        ("Central Jakarta", "West Jakarta", "East Jakarta", "North Jakarta", "South Jakarta")
    )


with col2:
    st.subheader("Temperature")
    temperature = st.number_input("Select Temperature (°C)", min_value=-5.0, max_value=60.0, value=25.0)

with col3:
    st.subheader("Humidity")
    humidity = st.number_input("Select Humidity (%)", min_value=0.0, max_value=130.0, value=50.0)

population_density = region_defaults[region]["pop_density"]
proximity_industrial = region_defaults[region]["industrial_proximity"]

st.markdown(f"**Population Density:** {population_density} people/km²")
st.markdown(f"**Proximity to Industrial Areas:** {proximity_industrial} km")


st.subheader("PM10 Level")
pm10 = st.slider("Select PM10 level (μg/m³)", min_value=0.0, max_value=320.0, step=0.1, value=50.0, help="Particulate Matter ≤10 micrometers in diameter (μg/m³)")

st.subheader("PM2.5 Level")
pm25 = st.slider("Select PM2.5 level (μg/m³)", min_value=0.0, max_value=300.0, step=0.1, value=25.0, help="Fine particulate matter (μg/m³)")

st.subheader("NO₂ Level")
no2 = st.slider("Select NO₂ level (ppb)", min_value=0.0, max_value=100.0, step=1.0, value=50.0, help="Nitrogen Dioxide level in parts per billion (ppb)")


st.subheader("SO₂ Level")
so2 = st.slider("Select SO₂ level (ppb)", min_value=0.0, max_value=200.0, step=1.0, value=30.0, help="Sulfur Dioxide level in parts per billion (ppb)")

st.subheader("CO Level")
co = st.slider("Select CO level (ppm)", min_value=0.0, max_value=410.0, step=0.1, value=5.0, help="Carbon Monoxide level in parts per million (ppm)")

population_density = region_defaults[region]["pop_density"]
proximity_industrial = region_defaults[region]["industrial_proximity"]

if st.button("🔍 Predict"):
    user_input = np.array([[temperature, humidity, pm25, pm10, no2, so2, co, proximity_industrial, population_density]])

    prediction = model.predict(user_input)[0]
    predicted_label = label_encoder.inverse_transform([prediction])[0]

    category_map = {
        "Good": "Good 🟢",
        "Moderate": "Moderate 🟡",
        "Poor": "Poor 🔴",
        "Hazardous": "Hazardous 🟣"
    }

    display_label = category_map.get(predicted_label, predicted_label)

    st.success(f"Predicted Air Quality: **{display_label}**")

    if predicted_label == "Good":
        st.info("""
        🟢 **Good Air Quality**

        - **Do:** Enjoy all outdoor activities freely! It's a perfect time to be outside.
        - **At Home:** Open windows to ventilate your home with fresh air.
        - **Health:** No specific health precautions needed for anyone.
        """)
    elif predicted_label == "Moderate":
        st.warning("""
        🟡 **Moderate Air Quality**

        - **Do:** Most outdoor activities are generally fine for the majority of people.
        - **Caution:** Sensitive individuals (children, elderly, those with heart/lung conditions) should reduce the intensity or duration of heavy outdoor exertion.
        - **At Home:** Usually okay to ventilate, but monitor pollutant levels if sensitive.
        """)
    elif predicted_label == "Poor":
        st.error("""
        🔴 **Poor (Unhealthy) Air Quality**

        - **Do:** Reduce prolonged or strenuous outdoor activities. Prioritize staying indoors.
        - **Protection:** Wear an N95 or KN95 mask if going outside.
        - **At Home:** Keep windows closed. Use air purifiers if available.
        """)
    elif predicted_label == "Hazardous":
        st.error("""
        🟣 **Hazardous Air Quality**

        - **Do:** Stay indoors. Avoid all outdoor physical activity.
        - **Protection:** If unavoidable, wear a well-fitted N95 or P100 respirator.
        - **At Home:** Keep windows and doors closed. Use air purifiers on high setting.
        """)
