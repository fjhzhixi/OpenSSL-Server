#coding:utf-8
from flask import Flask, json, request, Response
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
import binascii

app = Flask(__name__)

#AES公钥
aseKey = '1234123412ABCDEF'
#RSA公钥
pubkey_gl = ''
#mode = AES.MODE_OFB

@app.route('/sendkey', methods = ['GET', 'POST'])
def key_data():
    global pubkey_gl
    #GET请求
    if request.method == 'GET':
        #判断当前是否已收到RSA公钥
        if pubkey_gl == '':
            print("wrong")
            info=dict()
            info['seed'] = "empty"
            resp = Response(json.dumps(info), mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        #导入已得到的RSA公钥
        pubkey = RSA.importKey(pubkey_gl)
        #公钥加密
        cipher = PKCS1_cipher.new(pubkey)
        seed_ = base64.b64encode(cipher.encrypt(bytes(aseKey.encode("utf8"))))
        seed = seed_.decode("utf8")
        print(pubkey_gl)
        print(seed)
        #打包为json发送给前端
        info=dict()
        info['seed'] = seed
        resp = Response(json.dumps(info), mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    '''
    AES
    cryptor = AES.new(aseKey.encode('utf-8'), mode, b'0000000000000000')
    length = 16
    message = "123"
    count = len(message)
    if count % length != 0:
        add = length - (count % length)
    else:
        add = 0
    message = message + ('\0' * add)
    print(len(message))
    ciphertext = cryptor.encrypt(message)
    result = b2a_hex(ciphertext)
    print(result.decode('utf-8'))
    
    cryptor = AES.new(aseKey.encode('utf-8'), mode, b'0000000000000000')
    plain_text = cryptor.decrypt(a2b_hex(result))
    print(plain_text.decode('utf-8').rstrip('\0'))
    '''
    #POST请求
    if request.method == 'POST':
        #获取RSA公钥
        data_ = request.form['data']
        data = json.loads(data_)
        pubkey_ = data['pubkey']
        pubkey_gl = pubkey_
        pubkey = RSA.importKey(pubkey_)  
        #公钥加密
        cipher = PKCS1_cipher.new(pubkey)
        seed_ = base64.b64encode(cipher.encrypt(bytes(aseKey.encode("utf8"))))
        seed = seed_.decode("utf8")
        print(pubkey_gl)
        print(seed)
        #打包为json发送给前端
        info=dict()
        info['seed'] = seed
        resp = Response(json.dumps(info), mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

if __name__ == '__main__':
    app.run(debug=True, port=7000)