import platform
import shutil
import logging
import os

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
                        host_names = tmp[1:]
                        host_names[len(host_names) - 1] = host_names[len(host_names) - 1].replace('\n', '')

                        if ip in ih:
                            ih[ip] = set(list(ih[ip]) + [host_name for host_name in host_names if len(host_name) != 0])
                        else:
                            ih[ip] = set([host_name for host_name in host_names if len(host_name) != 0])


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