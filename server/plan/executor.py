"""
This modules contains executor of various stage type
"""
from subprocess import Popen,run
from ..config.config import Stage

"""
Genertic Stage executor
"""


class Executor:
    def __init__(self, stage: Stage, detach=False, cwd="."):
        self.stage = stage
        self.detach = detach
        self.cwd = cwd

    """
    execute, executes the executor
    """

    def execute(self):
        
        
