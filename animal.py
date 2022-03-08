from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)




class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(50))
    species = db.Column(db.String(50))
    age = db.Column(db.String(20))
    feeding_record = db.Column(db.DateTime)
    vet = db.Column(db.DateTime)

    # enclosure = db.Column(db.String(50))
    def __repr__(self):
        return '<Animal %s>' % self.id

    # simply store the current system time when this method is called
    def feed(self):
        self.feeding_record = datetime.now()

    def vet(self):
        self.vet = datetime.now()


class Enclosure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    area = db.Column(db.String(50))
    clean = db.Column(db.DateTime)

    def clean(self):
        self.clean = datetime.now()


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    # animal = db.relationship("Animal", backref )



class AnimalSchema(ma.Schema):
    class Meta:
        fields = ("id", "common_name", "species", "age", "feeding_record", "vet")


class EnclosureSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "area", "clean", "animal", "stats")


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "address", "animal", "stats")


animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)

enclosure_schema = EnclosureSchema()
enclosures_schema = EnclosureSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


class AddAnimal(ma.Schema):
    def post(self):
        new_animal = Animal(
            common_name=request.json['common_name'],
            species=request.json['species'],
            age=request.json['age']
        )
        db.session.add(new_animal)
        db.session.commit()
        return animal_schema.dump(new_animal)
    
        


class AnimalResource(Resource):
    def get(self, animal_id):
        animal = Animal.query.get_or_404(animal_id)
        return animal_schema.dump(animal)

    def delete(self, animal_id):
        animal = Animal.query.get_or_404(animal_id)
        db.session.delete(animal)
        db.session.commit()
        return "Animal with ID {animal_id} was removed"


class AnimalListResource(Resource):
    def get(self):
        animals = Animal.query.all()
        return animals_schema.dump(animals)


class FeedAnimal(Resource):
    def post(self, animal_id):
        animal = Animal.query.get_or_404(animal_id)
        if not animal:
            return jsonify("Animal with ID {animal_id} was not found")
        animal.feed()
        db.session.commit()
        return animal_schema.dump(animal)


class VetAnimal(Resource):
    def post(self, animal_id):
        animal = Animal.query.get_or_404(animal_id)
        if not animal:
            return jsonify("Animal with ID {animal_id} was not found")
        animal.vet()
        db.session.commit()
        return animal_schema.dump(animal)


# class EnclosureResource(Resource):
#     def post(self, animal_id):
#         if animal_id in request.json:
#             new_home = Animal(
#                 home=request.json['enclosure']
#             )
#             db.session.add(new_home)
#             db.session.commit()
#             return animal_schema.dump(new_home)

class EnclosureAddResource(Resource):
    def post(self):
        new_enclosure = Enclosure(
            name=request.json['name'],
            area=request.json['area']
        )
        db.session.add(new_enclosure)
        db.session.commit()
        return enclosure_schema.dump(new_enclosure)


class EnclosureListResource(Resource):
    def get(self):
        enclosures = Enclosure.query.all()
        return enclosure_schema.dump(enclosures)


class EnclosureDelete(Resource):
    def delete(self, enclosure_id):
        enclosure = Enclosure.query.get_or_404(enclosure_id)
        db.session.delete(enclosure)
        db.session.commit()
        return f"Enclosure with ID {enclosure_id} was removed"


class CleanEnclosure(Resource):
    def post(self, enclosure_id):
        enclosure = Enclosure.query.get_or_404(enclosure_id)
        if not enclosure:
            return jsonify("Enclosure with ID {enclosure_id} was not found")
        enclosure.clean()
        db.session.commit()
        return enclosure_schema.dump(enclosure)


# Employee Business Logic
class EmployeeAddResource(Resource):
    def post(self):
        new_employee = Employee(
            name=request.json['name'],
            address=request.json['address'],
        )
        db.session.add(new_employee)
        db.session.commit()
        return employee_schema.dump(new_employee)


class EmployeeDelete(Resource):
    def delete(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return f"Enclosure with ID {employee_id} was removed"


# API ROUTES
api.add_resource(AddAnimal, '/animal')
api.add_resource(AnimalResource, '/animal/<animal_id>')
api.add_resource(AnimalListResource, '/animals')
api.add_resource(FeedAnimal, '/animal/<animal_id>/feed')
api.add_resource(VetAnimal, '/animal/<animal_id>/vet')
# api.add_resource(EnclosureResource, '/animal/<animal_id>/home')
api.add_resource(EnclosureAddResource, '/enclosure')
api.add_resource(EnclosureListResource, '/enclosures')
api.add_resource(EnclosureDelete, '/enclosure/<enclosure_id>')
api.add_resource(CleanEnclosure, '/enclosure/<enclosure_id>/clean')
api.add_resource(EmployeeAddResource, '/employee/')
api.add_resource(EmployeeDelete, '/employee/<employee_id>')

if __name__ == '__main__':
    app.run(debug=True)
