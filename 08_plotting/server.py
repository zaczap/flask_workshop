from flask import Flask
from flask import request
import matplotlib.pyplot as plt
import cStringIO

# get an app instance
app = Flask(__name__)

template = """
<html>

 <head>
  <title>scatterplot plotter</title>
  
 </head>
 <body>

	<div id="content">

		<!-- Headline -->
		<h4>2D Scatter plot</h4>
		<form action='/' method='GET'>
		<textarea name='points' cols=75 rows=10 placeholder="Enter plotting points here">{points}</textarea>
		<br/>
		<input type='submit' name='submitted' value='Plot'/>
		</form>
	</div>

 </body>
</html>
"""



def generate_image_tag():
	template = "<img width=400 height=300 src='data:image/png;base64,{0}'/>"
	sio = cStringIO.StringIO()
	plt.savefig(sio, format='png')
	return template.format(sio.getvalue().encode("base64").strip()) 

@app.route('/', methods=['GET'])
def handleDNA():
	points = request.args.get('points', '')
	action = request.args.get('submitted', '')

	# Handle default requests - no submission
	if action == '':
		return template.format(points=points)

	# Handle an actual response
	else:
		x_points = []
		y_points = []
		for point in points.strip().split('\n'):
			x, y = point.split(',')
			x_points.append(float(x.strip()))
			y_points.append(float(y.strip()))
		plt.scatter(x_points, y_points)
		plt.xlabel('X points')
		plt.ylabel('Y points')
		plt.title('Scatterplot')
		return template.format(points=points) + generate_image_tag()
		

# launch the application with the debug messages
if __name__ == "__main__":		
	app.run(debug=True)