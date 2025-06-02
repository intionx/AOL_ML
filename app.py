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

col1, col2= st.columns(2)

with col1:
    st.subheader("Location")
    proximity_industrial = st.number_input("Proximity to Industrial Areas", min_value=0.0, max_value=50.0)

def get_ind_category(indvalue):
    if indvalue <= 1:
        return "Severe 🟣"
    elif indvalue <= 3:
        return "Poor 🟠"
    elif indvalue <= 10:
        return "Normal 🟡"
    else:
        return "Good 🟢"
indcategory = get_ind_category(proximity_industrial)
st.markdown(f"**Category:** {indcategory}")


with col2:
    st.subheader("Temperature")
    temperature = st.number_input("Select Temperature (°C)", min_value=-5.0, max_value=60.0, value=25.0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Humidity")
    humidity = st.number_input("Select Humidity (%)", min_value=0.0, max_value=130.0, value=50.0)
def get_hum_category(humvalue):
    if humvalue <= 30:
        return "Dry"
    elif humvalue <= 60:
        return "Ideal"
    else:
        return "Humid"
humcategory = get_hum_category(humidity)
st.markdown(f"**Category:** {humcategory}")

with col2:
    st.subheader("Population Density")
    population_density = st.number_input("Population Density", min_value=0.0, max_value=100000.0)




def get_pm10_category(pm10value):
    if pm10value <= 50:
        return "Good 🟢"
    elif pm10value <= 100:
        return "Normal 🟡"
    elif pm10value <= 250:
        return "Poor 🟠"
    else:
        return "Severe 🟣"
st.subheader("PM10 Level")
pm10 = st.slider("Select PM10 level (μg/m³)", min_value=0.0, max_value=320.0, step=0.1, value=50.0, help="Particulate Matter ≤10 micrometers in diameter (μg/m³)")
pm10category = get_pm10_category(pm10)
st.markdown(f"**Category:** {pm10category}")

def get_pm25_category(pm25value):
    if pm25value <= 12:
        return "Good 🟢"
    elif pm25value <= 35.4:
        return "Normal 🟡"
    elif pm25value <= 55.4:
        return "Poor 🟠"
    else:
        return "Severe 🟣"
st.subheader("PM2.5 Level")
pm25 = st.slider("Select PM2.5 level (μg/m³)", min_value=0.0, max_value=300.0, step=0.1, value=25.0, help="Fine particulate matter (μg/m³)")
pm25category = get_pm25_category(pm25)
st.markdown(f"**Category:** {pm25category}")

def get_no2_category(no2value):
    if no2value <= 20:
        return "Good 🟢"
    elif no2value <= 53:
        return "Normal 🟡"
    elif no2value <= 75:
        return "Poor 🟠"
    else:
        return "Severe 🟣"
st.subheader("NO₂ Level")
no2 = st.slider("Select NO₂ level (ppb)", min_value=0.0, max_value=100.0, step=1.0, value=50.0, help="Nitrogen Dioxide level in parts per billion (ppb)")
no2category = get_no2_category(no2)
st.markdown(f"**Category:** {no2category}")

def get_so2_category(so2):
    if so2 <= 10:
        return "Good 🟢"
    elif so2 <= 40:
        return "Normal 🟡"
    elif so2 <= 50:
        return "Poor 🟠"
    else:
        return "Severe 🟣"
st.subheader("SO₂ Level")
so2 = st.slider("Select SO₂ level (ppb)", min_value=0.0, max_value=50.0, step=1.0, value=30.0, help="Sulfur Dioxide level in parts per billion (ppb)")
so2category = get_so2_category(so2)
st.markdown(f"**Category:** {so2category}")

def get_co_category(covalue):
    if covalue <= 1:
        return "Good 🟢"
    elif covalue <= 9:
        return "Normal 🟡"
    elif covalue <= 35:
        return "Poor 🟠"
    elif covalue <= 70:
        return "Very Poor 🔴"
    else:
        return "Severe 🟣"
st.subheader("CO Level")
co = st.slider("Select CO level (ppm)", min_value=0.0, max_value=100.0, step=0.1, value=5.0, help="Carbon Monoxide level in parts per million (ppm)")
cocategory = get_co_category(co)
st.markdown(f"**Category:** {cocategory}")

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
