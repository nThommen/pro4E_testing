# src/dashboard.py
from flask import Flask, render_template, jsonify
import pandas as pd

def create_app():
    app=Flask(_name_,template_folder="src/templates")
    @app.route('/')
    def index():
        return render_template('dashboard.html')
    @app.route('/data')
    def data():
        df=pd.read_csv("results.csv",parse_dates=["timestamp"])
        return jsonify(df.to_dict("records"))
    return app