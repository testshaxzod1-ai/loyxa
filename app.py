from flask import Flask, render_template, request, redirect, session, url_for
import json, os

app = Flask(__name__)
app.secret_key = "supersecretkey123"   # Buni xavfsizroq qilib almashtiring

DATA_FILE = "data.json"

# ---- Login ma'lumotlari (xohlasangiz .env ga o‘tkazib beraman) ----
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# --------------------- LOGIN SAHIFASI ---------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect("/admin")
        else:
            return render_template("login.html", error="Login yoki parol noto‘g‘ri!")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# --------------------- ADMIN PANEL ---------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "logged_in" not in session:
        return redirect("/login")

    data = load_data()

    if request.method == "POST":
        data["problem"] = request.form.get("problem")
        data["solution"] = request.form.get("solution")
        data["why_us"] = request.form.get("why_us")
        data["roadmap"] = request.form.get("roadmap")
        data["implementation"] = request.form.get("implementation")

        # TEAM
        team_names = request.form.getlist("team_name[]")
        team_roles = request.form.getlist("team_role[]")
        team_skills = request.form.getlist("team_skills[]")
        team_links = request.form.getlist("team_link[]")

        data["team"] = []
        for i in range(len(team_names)):
            if team_names[i].strip():
                data["team"].append({
                    "name": team_names[i],
                    "role": team_roles[i],
                    "skills": team_skills[i],
                    "link": team_links[i],
                })

        save_data(data)
        return redirect("/admin")

    return render_template("admin.html", data=data)


# --------------------- ASOSIY SAYT ---------------------
@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
