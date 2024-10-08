# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import warnings
warnings.filterwarnings('ignore')

# Import your necessary modules (assuming they are installed)
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew

app = Flask(__name__)
CORS(app)  # Enables Cross-Origin Resource Sharing (if needed)

@app.route('/')
def home():
    # Render the HTML template
    return render_template('index.html')

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    # Get data from the frontend
    data = request.get_json()
    location = data.get('city')
    number_of_days = data.get('days')

    # For debugging purposes
    print(f"Received location: {location}, number_of_days: {number_of_days}")

    # Your logic to generate the itinerary
    # Here, we'll use a placeholder for the result
    # Replace this with your actual code

    # Example of your code (Commented out since external libraries are not available)
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        verbose=True,
        google_api_key="AIzaSyCPD-4v0Hklwzn_Xk4SnMQWLWtkx5DNvf4"
    )
    Content_generator = Agent(
        role="Content Generator",
        goal=f"Planning an itinerary for the city: {location} for {number_of_days} days.",
        backstory="You are a master at scraping different famous site locations in the city and understanding the best time to visit those places. You also calculate the cost of visiting each location.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    Content_editor = Agent(
        role="Content Editor",
        goal=f"Align the locations for {location} and create a detailed itinerary for {number_of_days} days.",
        backstory="You excel at organizing the places to visit and making the itinerary easy to follow.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    plan = Task(
        description=(f"Plan an itinerary for {location} for {number_of_days} days. Include costs for activities, food, travel, and accommodation."),
        expected_output="A detailed daily itinerary with expenses for entry, food, travel, and accommodation.",
        agent=Content_generator
    )

    write = Task(
        description="Format the itinerary in an easy-to-read way with the expenses clearly listed.",
        expected_output="A well-organized output in rows with clear day-wise expense breakdown.",
        agent=Content_editor
    )

    crew = Crew(
        agents=[Content_generator, Content_editor],
        tasks=[plan, write],
        verbose=2
    )

    result = crew.kickoff()


    # Return the result as JSON
    return jsonify({'itinerary': result})

if __name__ == '__main__':
    app.run(debug=True)
