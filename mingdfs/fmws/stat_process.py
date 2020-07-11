import json
import logging
import pprint
import time
import traceback
from threading import Thread, Lock

import requests
from redis import StrictRedis

from mingdfs.fmws import settings

LOCK = Lock()

REDIS_CLI = StrictRedis(host=settings.REDIS_CONFIG['host'],
                        port=settings.REDIS_CONFIG['port'],
                        db=settings.REDIS_CONFIG['db'],
                        password=settings.REDIS_CONFIG['passwd'],
                        socket_timeout=60,
                        socket_connect_timeout=60,
                        socket_keepalive=True)


def _fetch_request(host_name, port, stats: list):
    try:
        stat_api = settings.FRWS_API_TEMPLATE['stat']
        logging.debug('access_api: %s', stat_api)
        method = stat_api['method']
        url = stat_api['url'] % (host_name, port)

        form_data = {}
        r = requests.request(method, url, data=form_data,
                             headers={'Connection': 'close'},
                             timeout=(5, 5), verify=False)
        r.raise_for_status()
        j = r.json()
        if j['status'] != 1:
            return

        data = j['data'][0]

        with LOCK:
            stats[host_name] = {'port': port, 'data': data}
    except:
        logging.error(traceback.format_exc())


def _sort_stat(stats: list):
    sorted_list = []
    tmp_dict = dict()
    for host_name, d in stats.items():
        disk_free = d['data']['disk_free']
        all_disk_free = 0
        for v in disk_free.values():
            all_disk_free += v
        sorted_list.append(all_disk_free)
        tmp_dict[all_disk_free] = {
            host_name: d
        }

    if len(sorted_list) != 0:
        max_disk_free = max(sorted_list)
        return {
            "best_frws": tmp_dict[max_disk_free],
            "all_frws": stats
        }
    else:
        return {}


def _update_cache(stat_infor):
    logging.debug('stat_infor: \n%s', pprint.pformat(stat_infor))
    REDIS_CLI.set(settings.CACHE_FRWS_STAT_INFOR_KEY, json.dumps(stat_infor))


def start_stat(stat_interval):
    try:
        REDIS_CLI.set(settings.CACHE_STAT_INTERVAL_KEY, stat_interval)

        while 1:
            ts = []
            stats = dict()
            frws_computers = dict()
            try:
                frws_computers = REDIS_CLI.hgetall(settings.CACHE_FRWS_COMPUTERS_KEY)
            except:
                logging.error(traceback.format_exc())

            for host_name, port in frws_computers.items():
                t = Thread(target=_fetch_request, args=(host_name.decode(), int(port.decode()), stats))
                ts.append(t)
                t.start()

            for t in ts: t.join()
            try:
                stat_infor = _sort_stat(stats)
                _update_cache(stat_infor)

                stat_interval = int(REDIS_CLI.get(settings.CACHE_STAT_INTERVAL_KEY).decode())
                logging.debug('stat_interval: \n%d', stat_interval)
                time.sleep(stat_interval)
            except:
                logging.error(traceback.format_exc())
                time.sleep(60)
    except:
        pass
    finally:
        REDIS_CLI.delete(settings.CACHE_FRWS_COMPUTERS_KEY)
        REDIS_CLI.delete(settings.CACHE_STAT_INTERVAL_KEY)
        REDIS_CLI.delete(settings.CACHE_FRWS_STAT_INFOR_KEY)
        REDIS_CLI.close()