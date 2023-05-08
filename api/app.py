from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sheets
from  dateutil.parser import *

app = Flask(__name__)
# app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    company = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    # dob = db.Column(db.Date, nullable=False)
    # time = db.Column(db.String, nullable=False)
    # weight = db.Column(db.Float, nullable=False)
    # length = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'email': self.email,
            'mobile': self.mobile,
            'address': self.address
            # 'dob': self.dob.strftime('%d/%m'),
            # 'time': self.time,
            # 'weight': self.weight,
            # 'length': self.length
        }

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customers.query.all()
    return jsonify([customer.serialize() for customer in customers])

@app.route('/api/customers', methods=['POST'])
def create_customer():
    print(request.json)
    name = request.json['name']
    # dob = datetime.datetime.strptime(request.json['dob'], '%Y-%m-%dT%H:%M')
    email = request.json['email']
    company = request.json['company']
    mobile = request.json['mobile']
    address = request.json['address']
    customer = Customers(name=name, company=company, email=email, mobile=mobile, address=address)
    db.session.add(customer)
    db.session.commit()

    creds = sheets.authenticate()
    sheets.append_to_sheet(creds, name, company, email, mobile, address)
    return jsonify(customer.serialize()), 201

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
