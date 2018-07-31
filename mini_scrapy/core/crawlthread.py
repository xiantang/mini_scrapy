import sys
import threading
import traceback
from threading import Thread



class CrawlThread(Thread):
    def __init__(self,thread_id,callback,*args):
        threading.Thread.__init__(self,*args)
        self.thread_id = thread_id
        self.callback = callback
    def run(self) -> None:
        try:
            self.callback()
        except Exception as e:
            self.exitcode = 1  # 如果线程异常退出，将该标志位设置为1，正常退出为0
            self.exception = e
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))  # 在改成员变量中记录异常信息
