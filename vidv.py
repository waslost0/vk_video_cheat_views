import random
import argparse
import re
import time
import asyncio
import aiohttp
from fake_useragent import UserAgent
from random import choice
from aiohttp_proxy import ProxyConnector, ProxyType

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


UA = UserAgent()
with open('http.txt', 'r') as f:
    PROXY = f.read().splitlines()


CONFIG = {
    'oid': 0,
    'vid': 0,
    'threads': 50,
    'proxy_type': ProxyType.HTTP,
}


class VideoPayload:
    """
        Parse json file and get info from video
    """
    def __init__(self, payload_object):
        self.payload = payload_object['payload'][1]
        self.video_data = self.payload[4]
        self.video_info = self.video_data['mvData']
        self.player_params = self.video_data['player']['params'][0]


class CheatVideoViews:
    """
    CheatVideoViews class with asyncs funcs
    """
    def __init__(self):
        self.requests_count = 0
        self.start_time = time.time()

    @staticmethod
    async def request_increment_view_count(connector):
        """
            Get video params
            video data and player params
        """
        try:
            ua = UA.random
            async with aiohttp.ClientSession(connector=connector,trust_env=True) as session:
                async with session.post("https://vk.com/al_video.php?act=show", data={
                        'act': "show",
                        'al': 1,
                        'module':'profile_videos',
                        'video': f'{CONFIG["oid"]}_{CONFIG["vid"]}'
                }, headers={
                    "cookie": '',
                    "user-agent": ua,
                    "sec-fetch-mode": "cors",
                    "referer": "https://vk.com",
                    "X-Requested-With": "XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                },
                ) as response:
                    json = await response.json()

                    vid = VideoPayload(json)

                async with session.post("https://vk.com/al_video.php?act=video_view_started", data={
                        'al': 1,
                        'hash': vid.player_params['view_hash'],
                        'oid': f'{CONFIG["oid"]}',
                        'vid': f'{CONFIG["vid"]}',
                }, headers={
                    "cookie": '',
                    "referer": "https://vk.com",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "sec-fetch-mode": "cors",
                    "user-agent": ua,
                    "X-Requested-With": "XMLHttpRequest",
                    'Accept': '*/*',
                    'origin': 'https://vk.com',

                }
                ) as response:
                    await response.text()

                return vid
        except Exception as error:
            # print(error)
            return None

    async def start(self):
        """
            Start and print info status
        """
        while True:
            proxy = PROXY.pop()
            connector = ProxyConnector(
                proxy_type=CONFIG["proxy_type"],
                host=proxy.split(':')[0],
                port=int(proxy.split(':')[1]),
                rdns=True,
                ssl=False
            )

            video_payload = await self.request_increment_view_count(connector)

            if video_payload:
                print(
                    f"Views counts: {video_payload.video_info['info'][10]}. Time from start: "
                    f"{int(time.time() - self.start_time)}")
                await asyncio.sleep(random.randrange(1))
            PROXY.append(proxy) 


async def asynchronous():
    """
        Init async start
    """
    script = CheatVideoViews()
    tasks = [asyncio.ensure_future(script.start()) for i in range(0, CONFIG['threads'])]
    await asyncio.wait(tasks)


def main():
    """
        Init loop
    """
    ioloop = asyncio.get_event_loop()
    print('Asynchronous:')
    ioloop.run_until_complete(asynchronous())
    ioloop.close()


def get_uid_vid(url):
    try:
        match = re.findall('video-?(\\d+)_(\\d+)', str(url))[0]
        if '-' in url:
            CONFIG['oid'] = '-'+str(match[0])
        else:
            CONFIG['oid'] = str(match[0])
        CONFIG['vid'] = match[1]
        print(CONFIG)
    except IndexError as e:
        print('Invalid input')
        raise e


def set_threads(threads):
    """
        Threads count
    """
    CONFIG['threads'] = threads


def set_proxy_type(proxy_type):
    if 'socks4' in proxy_type.lower():
        CONFIG['proxy_type'] = ProxyType.SOCKS4
    elif 'http' in proxy_type.lower():
        CONFIG['proxy_type'] = ProxyType.HTTP
    elif 'https' in proxy_type.lower():
        CONFIG['proxy_type'] = ProxyType.HTTPS
    elif 'socks5' in proxy_type.lower():
        CONFIG['proxy_type'] = ProxyType.SOCKS5


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(description='VidViews')
    PARSER.add_argument('-t', '--threads', type=int, help='Threads count\n -t 50')
    PARSER.add_argument('-u', '--url', type=str, help='Url\n -u https://videos242888501?z=video242888501_456239030')
    PARSER.add_argument('-p', '--proxy_type', type=str, help='proxy type\n -p https')

    ARGS = PARSER.parse_args()

    try:
        if ARGS.threads:
            set_threads(ARGS.threads)
            set_proxy_type(ARGS.proxy_type)
        get_uid_vid(ARGS.url)
        main()
    except Exception as error:
        print('URL is required.\n')
        print(error)
    print('\nInput example: vidv.exe -u https://videos242888501?z=video242888501_456239030 -t 100\nOr: vidvk.exe -u '
          'video242888501_456239030 -t 50 -p http')
