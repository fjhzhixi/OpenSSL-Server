from Crypto.Cipher import AES
import base64
import string
import random
 
class AESCrypto(object):
 
    """AES加密算法"""
 
    def __init__(self):
 
        self.aes_mode = AES.MODE_ECB
        self.aes_bs = 16
        self.AES_PAD = lambda s: s + (self.aes_bs - len(s) % self.aes_bs) * chr(self.aes_bs - len(s) % self.aes_bs)
        self.AES_UN_PAD = lambda s: s[0:-s[-1]]
 
    def aes_decryption(self, data, key):
        """
        aes解密
        解密后，将补足的空格用strip() 去掉
        :param data: 接收到的密文数据集合
        :param key: 服务端返回的随机生成的AESKey,二进制形式
        :return: aes解密后的明文数据
        """
        generator = AES.new(key, self.aes_mode)  # ECB模式无需向量iv
        data += (len(data) % 4) * '='
        decrypt_bytes = base64.b64decode(data)
        result = generator.decrypt(decrypt_bytes)
        result = self.AES_UN_PAD(result)
        result = str(result,encoding="utf-8")  # 转换类型
        # 去除解码后的非法字符
        return result
 
    def aes_encryption(self, data, key):
        """
        aes加密
        如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
        :param data: 要上传的所有明文数据集合，包含sign
        :param key:  本地随机生成的AESKey，字符串形式
        :return: aes加密后的密文数据
        """
        generator = AES.new(key, self.aes_mode)  # ECB模式无需向量iv
        crypt = generator.encrypt(self.AES_PAD(data))
        encrypt_str = base64.b64encode(crypt)
        result = encrypt_str.decode()
        return result
 
    @classmethod
    def aes_encrypt_key(cls):
        """随机生成AESKey"""
        source_str=string.ascii_letters+string.digits
        aes_key="".join(random.sample(source_str,16))
        return aes_key