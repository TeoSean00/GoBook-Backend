from flask import Flask, render_template, request
from contentBasedFilter import get_recommendations
app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Recommendation page
@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the user's viewing history
    history = request.form['history']

    # Make recommendations based on the user's viewing history
    recommendations = get_recommendations(history)

    # Render the recommendations page with the recommendations
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)