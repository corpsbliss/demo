from flask import Flask, request, render_template, send_file
import subprocess
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure output and uploads directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    output_file_path = None
    selected_button = 'A'  # Default button

    if request.method == 'POST':
        selected_button = request.form.get('button')
        file = request.files.get('file')
        textarea_content = request.form.get('textarea_content')

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Execute the corresponding shell script based on the selected button
            script = 'scriptA.sh' if selected_button == 'A' else 'scriptB.sh'
            output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.txt')

            # Execute shell script
            with open(output_file_path, 'w') as output_file:
                subprocess.run(['bash', script, file_path], stdout=output_file)

            output = read_output_file()

        elif textarea_content:
            output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.txt')
            with open('temp_input.txt', 'w') as temp_input_file:
                temp_input_file.write(textarea_content)
            script = 'scriptA.sh' if selected_button == 'A' else 'scriptB.sh'

            # Execute shell script
            with open(output_file_path, 'w') as output_file:
                subprocess.run(['bash', script, 'temp_input.txt'], stdout=output_file)

            output = read_output_file()

    return render_template('index.html', output=output, output_file_path=output_file_path, selected_button=selected_button)

def read_output_file():
    output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.txt')
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r') as file:
            return file.read()
    return ''

@app.route('/download')
def download_output():
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], 'output.txt'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
