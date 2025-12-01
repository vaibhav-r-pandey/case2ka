# app.py
 
from flask import Flask, render_template, request
import markdown
import case2ka

app = Flask(__name__)
 
# Set a secret key for encrypting session data
app.secret_key = 'my_secret_key'
  
# To render a Index Page 
@app.route('/')
def view_form():
    return render_template('index.html')
  
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)