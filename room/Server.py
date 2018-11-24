from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/V1/sites/<siteId>/devices/<deviceId>/level',methods = ["PUT"])
def setlevel(siteId,deviceId):
    file = open("level.txt","w")
    file.write(request.form["level"])
    file.close()

@app.route('/V1/sites/<siteId>/devices/<deviceId>/color',methods = ["PUT"])
def setColor(siteId,deviceId):
    file = open("color.txt","w")
    file.write(request.form["color"])
    file.close()

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port = 7001)