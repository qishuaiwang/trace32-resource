'''
@author: ken.kuang
'''
import sys
import os

try:
    import fcntl
except ImportError:
    fcntl = None

OS_WIN = False
if 'win32' in sys.platform.lower():
    OS_WIN = True


class SingleInstance:
    def __init__(self, lock):
        self.fh = None
        self.is_running = False
        self.LOCK_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), lock)
        self.do_magic()

    def do_magic(self):
        if OS_WIN:
            #print(self.LOCK_PATH)
            try:
                if os.path.exists(self.LOCK_PATH):
                    os.unlink(self.LOCK_PATH)
                self.fh = os.open(self.LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except EnvironmentError as err:
                if err.errno == 13:
                    self.is_running = True
                else:
                    raise
        else:
            try:
                self.fh = open(self.LOCK_PATH, 'w')
                fcntl.lockf(self.fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except EnvironmentError as err:
                if self.fh is not None:
                    self.is_running = True
                else:
                    raise

    def clean_up(self):
        # this is not really needed
        try:
            if self.fh is not None:
                if OS_WIN:
                    os.close(self.fh)
                    os.unlink(self.LOCK_PATH)
                else:
                    fcntl.lockf(self.fh, fcntl.LOCK_UN)
                    self.fh.close() # ???
                    os.unlink(self.LOCK_PATH)
        except Exception as err:
            # logger.exception(err)
            raise # for debugging porpuses, do not raise it on production


if __name__ == "__main__":
    import time

    si = SingleInstance("lock.20000")
    try:
        if si.is_running:
            sys.exit("This app is already running!")
        time.sleep(5) # remove
        # do other stuff
    finally:
        si.clean_up()