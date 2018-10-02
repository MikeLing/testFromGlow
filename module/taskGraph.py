import logging
import uuid

from task import Task

LOG = logging.getLogger(__name__)

class TaskGraph(object):
    def __init__(self, taskMeta):
        """
        We wanna a task graph like {task1:[task2,task3], task2:[task5], task3:[]} 
        """
        self._taskSetList = []
        self._taskGraph = {}
        meta = taskMeta.get('taskInfo')
        for item in meta:
            id = uuid.uuid4()
            task = Task(str(id), item)

            self._taskGraph[task] = []

            # if we can find a dependence, mount on the node
            if task.deps and isinstance(task.deps, list):
                for d in task.deps:
                    for g in self._taskGraph.keys():
                        if d == g.name:
                            self._taskGraph[g].append(task)
    
    # run the taskgraph by DFS
    def triggerAllTasks(self):
        queue,order=[],[]
        # start with the first task node whatever it is
        startPoint = self._taskGraph.keys()[0]
        queue.append(startPoint)
        while queue:
            v = queue.pop()
            order.append(v)
            for w in self._taskGraph[v]:
                if w not in order and w not in queue: 
                    queue.append(w)
        self._taskSetList = order

        for task in self._taskSetList:
            try:
                task.execTask()
            except Exception as e:
                message = "The task %s has been killed because %s" % (task.name, str(e))
                LOG.warning(message)
                for alert in task.alert:
                    print ("send to %s, %s" % (alert, message))
