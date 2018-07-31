import threading, traceback, sys


class runScriptThread(threading.Thread):  # The timer class is derived from the class threading.Thread
    def __init__(self, funcName, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.funcName = funcName
        self.exitcode = 0
        self.exception = None
        self.exc_traceback = ''

    def run(self):  # Overwrite run() method, put what you want the thread do here

        self._run()
         # 在改成员变量中记录异常信息

    def _run(self):
        try:
            self.funcName(*(self.args))
        except Exception as e:
            raise e
if __name__ == '__main__':
    sth = 'hello world'
    try:
        printSth = "1"
        aChildThread = runScriptThread(printSth, sth)

        aChildThread.start()
        aChildThread.join()
        print(aChildThread.exc_traceback)
    except Exception as e:
        pass