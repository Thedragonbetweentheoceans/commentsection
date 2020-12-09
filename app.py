from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect("user.db")
mycursor = conn.cursor()

mycursor.execute('CREATE TABLE IF NOT EXISTS Users(username TEXT, comment TEXT)')

app = Flask(__name__)

@app.route("/comments.html", methods = ["POST","GET"])
def comments():
    if request.method == "POST":

        username = request.form["username"]
        comment = request.form["comment"]

        conn = sqlite3.connect("user.db", check_same_thread =  False)
        mycursor = conn.cursor()
        mycursor.execute("INSERT INTO Users(username, comment) VALUES(?,?)", (username, comment))
        conn.commit()
        mycursor.close()
        conn.close()

    conn = sqlite3.connect("user.db", check_same_thread = False)
    mycursor = conn.cursor()
    mycursor.execute("SELECT username FROM Users")
    usrname = []

    for i in mycursor:
        usrname.append(i)

    mycursor.execute("SELECT comment FROM Users")
    commt=[]

    for i in mycursor:
        commt.append(i)
    
    message = []

    for i in range(len(usrname)):
        string = "{} said {}".format(str(usrname[i]),str(commt[i]))
        message.append(string)
    
    k=0
    for i in range(len(message)):
        k+=1

    return render_template("comments.html", values=message, number=k)
if __name__=="__main__":
    app.run(debug=True)
