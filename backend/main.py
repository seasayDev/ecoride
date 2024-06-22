from flask import Flask ,jsonify
from flask_cors import CORS

app =Flask(__name__)

app.config.from_object(__name__)


CORS(app,resources={r"/*":{'origins':"*"}})
# CORS(app,resources={r"/*":{'origins':'http://localhost:8080',"allow_headers":"Acces-Control-Allow-Origins"}})
@app.route('/',methods=['GET'])
def greetings():
    return ("hello word")

@app.route('/shark',methods=['GET'])
def shark():
    return ("hello, this is a new shark your calling from flask app")

if __name__=="__main__":
    app.run(debug=True)
