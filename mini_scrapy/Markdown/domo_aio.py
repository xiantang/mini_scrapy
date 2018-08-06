"""
# @File  : domo_aio.py
# @Author: xiantang
# @Date  : 06/08/18
# @Email :zhujingdi1998@gmail.com
# blog : zhanshengpipidi.cn/blog
# Github : github.com/xiantang
"""
import time
import logging
import os
import asyncio
import aiohttp
from  threading import Thread

class Downloader:
    def __init__(self, queue,  exclude=None, headers=None,
                 concurrency=2, streaming=False, sub_dirs=True, verbose=True):



        self.exclude = exclude if exclude is not None else ''

        self.client = aiohttp.ClientSession(headers=headers)
        self.queue = queue
        self.concurrency = concurrency
        self._is_streaming = streaming
        self.sub_dirs = sub_dirs

        logging.basicConfig(level='INFO')
        self.log = logging.getLogger()
        if not verbose:
            self.log.disabled = True

    async def download(self, url):
        async with self.client.get(url) as response:
            if response.status != 200:
                self.log.error('BAD RESPONSE: {}'.format(response.status))
                return
            content = await response.read()
            return content


    async def worker(self):
        logging.info('Starting worker')
        while self.queue.qsize() >0 :

            link = await self.queue.get()
            logging.info('PROCESSING {}'.format(link))

            content=await self.download(link)
            print(len(content))
            self.queue.task_done()

    def run(self,loop):
        print('Starting downloading')
        tasks = [asyncio.ensure_future(self.worker())
                 for _ in range(3)]
        loop.run_until_complete(asyncio.wait(tasks))
        self.client.close()
def target(queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    Downloader(queue).run(loop)
    loop.close()
    print("111111")



async  def enqueue(queue):
    array = []
    for i in range(1000):
        array.append("https://pic.xiaojianjian.net/")
    await asyncio.wait([queue.put(link) for link in array])
loop = asyncio.get_event_loop()
queue = asyncio.Queue()
loop.run_until_complete(enqueue(queue))



array = []
for i in range(40):
    array.append(Thread(target=target,args=(queue,)))

for i in array:
    i.start()

loop.close()
