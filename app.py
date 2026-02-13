from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    #home page
    return "Hellow again!"

if __name__ == "__main__":
    app.run(debug=True)