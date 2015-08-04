from flask import Flask

# create the 'app' object: this is the server application
app = Flask(__name__)

# tell the 'app' what function should be called on a basic request
@app.route("/")
def hello():
	html_response = "<html>Hello, world!</html>"
	return html_response

# launch the application with the debug messages
if __name__ == "__main__":
	app.run(debug=True)