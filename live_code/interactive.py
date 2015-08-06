from flask import Flask, request

template = """
<html>
 <head>
  <title>dna statistics</title>
 </head>

 <body>
	<div id="content">

		<!-- Headline -->
		<h4>Manipulate your DNA sequence</h4>
		<form action='/' method='GET'>
		<textarea name='dna' cols=75 rows=10 placeholder="Paste your DNA sequence here...">{dna}</textarea>
		<textarea name='manipulated' cols=75 rows=10 placeholder="Manipulated DNA will appear here" readonly>{manipulated}</textarea>
		<br/>
		<input type='submit' name='transformation' value='Reverse'/>
		<input type='submit' name='transformation' value='Complement'/>
		<input type='submit' name='transformation' value='Reverse Complement'/>
		</form>
	</div>

 </body>
</html>
"""

def reverse_string(arg):
	return arg[::-1]

def complement_string(arg):
	arg = arg.lower()
	arg = arg.replace('a', 'T')
	arg = arg.replace('t', 'A')
	arg = arg.replace('g', 'C')
	arg = arg.replace('c', 'G')
	return arg

def reverse_complement(arg):
	return reverse_string(complement_string(arg))

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
	dna_string = request.args.get('dna', '')
	action = request.args.get('transformation', '')

	if dna_string == '':
		# handling a new user
		return template.format(dna = '', manipulated = '')
	else:
		# handle a meaningful request
		manipulated = dna_string

		# perform requested action
		if action == "Reverse":
			manipulated = reverse_string(dna_string)
		elif action == "Complement":
			manipulated = complement_string(dna_string)
		elif action == "Reverse Complement":
			manipulated = reverse_complement(dna_string)

		return template.format(dna = dna_string, manipulated = manipulated)

if __name__ == "__main__":
	app.run(debug=True)












