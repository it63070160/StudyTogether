from flask import Flask, render_template

app = Flask(__name__, template_folder="")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/findGroups')
def findGroup():
    return render_template("findGroups.html")

@app.route('/forums')
def forums():
    return render_template("forums.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
