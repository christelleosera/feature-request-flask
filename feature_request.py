from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
import datetime

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'feature_request'
mysql.init_app(app)

# conn = mysql.connect()
# cursor = conn.cursor()

@app.route("/")
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

@app.route('/submit',methods=['POST'])
def submit():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursorf = conn.cursor()

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



	query = "INSERT INTO `feature` (`title`, `description`, `id_client`, `priority`, `target_date`, `ticket_url`, `id_product_area`) VALUES ('%s', '%s', %s, %s, '%s', '%s', %s);" % (title, description, clientID, priority, targetDate, ticketUrl, productArea)
	ok = cursor.execute(query)

	query = "SELECT title from feature where priority=%s and id_client=%s" % (priority, clientID)
	qcount = cursor.execute(query)
	
	prior = int(priority)
	print "qqq", qcount

	if(qcount > 1):
		while (qcount > 1):
			query_qcount = "SELECT id from feature where priority=%s and id_client=%d order by priority, id" % (prior, clientID)
			print query_qcount
			qcount = cursor.execute(query_qcount)
			print "qqq", qcount
			if(qcount > 1):
				# print cursor.fetchall()[0][0]
				query = "UPDATE feature set priority=priority+1 where id=%s" % (cursor.fetchall()[0][0])
				print query, "*"
				cursorf.execute(query)
				
				prior += 1


	conn.commit()
	cursor.close()
	conn.close()
	return render_template('submit.html', title=title, description=description, client=client, priority=priority, targetDate=targetDate, ticketUrl=ticketUrl, productArea=productArea)


if __name__ == "__main__":
    app.run(debug=True)