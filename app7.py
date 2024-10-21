from flask import Flask, render_template, request, send_file
import subprocess
import os

app = Flask(__name__)
output_directory = 'output'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    output_file_path = None
    selected_button = 'A'  # Default to button A

    if request.method == 'POST':
        selected_button = request.form.get('button')
        file = request.files.get('file')
        textarea_content = request.form.get('textarea_content')

        # Determine which shell script to run based on the selected button
        script_name = 'script_a.sh' if selected_button == 'A' else 'script_b.sh'
        output_file_path = os.path.join(output_directory, 'output.txt')

        # Prepare input based on file upload or textarea
        if file:
            # Save the uploaded file
            file_path = os.path.join(output_directory, file.filename)
            file.save(file_path)
            # Execute shell script with the uploaded file
            subprocess.run([f'./{script_name}', file_path], stdout=open(output_file_path, 'w'))

        elif textarea_content:
            # Write the textarea content to a temporary file
            temp_input_file = os.path.join(output_directory, 'temp_input.txt')
            with open(temp_input_file, 'w') as f:
                f.write(textarea_content)
            # Execute shell script with the temp input file
            subprocess.run([f'./{script_name}', temp_input_file], stdout=open(output_file_path, 'w'))

        # Read output from the generated output file
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r') as f:
                output = f.read()

    return render_template('index.html', output=output, output_file_path=output_file_path, selected_button=selected_button)

@app.route('/download')
def download_output():
    return send_file(os.path.join(output_directory, 'output.txt'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
