from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'feature_request'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

query = ("SELECT name FROM client")
cursor.execute(query)

names = [item[0] for item in cursor.fetchall()]

print names

@app.route("/")
def main():
	return render_template('index.html', clientList=names)

@app.route('/submit',methods=['POST'])
def submit():
    # read the posted values from the UI
    title = request.form['inputTitle']
    description = request.form['inputDescription']
    client = request.form['inputClient']
    priority = request.form['inputPriority']
    targetDate = request.form['inputTargetDate']
    ticketUrl = request.form['inputTicketUrl']
    productArea = request.form['inputProductArea']
    
    return render_template('submit.html', title=title, description=description, client=client, priority=priority, targetDate=targetDate, ticketUrl=ticketUrl, productArea=productArea)
if __name__ == "__main__":
    app.run(debug=True)