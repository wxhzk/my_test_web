#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import Queue
import threading
import functools
import tornado.ioloop

class TaskThread(threading.Thread):
    def __init__(self, **kwargs):
        self._name = kwargs.pop('name')
        self._pool = kwargs.pop('pool')
        super(TaskThread,self).__init__()
        print "TaskThread %s start"%self._name

    def get_handler(self):
        raise NotImplementedError("Not Implemented")

    def run(self):
        while self._pool._running:
            try:
                func, callback = self._pool._queue.get(True, self._pool._timeout)
                print "TaskThread %s get a task"%(self._name)
                handler = self.get_handler()
                result, ex = None, None
                if hasattr(handler, func.func.func_name):
                    try:
                        data = func()
                        result = getattr(handler, func.func.func_name)(*data)
                    except Exception:
                        ex = sys.exc_info()
                        print "%s exception %s"%(self._name, ex)
                if callback:
                    self._pool._ioloop.add_callback(functools.partial(callback, result, ex))
            except Queue.Empty:
                pass
        if hasattr(self, "close"):
            print "TaskThread %s close"%self._name
            self.close()

class AsyncMixin(object):
    def __init__(self, taskclass=TaskThread, taskargs={}, ioloop=None, taskNum=10, timeout=1):
        self._taskclass = taskclass
        self._taskargs = taskargs
        self._tasknum = taskNum
        self._timeout = timeout
        self._queue = Queue.Queue()
        self._ioloop = ioloop or tornado.ioloop.IOLoop.current()
        self._threads = []
        self._running = True
        for i in xrange(self._tasknum):
            self._taskargs['name'] = "thread_%s"%i
            self._taskargs['pool'] = self
            thread = self._taskclass(**self._taskargs)
            thread.start()
            self._threads.append(thread)

    def add_task(self, func, callback=None):
        print 'add_task callback:%s'%(callback.func_name if callback else '')
        self._queue.put((func, callback))

    def stop(self):
        self._running = False
        map(lambda t: t.join(), self._threads)

def async_method(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]
        if isinstance(obj, AsyncMixin):
            callback = kwargs.pop('callback', None)
            obj.add_task(functools.partial(func, *args, **kwargs), callback)
        else:
            raise ValueError("error")
    return wrapper

def async_class(kclass):
    if hasattr(kclass, '__async_methods__'):
        async_methods = getattr(kclass, '__async_methods__')
        for name in async_methods:
            method = getattr(kclass, name)
            setattr(kclass, 'hooked_%s'%name, method)
            setattr(kclass, name, async_method(method))
    return kclass







