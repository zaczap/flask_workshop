from flask import Flask
from flask import request
import re

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

	# We need to make sure it's only DNA...
	if len(re.findall('[^ATGC]', dna)) > 0:
		app.logger.error('Flagged sequence: {0}'.format(dna))
		dna = re.sub('[^ATGC]', 'x', dna)



	dna_length = len(dna)
	a_counts = dna.count('A')
	t_counts = dna.count('T')
	g_counts = dna.count('G')
	c_counts = dna.count('C')
	gc_percent = (g_counts + c_counts) / float(dna_length) * 100.0

	# not the best way to build a table but easy to follow
	table = "<table>"
	table += "<tr>  <td><strong>Field</strong></td>  <td><strong>Value</strong></td>  </tr>"
	table += "<tr>  <td>Sequence</td>  <td>"+dna+"</td>  </tr>"
	table += "<tr>  <td>Length</td>  <td>"+str(dna_length)+"</td></tr>"
	table += "<tr>  <td>A count</td>  <td>"+str(a_counts)+"</td></tr>"
	table += "<tr>  <td>T count</td>  <td>"+str(t_counts)+"</td></tr>"
	table += "<tr>  <td>G count</td>  <td>"+str(g_counts)+"</td></tr>"
	table += "<tr>  <td>C count</td>  <td>"+str(c_counts)+"</td></tr>"
	table += "<tr>  <td>GC %</td>  <td>"+str(round(gc_percent, 2))+"</td></tr>"
	table += "</table>"

	homepage_link = "<a href='/'>Go back</a>"

	return "<html>{0}<br/>{1}</html>".format(table, homepage_link)

# launch the application with the debug messages
if __name__ == "__main__":
	app.run(debug=True)