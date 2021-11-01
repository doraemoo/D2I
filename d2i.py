import socket
import argparse
import threading
from queue import Queue


class Start(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        queue = self.queue
        while not queue.empty():
            info = queue.get()  # 逐个提取队列中的数据
            try:
                result = socket.getaddrinfo(info[0], None)
                ip = result[0][4][0]
                print(info[0] + "   " + ip)
                with open(f"{info[1]}", "a+") as f:
                    f.write(info[0] + "   " + ip + "\n")
            except Exception as e:
                pass


def helpinfo():
    print("""
usage: python3 d2i.py -f domains.txt
    """)


def title():
    print("""

 ____       ___   ______
/\  _`\   /'___`\/\__  _\\
\ \ \/\ \/\_\ /\ \/_/\ \/
 \ \ \ \ \/_/// /__ \ \ \\
  \ \ \_\ \ // /_\ \ \_\ \__
   \ \____//\______/ /\_____\\
    \/___/ \/_____/  \/_____/
                       
                       Author:JoJosec         
    """)


def get_text(filename, output):
    queue = Queue()
    try:
        with open(f"{filename}", "r") as f:
            for domain in f.readlines():
                domain = domain.strip("\n")
                queue.put([domain, output])
    except Exception:
        print("123")
        exit(0)

    thread_count = 64  # 线程数
    threads = []

    for i in range(0, thread_count):
        thread = Start(queue)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def usage():
    parser = argparse.ArgumentParser(description="python3 d2i.py -f domains.txt")
    parser.add_argument('-f', '--file', help="domains.txt")
    parser.add_argument('-o', '--output', default='result.txt', help="xxx.txt")
    args = parser.parse_args()
    file = ''
    output = ''
    if args.file:
        file = args.file
        if args.output:
            output = args.output
        get_text(file, output)
    else:
        helpinfo()


if __name__ == '__main__':
    title()
    usage()
