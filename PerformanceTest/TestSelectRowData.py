import os
import requests
import datetime
import time
import threading
#Add the root directory to sys.path to solve the problem of not finding packages on the command line
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import psutil as ps
from UnitTestCase.Tools import Tools


class TestSelectRowData:
    times = []
    error = []
    url = 'http://127.0.0.1:8050/'
    upload_file = '_dash-update-component'
    upload_url = url + upload_file
    def get_post_data(self, path):
        json_data = Tools.read_file(path)
        return json_data
    def get_select_response(self, path):
        post_data = self.get_post_data(path)
        response = Tools.post_method2(TestSelectRowData.upload_url, post_data)
        return response
    def select(self):
        path = os.getcwd() + '/../UnitTestCase/distinct_labels_asc.json'
        respone = self.get_select_response(path)
        respone_time = float(respone.elapsed.microseconds)/1000
        self.times.append(respone_time)
        if respone.status_code!= 200:
            TestSelectRowData.error.append("0")
    def get_cpu_load_avg(self):
        # Get the average system load
        load_avg = ps.getloadavg()
        print('load_avg=', load_avg)
        return load_avg
    def get_cpu_percent(self):
        # Get CPU usage
        cpu_percent = ps.cpu_percent()
        print('cpu_percent=', cpu_percent)
        return cpu_percent
    def get_cpu_stats(self):
        # Get CPU statistics
        cpu_stats = ps.cpu_stats()
        print('cpu_stats=', cpu_stats)
        return cpu_stats
    def get_cpu_freq(self):
        # Get CPU frequency
        cpu_freq = ps.cpu_freq()
        print('cpu_freq=', cpu_freq)
        return cpu_freq
    def get_cpu_times_percent(self):
        # Acquisition time ratio
        cpu_times_percent = ps.cpu_times_percent()
        print('cpu_times_percent=', cpu_times_percent)
        return cpu_times_percent
    def get_virtual_memory(self):
        # Memory usage
        virtual_memory = ps.virtual_memory()
        print('virtual_memory=', virtual_memory)
        return virtual_memory
    def get_disk_usage(self):
        # Gets disk partition information
        disk_usage = ps.disk_usage('/')
        print('disk_usage=', disk_usage)
        return disk_usage
    def get_disk_io_counters(self):
        # Get IO statistics
        disk_io_counters = ps.disk_io_counters()
        print('disk_io_counters=', disk_io_counters)
        return disk_io_counters
    def get_net_io_counter(self):
        # Obtain network card IO statistics
        net_io_counters = ps.net_io_counters()
        print('net_io_counters=', net_io_counters)
        return net_io_counters
    def get_server_info(self):
        self.get_cpu_freq()
        self.get_cpu_load_avg()
        self.get_cpu_percent()
        self.get_cpu_stats()
        self.get_cpu_times_percent()
        self.get_virtual_memory()
        self.get_disk_usage()
        self.get_disk_io_counters()
        self.get_net_io_counter()
        time.sleep(3)
    def thread_task(self):
        threads = []
        start_time = datetime.datetime.now()
        print ("request start_time %s " % start_time)
        print('Monitor metrics before performing performance tests')
        self.get_server_info()
        print('Start performing performance tests')
        nub = 100
        think_time = 0.1
        for i in range(1, nub+1):
            t = threading.Thread(target=self.select(), args='')
            threads.append(t)
        for t in threads:
            time.sleep(think_time)
            t.setDaemon(True)
            t.start()
        t.join()
        end_time = datetime.datetime.now()
        print("request end_time   %s " % end_time)
        time.sleep(0.1)
        average_time = "{:.3f}".format(float(sum(self.times))/float(len(self.times)))
        print ("Average Response Time %s ms" % average_time)
        use_time = str(end_time - start_time)
        hour = use_time.split(":").pop(0)
        minute = use_time.split(":").pop(1)
        second = use_time.split(":").pop(2)
        totaltime = float(hour) * 60 * 60 + float(minute) * 60 + float(second)
        print ("Concurrent processing %s" % nub)
        print ("use total time %s s" % (totaltime - float(nub * think_time )))
        print ("fail request %s" % self.error.count("0"))
        self.get_server_info()
        print('The performance test execution ends')
if __name__ == '__main__':
    row = TestSelectRowData()
    row.thread_task()
    