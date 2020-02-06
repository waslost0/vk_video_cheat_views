import random
import argparse
import re
import time
import asyncio
import aiohttp


CONFIG = {
    'oid': 0,
    'vid': 0,
    'threads': 50
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
    async def video_params():
        """
            Get video params
            video data and player params
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://vk.com/al_video.php", data={
                        'al': 1,
                        'act': "show",
                        'video': f'{CONFIG["oid"]}_{CONFIG["vid"]}'
                }, headers={
                    "cookie": '',
                    "user-agent": f'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/'
                                  f'{(random.random() * 600)}.36 (KHTML, like Gecko) Chrome/'
                                  f'{(random.random() * 59)}.0.3029.110 Safari/$'
                                  f'{(random.random() * 1000)}.36',
                    "sec-fetch-mode": "cors",
                    "referer": "https://vk.com",
                    "X-Requested-With": "XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }) as response:
                    json = await response.json()

                    vid = VideoPayload(json)
            return vid
        except (RuntimeError, ConnectionError) as error:
            print(error)

    @staticmethod
    async def request_increment_view_count(hash_date):
        """
            POST increase video view count
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://vk.com/al_video.php", data={
                        'act': "video_view_started",
                        'al': 1,
                        'oid': str(CONFIG['oid']),
                        'vid': str(CONFIG['vid']),
                        'hash': hash_date
                }, headers={
                    "cookie": '',
                    "user-agent": f'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/'
                                  f'{(random.random() * 600)}.36 (KHTML, like Gecko) Chrome/'
                                  f'{(random.random() * 59)}.0.3029.110 Safari/$'
                                  f'{(random.random() * 1000)}.36',
                    "sec-fetch-mode": "cors",
                    "referer": "https://vk.com",
                    "X-Requested-With": "XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }) as response:
                    return response
        except (RuntimeError, ConnectionError) as error:
            print(error)

    async def start(self):
        """
            Start and print info status
        """
        while True:
            video_payload = await self.video_params()
            await self.request_increment_view_count(hash_date=video_payload.player_params['view_hash'])
            print(
                f"Views counts: {video_payload.video_info['info'][10]}. Time from start: "
                f"{int(time.time() - self.start_time)}  Requests counts: "
                f"{self.requests_count}")
            self.requests_count = self.requests_count + 1
            await asyncio.sleep(random.randrange(0, 1))


async def asynchronous():
    """
        Init async
    """
    script = CheatVideoViews()
    tasks = [asyncio.ensure_future(script.start()) for i in range(0, int(CONFIG['threads']))]
    await asyncio.wait(tasks)


def main():
    """
        Just main/ Init loop
    """
    ioloop = asyncio.get_event_loop()
    print('Asynchronous:')
    ioloop.run_until_complete(asynchronous())
    ioloop.close()


def get_uid_vid(url):
    """
        Get uid and vid data
    """
    try:
        match = re.findall('video-?(\\d+)_(\\d+)', str(url))[0]
        CONFIG['oid'] = match[0]
        CONFIG['vid'] = match[1]
    except IndexError as error:
        print('Invalid input')
        raise error


def get_threads(threads):
    """
        Threads count
    """
    CONFIG['threads'] = threads


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(description='VidViews')
    PARSER.add_argument('-t', '--threads', type=int, help='Threads count\n -t 50')
    PARSER.add_argument('-u', '--url', type=str, help='Url\n -u https://videos242888501?z=video242888501_456239030')

    ARGS = PARSER.parse_args()

    try:
        if ARGS.threads:
            get_threads(ARGS.threads)
        get_uid_vid(ARGS.url)
        main()
    except Exception as error:
        print('URL is required.\n')
        print(error)
    print('\nInput example: vidv.exe -u https://videos242888501?z=video242888501_456239030 -t 100\nOr: vidvk.exe -u '
          'video242888501_456239030 -t 50')
