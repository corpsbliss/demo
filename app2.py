from flask import Flask, render_template, request, send_file, redirect, url_for
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_button = 'A'  # Default button is A
    output = ""
    output_file_path = None

    if request.method == 'POST':
        selected_button = request.form['button']
        file = request.files.get('file')
        textarea_content = request.form.get('textarea_content')

        # Determine if a file was uploaded or textarea input was provided
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        elif textarea_content:
            filename = 'textarea_input.txt'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(file_path, 'w') as f:
                f.write(textarea_content)
        else:
            return "Please upload a file or enter content in the textarea."

        # Execute the appropriate shell script based on the button selected
        if selected_button == 'A':
            script = './scriptA.sh'
        else:
            script = './scriptB.sh'

        try:
            # Run the shell script with the file path as input
            result = subprocess.run([script, file_path], capture_output=True, text=True)
            output = result.stdout

            # Save the output to a file
            output_filename = f'{filename}_output.txt'
            output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            with open(output_file_path, 'w') as f:
                f.write(output)
        except Exception as e:
            output = f"Error running script: {str(e)}"

    return render_template('index.html', selected_button=selected_button, output=output, output_file_path=output_file_path)

@app.route('/download_output')
def download_output():
    """Serve the generated output file for download."""
    output_file_path = request.args.get('file')
    if output_file_path and os.path.exists(output_file_path):
        return send_file(output_file_path, as_attachment=True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
