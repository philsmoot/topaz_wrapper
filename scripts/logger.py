# logger.py
# 
from datetime import datetime

#
# initialize()
#
# open eventlog for writing in append mode.  The file is created if it doesn't exist.
# event log format - [date time of event][calling module] msg
# 
# open perflog for writing in append mode.  
# output format - datetime,module,metric,measure,unit  (comma deliminated for easy parsing)
#
# input: 
# eventlog - the path to the eventlog file
# perflog - the path to the perflog file
# logging level - 0 == write to file;  1 == write to file and console
# 
# return:
# none
#

class Logger:

    def __init__(self, eventlog, perflog, level): 

        self.level = level
        self.datetime_format = "%m/%d/%Y, %H:%M:%S"

        # initialize eventlog
        try:
            self.eventlog = open(eventlog, "a")
        except:
            if self.level:
                print("file open failed for eventlog = " + eventlog)
        else:
            now = datetime.now()
            date_time = now.strftime(self.datetime_format)
            message = "[" + date_time + "] Intialized eventlog"
            try: 
                self.eventlog.write(message + "\n")
            except:
                if self.level:
                    print("file write failed to eventlog")
            else:
                if self.level:
                    print(message)

        # initialize perflog
        try:
            self.perflog = open(perflog, "a")
        except:
            if self.level:
                print("file open failed for perflog = " + perflog)
        else:
            now = datetime.now()
            date_time = now.strftime(self.datetime_format)
            message = "[" + date_time + "] Intialized perflog"
            try: 
                self.eventlog.write(message + "\n")
            except:
                if self.level:
                    print("file write into perflog failed")
            else:
                if self.level:
                    print(message)           

    #                  
    # loginfo()
    # append info to eventlog
    # format - [date time of message][module] msg
    #           
    def loginfo(self, module, msg):
        now = datetime.now()
        date_time = now.strftime(self.datetime_format)
        message = "[" + date_time + "] [" + module + "] " + msg
        self.eventlog.write(message + "\n")
        if self.level:
            print(message)

    #                  
    # logperf()
    # append info to perflog
    # format - datetime,calling_module,metric,measure,unit 
    #           
    def logperf(self, project, module, metric, measure, unit):
        now = datetime.now()
        date_time = now.strftime(self.datetime_format)
        message = date_time + "," + project + "," + module + "," + metric + "," + measure + "," + unit
        self.perflog.write(message + "\n")
        if self.level:
            print(message)

    #
    # close() - closes the eventlog and perflog
    #
    def close(self) -> None:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        message = "[" + date_time + "] [" +  "Logger.close" + "] " + "log files closed"
        self.eventlog.write(message + "\n")
        self.eventlog.close()
        self.perflog.close()
        if self.level:
            print(message)

# test code for above functions - 
# logger = Logger("", "testperflog", 1)
# logger = Logger("testeventlog", "", 1)
# logger = Logger("testevent.log", "testperf.log", 1)
# logger.loginfo("hpcutil.loginfo", "test msg")
# logger.logperf("test", "hpcutil.logperf", "particle_picking_per_tomo", "6000", "seconds" )
# logger.close()