from flask import Flask, request
from collections import Counter
import re
import matplotlib.pyplot as plt
import cStringIO

homepage_html = """
<html>
	<h3>Upload a FASTA file (from miRbase)</h3>
	<form method='POST' action='/upload_file' enctype='multipart/form-data'>
		<input type='file' name='uploadedFile' />
		<input type='submit' value='Upload' />
	</form>
</html>
"""


app = Flask(__name__)

@app.route('/')
def homepage():
	return homepage_html

@app.route('/upload_file', methods=['POST'])
def handle_upload():
	f = request.files['uploadedFile'].readlines()

	data = "".join(f)

	pattern = "\s([A-Za-z\s]*)\smiR"

	species = re.findall(pattern, data)

	mirna_counts = Counter(species)

	print mirna_counts

	plt.cla()
	x = 1
	x_points = []
	y_points = []

	table = "<table>"
	for s, c in mirna_counts.most_common(10):
		table += "<tr> <td>{0}</td> <td>{1}</td> </tr>".format(s, c)
		x_points.append(x)
		y_points.append(c)
		x += 1
	table += "</table>"

	plt.scatter(x_points, y_points)
	plt.xlabel('Species')
	plt.ylabel('Number of micro RNA')

	sio = cStringIO.StringIO()
	plt.savefig(sio, format='png')
	encoded_img = sio.getvalue().encode("base64").strip()
	image_tag = "<img width=400 height=300 src='data:image/png;base64,{0}'/>".format(encoded_img)


	return "<html><h3>miRNA by species</h3>" + image_tag + "<br/>" + table + "</html>"

if __name__ == "__main__":
	app.run(debug=True)





