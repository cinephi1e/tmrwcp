from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.vxurnmg.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.theTomorrowCamp

@app.route('/')
def home():
   return render_template('bsy.html')

@app.route("/introduction", methods=["POST"])
def introduction_post():
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]
    date_receive = request.form["date_give"]

    guestbookList = list(db.bsy.find({}, {'_id': False}))
    count = len(guestbookList) + 1

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'date': date_receive,
        'num': count,
        'read': 0
    }

    db.bsy.insert_one(doc)

    return jsonify({'msg':'😘'})

@app.route("/introduction", methods=["GET"])
def introduction_get():
    comment_list = list(db.bsy.find({},{'_id':False}))
    return jsonify({'comments':comment_list})

@app.route("/introduction/read", methods=["POST"])
def introduction_read():
    num_receive = request.form["num_give"]
    db.bsy.update_one({'num': int(num_receive)}, {'$set': {'read': 1}})
    return jsonify({'msg': '방명록 확인 ✅'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)