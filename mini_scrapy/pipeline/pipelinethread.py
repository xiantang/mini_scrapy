"""
# @File  : pipelinethread.py
# @Author: xiantang
# @Date  : 03/08/18
# @Email :zhujingdi1998@gmail.com
# blog : zhanshengpipidi.cn/blog
# Github : github.com/xiantang
"""
from queue import Queue
from threading import Thread, Event


class ActorExit(Exception):
    pass


class PipelineThread:
    """
    爬虫的item收集线程
    1. 收集item
    2. 批量吐出item
    """

    def __init__(self, queue):
        self._itembox = queue

    def recv(self):
        item = self._itembox.get()
        return item

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass

    def start(self):
        t = Thread(target=self._bootstrap)
        t.run()

    def run(self):
        while True:
            item = self.recv()
            print("GET:", item)
if __name__ == '__main__':

    queue = Queue()

    thread = PipelineThread(queue)

    thread.start()
