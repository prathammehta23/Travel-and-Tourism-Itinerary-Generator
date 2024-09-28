from flask import Flask, render_template, request, jsonify
import warnings
warnings.filterwarnings('ignore')

# Import necessary classes from langchain_google_genai
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew

# Create a Flask app
app = Flask(__name__)

@app.route('/')
def home():
    # Serve the HTML page
    return render_template('index.html')

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    # Get data from the POST request (from the form)
    location = request.json.get('city')
    number_of_days = request.json.get('days')

    # Your logic to generate the itinerary
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.5,
        verbose=True,
        google_api_key="AIzaSyCPD-4v0Hklwzn_Xk4SnMQWLWtkx5DNvf4"
    )
    Content_generator = Agent(
        role="Content Generator",
        goal=f"Planning an itinerary for the city: {location} for {number_of_days} days.",
        backstory="You are a master at scraping different famous site locations in the city and understanding "
                  "the best time to visit those places. You also calculate the cost of visiting each location.",
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
        description=(f"Plan an itinerary for {location} for {number_of_days} days. "
                     f"Include costs for activities, food, travel, and accommodation."),
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

    # Return the result to the frontend as JSON
    return jsonify({'itinerary': result})

if __name__ == '__main__':
    app.run(debug=True)
