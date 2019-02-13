from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import pandas
import os
from geopy.geocoders import Nominatim


app=Flask(__name__)



@app.route("/")
def index():
	return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
	global file
	if request.method=="POST":
		file=request.files["file"]
		df=pandas.read_csv(file)


		geolocator = Nominatim()
		address = df['address']
		df['coordinates']=df['address'].apply(geolocator.geocode)
		df['latitude']=df['coordinates'].apply(lambda x: x.latitude if x != None else None)
		df['longitude']=df['coordinates'].apply(lambda x: x.longitude if x != None else None)
		df = df.drop('coordinates', axis=1)
		print(df)

		df.to_csv("uploads/edited.csv", index=None)

		return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, btn="download.html")

@app.route("/download")
def download():
	return send_file('uploads/edited.csv',  attachment_filename="yourfile.csv", as_attachment=True)



if __name__ == '__main__':
		app.debug=True
		app.run()	