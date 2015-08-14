from flask import Flask, render_template, json, request
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient()
db = client.feature_request
clientList = list(db.client.find({}, {'name': 1, '_id': 0}))



@app.route("/")
def main():
	return render_template('index.html', clientList=clientList)

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