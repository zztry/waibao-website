from flask import Flask,request,render_template,jsonify,session
from markupsafe import escape
import processing
import output

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
   
    massage2 = session.get('total_user')
    return render_template('report.html', massage2=massage2)


@app.route('/add', methods=['POST'])
def add():
    print(request.headers)
    print(type(request.json))
    print(request.json)
    result = request.json['a'] + request.json['b']
    return str(result)


prob_list = ['blank_page_error', 
            'repeat_click_error', 
            'poor_loading_problem',
            'unpleasant_first_interaction_problem', 
            'network_latency_problem', 
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
    score = 0
    total_user = len(probs)
    total_prob = 0
    for prob in probs:
        score += prob[4]
        for p in prob[3]:
            total_prob += 1
            if p in prob_list:
                num_prob_list[prob_list.index(p)] += 1
    print(prob_list)
    print(num_prob_list)
    print(total_user)
    print(total_prob)
    score = score/total_user #只保留1位小数
    score = round(score,1)
    session['total_user'] = str(score)
    return "hello coder"

    # return jsonify({'massage1': 'File uploaded successfully!', 'massage2': '60'})
    # #return redirect(url_for('report',massage1='File uploaded successfully!', massage2="60"))
    # return render_template('report.html', massage1='File uploaded successfully!', massage2="60")

if __name__ == '__main__':
    app.run(port=5000,debug=True)
