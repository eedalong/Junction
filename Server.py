from flask import Flask
from flask import request
from flask import Response
import json
app = Flask(__name__)

@app.route('/V1/sites/<string:siteId>/devices/<string:deviceId>/level/<int:level>',methods = ["POST"])
def setlevel(siteId,deviceId,level):
    print(level)
    bfile = open("level.txt","w")
    bfile.write(str(level))
    print("set = {}".format(level))
    bfile.close()
    return json.dumps({"good":level})

@app.route('/V1/sites/<string:siteId>/devices/<string:deviceId>/color/<int:color>',methods = ["POST"])
def setColor(siteId,deviceId,color):
    print(color)
    bfile = open("color.txt","w")
    bfile.write(str(color))
    print("set = {}".format(color))
    bfile.close()
    return json.dumps({"good":color})
if __name__ == "__main__":
    app.run(port = 7001)