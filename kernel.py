from flask import Flask, request, render_template_string, send_file
import io

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Text Sync</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
        }
        .container {
            display: flex;
            flex-direction: column;
            width: 80%;
            max-width: 1200px;
            align-items: center;
        }
        textarea {
            width: 45%;
            height: 300px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            resize: none;
            margin: 10px;
        }
        .form-group {
            display: flex;
            width: 100%;
            justify-content: space-between;
        }
        input[type="submit"], .upload-button, .download-button {
            display: block;
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .upload-button {
            background-color: #28a745;
            color: white;
        }
        .upload-button:hover {
            background-color: #218838;
        }
        .download-button {
            background-color: #17a2b8;
            color: white;
        }
        .download-button:hover {
            background-color: #117a8b;
        }
    </style>
</head>
<body>
    <div class="container">
        <form method="post" action="/" enctype="multipart/form-data">
            <input type="file" name="file" class="upload-button">
            <div class="form-group">
                <textarea name="left_text" placeholder="Enter text on the left">{{ left_text }}</textarea>
                <textarea name="right_text" placeholder="Content will appear on the right" readonly>{{ right_text }}</textarea>
            </div>
            <input type="submit" value="Submit">
        </form>
        {% if right_text %}
        <a href="/download" class="download-button">Download Text</a>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    right_text = ""
    left_text = ""
    
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.txt'):
                file.save('textfile.txt')
        
        if 'left_text' in request.form:
            left_text = request.form['left_text']
            with open('textfile.txt', 'w') as f:
                f.write(left_text)
        
        with open('textfile.txt', 'r') as f:
            right_text = f.read()

    return render_template_string(HTML_TEMPLATE, right_text=right_text, left_text=left_text)

@app.route('/download')
def download():
    with open('textfile.txt', 'r') as f:
        file_content = f.read()
    
    buffer = io.BytesIO()
    buffer.write(file_content.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='textfile.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True)
