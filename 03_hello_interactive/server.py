from flask import Flask
from flask import request
# create the 'app' object: this is the server application
app = Flask(__name__)

# create my style definitions
css_style = """
<style>
#message {
	font-size: 20px;
	color: blue;
	font-family: 'Helvetica';
}
</style>
"""

# tell the 'app' what function should be called on a basic request
@app.route("/", methods=['GET'])
def hello():
	username = request.args.get('username', '')
	if username != '':
		html_response = "<html>"
		html_response += css_style
		html_response += "<div id='message'>Hello, {0}!</div>".format(username)
		html_response += "</html>"
	else:
		html_response = "<html>"
		html_response += css_style
		html_response += "What's your name?"
		html_response += "<form action='/' method='GET'>"
		html_response += "<input type='text' name='username'>"
		html_response += "<input type='submit'>"
		html_response += "</form>"
		html_response += "</html>"
	return html_response

# launch the application with the debug messages
if __name__ == "__main__":
	app.run(debug=True)