import os

from flask import Flask, request, jsonify
from wechatpy import parse_message
from wechatpy.replies import TextReply
import xmltodict

app = Flask(__name__)

# 主页
@app.route('/')
def hello_world():
    return '欢迎来到HsuHeinrich的世界'

# 测试消息
@app.route('/test', methods=['POST'])
def test():
  return jsonify({'success':True,'msg':'测试中，请忽略'})

# 消息推送
@app.route('/message/post', methods=['POST'])
def wechat_message():
    # 根据请求方式进行判断
    if request.method == 'POST':
        xml = request.data
        print(xml)
        return
        # # 把xml格式的数据进行处理，转换成字典进行取值
        # req = xmltodict.parse(xml)['xml']
        # # 判断post过来的数据中数据类型是不是文本
        # if 'text' == req.get('MsgType'):
        #     # 获取用户的信息，开始构造返回数据，把用户发送的信息原封不动的返回过去，字典格式
        #     resp = {
        #         'ToUserName':req.get('FromUserName'),
        #         'FromUserName':req.get('ToUserName'),
        #         'CreateTime':int(time.time()),
        #         'MsgType':'text',
        #         'Content':req.get('Content')
        #     }
        #     # 把构造的字典转换成xml格式
        #     xml = xmltodict.unparse({'xml':resp})
        #     # print(req.get('Content'))
        #     # 返回数据
        #     return xml
        # else:
        #     resp = {
        #         'ToUserName': req.get('FromUserName', ''),
        #         'FromUserName': req.get('ToUserName', ''),
        #         'CreateTime': int(time.time()),
        #         'MsgType': 'text',
        #         'Content': '暂不支持非文本消息'
        #     }
        #     xml = xmltodict.unparse({'xml':resp})
        #     return xml

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=80)
