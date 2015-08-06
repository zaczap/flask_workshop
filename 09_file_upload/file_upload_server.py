from flask import Flask, request
import re
from collections import Counter
basic_template = """
<html>
<form action='/' method='POST' enctype='multipart/form-data'>
<input type='file'  name='file' />
<input type='submit' value='Upload' />
</form>
</html>
"""

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		data = "".join(f.readlines())
		matches = re.findall("\s([A-Za-z\s]*)\smiR", data)
		print Counter(matches)
		output = "<table>"
		for species, count in Counter(matches).most_common(10):
			output += "<tr><td>{0}</td><td>{1}</td></tr>".format(species, count)
		output += "</table>"
		return "<html>" + output + "</html>"
	else:
		return basic_template


if __name__ == "__main__":
	app.run(debug=True)