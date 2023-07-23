# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from GitCode import main

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__, template_folder='frontend')

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def landing_page():
	import markdown
	with open('../README.md', 'r') as f:
		readme_text = f.read()
	html_text = markdown.markdown(readme_text)
	open('frontend/readme.html', 'w').write(html_text)
	return render_template('index.html')

@app.route('/GitCode', methods=['GET', 'POST'])
def GitCode():
	if request.method == 'POST':
		path = request.form['path']
		browser = int(request.form['browser'])
		return main(path, browser)
	return {}, 200

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()
