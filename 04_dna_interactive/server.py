from flask import Flask
from flask import request

app = Flask(__name__)

homepage_html = """
<html>
	<style>
	body {
		margin: 100px;
	}
	</style>
	<form action='/stats' method='GET'>

		<textarea name='dna' placeholder='Enter your DNA sequence here...' rows=20 cols=50></textarea><br/>
		<input type='submit' value='Get stats'>

	</form>
</html>
"""

@app.route("/")
def homepage():
	return homepage_html

@app.route("/stats", methods=['GET'])
def statistics():
	dna = request.args.get('dna', '')
	
	dna = dna.upper()
	dna_length = len(dna)

	homepage_link = "<a href='/'>Go back</a>"

	return "<html>The DNA sequence <i>{0}</i> is <strong>{1}</strong> base pairs. {2}</html>".format(dna, dna_length, homepage_link)

# launch the application with the debug messages
if __name__ == "__main__":
	app.run(debug=True)