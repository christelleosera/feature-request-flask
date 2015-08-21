from flask import Flask, render_template, json, request, redirect, url_for
from flask.ext.mysql import MySQL
from flask.ext.basicauth import BasicAuth
import datetime

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'bg2Twed5UWYS2&$w'

basic_auth = BasicAuth(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'feature_request'
mysql.init_app(app)

# conn = mysql.connect()
# cursor = conn.cursor()

@app.route("/")
@basic_auth.required
def main():
	# query = ("SELECT name FROM client")
	# cursor.execute(query)
	# names = [item[0] for item in cursor.fetchall()]

	return render_template('index.html')

@app.route('/check',methods=['POST'])
def check():
	conn = mysql.connect()
	cursor = conn.cursor()

	client = request.form['inputClient']
	priority = request.form['inputPriority']

	query = "SELECT id from client where name='%s';" % (client)
	cursor.execute(query)
	clientID = cursor.fetchall()[0][0]

	query = "SELECT title from feature where priority=%s and id_client=%s" % (priority, clientID)
	count = cursor.execute(query)
	print count

	

	if(count > 0):
		title = cursor.fetchall()[0][0]
		conn.commit()
		cursor.close()
		conn.close()
		return json.dumps({'exists':'1', 'title' : title})
	else:
		conn.commit()
		cursor.close()
		conn.close()
		return json.dumps({'exists': '0'})

@app.route('/requests')
def requests():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT feature.*, client.name, product_area.name FROM feature, client, product_area WHERE feature.id_client = client.id AND product_area.id = feature.id_product_area ORDER BY feature.target_date, feature.id_client, feature.priority")
	features = cursor.fetchall()

	conn.commit()
	cursor.close()
	conn.close()
	return render_template('requests.html', features=features)

@app.route('/submit',methods=['POST'])
def submit():
	conn = mysql.connect()
	cursor = conn.cursor()

	# read the posted values from the UI
	title = request.form['inputTitle']
	description = request.form['inputDescription']
	client = request.form['inputClient']
	priority = request.form['inputPriority']
	targetDate = request.form['inputTargetDate']
	ticketUrl = request.form['inputTicketUrl']
	productArea = request.form['inputProductArea']

	query = "SELECT id from client where name='%s';" % (client)
	cursor.execute(query)
	clientID = cursor.fetchall()[0][0]

	query = "SELECT id from product_area where name='%s';" % (productArea)
	cursor.execute(query)
	productArea = cursor.fetchall()[0][0]



	query = "INSERT INTO `feature` (`title`, `description`, `id_client`, `priority`, `target_date`, `ticket_url`, `id_product_area`) VALUES (%s, %s, %s, %s, %s, %s, %s);"
	ok = cursor.execute(query, (title, description, clientID, priority, targetDate, ticketUrl, productArea))

	query = "SELECT title from feature where priority=%s and id_client=%s"
	qcount = cursor.execute(query, (priority, clientID))
	
	prior = int(priority)

	if(qcount > 1):
		while (qcount > 1):
			query_qcount = "SELECT id from feature where priority=%s and id_client=%s order by priority, last_modified, id"
			qcount = cursor.execute(query_qcount, (prior, clientID))
			if(qcount > 1):
				query = "UPDATE feature set priority=priority+1 where id=%s"
				cursor.execute(query, (cursor.fetchall()[0][0],))
				
				prior += 1
	

	conn.commit()
	cursor.close()
	conn.close()
	return redirect(url_for('requests'))


if __name__ == "__main__":
    app.run(debug=True)