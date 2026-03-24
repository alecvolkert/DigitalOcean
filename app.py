from flask import Flask,  request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

DB_CONFIG = {
    "dbname": "environment",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": "5432"
}


@app.route('/')
def index():
	return render_template("~/html/index.html")


@app.route('/api/submit', methods = ['POST'])
def submit_reading():
	if request.headers.get('API_KEY') != os.getenv("API_KEY"):
		return jsonify({"error":"unauthaurized"}), 401 
	data = request.get_json()
	conn = 	psycopg2.connect(**DB_CONFIG)
	cur = conn.cursor()
	keys = list(data.keys())
	values = list(data.values())
	columns = ", ".join(keys)
	placeholders = ", ".join(["%s"] * len(values))
	cur.execute(f"INSERT INTO enviroreadings ({columns}) VALUES ({placeholders})", values)	
	conn.commit()
	cur.close()
	conn.close()

