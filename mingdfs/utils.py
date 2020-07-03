import platform
import shutil
import logging
import os
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

PC = 1
MOBILE = 2

def _is_mobile(user_agent: str) -> bool:
    if 'iphone' in user_agent \
        or 'android' in user_agent \
        or 'micromessenger' in user_agent:
        return True
    else:
        return False


def pc_or_mobile(user_agent: str) -> bool:
    user_agent = user_agent.lower()
    if _is_mobile(user_agent):
        return MOBILE
    else:
        return PC


def load_hosts():
    ih = {}
    if 'Linux' in platform.platform():
        hosts = '/etc/hosts'
        with open(hosts, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                logging.debug(line)
                if len(line) != 0:
                    tmp = line.split(' ')
                    ip = tmp[0]
                    if ip != '#':
                        if len(tmp) == 1:
                            continue
                        host_names = tmp[1:]
                        host_names[len(host_names) - 1] = host_names[len(host_names) - 1].replace('\n', '')

                        if ip in ih:
                            ih[ip] = set(list(ih[ip]) + [host_name for host_name in host_names if len(host_name) != 0])
                        else:
                            ih[ip] = set([host_name for host_name in host_names if len(host_name) != 0])


    return ih


def add_hosts(ih: dict, ip, host_name):
    for i in ih.keys():
        try:
            ih[i].remove(host_name)
        except:
            pass

    if ip in ih:
        ih[ip].add(host_name)
    else:
        ih[ip].add(host_name)

    return ih


def delete_hosts(ih: dict, ip, host_name):
    if ip in ih:
        try:
            ih[ip].remove(host_name)
        except:
            pass

    return ih


def dump_hosts(ih: dict):
    content = ''
    for ip, host_names in ih.items():
        line = ' '.join([ip] + list(host_names))
        content += line + '\n'

    logging.debug(content)

    if content != '' and 'Linux' in platform.platform():
        hosts = '/etc/hosts'
        bak = hosts + '.bak'
        if not os.path.exists(bak):
            os.mknod(bak)
        shutil.copyfile(hosts, bak)

        with open(hosts, 'w') as f:
            f.write(content)


my_crypt_number_dict = {
    "1": "拟把疏狂图一醉，对酒当歌，强乐还无味。",
    "2": "望极春愁，黯黯生天际。",
    "3": "东风夜放花千树，更吹落，星如雨。",
    "4": "雾失楼台，月迷津渡，桃源望断无寻处。",
    "5": "锦壶催画箭，玉佩天涯远。",
    "6": "细雨梦回鸡塞远，小楼吹彻玉笙寒。",
    "7": "送春春去几时回。",
    "8": "绿杨烟外晓寒轻，红杏枝头春意闹。",
    "9": "栏干十二独凭春，晴碧远连云。",
    "0": "几日行云何处去？忘却归来，不道春将莫。",
    ".": "迟钝的我。",

    "迟钝的我。": ".",
    "几日行云何处去？忘却归来，不道春将莫。": "0",
    "栏干十二独凭春，晴碧远连云。": "9",
    "绿杨烟外晓寒轻，红杏枝头春意闹。": "8",
    "送春春去几时回。": "7",
    "细雨梦回鸡塞远，小楼吹彻玉笙寒。": "6",
    "锦壶催画箭，玉佩天涯远。": "5",
    "雾失楼台，月迷津渡，桃源望断无寻处。": "4",
    "东风夜放花千树，更吹落，星如雨。": "3",
    "望极春愁，黯黯生天际。": "2",
    "拟把疏狂图一醉，对酒当歌，强乐还无味。": "1"
}


def crypt_number(num):
    b = str(num)
    c = list(b)
    for i in range(len(c)):
        c[i] = my_crypt_number_dict[c[i]]

    return ''.join(c)

def decrypt_number(msg):
    b = msg.split('。')
    for i in range(len(b) - 1):
        if b[i] == "":
            continue
        b[i] = my_crypt_number_dict[b[i] + "。"]
    return float(''.join(b))

# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(key, text):
    logging.debug("key: %s", key)
    key = key.encode('utf-8')
    mode = AES.MODE_CBC
    iv = b'qqqqqqqqqqqqqqqq'
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(key, text):
    logging.debug("key: %s", key)
    key = key.encode('utf-8')
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    key = '1234567890123456'
    msg = encrypt(key, 'hello')
    print('msg:', msg)
    my = decrypt(key, msg)
    print('my:', msg)

    en = crypt_number(123.4)
    print(en)
    print(decrypt_number(en))