import test
import logging
import subprocess

from timeout import timeout
from subprocess import call


LOG = logging.getLogger(__name__)

TASK_TYPE = ['pyfunc', 'shell']

class Task(object):
    """This represents a Task"""
    def __init__(self, task_id, task_info=None):
        """
        Object that can represent each task in the task queue.

        :param task_id:  We need to have a push id to identify a unique task.
        :type  task_id:    str

        :param task_info: the init information for this task
        :type task_info: Meta data for this task which beed defined as json. e.g:
            {  "type": "pyfunc",
                "name": "test_pyfunc",
                "call": "module.test:func",
                "args": ["arg_a","arg_b"],
                "kwargs": {"kw_a": "a","kw_b": "b"},
                "alert": ["a@a.com", "b@b.com"],
                "timeout": 30},
        """
        self._id = task_id

        # handle the task info anyway, to avoide the unnecessary Exception 
        self._task = dict()
        self._task['type'] = task_info.get('type', None)
        self._task['name'] = task_info.get('name', None)
        self._task['call'] = task_info.get('call', None)
        self._task['cmd'] = task_info.get('cmd', None)
        self._task['deps'] = task_info.get('deps', [])
        self._task['args'] = task_info.get('args', [])
        self._task['kwargs'] = task_info.get('kwargs', {})
        self._task['alert'] = task_info.get('alert', [])
        self._task['timeout'] = task_info.get('timeout', None)

        # the type, alert, timeout is necessary for all the kinds of tasks
        if not (self._task['type'] and len(self._task['alert']) > 0 and self._task['timeout']):
            raise Exception("The type, alert, timeout is necessary for all the kinds of tasks")

        if self._task['type'] not in TASK_TYPE:
            raise Exception("The Task must be either python function or shell command")
        
        # python function must know which function gonna call
        if self._task['type'] == 'pyfunc' and self._task['call'] == None:
            raise Exception("Needs to know which python function gonna call")

        # shell command must know the command
        if self._task['type'] == 'shell' and self._task['cmd'] == None:
            raise Exception("Needs to know which shell cmd gonna call")

    # we need it hashable
    def __hash__(self):
        return hash((self._id, self._task['type']))

    # we to compre its name in dict list
    def __eq__(self, other):
        return self._task['name'] == other.name
    
    # display the task info
    def __repr__(self):
        return "<Task id:%s info:%s>" % (self._id, self._task)

    # exec the task
    def execTask(self):
        with timeout(seconds=self.timeout):
            if self.type == "pyfunc":
                self._execPy()
            if self.type == "shell":
                self._execShell()

    # exec a python task
    def _execPy(self):
        functionName = self.call.split(":")[-1]
        getattr(test, functionName)(*self.args, **self.kwargs)
        
    # exec a shell tasl
    def _execShell(self):
        subprocess.call(self.cmd, shell=True)

    # getter for id
    @property
    def id(self):
        return self._id

    # getter for type
    @property
    def type(self):
        return self._task.get('type')

    # getter for name
    @property
    def name(self):
        return self._task.get('name')
    
    # getter alert
    @property
    def alert(self):
        return self._task.get('alert')

    # getter for all
    @property
    def call(self):
        return self._task.get('call')

    # getter for cmd
    @property
    def cmd(self):
        return self._task.get('cmd')

    # getter for args
    @property
    def args(self):
        return self._task.get('args')

    # getter for kwargs
    @property
    def kwargs(self):
        return self._task.get('kwargs')

    # getter for deps
    @property
    def deps(self):
        return self._task.get('deps')

    # getter and setter for timeout
    @property
    def timeout(self):
        return self._task.get('timeout')

    @timeout.setter
    def timeout(self, newTimeout):
        self._task['timeout'] = newTimeout
