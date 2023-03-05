from flask import Flask, request, make_response
import hashlib
import time
import xmltodict
import openai


app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world！'


@app.route('/wechat',methods=['GET','POST'])
def wechat():
    if request.method =='GET':
        # 设置token,开发者配置中心使用
        token = 'hsuheinrich003'

        # 获取微信服务器发送过来的参数
        data = request.args
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')

        # 对参数进行字典排序，拼接字符串
        temp = [timestamp, nonce, token]
        temp.sort()
        temp = ''.join(temp)

        # 加密
        if (hashlib.sha1(temp.encode('utf8')).hexdigest() == signature):
            return echostr
        else:
            return 'error', 403

    # 根据请求方式进行判断
    if request.method == 'POST':
        # 获取微信服务器post过来的xml数据
        xml = request.data
        # 把xml格式的数据进行处理，转换成字典进行取值
        req = xmltodict.parse(xml)['xml']
        # 判断post过来的数据中数据类型是不是文本
        if 'text' == req.get('MsgType'):
            # 获取用户的信息，开始构造返回数据
            try:
                resp = {
                    'ToUserName':req.get('FromUserName'),
                    'FromUserName':req.get('ToUserName'),
                    'CreateTime':int(time.time()),
                    'MsgType':'text',
                    'Content':chat_reply(req.get('Content'))
                }
                xml = xmltodict.unparse({'xml':resp})
                return xml
            except:
                resp = {
                    'ToUserName':req.get('FromUserName'),
                    'FromUserName':req.get('ToUserName'),
                    'CreateTime':int(time.time()),
                    'MsgType':'text',
                    'Content':'好像发生了点问题，请稍后再重新提问～'
                }
                xml = xmltodict.unparse({'xml':resp})
                return xml
            finally:
                return
        else:
            resp = {
                'ToUserName': req.get('FromUserName', ''),
                'FromUserName': req.get('ToUserName', ''),
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': '仅支持文本消息～'
            }
            xml = xmltodict.unparse({'xml':resp})
            return xml

def chat_reply(content):
    openai.api_key = 'sk-qdu******7kCA'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301", # 最新模型
        messages=[{"role": "user", "content": content}],
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
