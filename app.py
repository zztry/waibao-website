from flask import Flask,request,render_template
from markupsafe import escape
import processing
import output

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
    #print(json_data)

    #processing.analyze_file(json_data)

    probs = processing.analyze_file(json_data)
    print("No.1success")
    output.word_output('90', probs)
    print("No.2success")
    return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(port=5000,debug=True)
