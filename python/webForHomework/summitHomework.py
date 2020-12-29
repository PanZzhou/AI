# 文件上传
import flask, os, sys,time
from flask import request

#文件存储的路径
filePath = "/software/homework/all/"
#filePath = "D:/tmp/"
your_port=9020 #开放的端口

interface_path = os.path.dirname(__file__)
sys.path.insert(0, interface_path)  #将当前文件的父目录加入临时系统变量

server = flask.Flask(__name__, static_folder='static')

'''
DROP TABLE IF EXISTS dsp;

CREATE TABLE dsp (
  id int(4) unsigned NOT NULL AUTO_INCREMENT,
  name varchar(100) NOT NULL COMMENT '文件名',
  time varchar(100) NOT NULL COMMENT '上传时间',
  PRIMARY KEY (id),
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
INSERT INTO dsp VALUES (1,'测试文件.rar','2020-12-17 21:55:21');
'''
array = []
@server.route('/', methods=['get'])
def index():
    print("index")
    h1 = '<h2>请上传作业文件（工程伦理命名格式：题目-工程伦理-姓名-学号.PDF），</h2>'
    h2 = '<form action="/upload" method="post" enctype="multipart/form-data"><input type="file" id="img" name="img"><button type="submit">上传</button></form>'
    h3 = '<h3>&gt;&gt;已提交的作业列表：</h3>'
    #连接数据库后，读取数据，按照时间倒序（最近提交排在前面）
    lent = len(array)
    h4 = ''
    for i in range(lent):
        h4 += '<li>{}(提交于{})<hr></li>'.format(array[lent-i-1][0],array[lent-i-1][1])
    return h1+h2+h3+h4
    

@server.route('/upload', methods=['post'])
def upload():
    fname = request.files['img']  #获取上传的文件
    if fname:
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        #print(t)
        
        new_fname = filePath + fname.filename
        fname.save(new_fname)  #保存文件到指定路径
        array.append((fname.filename,t))
        print(array[len(array)-1][0])
        print(array[len(array)-1][1])
        return fname.filename + "文件提交成功"
        #return '<img src=%s>' %  new_fname
    else:
        return '{"msg": "请上传文件！"}'
print('----------路由和视图函数的对应关系----------')
print(server.url_map) #打印路由和视图函数的对应关系
server.run(host='0.0.0.0',port=your_port,debug=True)#任何电脑都能访问，需要电脑开启端口的外部访问
#server.run(port=your_port) #只能本地访问




