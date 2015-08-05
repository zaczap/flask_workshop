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
	<form action='/lookup' method='GET'>

		<input type='text' name='gene_name' placeholder='Enter a gene name'>
		<input type='submit' value='Get stats'>

	</form>
</html>
"""

@app.route("/")
def homepage():
	return homepage_html

@app.route("/lookup", methods=['GET'])
def statistics():
	gene_name = request.args.get('gene_name', '')
	gene_name = gene_name.upper()
	homepage_link = "<a href='/'>Go back</a>"

	return "<html>{0}. {1}</html>".format(gene_data['CICP4'], homepage_link)



# launch the application with the debug messages
if __name__ == "__main__":

	# load in the data from the GTF file
	path_to_gtf_file = "gencode.chr20.genes.annotation.gtf"
	gtf_file = open(path_to_gtf_file)
	gene_data = {}
	for line in gtf_file:
		seqname, source, feature, start, end, score, strand, frame, attribute = line.strip().split('\t')
		fields = attribute.split(';')[:-1]
		fields = [x.strip().split(' ') for x in fields]
		fields = {key:value.strip('"') for (key,value) in fields}
		gene_name = fields['gene_name']
		gene_id = fields['gene_id']
		gene_type = fields['gene_type']
		record = {}
		record['chrom'] = seqname
		record['start'] = start 
		record['end'] = end
		record['strand'] = strand
		record['name'] = gene_name
		record['id'] = gene_id
		record['type'] = gene_type
		gene_data[gene_name] = record
		
	app.run(debug=True)