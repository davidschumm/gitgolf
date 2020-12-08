from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api, reqparse
#import smtplib
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize the database
db = SQLAlchemy(app)

GOLFCOURSES = {
	'1': {'name': 'Pine Hills Golf Course', 'Tee Color': 'White', 'Holes': 18, 'Course Handicap': 8, 'Course Par': 72, 'Course Rating': 68.4, 'Course Slope': 113},
	'2': {'name': 'Pine Hills Golf Course', 'Tee Color': 'Blue', 'Holes': 18, 'Course Handicap': 10, 'Course Par': 72, 'Course Rating': 69.5, 'Course Slope': 116},
	'3': {'name': 'Steel Canyon Golf Club', 'Tee Color': 'White', 'Holes': 18, 'Course Handicap': 9, 'Course Par': 61, 'Course Rating': 58.9, 'Course Slope': 104},
	'4': {'name': 'Steel Canyon Golf Club', 'Tee Color': 'Black', 'Holes': 18, 'Course Handicap': 10, 'Course Par': 61, 'Course Rating': 60.2, 'Course Slope': 107},
}

parser = reqparse.RequestParser()

class golfCourseList(Resource):
	def get(self):
		return GOLFCOURSES
	
	def post(self):
		parser.add_argument("name")
		parser.add_argument("Tee Color")
		parser.add_argument("Holes")
		parser.add_argument("Course Handicap")
		parser.add_argument("Course Par")
		parser.add_argument("Course Rating")
		parser.add_argument("Course Slope")
		args = parser.parse_args()

		course_id = int(max(GOLFCOURSES.keys())) + 1
		course_id = '%i' % course_id

		GOLFCOURSES[course_id] = {
		"name": args["name"],
		"Tee Color": args["Tee Color"],
		"Holes": args["Holes"],
		"Course Handicap": args["Course Handicap"],
		"Course Par": args["Course Par"],
		"Course Rating": args["Course Rating"],
		"Course Slope": args["Course Slope"],
		}

		return GOLFCOURSES[course_id], 201

class golfCourse(Resource):
	def get(self, course_id):
		if course_id not in GOLFCOURSES:
			return "Not found", 404
		else:
			return GOLFCOURSES[course_id]

	def put(self, course_id):
		parser.add_argument("name")
		parser.add_argument("Tee Color")
		parser.add_argument("Holes")
		parser.add_argument("Course Handicap")
		parser.add_argument("Course Par")
		parser.add_argument("Course Rating")
		parser.add_argument("Course Slope")
		args = parser.parse_args()

		if course_id not in GOLFCOURSES:
			return "Record not found", 404

		else:
			course = GOLFCOURSES[course_id]
			course['name'] = args["name"] if args["name"] is not None else student["name"]
			course['Tee Color'] = args["Tee Color"] if args["Tee Color"] is not None else student["Tee Color"]
			course['Holes'] = args["Holes"] if args["Holes"] is not None else student["Holes"]
			course['Course Handicap'] = args["Course Handicap"] if args["Course Handicap"] is not None else student["Course Handicap"]
			course['Course Par'] = args["Course Par"] if args["Course Par"] is not None else student["Course Par"]
			course['Course Rating'] = args["Course Rating"] if args["Course Rating"] is not None else student["Course Rating"]
			course['Course Slope'] = args["Course Slope"] if args["Course Slope"] is not None else student["Course Slope"]
			return course, 200

	def delete(self, course_id):
		if course_id not in GOLFCOURSES:
			return 'Not found', 404
		else:
			del GOLFCOURSES[course_id]
			return '', 204

api.add_resource(golfCourseList, '/courses/')
api.add_resource(golfCourse, '/courses/<course_id>')



# create db model
class Friends(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	# Create a function to return a string when we add something
	def __repr__(self):
		return '<Name %r>' % self.id



subscribers = []


@app.route('/delete/<int:id>')
def delete(id):
	friend_to_delete = Friends.query.get_or_404(id)

	try:
		db.session.delete(friend_to_delete)
		db.session.commit()
		return redirect('/friends')

	except:
		return "There was a problem deleting that friend"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
	friend_to_update = Friends.query.get_or_404(id)
	if request.method == "POST":
		friend_to_update.name = request.form['name']
		try:
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was a problem updating that friend"

	else:
		return render_template('update.html', friend_to_update=friend_to_update)



@app.route('/friends', methods=['POST', 'GET'])
def friends():
	title = "!GitGolf Users!"

	if request.method == "POST":
		friend_name = request.form['name']
		new_friend = Friends(name=friend_name)


		# Push to database
		try:
			db.session.add(new_friend)
			db.session.commit()
			return redirect('friends')
		except:
			return "There was an error adding friend"

	else:
		friends = Friends.query.order_by(Friends.date_created)
		return render_template("friends.html", title=title, friends=friends)


@app.route('/handicap_calc')
def handicap_calc():
	title = "Handicap Calculator"
	return render_template("handicap_calc.html", title=title)



@app.route('/')
def index():
	title = "GitGolf Quikbook"
	return render_template("index.html", title=title)

@app.route('/about')
def about():
	title = "!About GitGolf!"
	names = ["Dave", "Mary", "Jon", "Dan"]
	return render_template("about.html", names=names, title=title)

@app.route('/subscribe')
def subscribe():
	title = "Subscribe to GitGolf"
	return render_template("subscribe.html", title=title)


@app.route('/form', methods=['POST'])
def form():
	first_name = request.form.get("first_name")
	last_name = request.form.get("last_name")
	email = request.form.get("email")
	password = request.form.get("password")

	#message = "You have been subscribed to my email newsletter"
	#server = smtplib.SMTP("smtp.gmail.com", 587)
	#server.starttls()
	#server.login("myemail@gmail.com", "password")
	#server.sendmail("myemail@gmail.com", email, message)

	if not first_name or not last_name or not email or not password:
		error_statement = "All Form Fields Required..."
		return render_template("subscribe.html",
			error_statement=error_statement,
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=password)

	subscribers.append(f"{first_name} {last_name} | {email} {password}")
	title = "Thank You!"
	return render_template("form.html", title=title, subscribers=subscribers)
