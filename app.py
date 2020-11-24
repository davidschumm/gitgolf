from flask import Flask, render_template, request

app = Flask(__name__)


subscribers = []

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
