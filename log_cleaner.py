#coding: UTF-8

#############################
#          Imports          #
#############################
import os
import re
import logging

# logging setting.
# output debug messages to stdout.
logging.basicConfig(level=logging.DEBUG)


##############################
#           Class            #
##############################
class LogCleaner(object):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def clean(self, regex, get_date, sort_by = None, days = 40, logs_max = 50):
        # params type check
        if not type(regex) is type(re.compile("")):
            logging.debug("Argument is bas. Please input re.complie pattern.")
            return None

        # if not exist or not access directory
        if not (os.path.exists(self.dir_path) and os.access(self.dir_path, os.R_OK) and os.access(self.dir_path, os.W_OK)):
            logging.debug("Directory is Permission denied.")
            return None

        # make logs hash
        # key: logs date, value: log files name (list)
        logs_set = {}
        needless_logs = []

        for file in os.listdir(self.dir_path):
            if regex.search(file) is not None:
                # has_key
                _date = get_date(file)
                if _date is None:
                    continue

                if _date in logs_set:
                    logs_set[_date].append(file) # yes!! add value!!
                else:
                    logs_set[_date] = [file]     # no!! make new list, and add value!!

        # if notting logs
        if len(logs_set) < 1:
            logging.debug("Noting log files.")
            return 0

        # sort by date (new -> old)
        # Maybe "sorted" func reverse=True option
        date_count = 0
        logs_size = 0
        for k in sorted(logs_set.keys(), reverse=True):
            # under days max
            if date_count < days:
                date_count += 1                       # date count
                logs_size += len(logs_set[k]) # get logs size
            else:
                needless_logs.extend(logs_set[k])
                del logs_set[k]                       # needless logs

        # logs delete from the oldest log files.
        # however, leave one log file par day in the minimun
        if logs_size > logs_max:
            logging.debug("Logs size is over the logs max: %s. So more delete logs by older.", logs_max)
            # sort by old -> new
            for k in sorted(logs_set.keys()):
                if sort_by is not None:
                    l = sort_by(logs_set[k])[::-1]
                else:
                    l = logs_set[k][::-1]

                end_flag = False
                while len(l) > 1:
                    needless_logs.append(l.pop())
                    logs_size -= 1

                    if logs_size <= logs_max:
                        end_flag = True
                        break

                if end_flag:
                    break

        # delete logs
        return self.delete_logs(needless_logs)


    def delete_logs(self, logs):
        delete_logs_size = len(logs)

        if len(logs) > 0:
            for file in logs:
                os.remove(self.dir_path + "/" + file)
                logging.debug("rm %(file)s" % locals())
        else:
            logging.debug("Noting need to delete log files.")

        logging.debug("Log files ware optimized.")
        return delete_logs_size
