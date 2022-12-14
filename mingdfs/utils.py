import logging
import platform
import shutil
from binascii import b2a_hex, a2b_hex
import cv2
from io import BytesIO
import traceback
from PIL import Image
from Crypto.Cipher import AES

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
    plt = platform.platform()
    hosts = None

    if 'Linux' in plt:
        hosts = '/etc/hosts'
    elif 'Windows' in plt:
        hosts = 'C:\Windows\System32\drivers\etc\hosts'

    if hosts is None:
        raise
    with open(hosts, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            logging.debug(line)
            if len(line) != 0:
                tmp = line.split(' ')
                ip = tmp[0]
                if not ip.startswith('#'):
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
        ih[ip] = set()
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

    plt = platform.platform()
    hosts = None

    if 'Linux' in plt:
        hosts = '/etc/hosts'
    elif 'Windows' in plt:
        hosts = 'C:\Windows\System32\drivers\etc\hosts'

    if hosts is None:
        raise

    if content != '':
        bak = hosts + '.bak'
        shutil.copyfile(hosts, bak)

        with open(hosts, 'w') as f:
            f.write(content)


my_crypt_number_dict = {
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h",
    "9": "i",
    "0": "j",
    ".": "k",

    "k": ".",
    "j": "0",
    "i": "9",
    "h": "8",
    "g": "7",
    "f": "6",
    "e": "5",
    "d": "4",
    "c": "3",
    "b": "2",
    "a": "1"
}


def crypt_number(num):
    b = str(num)
    c = list(b)
    for i in range(len(c)):
        c[i] = my_crypt_number_dict[c[i]]

    return ''.join(c)

def decrypt_number(msg):
    b = list(msg)
    for i in range(len(b)):
        if b[i] == "":
            continue
        b[i] = my_crypt_number_dict[b[i]]
    return float(''.join(b))

# ??????text??????16?????????????????????????????????16???
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# ????????????
def encrypt(key, text):
    logging.debug("key: %s", key)
    if isinstance(key, str):
        key = key.encode('utf-8')
    elif isinstance(key, bytes):
        pass
    else:
        raise
    mode = AES.MODE_CBC
    iv = b'qqqqqqqqqqqqqqqq'
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # ??????AES?????????????????????????????????ascii??????????????????????????????????????????????????????????????????16???????????????
    return b2a_hex(cipher_text)


# ????????????????????????????????????strip() ??????
def decrypt(key, text):
    logging.debug("key: %s", key)
    if isinstance(key, str):
        key = key.encode('utf-8')
    elif isinstance(key, bytes):
        pass
    else:
        raise
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


def get_video_num_image(file_name, num=1):
    """??????????????????n?????????

    :param file_name: ???????????????
    :type file_name: str
    :param num: ??????????????????????????????
    :type num: int

    """
    try:
        vidcap = cv2.VideoCapture(file_name)
        success, img_cv2 = vidcap.read()
        n = 1
        while n < num:
            success, img_cv2 = vidcap.read()
            n += 1

        img = Image.fromarray(img_cv2)
        # img.save('/root/test.png')

        bts = BytesIO()
        img.save(bts, format='png')

        return BytesIO(bts.getvalue())
    except:
        logging.error(traceback.format_exc())
        return None
    finally:
        if vidcap: vidcap.release()
        if bts: bts.close()


if __name__ == '__main__':
    key = '1234567890123456'
    msg = encrypt(key, 'hello')
    print('msg:', msg)
    my = decrypt(key, msg)
    print('my:', my)
    #
    # en = crypt_number(123.4)
    # print(en)
    # print(decrypt_number(en))
