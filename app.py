from flask import Flask,request,render_template,session,send_file,jsonify
import processing
import json
import output

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    score = session.get('score')
    return render_template('report.html', score=score, pro_num_dict=session.get('pro_num_dict'),
                           data_list=session.get('data_list')
                           , suggestion=session.get('suggestion')
                           ,problem_analysis=session.get('problem_analysis'))


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

cn_prob_list = ['出现空白页面错误',
                '重复点击某个元素',
                '页面加载质量差',
                '用户首次与网站交互时感到不愉快',
                '网络通信延迟',
                '缺乏引人注意的内容',
                '控制台报错',
                '控制台警告',
                '页面内容或文本出现错误',
                '页面加载错误',
                '高点击延迟',
                '高渲染延迟'] #len = 12

answer_list={
    #1.出现空白页面错误
    'blank_page_error':'对于空白页面错误，建议开发者扩充检查页面加载过程中的网络请求，确保网络连接正常；审查服务器响应，确认服务器状态良好；同时仔细检查页面内容，以确定并解决问题。',
    #2控制台报错
    'console_error':'针对控制台报错问题，建议开发者仔细检查 JavaScript 代码，特别是关注报错信息所指示的文件、行号和错误类型，以便准确定位问题所在；随后修复代码中的错误或异常情况，以确保网页的正常运行和用户体验。',
    #3控制台警告
    'console_warning':'对于控制台警告问题，虽然不会导致代码完全失败，但可能会影响网页性能。建议开发者仔细检查警告信息，特别关注其中提到的潜在问题，并进行相应的代码修复，以提高代码的质量和性能。',
    #4高点击延迟
    'high_click_latency_problem':'针对高点击延迟问题，开发者应该分析页面加载速度、响应时间和事件处理逻辑，以及优化 JavaScript 代码执行效率和事件处理逻辑，优化资源加载、压缩文件、减少不必要的请求，以提升用户体验。',
    #5高渲染延迟
    'high_rendering_latency_problem':'对于高渲染延迟问题，建议开发者分析页面的渲染流程，优化页面的渲染性能，减少页面元素的加载时间和渲染时间，提升页面的加载速度和响应性能，以改善用户体验。',
    #6缺乏引人注意的内容
    'lack_of_engaging_content':'对于页面不具有吸引力的问题，开发者可以取尝试改善页面的设计、添加更多有趣的内容、提供交互式功能、增加视觉效果等方式来提升用户体验，使用户更愿意停留在页面上并与内容进行互动。',
    #7网络通信延迟
    'network_latency_problem':'对于网络通信延迟问题，开发者应分析网络通信流程，确定延迟原因，并采取措施优化网络通信以减少传输延迟，如调整网络配置、减少传输量、利用CDN加速、数据压缩、缓存和预加载等。',
    #8页面加载错误
    'page_loading_error':'针对页面加载错误问题，开发者应该仔细检查页面加载过程中的各个环节，包括网络请求、服务器响应、前端代码执行等，以确定并解决造成页面加载错误的根本原因。',
    #9页面内容或文本出现错误
    'page_text_error':'针对页面内容或文本出现错误问题，开发者应该检查页面内容或文本数据源，确保数据源的准确性和完整性。如果是前端渲染问题，可能需要检查前端代码中的文本处理逻辑，确保正确地显示文本内容。',
    #10页面加载质量差
    'poor_loading_problem':'关于页面加载质量差问题，开发者应该分析页面加载过程中可能存在的瓶颈，并采取相应的措施来优化页面加载速度和质量。可能的解决方案包括优化页面资源的加载顺序和大小、使用 CDN 加速、减少 HTTP 请求次数等。',
    #11重复点击某个元素
    'repeat_click_error':'针对用户多次重复点击同一元素问题，开发者应该实现防止重复点击的机制，可通过禁用按钮或添加点击延迟来确保用户不会多次点击造成问题。另外，开发者还可以通过前端代码或服务器端逻辑来处理重复点击事件，例如在前端使用 JavaScript 进行点击事件的监听和处理。',
    #12用户首次与网站交互时感到不愉快
    'unpleasant_first_interaction_problem':'关于用户首次使用网站体验感较差的问题，开发者应该重视用户的首次交互体验，优化页面加载速度、布局设计和功能交互，以提升用户的满意度和使用体验。能的解决方案包括简化界面设计、减少加载时间、提供清晰的引导和提示等。'


}



qusetion_anylist={
    #1.出现空白页面错误
    'blank_page_error':'空白页面错误的出现可能由于多种原因，包括网络连接问题、服务器故障、页面代码错误或浏览器问题等，这些因素都可能导致页面无法正常加载。',
    #2控制台报错
    'console_error':'控制台报错通常出现在浏览器的开发者工具中，表示页面中的 JavaScript 代码出现了错误。这种错误可能是由于语法错误、未定义的变量、函数调用问题等引起的。',
    #3控制台警告
    'console_warning':'控制台警告表示页面中的 JavaScript 代码出现了警告信息。这些警告可能是由于代码中一些潜在问题或不规范的写法引起的。',
    #4高点击延迟
    'high_click_latency_problem':'高点击延迟可能是由于页面加载速度慢、事件处理逻辑复杂或网络通信延迟等原因引起的。',
    #5高渲染延迟
    'high_rendering_latency_problem':'高渲染延迟问题可能是由于页面结构复杂、资源加载过多、CSS 或 JavaScript 代码执行效率低下等原因引起的。',
    #6缺乏引人注意的内容
    'lack_of_engaging_content':'页面不具有吸引力问题的出现可能是由于内容数量不足、质量不高、设计不佳或缺乏交互性等因素造成的。',
    #7网络通信延迟
    'network_latency_problem':'网络通信延迟问题可能是由于网络连接不稳定、服务器响应时间长、网络拥塞或数据传输量过大等原因造成的。',
    #8页面加载错误
    'page_loading_error':'页面加载错误问题可能是由于网络问题、服务器故障、页面资源加载失败、JavaScript 代码错误等多种原因引起的。',
    #9页面内容或文本出现错误
    'page_text_error':'页面内容或文本出现错误可能是由于数据源问题、页面代码问题、字符编码问题或其他原因引起的。',
    #10页面加载质量差
    'poor_loading_problem':'页面加载质量差可能是由于网络连接不稳定、服务器响应时间长、页面资源加载过多或过大、JavaScript 代码执行效率低下等原因造成的。',
    #11重复点击某个元素
    'repeat_click_error':'用户多次重复点击同一元素可能是由于页面交互逻辑设计不佳，未能有效处理用户的快速点击行为，或者是由于用户体验较差，用户感知不到他们的点击操作已经被处理而导致的。',
    #12用户首次与网站交互时感到不愉快
    'unpleasant_first_interaction_problem':'用户首次使用网站体验感较差可能是由于页面加载速度过慢、界面设计不吸引人、内容不清晰或交互过程不流畅等原因导致的。'

}

#下载文件
@app.route('/download', methods=['GET'])
def download():
    # 要下载的文件路径
    file_path = 'output_report.docx'

    # 发送文件
    return send_file(file_path, as_attachment=True)
   

@app.route('/upload_json', methods=['POST'])
def upload_file():
    files = request.files.getlist('file')  # 获取名为 'file' 的所有文件

    print(len(files))
    probs = []
    if len(files) == 0:
        print("No file uploaded")
        return "No file uploaded"
    for file in files:
        file.content = file.read()
        json_data = json.loads(file.content)
        print("1111")
        probs += processing.analyze_file(json_data)
    # # 从请求中获取 JSON 数据
    # json_data = request.json
    # #print(json_data)
   
    # probs = processing.analyze_file(json_data)
    #print("No.1success")
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
    
    score = score/total_user #只保留1位小数
    score = round(score,1)
    
    #print("No.2success")
     
    #print(num_prob_list) #每个问题出现的次数
    #print(total_user)   #用户总数
    #print(total_prob)   #问题总数
    pro_num_dict = dict(zip(prob_list, num_prob_list)) #<问题名，次数>
    cn_pro_num_dict = dict(zip(cn_prob_list, num_prob_list)) #<问题名cn，次数>
    
    
    data_list = []  # 构建数据列表,用于echarts
    suggestion = ''
    suggestion_output = ''
    i1 = 1

    for name, value in cn_pro_num_dict.items():
        if value != 0:
            data_list.append({'value': value, 'name': name})

    for name, value in pro_num_dict.items():
        if value != 0:
            suggestion += f"{i1}. "+ answer_list[name] + "<br>"
            suggestion_output += f"{i1}. "+ answer_list[name] + "\n\t"
            i1 += 1

    
    num=0
    for name, value in pro_num_dict.items():
        if value != 0:
           num+=1
    #num表示一共出现几种问题

    problem_analysis = ''
    problem_analysis_output = ''
    problem_analysis+="经过算法分析共识别出"+ f"{num} " + "种可能的问题，这里按问题发生概率大小展示<b>部分</b>问题如下（详情见报告）："+ "<br>"
    problem_analysis_output+="经过算法分析共识别出"+ f"{num} " + "种可能的问题，如下："+ "\n\t"

    
    i2=1

    for name, value in pro_num_dict.items():
        if value != 0:
            problem_analysis_output += f"{i2}. "+name+"发生的概率是"+f"{round(pro_num_dict[name]/total_user, 3)}"+"。具体分析如下："+ qusetion_anylist[name] + "\n\t"
            i2 += 1

    ##New 输出部分结果4.15   02：04
    i3=1
    nowlen=1


    sorted_items = sorted(pro_num_dict.items(), key=lambda x: x[1], reverse=True)

    for name, value in sorted_items:
        if value != 0:
            if nowlen < len(pro_num_dict.items()) / 4:
                problem_analysis += f"{i3}. {name}发生的概率是<b>{round(value / total_user, 3)}</b>。<br>{qusetion_anylist[name]}<br>"
                nowlen += 1
                i3 += 1

    output.word_output(str(score), probs, suggestion_output,problem_analysis_output)



    

    session['score'] = str(score)
    session['pro_num_dict'] = pro_num_dict
    session['data_list'] = data_list
    session['suggestion'] = suggestion
    session['problem_analysis'] = problem_analysis

    return "hello coder"

    # return jsonify({'massage1': 'File uploaded successfully!', 'massage2': '60'})
    # #return redirect(url_for('report',massage1='File uploaded successfully!', massage2="60"))
    # return render_template('report.html', massage1='File uploaded successfully!', massage2="60")

if __name__ == '__main__':
    app.run(port=5000,debug=True)
