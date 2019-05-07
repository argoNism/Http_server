import sqlite3
import re
import main

class Logger:
    def __init__(self, msg, ip, request):
        if request:
            print(request.headers)
            self.host_name = request.headers["Host"]
        else:
            self.host_name = self.parse_request(msg)

        self.request = msg
        self.ip = ip[0]
        print(self.ip)

    def parse_request(self, msg):
        try:
            lines = msg.splitlines()
            host_line = [s for s in lines if s.startswith('Host')]

            if host_line:
                host = re.search('Host:\s(.?)', host_line)
            else:
                host = "not listed"
        except:
            host = "Error in 'parse_request'"

        return host

    @classmethod
    def add_row(self, msg, ip, request):
        try:
            conn = sqlite3.connect(main.DOCUMENT_ROOT + '../db/log.db')
            c = conn.cursor()
            logger = Logger(msg, ip, request)
            c.execute("insert into log (host, ip, request) values (?,?,?)", (logger.host_name, logger.ip, logger.request))
            conn.commit()
            print("save log", (logger.host_name, logger.ip, logger.request))
        except sqlite3.OperationalError as e:
            print("sqlite3.OperationalError:",e)