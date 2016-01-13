from flask import Flask
#from version_control import 

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return "Thank you for hitting the api! Unfortunately we don't offer shell access"

if __name__ == '__main__':
    app.run()
