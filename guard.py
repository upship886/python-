#!/usr/bin/python
# coding:utf-8
# !/usr/bin/python
# -*- coding:utf-8 -*-
import subprocess, time, sys, os
from configparser import ConfigParser
import re

def remove_BOM(config_path):
    content = open(config_path).read()
    content = re.sub(r"\xfe\xff","", content)
    content = re.sub(r"\xff\xfe","", content)
    content = re.sub(r"\xef\xbb\xbf","", content)
    open(config_path, 'w').write(content)
class Auto_Run():
    def __init__(self, sleep_time, cmd):
        self.sleep_time = sleep_time
        self.cmd = cmd
        self.p = None  # self.p为subprocess.Popen()的返回值，初始化为None
        self.run()  # 启动时先执行一次程序
        try:
            while 1:
                time.sleep(sleep_time)  # 休息，判断程序状态
                self.poll = self.p.poll()  # 判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出
                if self.poll is None:
                    print("运行正常")
                else:
                    print("未检测到程序运行状态，准备启动程序")
                    self.run()
        except KeyboardInterrupt as e:
            print("检测到CTRL+C，准备退出程序!")
            self.p.kill()                   #检测到CTRL+C时，kill掉CMD中启动的exe或者jar程序

    def run(self):
        print('start OK!')
        self.p = subprocess.Popen(self.cmd,stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=True)




if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
    print("cwd",cwd)
    config = ConfigParser()
    remove_BOM(cwd + '\\config.ini')
    config.read(cwd + '\\config.ini', encoding='utf-8')
    # sections = con.sections()
    if config.has_section("default"):
        cmd = config.get("default", "cmd")
        Time = config.getint("default",'timespan')
        print("cmd",cmd)
    else:
        raise Exception('请在配置文件中加入default节点及 cmd、timespan')
    app = Auto_Run(Time, cmd)
