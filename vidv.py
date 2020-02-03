import aiohttp
import asyncio
import random
import sys
import argparse
import re
import time

CONFIG = {
    'oid': 0,
    'vid': 0,
    'threads': 50
}


class VideoPayload:
    def __init__(self, payload_object):
        self.payload = payload_object['payload'][1]
        self.videoData = self.payload[4]
        self.videoInfo = self.videoData['mvData']
        self.playerParams = self.videoData['player']['params'][0]


class CheatVideoViews:
    def __init__(self):
        self.requestCount = 0
        self.startTime = time.time()

    @staticmethod
    async def video_params():
        try:
            async with aiohttp.ClientSession() as session:

                async with session.post("https://vk.com/al_video.php", data={
                    'al': 1,
                    'act': "show",
                    'video': f'{CONFIG["oid"]}_{CONFIG["vid"]}'
                }, headers={
                    "cookie": '',
                    "user-agent": f'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/{(random.random() * 600)}.36 (KHTML, like Gecko) Chrome/{(random.random() * 59)}.0.3029.110 Safari/${(random.random() * 1000)}.36',
                    "sec-fetch-mode": "cors",
                    "referer": "https://vk.com",
                    "X-Requested-With": "XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }) as response:
                    json = await response.json()

                    vid = VideoPayload(json)
            return vid
        except Exception as e:
            print(e)

    @staticmethod
    async def request_increment_view_count(hash):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://vk.com/al_video.php", data={
                    'act': "video_view_started",
                    'al': 1,
                    'oid': str(CONFIG['oid']),
                    'vid': str(CONFIG['vid']),
                    'hash': hash
                }, headers={
                    "cookie": '',
                    "user-agent": f'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/{(random.random() * 600)}.36 (KHTML, like Gecko) Chrome/{(random.random() * 59)}.0.3029.110 Safari/${(random.random() * 1000)}.36',
                    "sec-fetch-mode": "cors",
                    "referer": "https://vk.com",
                    "X-Requested-With": "XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }) as response:
                    return response
        except Exception as e:
            print(e)

    async def start(self, i=None):
        while True:
            video_payload = await self.video_params()
            await self.request_increment_view_count(hash=video_payload.playerParams['view_hash'])
            print(
                f"Views counts: {video_payload.videoInfo['info'][10]}. Time from start: {int(time.time() - self.startTime)}  Requests counts: {self.requestCount}")
            self.requestCount = self.requestCount + 1
            await asyncio.sleep(random.randrange(0, 1))


async def asynchronous():
    script = CheatVideoViews()
    tasks = [asyncio.ensure_future(script.start(i)) for i in range(0, int(CONFIG['threads']))]
    await asyncio.wait(tasks)


def main():
    ioloop = asyncio.get_event_loop()
    print('Asynchronous:')
    ioloop.run_until_complete(asynchronous())
    ioloop.close()


def get_uid_vid(url):
    try:
        match = re.findall('video-?(\\d+)_(\\d+)', str(url))[0]
        CONFIG['oid'] = match[0]
        CONFIG['vid'] = match[1]
    except IndexError as e:
        print('Invalid input')
        raise e


def get_threads(threads):
    CONFIG['threads'] = threads


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='VidViews')
    parser.add_argument('-t', '--threads', type=int, help='Threads count\n -t 50')
    parser.add_argument('-u', '--url', type=str, help='Url\n -u https://videos242888501?z=video242888501_456239030')

    args = parser.parse_args()


    try:
        if args.threads:
            get_threads(args.threads)
        get_uid_vid(args.url)
        main()
    except Exception as e:
        print('URL is required.\n')
        print(e)
    print('\nInput example: vidv.exe -u https://videos242888501?z=video242888501_456239030 -t 100\nOr: vidvk.exe -u video242888501_456239030 -t 50')

   
