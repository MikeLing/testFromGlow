import os
import json
from module.taskGraph import TaskGraph

CONFIG_PATH = os.getcwd() + "/job.json"

if __name__ == '__main__':
    with open(CONFIG_PATH, 'r') as f:
        meta = json.load(f)
        tg = TaskGraph(meta)
        tg.triggerAllTasks()
