from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()  

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Load API key securely

from flask import Flask, render_template, request
import google.generativeai as genai
import markdown  # Import markdown module to convert markdown text to HTML

app = Flask(__name__)

# Set up Gemini API using the securely loaded API key
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    raise ValueError("API key not found. Please ensure GOOGLE_API_KEY is set in your .env file.")

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET", "POST"])
def index():
    scholarships = None
    advice = None

    if request.method == "POST":
        # Get user inputs securely
        name = request.form.get("name")
        gpa = float(request.form.get("gpa"))  # Ensure GPA is treated as a number
        study_field = request.form.get("study_field")
        study_area = request.form.get("study_area")

        if not name or not study_field or not study_area:
            return "All fields are required!"  # Basic validation for empty fields

        # Generate prompt for Gemini
        prompt = f"Generate personalized scholarship opportunities for a student named {name} with a GPA of {gpa} who wants to study {study_field} in {study_area}. Provide tailored advice based on GPA and field of study."

        try:
            # Send the prompt to Gemini and get the response
            response = model.generate_content(prompt)
            scholarships = format_scholarship_response(response.text)
            advice = generate_advice(gpa, study_field)
        except Exception as e:
            return f"An error occurred while processing your request: {e}"

    return render_template("index.html", scholarships=scholarships, advice=advice)

def format_scholarship_response(response_text):
    # Convert markdown response to HTML
    html_response = markdown.markdown(response_text)  # Convert markdown to HTML
    formatted_response = f"<h2>Scholarship Opportunities:</h2>{html_response}"
    return formatted_response

def generate_advice(gpa, study_field):
    # Generate personalized advice based on GPA and study field
    advice = ""

    # GPA-based advice
    if gpa < 3.0:
        advice += "<p><strong>Advice:</strong> Your GPA is below 3.0, which may limit scholarship opportunities. Consider improving your GPA through additional coursework or retaking exams if possible. Focus on extracurricular activities to make your application stand out.</p>"
    elif 3.0 <= gpa < 3.5:
        advice += "<p><strong>Advice:</strong> A GPA between 3.0 and 3.5 can still qualify you for many scholarships, but competition may be tougher. Look for scholarships that emphasize holistic review (including extracurriculars, essays, etc.).</p>"
    else:
        advice += "<p><strong>Advice:</strong> With a GPA above 3.5, you are a strong candidate for many merit-based scholarships. Focus on your area of study and apply for competitive scholarships in your field.</p>"

    # Add bonus tips for specific study fields
    if study_field.lower() == "computer science":
        advice += "<p><strong>Bonus Tip:</strong> In the field of Computer Science, many companies and organizations offer scholarships, particularly if you are interested in artificial intelligence, machine learning, or data science. Don't forget to apply for tech company-sponsored scholarships.</p>"
    elif study_field.lower() == "law":
        advice += "<p><strong>Bonus Tip:</strong> Law students with strong academic records can apply for various law society scholarships. Explore opportunities with international law firms or NGOs if you are interested in social justice.</p>"

    return advice

if __name__ == "__main__":
    app.run(debug=True)
