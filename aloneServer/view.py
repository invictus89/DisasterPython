# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    View Controller
    Flask서버의 전체적인 view 관리
    a.k.a Servlet
"""
from aloneServer import app
from aloneServer.pulse import Pulse
from aloneServer.util import tool, errLog
from aloneServer.util import ENC
from flask import request, render_template, redirect, send_file
from multiprocessing import Queue, Process

logger = errLog.ErrorLog.__call__()
q = Queue()
keyword_q = Queue()
"""
    API서버 Index Page
    
    * Token Key가 이미 발급됬을 경우
    key확인 Page로 redirect

    * Token Key가 미발급됬을 경우
    key발급 절차 진행
"""
@app.route('/', methods=["GET"])
def index():
    from aloneServer import socketio
    from aloneServer.manager import APIC
    
    if request.method == 'GET':
        key = request.args.get('Key')
        uri = request.args.get('URI')
        userIP = request.remote_addr
        decrypt_Key = APIC.process("home", userIP)
        
        if key == None:
            if decrypt_Key =='None':
                return render_template("index.html")
            else:
                return render_template("auth.html", key=decrypt_Key)
        else:
            if key == decrypt_Key:
                if uri == None:
                    return tool.HTTPError(412, "Wrong URL", userIP)
                else:
                    return redirect("/pulse?Key="+key+"URI="+uri)
            else:
                return tool.HTTPError(401,'Check Your Authorization Key',userIP)
"""
    API서버 Auth Page

    * key발급 절차완료 후 Token Key출력

    * 외부접근 불가능
"""
@app.route('/auth', methods=['GET','POST'])
def auth():
    from aloneServer.manager import APIC
    
    userIP = request.remote_addr
    if request.method == 'POST':
        type_1 = request.form['pulse_permission']
        type_2 = request.form['noti_permission']
        encryptKey = ENC.keyEncrypt(userIP)
        
        if APIC.process("auth", userIP, encryptKey):
            logger.writeLog("info", "Token issued : {0}".format(userIP))
            return render_template("auth.html", key=encryptKey)
        else:
            return tool.HTTPError(500, 'Token issued Failed.', userIP)
    elif request.method == 'GET':
        return tool.HTTPError(403, 'Unauthorized Access!', userIP)
"""
    API서버 Pulse Page

    * pulse Data 요청에 대한 return 기능 수행

    * 외부접근 가능 [PARAMETER : TOKEN KEY, TARGET URI]
"""
@app.route('/pulse', methods=['GET'])
def pulse():
    from aloneServer.manager import APIC

    key = request.args.get('Key')
    userIP = request.remote_addr
    if APIC.process("valid", key):
        uri = request.args.get('URI')
        
        if len(uri) < 10:
            return tool.HTTPError(412, "Wrong URL", userIP)
        else:
            try:
                done_queue = Queue()
                pulse_proc = Pulse(uri, done_queue, key)
                pulse_proc.start()
                resp = done_queue.get()
            except BaseException as e:
                return tool.HTTPError(500, "Wrong URL : {0}".format(e), userIP)
            finally:
                done_queue.close()
                done_queue.join_thread()
                pulse_proc.join()
                return resp
    else:
        return tool.HTTPError(401,'Check Your Authorization Key', userIP)
"""
    API서버 Detect Admin

    * 서버시작 후 Detect기능 활성화를 위한 ADMIN Page
"""
@app.route('/admin', methods=['GET'])
def admin():
    from aloneServer import jobs
    twit = "Ready"
    web = "Ready"
    keyword = "Ready"
    news = "Ready"

    if len(jobs) is not 0:
        if jobs['twit']:
            twit = "Twiter Detecting...."

        if jobs['web']:
            web = "Web Detecting...."

        if jobs['key']:
            keyword = "RealTime Keyword Detecting...."

        if jobs['key']:
            news = "NEWS Detecting...."

    return render_template("admin.html", twit=twit, web=web, keyword=keyword, news=news)
"""
    API서버 Twit Detect

    * 서버시작 후 Twit Detect기능 활성화 기능 수행

    * 외부접근 불가능, Root User만 활성화 가능,[PARAMETER : Key]
"""
@app.route('/twit', methods=['GET', 'POST'])
def twit():
    from aloneServer.manager import APIC
    userIP = request.remote_addr
    
    if request.method == 'POST':
        key = request.form['Key']

        if len(key) is 0:
            return tool.HTTPError(401,'Check Your Authorization Key',userIP)

        if not APIC.process("admin", key):
            return tool.HTTPError(403, 'Unauthorized Access!', key)

        from aloneServer import socketio, jobs
    
        if jobs['twit']:
            return tool.HTTPError(423, 'Already Detecting.')
        else: #첫 접근
            from aloneServer.detect import twitDetect, config
            
            proc = twitDetect.TwitDetect(**config.Detect_Config.twitConfig, _sock = socketio, _q = q, _kq = keyword_q)
            jobs['twit'] = proc
            proc.start()
        
        return "Twiter Detecting...."
    elif request.method == 'GET':
        return tool.HTTPError(403,'Wrong Access', userIP)
"""
    API서버 Web Detect

    * 서버시작 후 Web Detect기능 활성화 기능 수행

    * 외부접근 불가능, Root User만 활성화 가능,[PARAMETER : Key]
"""
@app.route('/web', methods=['GET','POST'])
def web():
    from aloneServer.manager import APIC
    userIP = request.remote_addr

    if request.method == 'POST':
        key = request.form['Key']

        if len(key) is 0:
            return tool.HTTPError(401,'Check Your Authorization Key',userIP)
    
        if not APIC.process("admin", key):
            return tool.HTTPError(403, 'Unauthorized Access!', key)

        from aloneServer import socketio, jobs
    
        if jobs['web']:
            return tool.HTTPError(423, 'Already Detecting.')
        else: #첫 접근
            from aloneServer.detect import webDetect, config
            proc = webDetect.WebDetect(**config.Detect_Config.webConfig_2)
            jobs['web'] = proc
            proc.start()
    
        return "Web Detecting...."
    elif request.method == 'GET':
        return tool.HTTPError(403,'Wrong Access', userIP)
"""
    API서버 Key Detect

    * 서버시작 후 Key Detect기능 활성화 기능 수행

    * 외부접근 불가능, Root User만 활성화 가능,[PARAMETER : Key]
"""
@app.route('/realKey', methods=['GET','POST'])
def realKey():
    from aloneServer.manager import APIC
    userIP = request.remote_addr

    if request.method == 'POST':
        key = request.form['Key']

        if len(key) is 0:
            return tool.HTTPError(401,'Check Your Authorization Key',userIP)
    
        if not APIC.process("admin", key):
            return tool.HTTPError(403, 'Unauthorized Access!', key)

        from aloneServer import socketio, jobs
        
        if jobs['key']:
            return tool.HTTPError(423, 'Already Detecting.')
        else: #첫 접근
            from aloneServer.detect import keyDetect, config
            proc = keyDetect.KeyDetect(**config.Detect_Config.keyConfig, _q = keyword_q)
            jobs['key'] = proc
            proc.start()
    
        return "RealTime Keyword Detecting...."
    elif request.method == 'GET':
        return tool.HTTPError(403,'Wrong Access', userIP)
"""
    API서버 News Detect

    * 서버시작 후 News Detect기능 활성화 기능 수행

    * 외부접근 불가능, Root User만 활성화 가능,[PARAMETER : Key]
"""
@app.route('/news', methods=['GET','POST'])
def news():
    from aloneServer.manager import APIC
    userIP = request.remote_addr

    if request.method == 'POST':
        key = request.form['Key']

        if len(key) is 0:
            return tool.HTTPError(401,'Check Your Authorization Key',userIP)
    
        if not APIC.process("admin", key):
            return tool.HTTPError(403, 'Unauthorized Access!', key)

        from aloneServer import socketio, jobs
        if jobs['news']:
            return tool.HTTPError(423, 'Already Detecting.')
        else: #첫 접근
            from aloneServer.detect import newsDetect, config
            proc = newsDetect.NewsDetect(**config.Detect_Config.newsConfig, _q = q)
            proc.start()
            jobs['news'] = proc
        return "NEWS Detecting...."
    elif request.method == 'GET':
        return tool.HTTPError(403,'Wrong Access', userIP)
"""
    API서버 WordCloud Draw

    * 호출시 wordCloud 이미지 생성

    * 외부접근시 이미지출력, [PARAMETER : type]
"""
@app.route('/word')
def word():
    import nltk
    from konlpy.corpus import kolaw
    from konlpy.tag import Twitter; nlp = Twitter()
    from wordcloud import WordCloud, ImageColorGenerator

    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
    from matplotlib import font_manager, rc

    from aloneServer.manager import APIC
    data = dict()
    stop_words = ['일','년','이','것','그','수','존나','너무','등','때','중','분','나','짱']
    wType = "지진"
    src = "img\\"

    if wType is "지진":
        templetName = "earth.png"
        fileName = "wordEq.png"
    elif wType is "날씨이상":
        templetName = "earth.png"
        fileName = "wordWe.png"
    elif wType is "사고":
        templetName = "earth.png"
        fileName = "wordAc.png"

    row = APIC.process("wordSelect", wType, 1000)
    for r in row:
        if r[0] not in stop_words:
            data[r[0]] = r[1]

    korea_coloring = np.array(Image.open(src+"earth.png"))
    image_colors = ImageColorGenerator(korea_coloring)
    wordcloud = WordCloud(font_path="c:/Windows/Fonts/H2SA1M.ttf",
                            relative_scaling=0.1,
                            mask=korea_coloring,
                            background_color=None,
                            mode='RGBA',
                            min_font_size=1,
                            max_font_size=140,
                            max_words=2000,
                            color_func=tool.grey_color_func,
                            random_state=42).generate_from_frequencies(data)
    
    wordcloud.to_file(src+fileName)
    return send_file("..\\"+src+fileName, mimetype='image/png')