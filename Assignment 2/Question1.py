from flask import Flask
import re

app = Flask(__name__)

def generateReponse(inputString):
	outputString = ''
	if inputString.isalpha():
		if inputString.islower():
			outputString = inputString.upper()
		elif inputString.isupper():
			
			outputString = inputString.lower()
		else:
			outputString = inputString
	else:
		outputString = re.sub(r'[^a-zA-Z ]', '', inputString)
	return outputString



@app.route('/<obtained_string>')
def root(obtained_string):

	pageString = generateReponse(obtained_string)
	return '''<html>
	<head>
	</head>
	<body>
	Hello {0} welcome again and here are new updates
	</body>
	</html>'''.format(pageString)
	
if __name__ == '__main__':
	app.run(debug=True)