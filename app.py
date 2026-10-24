

from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

TASK_LIBRARY = {
    "study": [
        "Choose one small topic and read its basics.",
        "Write 5 important points from what you learned.",
        "Solve 3 beginner practice questions.",
        "Review yesterday's notes for a few minutes.",
        "Explain one concept in your own words.",
        "Practice one topic you find difficult.",
        "Take a short quiz and review your mistakes."
    ],
    "coding": [
        "Learn one programming concept.",
        "Write a small program using that concept.",
        "Solve one beginner coding problem.",
        "Read and understand a short code example.",
        "Fix one bug in your existing code.",
        "Build one tiny feature for your project.",
        "Review your code and write down what you learned."
    ],
    "fitness": [
        "Start with a comfortable 5-minute walk.",
        "Do gentle stretching at your own pace.",
        "Take a short walk and notice how you feel.",
        "Try a few comfortable bodyweight movements.",
        "Walk a little and take breaks when needed.",
        "Repeat your favourite easy movement.",
        "Reflect on your consistency this week."
    ],
    "reading": [
        "Read a few pages of your chosen book.",
        "Write down one interesting idea.",
        "Read for a few minutes without distractions.",
        "Summarize what you read in 2 sentences.",
        "Revisit a favourite passage.",
        "Read a little further at a comfortable pace.",
        "Write one thing you learned this week."
    ],
    "general": [
        "Break your goal into one tiny action.",
        "Spend a few minutes getting started.",
        "Complete one small part of your goal.",
        "Review your progress so far.",
        "Practise one skill related to your goal.",
        "Repeat an action that worked well.",
        "Reflect on your progress and choose the next step."
    ]
}


def choose_category(goal):
    goal = goal.lower()

    if any(word in goal for word in
           ["study", "exam", "learn", "subject", "college"]):
        return "study"

    if any(word in goal for word in
           ["coding", "code", "python", "program", "developer"]):
        return "coding"

    if any(word in goal for word in
           ["fitness", "walk", "exercise", "health"]):
        return "fitness"

    if any(word in goal for word in
           ["read", "reading", "book"]):
        return "reading"

    return "general"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.get_json(silent=True) or {}

    goal = str(data.get("goal", "")).strip()
    mood = str(data.get("mood", "unsure")).strip().lower()

    try:
        days = int(data.get("days", 7))
        minutes = int(data.get("minutes", 30))
    except (TypeError, ValueError):
        return jsonify({"error": "Please select valid settings."}), 400

    if not goal:
        return jsonify({"error": "Please enter your goal first."}), 400

    if len(goal) > 500:
        return jsonify({"error": "Keep your goal under 500 characters."}), 400

    if days not in (7, 14, 30):
        return jsonify({"error": "Choose 7, 14, or 30 days."}), 400

    if minutes not in (15, 30, 60):
        return jsonify({"error": "Choose 15, 30, or 60 minutes."}), 400

    category = choose_category(goal)
    activities = TASK_LIBRARY[category].copy()

    if mood in ("tired", "overwhelmed"):
        activities = [
            "Spend just 5 minutes getting started.",
            "Complete one very small step toward your goal.",
            "Take a gentle first step without rushing.",
            "Review what you have already accomplished.",
            "Try one easy activity and rest if needed.",
            "Practise for a few minutes at your own pace.",
            "Choose the smallest useful next step."
        ]

    tasks = []

    for day in range(1, days + 1):
        activity = activities[(day - 1) % len(activities)]

        if minutes == 15:
            duration = "about 5–10 minutes"
        elif minutes == 30:
            duration = "about 15–20 minutes"
        else:
            duration = "about 30–45 minutes"

        tasks.append({
            "day": day,
            "task": f"{activity} ({duration})"
        })

    random.shuffle(tasks)
    tasks.sort(key=lambda item: item["day"])

    return jsonify({
        "success": True,
        "goal": goal,
        "days": days,
        "minutes_per_day": minutes,
        "tasks": tasks
    })


if __name__ == "__main__":
    app.run(debug=True)
