from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource # Enfocing RESTFul principles
from flask_cors import CORS
import bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies
)

from models import db, Student, Cohort, Reward, Mentor, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # or True with CSRF token

jwt = JWTManager(app)


CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3001",
            "http://localhost:3000",
            "http://localhost:3005",
        ]
    }
}
)
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app) # we link our flask app to flaks_restful

class Home(Resource):
    def get(self):
        # response = {
        #     "message": "Welcome to Moringa School"
        # }

        return make_response("Welcome to Moringa School", 200)
    
api.add_resource(Home, '/')


class Students(Resource):
    @jwt_required()
    def get(self):
        students = [student.to_dict() for student in Student.query.all()]

        return make_response(students, 200)

    def post(self):
        data = request.get_json()
        student = Student(name=data["name"])

        db.session.add(student)
        db.session.commit()

        return make_response(student.to_dict(), 200)
    
api.add_resource(Students, '/students')

class StudentsById(Resource):
    def get(self, id):
        student = Student.query.get(id)

        return make_response(student.to_dict(), 200)
    
    def delete(self, id):
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()

        return make_response(f'{student.name} was deleted successfully')
    
    def patch(self, id):
        data = request.get_json()   

        # {
        #     "name": "sam",
        #     "gender": "M",
        #     "DOB": "13/04/2000"
        # }
        student = Student.query.get(id)
        student.name = data["name"]
        # student.gender = data["gender"]
        db.session.commit()

        return make_response(f'{student.name} was modified successfully')
    
api.add_resource(StudentsById, '/students/<int:id>')


class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        email = data["email"]

        if User.query.filter_by(email=email).first():
            return make_response(f'This user already exists', 400)
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(email=email, username=username, password_hash=hashed)
        db.session.add(new_user)
        db.session.commit()

        return make_response(f'New user created successfully', 200)
    
api.add_resource(Register, '/register')


class Login(Resource):
    def post(self):
        data = request.get_json()
        password = data["password"]
        email = data["email"]

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            access_token = create_access_token(identity=email) #gerate JWT
            response = make_response(f"Welcome {user.username}")
            # response.set_cookie("username", user.username, httponly=True, max_age=3600)
            set_access_cookies(response, access_token) # save JWT in httponly cookies
            return response        
        return make_response(f"Invalid credentials!")
api.add_resource(Login, '/login')

class ReadCookie(Resource):
    def get(self):
        cookie_value = request.cookies.get("username")

        return make_response(f"cookie: {cookie_value}")
api.add_resource(ReadCookie, '/read-cookie')



if __name__ == '__main__':
    app.run(port=5555, debug=True)