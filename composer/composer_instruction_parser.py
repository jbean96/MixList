import os
import json

class parser(object):
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.instruction_dict = json.load(f)

