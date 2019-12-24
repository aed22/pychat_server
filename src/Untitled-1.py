import re
import os
import queue
import requests
from requests.auth import HTTPProxyAuth
import time
import threading
from PyQt4.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt4 import QtCore , QtGui
import CusLog
from pypac import PACSession

log = CusLog.CusLog(CusLog.LOG_INFO,"logs.txt")


class DClass(QThread):
    complete_signal = pyqtSignal('PyQt_PyObject')
    failed_signal = pyqtSignal('PyQt_PyObject')
    progress_signal = pyqtSignal('PyQt_PyObject')
    speed_signal = pyqtSignal('PyQt_PyObject')
    label_signal = pyqtSignal('PyQt_PyObject')
    eta_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self,
                 url,
                 dest,
                 chunk_size,
                 d_id,
                 complete_callback,
                 failed_callback,
                 progress_callback,
                 speed_callback,
                 label_callback,
                 time_callback,
                 proxy = None,
                 batch = False):

        super(DClass, self).__init__()

        self.url = url
        self.dest = dest
        self.chunk_size = chunk_size
        self.id = d_id
        self.complete_signal.connect(complete_callback)
        self.failed_signal.connect(failed_callback)
        self.progress_signal.connect(progress_callback)
        self.speed_signal.connect(speed_callback)
        self.label_signal.connect(label_callback)
        self.eta_signal.connect(time_callback)
        self.batch = batch
        self.proxy = proxy
        self.cancelled = False
        self.paused = False
        self.total_bytes = 0
        self.written_bytes = 0
        self._lock = threading.Lock()

    def run(self):

        # self.label_signal.emit(dict(id=self.id, txt='sdfgsdthwteh'))

        if self.batch and False:
            with open(self.url, 'r') as file:
                urls = file.readlines()
                count = len(urls)
                log("count:{}".format(count))
                for url in urls:
                    if self.cancelled:
                        break
                    if is_valid_url(url):
                        url = url.strip('\n')
                        count -= 1
                        dest = os.path.join(self.dest, url.split('/')[-1])
                        dest = det_filename(dest)
                        log(dest)
                        self.label_signal.emit(dict(id=self.id, txt="{}/{} {}".format(len(urls) - count, len(urls), dest)))
                        self.handler = DHandler(url, dest, self.chunk_size,
                                           self.complete,
                                           self.failed,
                                           self.progress,
                                           self.speed,
                                           self.proxy)

                        self.handler.start()

                    # time.sleep(2)
                    while self.handler.is_running():
                        time.sleep(.5)
                self.batch = False
                self.complete()

        else:
            with self._lock:
                self.handler = DHandler( self.url, self.dest,self.chunk_size,
                                    self.complete,
                                    self.failed,
                                    self.progress,
                                    self.speed,
                                    self.proxy)
                self.handler.start()

    def toggle_pause(self):
        self.handler.toggle_pause()
        self.paused = self.handler.is_paused()

    def cancel(self):
        self.cancelled = True
        self.handler.cancel()

    def stop(self):
        pass

    def complete(self):
        if not self.batch:
            self.progress((self.written_bytes,self.total_bytes))
            log((self.written_bytes,self.total_bytes))
            self.speed()
            self.complete_signal.emit({'id':self.id})

    def failed(self, val = 0):
        log("download Failed")
        if val == 1:
            self.failed_signal.emit({'id':self.id,'error':'proxy'})

    def progress(self, tup):
        self.total_bytes = tup[1]
        self.written_bytes = tup[0]
        self.progress_signal.emit(int( (float(tup[0])/tup[1])*100 ))

    def speed(self, dbyte = 0, dtime = 0):

        if dbyte and dtime :
            spd = float(dbyte) / dtime
            if spd > 1024 * 512:
                speed = "{:.2f} MB/s".format(float(spd) / (1024 * 1024))
            elif spd > 512:
                speed = "{:.2f} KB/s".format(float(spd) / 1024)
            else:
                speed = "{} B/s".format(spd)
        else:
            speed = "0 B/s"

        if self.total_bytes > 1024 * 1024:
            tb = "{:.1f}MB".format(float(self.total_bytes) / (1024 * 1024))
            rb = "{:.1f}".format(float(self.written_bytes) / (1024 * 1024))
        elif self.total_bytes > 1024:
            tb = "{:.1f}KB".format(float(self.total_bytes) / (1024))
            rb = "{:.1f}".format(float(self.written_bytes) / (1024))
        else:
            tb = "{}B".format(self.total_bytes)
            rb = "{}".format(self.written_bytes)

        signal_dic = {'id': self.id, 'progress': '{}/{}'.format(rb, tb), 'speed': '{}'.format(speed)}

        self.speed_signal.emit(signal_dic)
        if dbyte:
            self.eta_signal.emit(dict(id=self.id, eta=int((self.total_bytes - self.written_bytes) / spd)))
        else:
            self.eta_signal.emit(dict(id=self.id, eta=0))
            # self.speed_signal.emit(val)




class DHandler(object):

    def __init__(self,
                 url,
                 dest,
                 chunk_size,
                 complete_callback,
                 failed_callback,
                 progress_callback,
                 speed_callback,
                 proxy=None):
        self.url = url
        self.dest = dest
        self._chunk_size = chunk_size
        self._total_bytes = 0
        self._complete = complete_callback
        self._failed = failed_callback
        self._progress = progress_callback
        self._speed = speed_callback
        self._proxy = proxy
        self._cancelled = False
        self._paused = False
        self._lock = threading.Lock()

        self.thread = threading.Thread(target=self._download, daemon=True)


    def start(self):
        self.thread.start()

    def toggle_pause(self):
        log("toggle Pause")

        if self.is_paused():
            with self._lock:
                self._paused = False
        else:
            with self._lock:
                self._paused = True

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self):
        return self._cancelled

    def is_paused(self):
        return self._paused

    def is_running(self):
        return self.thread.is_alive()

    def wait(self):

        while self.thread.is_alive():
            try:
                # in case of exception here (like KeyboardInterrupt),
                # cancel the task.
                self.thread.join(0.02)
            except:
                self.cancel()
                raise
            # this will raise exception that may happen inside the thread.
        if raise_if_error:
            self.raise_if_error()


    def _download(self):
        log('Download Handler thread started {}'.format(self.url))



        ch = (2 ** 20) * self._chunk_size   # in MBs
        log("Chunk-Size:{} B".format(ch))
        if self._chunk_size > 20:
            stream_unit_size = (2 ** 20) * 20
        else:
            stream_unit_size = int( (2 ** 20) * self._chunk_size/2)
        n_bytes_read = 0

        # req = requests.session()
        req = PACSession()

        if self._proxy['user'] != '' and self._proxy['user'] is not None:
            log(self._proxy['user'])
            req.proxy_auth = HTTPProxyAuth(self._proxy['user'],self._proxy['pwd'])


        # if self._proxy['user'] is None:


        # req = requests.session()
        if self._proxy['addr'] is None or self._proxy['addr'] == '':
            proxies = None
        else:
            log(self._proxy['user'])
            proxies = {'http': 'http://{}:{}'.format(self._proxy['addr'],self._proxy['port']),
                       'https': 'http://{}:{}'.format(self._proxy['addr'],self._proxy['port'])}

        try:
            with req.get(self.url, stream = True, proxies= proxies) as r:
                log("Response:{}".format(r.status_code))
                if (r.status_code < 200) or (r.status_code > 300):
                    error_text = "Download Failed status code:{}".format(r.status_code)
                    log(error_text, CusLog.LOG_ERROR)
                    self._failed()
                    return 1
                total_bytes = int(r.headers['Content-Length'])
        except requests.exceptions.ProxyError:
            log('proxy error')
            self._failed(1)

            return  1
        except Exception as e:
            log("Failed to connect :{}".format(e), CusLog.LOG_ERROR)
            self._failed()
            return 1

        log("total-Size:{} B".format(total_bytes))
        overall_start = time.perf_counter()
        with open(self.dest, 'ab') as file:

            st1 = time.perf_counter()
            sb1 = n_bytes_read
            time_out_count =0
            while n_bytes_read < total_bytes:
                self._progress((n_bytes_read, total_bytes))

                while self.is_paused():
                    time.sleep(.25)
                    #speed = "0 B/s"
                    self._speed()
                    if self.is_cancelled():
                        return 1

                if self.is_cancelled():
                    return 1

                header = {"Range": "bytes={}-{}".format(n_bytes_read, n_bytes_read + ch - 1)}

                try:


                    with req.get(self.url, headers=header,stream = True, timeout=(10,10)) as r:
                        chunk = bytes()
                        for chun in r.iter_content(chunk_size=stream_unit_size):
                        # for chun in r.iter_content():
                            if self.is_cancelled():
                                return 1

                            if chun:
                                chunk += chun
                                chunklen = len(chunk)

                            self._progress((n_bytes_read+chunklen, total_bytes))

                            db = n_bytes_read+chunklen-sb1
                            dt = time.perf_counter()-st1
                            #log("{}".format(dt))
                            if dt > 1:
                                self._speed(db, dt)
                                sb1 = n_bytes_read+chunklen
                                st1 = time.perf_counter()

                            if self.is_paused():
                                break


                except Exception as e:
                    # if len(chunk) > 0:                                      # send write portion of chunk data that has been downloaded
                    #     n_bytes_read += len(chunk)
                    #     file.write(chunk)
                    #     log("writing chunk")
                    self._progress((n_bytes_read, total_bytes))

                    time_out_count += 1
                    log(e, CusLog.LOG_ERROR)
                    log("Timeout count: {}".format(time_out_count), CusLog.LOG_ERROR)
                    if time_out_count % 2 ==0:  # TODO: put this in a thread and exit o
                        log("Sleep for {} secs".format(30), CusLog.LOG_ERROR)
                        time.sleep(30)
                    continue
                else:
                    if len(chunk) > 0:                                      # send write chunk data that has been downloaded
                        n_bytes_read += len(chunk)
                        file.write(chunk)
                        self._progress((n_bytes_read, total_bytes))

        self._progress((n_bytes_read , total_bytes))
        self._speed()
        log("download complete---time taken:{}".format(time.perf_counter()-overall_start))
        self._complete()

            # TODO: COMPLETE THIS DOWNLOAD FUNCTION




def is_batch(url):
    if os.path.isfile(url):
        log(" ")
        log("Batch Download")
        return True
    else:
        log("not Batch Download")
        return False




def det_filename(filename):

    out_file_name = os.path.basename(filename)
    temp = out_file_name
    n = 0
    try:
        while out_file_name in os.listdir(os.path.dirname(filename)):
            n += 1
            spl = os.path.splitext(temp)
            # print(spl)
            out_file_name = '{}({}){}'.format(spl[0], n, spl[1])
    except:
        return 1

    return os.path.join(os.path.dirname(filename), out_file_name)


def is_valid_url(url, test = False):
    #valid_url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+"
    #                      , url)
    if not test:
        valid_url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [! *,] |(?: %[0-9a-fA-F][0-9a-fA-F]))+"
                              , url)
        if valid_url:
            return True
        else:
            return False
    else:
        try:
            with requests.get(url,timeout=1,stream=True) as r:
                if r.status_code >199 and not r.status_code >= 300:
                    flag = True
                else:
                    flag = False

            return flag
        except:
            return False