# app.py
 
from flask import Flask, render_template, request
import markdown
import case2ka
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

app = Flask(__name__)
 
# Set a secret key for encrypting session data
app.secret_key = 'my_secret_key'

@app.before_request
def log_request_info():
    logger.info('Request: %s %s', request.method, request.url)
    logger.info('Headers: %s', dict(request.headers))
  
# Multiple health check endpoints for different platforms
@app.route('/health')
@app.route('/healthz')
@app.route('/ping')
def health_check():
    logger.info('Health check requested')
    return {'status': 'healthy', 'message': 'Flask app is running'}, 200

# Simple test endpoint
@app.route('/test')
def test():
    logger.info('Test endpoint accessed')
    return 'Flask app is working!', 200

# To render a Index Page 
@app.route('/')
def view_form():
    try:
        logger.info('Rendering index page')
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return f"Error: {str(e)}", 500
  
# For handling post request form we can get the form
# inputs value by using POST attribute.
# this values after submitting you will never see in the urls.
@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        Case_Number = request.form['Case_Number']
        Case_Subject = request.form['Case_Subject']
        Case_Description = request.form['Case_Description']
        Case_Description_file = request.files['Case_Description_file']

        print(Case_Number)
        print(Case_Subject)
        print(Case_Description)
        print(Case_Description_file.filename)

        if Case_Number != '' and Case_Subject != '' and Case_Description != '' and Case_Description_file.filename != '':
            kba = case2ka.MSDReadCaseData(Case_Number, Case_Subject, Case_Description, Case_Description_file)
            kbahtml = markdown.markdown(kba)
            print(kbahtml)
            return render_template('index.html', kbahtml=kbahtml)
        else:
            return render_template('index.html', kbahtml='<h1>Invalid Input</h1>')
    else:
        return render_template('index.html', kbahtml='<h1>Invalid Input</h1>')
 
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    logger.info(f'Starting Flask app on host=0.0.0.0, port={port}')
    app.run(host='0.0.0.0', port=port, debug=False)