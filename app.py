import streamlit as st
import anthropic

api_key = st.secrets["claude_api_key"]

# Function to get a meal plan from Claude AI
def get_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preference):
    # Initialize the client with the API key
    client = anthropic.Anthropic(api_key=api_key)
    
    # Formulate the prompt to send to Claude AI
    prompt = (
        f"You are a world-class nutritionist and dietitian specialized in diabetes management. "
        f"Based on the following information, create a personalized meal plan:\n\n"
        f"Fasting Sugar Level: {fasting_sugar} mg/dL\n"
        f"Pre-Meal Sugar Level: {pre_meal_sugar} mg/dL\n"
        f"Post-Meal Sugar Level: {post_meal_sugar} mg/dL\n"
        f"Dietary Preference: {dietary_preference}\n\n"
        "Please provide a meal plan with breakfast, lunch, dinner, and snacks, considering these blood sugar levels and dietary preference."
    )

    # Make the API request to Claude AI
    messsages = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.7,
        system="You are a world-class nutritionist.",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_context = messsages.content
    itinerary = raw_context[0].text
    return itinerary
# Streamlit App
st.title("Diabetes Mellitus: Personalized Meal Plan")

# Description of the app
st.write("""
This application is designed to help diabetic patients manage their blood sugar levels through personalized meal planning.
By entering your blood sugar readings and dietary preferences, you'll receive meal recommendations tailored to your needs.
""")

# Sidebar for user inputs
st.sidebar.header("Enter Your Information")

# Input for API Key
# api_key = st.sidebar.text_input("API Key", type="password")

# Input fields for sugar levels
fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0, max_value=400)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Level (mg/dL)", min_value=0, max_value=400)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Level (mg/dL)", min_value=0, max_value=400)

# Dietary preferences
dietary_preference = st.sidebar.selectbox(
    "Dietary Preference",
    ("Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Low-Carb")
)

# Button to generate meal plan
if st.sidebar.button("Generate Meal Plan"):
    meal_plan = get_meal_plan(api_key,fasting_sugar,pre_meal_sugar,post_meal_sugar,dietary_preference)
    st.write("Based on your sugar level and dietary preferences, here is the personolized meal plan:")
    st.markdown(meal_plan)
