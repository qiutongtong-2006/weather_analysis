import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # 保存路径到 session 或直接重定向到预览页
            return redirect(url_for('preview', filename=file.filename))
    return render_template('index.html')

@app.route('/preview/<filename>')
def preview(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file_path) if filename.endswith('.csv') else pd.read_excel(file_path)
    return render_template('preview.html', table=df.head().to_html(), filename=filename)

if __name__ == '__main__':
    app.run(debug=True)