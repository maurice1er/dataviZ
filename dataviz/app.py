# -*- coding: utf-8 -*-
# Librarys
from flask import Flask, render_template

import psycopg2

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8


import pandas as pd

# Variables
app = Flask(__name__)

# Settings
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret'

#database
connection = psycopg2.connect(
	database="postgres",
	user="postgres",
	password="xxxxxxxxx+",
	host = "127.0.0.1",
	port = "5432"
)

cursor = connection.cursor()


# Views
query = cursor.execute("SELECT * FROM clients_")
result = cursor.fetchall()
result = pd.DataFrame(result)


@app.route('/')
@app.route('/revenu_score')
def revenu_score():

	#columns revenu and score
	revenu_score = result.iloc[:,5:7]

	#revenu
	x = revenu_score.iloc[:,[0]].T
	x = x.values
	x = x[0]

	#score
	y = revenu_score.iloc[:,[1]].T
	y = y.values
	y = y[0]
	
	fig = figure(plot_width=550, plot_height=400, x_range=(0,150), y_range=(0,120),title = "Graphique representatif du Score en fonction du Revenu annuel",toolbar_location=None,)
	fig.circle(x,y,size=6)
	fig.xaxis.axis_label = "revenu annuel"
	fig.yaxis.axis_label = "score"

	script, div = components(fig)
	
	# grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	# render template
	html = render_template(
		'index.html',
		plot_script=script,
		plot_div=div,
		js_resources=js_resources,
		css_resources=css_resources,
		r=result,
	)
	return encode_utf8(html)


@app.route('/age_score')
def age_score():


	#columns age and score
	age_score = result.iloc[:,[4,6]]
	
	#score
	x = age_score.iloc[:,[1]].T
	x = x.values
	x = x[0]

	#age
	y = age_score.iloc[:,[0]].T
	y = y.values
	y = y[0]
	
	fig = figure(plot_width=550, plot_height=400, x_range=(0,105), y_range=(0,80),title = "Graphique representatif du Score en fonction de l'Age",toolbar_location=None,)
	fig.circle(x,y,size=6)
	fig.xaxis.axis_label = "score"
	fig.yaxis.axis_label = "age"

	script, div = components(fig)

	# grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	# render template
	html = render_template(
		'index.html',
		plot_script=script,
		plot_div=div,
		js_resources=js_resources,
		css_resources=css_resources,
		r=result,
	)
	return encode_utf8(html)



@app.route('/genre_score')
def genre_score():
	#columns genre and score
	genre_score = result.iloc[:,[3,6]]
	genre_score.columns = ["genre","score"]

	#genre
	genre = ['Male', 'Female']
	p = genre_score.groupby('genre').sum()
	nb_score_female = int(p[0:1].values[0][0])
	nb_score_male = int(p[1:2].values[0][0])
	total = int(nb_score_male) + int(nb_score_female)

	# pourcentage
	p_m = nb_score_male/total * 100
	p_f = 100 - p_m

	counts = [p_m, p_f]

	fig = figure(x_range=genre,plot_width=550, plot_height=350, toolbar_location=None, title="Pourcentage d'Homme et de Femme")
	fig.vbar(x=genre, top=counts, width=0.4, line_color='white',color=['#00a9FF']+['#cc95FF'])
	
	script, div = components(fig)

	# grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	# render template
	html = render_template(
		'index.html',
		plot_script=script,
		plot_div=div,
		js_resources=js_resources,
		css_resources=css_resources,
		r=result,
	)
	return encode_utf8(html)
	

# Run
if __name__ == '__main__':
	#return str(genre_score.loc[genre_score["genre"] == "Male"])
    app.run(debug=True)
