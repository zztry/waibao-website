from flask import Flask,request,render_template
from markupsafe import escape
import processing

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report.html')
def report():
    return render_template('report.html')


@app.route('/add', methods=['POST'])
def add():
    print(request.headers)
    print(type(request.json))
    print(request.json)
    result = request.json['a'] + request.json['b']
    return str(result)





@app.route('/upload_json', methods=['POST'])
def upload_file():
    # 从请求中获取 JSON 数据
    json_data = request.json
    processing.analyze_file(json_data)
    
    print(type(json_data))
    
    # 在这里处理接收到的 JSON 数据
    print("I like coding")
    return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(port=5000,debug=True)
