from flask import Flask, g, render_template
import sqlite3 

DATABASE = 'database.db'

#initiallise app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g.database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    #home page- just the ID, maker, model and image url
    sql = """SELECT Bikes.BikeID,makers.name,Bikes.model,Bikes.ImageURL
             FROM Bikes
             JOIN makers ON makers.MakerID=Bikes.MakerID;"""
    results = query_db(sql)
    return render_template("home.html", results=results)


@app.route("/bike/<int:id>")
def bike(id):
    #just one bike based on the id
    sql = """SELECT * FROM Bikes 
    JOIN makers ON makers.MakerID=Bikes.MakerID
    WHERE Bikes.BikeID = ?;"""
    result = query_db(sql,(id,),True)
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)