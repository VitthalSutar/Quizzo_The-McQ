from flask import Flask, request, jsonify, session, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/quizdb")
mongo = PyMongo(app)

# Serve all frontend HTML files dynamically
@app.route('/', defaults={'page': 'index'})
@app.route('/<page>')
def serve_page(page):
    try:
        return render_template(f"{page}.html")
    except:
        return render_template("index.html")

# (Optional) You can remove all API endpoints below if you want to remove API routes as well.
# If you want to keep API functionality, leave the following code.
# If you want to remove API routes, delete everything below this comment.

# User registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    if mongo.db.users.find_one({'username': username}):
        return jsonify({"msg": "User already exists"}), 409
    hashed_pw = generate_password_hash(password)
    mongo.db.users.insert_one({'username': username, 'password': hashed_pw, 'role': role})
    return jsonify({"msg": "User registered"}), 201

# User login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        session['role'] = user.get('role', 'user')
        return jsonify({"msg": "Login successful", "role": user.get('role', 'user')}), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

# User logout
@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"msg": "Logged out"})

# Admin: Add quiz
@app.route('/api/quiz', methods=['POST'])
def add_quiz():
    if session.get('role') != 'admin':
        return jsonify({"msg": "Admins only"}), 403
    data = request.json
    mongo.db.quizzes.insert_one(data)
    return jsonify({"msg": "Quiz added"}), 201

# Get available quizzes
@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    # Fetch all quizzes from the database
    quizzes = list(mongo.db.quizzes.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
    return jsonify(quizzes)

# Submit quiz performance
@app.route('/api/performance', methods=['POST'])
def submit_performance():
    if 'username' not in session:
        return jsonify({"msg": "Unauthorized"}), 401

    data = request.json
    username = session['username']
    answers = data.get('answers')
    correct_count = data.get('correctCount')

    # Store the performance in the database
    performance = {
        "username": username,
        "answers": answers,
        "correct_count": correct_count,
        "submitted_at": datetime.utcnow()  # Add a timestamp
    }
    mongo.db.performances.insert_one(performance)

    return jsonify({"msg": "Performance recorded successfully"}), 201

# Get user performance
@app.route('/api/performance', methods=['GET'])
def get_performance():
    quiz_title = request.args.get('quiz_title')  # Get the quiz title from query parameters
    query = {}
    if quiz_title:
        query['quiz_title'] = quiz_title  # Filter by quiz title if provided
    performances = list(mongo.db.performances.find(query, {'_id': 0}))  # Fetch performances, exclude MongoDB's _id field
    return jsonify(performances)

if __name__ == '__main__':
    app.run(debug=True)