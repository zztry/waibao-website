from flask import Flask,request,render_template,redirect,url_for,jsonify
from markupsafe import escape
import processing
import output

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report.html')
def report():
    massage1 = request.args.get('massage1', '')
    massage2 = request.args.get('massage2', '')
    return render_template('report.html',massage1=massage1, massage2=massage2)


@app.route('/add', methods=['POST'])
def add():
    print(request.headers)
    print(type(request.json))
    print(request.json)
    result = request.json['a'] + request.json['b']
    return str(result)


prob_list = ['blank_page_error', 
            'repeat_click_error', 
            'poor_page_loading_problem',
            'poor_first_interaction_problem', 
            'poor_network_problem', 
            'lack_of_engaging_content', 
            'console_error',
            'console_warning',
            'page_text_error',
            'page_loading_error', 
            'high_click_latency_problem', 
            'high_rendering_latency_problem'] #len = 12

num_prob_list = [0,0,0,0,0,0,0,0,0,0,0,0]


@app.route('/upload_json', methods=['POST'])
def upload_file():
    # 从请求中获取 JSON 数据
    json_data = request.json
    #print(json_data)

    probs = processing.analyze_file(json_data)
    print("No.1success")
    output.word_output('90', probs)
    print("No.2success")
    num_prob_list = [0,0,0,0,0,0,0,0,0,0,0,0]
    total_user = len(probs)
    total_prob = 0
    for prob in probs:
        for p in prob[3]:
            total_prob += 1
            if p in prob_list:
                num_prob_list[prob_list.index(p)] += 1
    print(prob_list)
    print(num_prob_list)
    print(total_user)
    print(total_prob)
    return jsonify({'massage1': 'File uploaded successfully!', 'massage2': '60'})
    #return redirect(url_for('report',massage1='File uploaded successfully!', massage2="60"))
    return render_template('report.html', massage1='File uploaded successfully!', massage2="60")

if __name__ == '__main__':
    app.run(port=5000,debug=True)
