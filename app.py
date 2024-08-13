from flask import Flask, request, render_template, send_file, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'log', 'text'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file1' in request.files:
            file = request.files['file1']
            if file and allowed_file(file.filename):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'error.log')
                file.save(filepath)

        if 'textarea' in request.form:
            content = request.form['textarea']
            with open(os.path.join(app.config['UPLOAD_FOLDER'], 'error.log'), 'a') as f:
                f.write(content + '\n')

    return render_template('index.html')

@app.route('/view')
def view_file():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'error.log')
    with open(filepath, 'r') as f:
        content = f.read()
    return render_template('view.html', content=content)

@app.route('/download')
def download_file():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'error.log')
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
  
