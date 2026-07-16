import base64
import binascii

class Confusion:
    def __init__(self):
        pass

    def multi_obscure(self, text: str) -> str:
        """
        对明文进行多重编码混淆
        :param text: 原始明文字符串
        :return: 混淆后的字符串
        """
        try:
            # 第一层：Base64 编码
            step1 = base64.b64encode(text.encode('utf-8'))

            # 第二层：Hex 编码（转为 0-9a-f 字符）
            step2 = binascii.hexlify(step1)

            # 第三层：Base32 编码
            step3 = base64.b32encode(step2).decode('utf-8')

            return step3
        except Exception as e:
            print(f"[混淆失败] 发生错误: {e}")
            return None

    def multi_obscure_decode(self, encoded_str: str) -> str:
        """
        对混淆后的字符串进行逆向解码还原
        :param encoded_str: 混淆后的字符串
        :return: 还原后的原始明文字符串
        """
        try:
            # 第一层逆向：Base32 解码
            step1 = base64.b32decode(encoded_str)

            # 第二层逆向：Hex 解码
            step2 = binascii.unhexlify(step1)

            # 第三层逆向：Base64 解码
            step3 = base64.b64decode(step2)

            # 最终转换为字符串返回
            return step3.decode('utf-8')
        except Exception as e:
            print(f"[解码失败] 发生错误: {e}")
            return None

    # def to_base64_old(self, str):
    #     encoded = base64.b64encode(str.encode('utf-8')).decode('utf-8')
    #     # print("Base64 编码结果:", encoded)
    #     decoded = base64.b64decode(encoded).decode('utf-8')
    #     # print("Base64 解码结果:", decoded)
    #     return encoded

    # def tide_non_local_url(self):
    #     str = "https://publictide.nmdis.org.cn/Tide/GetTideData"
    #     return self.to_base64(str)
    #
    # def tide_local_url(self):
    #     str = "https://open.feddon.com/api/edq_dev/"
    #     return self.to_base64(str)
    #
    # def tide_local_key(self):
    #     str = "yH5l9Mx9V4NZgJWV5NDI4rfWbmCUPsnh"
    #     return self.to_base64(str)

if __name__ == '__main__':
    conf = Confusion()
    # print(conf.tide_non_local_url())
    # print(conf.tide_local_url())
    # print(conf.tide_local_key())

    print(conf.multi_obscure("https://open.feddon.com/api/edq/"))
    print(conf.multi_obscure("yH5l9Mx9V4NZgJWV5NDI4rfWbmCUPsnh"))
    print(conf.multi_obscure("https://publictide.nmdis.org.cn/Tide/GetTideData"))
    # print(conf.multi_obscure("http://localhost:8080/"))
    #
    # print(conf.multi_obscure_decode(conf.multi_obscure("http://localhost:8080/")))