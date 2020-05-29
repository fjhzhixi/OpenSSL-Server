from flask import Flask, json, request, Response
import rsa
import base64
import binascii

app = Flask(__name__)

aseKey = 'yzxfjhxqzjh'

def str2key(s):
    # 对字符串解码
    b_str = base64.b64decode(s)

    hex_str = ''

    # 按位转换成16进制
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h

    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2

    modulus_ = hex_str[m_start:m_start + m_len]
    exponent_ = hex_str[e_start:e_start + e_len]

    modulus = int(modulus_, 16)
    exponent = int(exponent_, 16)
    pubkey = rsa.PublicKey(modulus, exponent)
    return pubkey

@app.route('/sendkey', methods = ['POST'])
def key_data():
    data_ = request.form['data']
    data = json.loads(data_)
    pubkey_ = data['pubkey']
    print("收到的公钥：")
    print(pubkey_)
    pubkey = str2key(pubkey_)
    seed_ = rsa.encrypt(aseKey.encode('utf8'), pubkey)
    seed = binascii.hexlify(seed_)
    info=dict()
    print(seed)
    info['seed'] = bytes.decode(seed)
    resp = Response(json.dumps(info), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=7000)