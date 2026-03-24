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

@app.route('/api/readings')
def get_readings():
	conn = psycopg2.connect(**DB_CONFIG)
	cur = conn.cursor()
	cur.execute("SELECT timestamp, tempurature, humidity, pressure, oxidising, reducing, nh3, PM2.5  FROM environment")
	rows = cur.fetchall()
	cur.close()
	conn.close()
	data = []
	for row in rows:
		data.append({
			"timestamp": row[0],
			"tempurature": row[1],
			"humidity": row[2],
			"pressure": row[3],
			"oxidising": row[4],
			"reducing": row[5],
			"nh3": row[6],
			"PM2.5":row[7]
		})
	return jsonify(data)
