from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import mysql.connector

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
host = "localhost"
user = "root"
password = ""
db = "dbconnect"

@app.route("/", methods=["GET"])
def home():
    return "backend test api"

#เรียกข้อมูล Product ทั้งหมด
@app.route("/product", methods=["GET"])
def getdata():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    sql = "Select * From product"
    lvSQL.execute(sql)
    result = lvSQL.fetchall()
    print(result)
    return make_response(jsonify(result), 200)

#เรียกข้อมูล Product Limit ด้วย 10,20,50
@app.route("/product/limit", methods=["GET"])
def getdatareqlim():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    sql = "Select * From product LIMIT %s"
    val = (data['limit'])
    lvSQL.execute(sql, (val,))
    result = lvSQL.fetchall()
    print(result)
    return make_response(jsonify(result), 200)

#Product List Gender Filter
@app.route("/product/gender", methods=["GET"])
def getdatafiltergender():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "Select * from product WHERE 1=1 AND Gender = %s LIMIT %s "
    val = (data['gender'], data['limit'])
    lvSQL.execute(SQL, val)
    result = lvSQL.fetchall()
    return make_response(jsonify(result), 200)

#Product List Category Filter
@app.route("/product/category", methods=["GET"])
def getdatafiltercategory():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "Select * from product WHERE 1=1 AND Category = %s LIMIT %s "
    val = (data['category'], data['limit'])
    lvSQL.execute(SQL, val)
    result = lvSQL.fetchall()
    return make_response(jsonify(result), 200)

#Product List Size Filter
@app.route("/product/size", methods=["GET"])
def getdatafiltersize():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "Select * from product WHERE 1=1 AND Size = %s LIMIT %s "
    val = (data['size'], data['limit'])
    lvSQL.execute(SQL, val)
    result = lvSQL.fetchall()
    return make_response(jsonify(result), 200)

#Order Create
@app.route("/order/create", methods=["POST"])
def createorder():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "INSERT INTO orders (Address, Date, OrderStatus) VALUES (%s, %s, %s)"
    val = (data['address'], data['date'], data['orderstatus'])
    lvSQL.execute(SQL, val)
    mydb.commit()
    return make_response(jsonify({"Success" : lvSQL.rowcount}), 200)

#Create Order Detail
@app.route("/order/createdetail", methods=["POST"])
def createorderdetail():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "INSERT INTO ordersdetail (OrderID, ProductID) VALUES (%s, %s)"
    val = (data['orderid'], data['productid'])
    lvSQL.execute(SQL, val)
    mydb.commit()
    return make_response(jsonify({"Success" : lvSQL.rowcount}), 200)

#Get Order List
@app.route("/orderlist", methods=["GET"])
def getorderlist():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "Select * from orders a inner join ordersdetail b on a.id = b.orderid inner join product c on c.id = b.productid WHERE 1=1 "
    lvSQL.execute(SQL)
    result = lvSQL.fetchall()
    return make_response(jsonify(result), 200)

#Get Order List
@app.route("/orderlist/count", methods=["GET"])
def getorderlistccount():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "SELECT COUNT(a.Id) AS Count FROM orders a INNER JOIN ordersdetail b ON a.id = b.orderid INNER JOIN product c ON c.id = b.productid WHERE 1 = 1 AND a.ID = %s "
    val = (data['id'])
    lvSQL.execute(SQL, (val,))
    result = lvSQL.fetchall()
    return make_response(jsonify(result), 200)

#Get Order List Filter
@app.route("/orderlist/filter", methods=["GET"])
def getorderlistfilter():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "Select * from orders a inner join ordersdetail b on a.id = b.orderid inner join product c on c.id = b.productid WHERE 1=1 AND a.OrderStatus = 'ชำระเงินแล้ว' AND Date >= %s AND Date <= %s "
    val = (data['datestart'], data['dateend'])
    lvSQL.execute(SQL, val)
    result = lvSQL.fetchall()
    return make_response(jsonify(result), 200)

#Get Order List Filter
@app.route("/orderlist/status", methods=["GET"])
def getorderliststatus():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    SQL = "Select * from orders a inner join ordersdetail b on a.id = b.orderid inner join product c on c.id = b.productid WHERE 1=1 AND a.OrderStatus = %s LIMIT %s"
    val = (data['status'], data['limit'])
    lvSQL.execute(SQL, val)
    result = lvSQL.fetchall()
    return make_response(jsonify(result), 200)


#สำหรับ Test Method
@app.route("/test", methods=["GET"])
def testapi():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    lvSQL = mydb.cursor(dictionary=True)
    gender = ""
    limit = 0
    gender = data['gender']
    limit = data['limit']
    SQL = "Select * from product WHERE 1=1 "
    if gender != "":
        SQL += "AND Gender = %s"
    elif limit != 0:
        SQL += "LIMIT %s "
    val = (gender, limit)
    lvSQL.execute(SQL, val)
    result = lvSQL.fetchall()
    return make_response(jsonify(result), 200)