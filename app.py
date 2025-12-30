import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """ test """
    app = Flask(__name__)
    # client = MongoClient("mongodb+srv://scottsandwith_db_user:SA4Ever2Day@microblog-application.75j7yss.mongodb.net/")
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.MicroBlog

    @app.route("/", methods=["GET", "POST"])
    def home():
        """ home function """
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_dates = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"),
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_dates)
    return app