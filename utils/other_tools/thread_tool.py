#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""


import time
import threading


class PyTimer:
    """定时器类"""

    def __init__(self, func, *args, **kwargs):
        """构造函数"""

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.running = False

    def _run_func(self):
        """运行定时事件函数"""

        _thread = threading.Thread(target=self.func, args=self.args, kwargs=self.kwargs)
        _thread.setDaemon(True)
        _thread.start()

    def _start(self, interval, once):
        """启动定时器的线程函数"""

        interval = max(interval, 0.01)

        if interval < 0.050:
            _dt = interval / 10
        else:
            _dt = 0.005

        if once:
            deadline = time.time() + interval
            while time.time() < deadline:
                time.sleep(_dt)

            # 定时时间到，调用定时事件函数
            self._run_func()
        else:
            self.running = True
            deadline = time.time() + interval
            while self.running:
                while time.time() < deadline:
                    time.sleep(_dt)

                # 更新下一次定时时间
                deadline += interval

                # 定时时间到，调用定时事件函数
                if self.running:
                    self._run_func()

    def start(self, interval, once=False):
        """启动定时器

        interval    - 定时间隔，浮点型，以秒为单位，最高精度10毫秒
        once        - 是否仅启动一次，默认是连续的
        """

        thread_ = threading.Thread(target=self._start, args=(interval, once))
        thread_.setDaemon(True)
        thread_.start()

    def stop(self):
        """停止定时器"""

        self.running = False


def do_something(name, gender='male'):
    """执行"""
    print(time.time(), '定时时间到，执行特定任务')
    print('name:%s, gender:%s', name, gender)
    time.sleep(5)
    print(time.time(), '完成特定任务')


timer = PyTimer(do_something, 'Alice', gender='female')
timer.start(0.5, once=False)

input('按回车键结束\n')  # 此处阻塞住进程
timer.stop()
