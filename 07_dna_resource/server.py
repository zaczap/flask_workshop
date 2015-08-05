from flask import Flask
from flask import request

# get an app instance
app = Flask(__name__)

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
		<textarea name='dna' cols=75 rows=10 placeholder="Paste your DNA sequence here...">{dna.original}</textarea>
		<textarea name='dna.manipulated' cols=75 rows=10 placeholder="Manipulated DNA will appear here" readonly>{dna.manipulated}</textarea>
		<br/>
		<input type='submit' name='transformation' value='Reverse'/>
		<input type='submit' name='transformation' value='Complement'/>
		<input type='submit' name='transformation' value='Reverse Complement'/>
		</form>
	</div>

 </body>
</html>
"""

class DNA:
	def __init__(self, dna):
		self.original = dna.upper()
		self.manipulated = dna.upper()

	def reverse(self):
		self.manipulated = self.original[::-1]

	def complement(self):
		self.manipulated = self.original.lower()
		self.manipulated = self.manipulated.replace('a','T')
		self.manipulated = self.manipulated.replace('t','A')
		self.manipulated = self.manipulated.replace('g','C')
		self.manipulated = self.manipulated.replace('c','G')

	def reverse_complement(self):
		self.manipulated = self.original[::-1].lower()
		self.manipulated = self.manipulated.replace('a','T')
		self.manipulated = self.manipulated.replace('t','A')
		self.manipulated = self.manipulated.replace('g','C')
		self.manipulated = self.manipulated.replace('c','G')

@app.route('/', methods=['GET'])
def handleDNA():
	sequence = request.args.get('dna', '')
	action = request.args.get('transformation', '')

	# Handle default requests - no submission
	if action == '':
		dna = DNA("") # make a null object
		return template.format(dna=dna)

	# Handle an actual response
	else:
		dna = DNA(sequence)

		if action == 'Reverse':
			dna.reverse();
		elif action == 'Complement':
			dna.complement();
		elif action == 'Reverse Complement':
			dna.reverse_complement()

		return template.format(dna=dna)
		

# launch the application with the debug messages
if __name__ == "__main__":		
	app.run(debug=True)