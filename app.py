from flask import Flask, request, abort, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///receiver.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String)
    environment = db.Column(db.String)
    data = db.Column(db.JSON)

    def __repr__(self):
        return f"{self.id} | {self.environment} | {self.model}"

class DataSchema(ma.ModelSchema):
    class Meta:
        model = Data

data_schema = DataSchema()
datas_schema = DataSchema(many=True)

@app.route("/api/1.0/data", methods=["GET"])
def get_data():
    ds = Data.query.all()
    return jsonify(datas_schema.dump(ds))


@app.route("/api/1.0/data", methods=["POST"])
def create_data():
    req_data = request.json or json.loads(request.data)
    # if not request.json:
    #     abort(400)
    data = Data()
    data.environment = req_data.get("env", "")
    data.model = req_data.get("model", "")
    data.data = req_data.get("data", "")
    db.session.add(data)
    db.session.commit()
    return jsonify(data_schema.dump(data))



@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
