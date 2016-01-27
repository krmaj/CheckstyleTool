import os

import re

AUTHOR_REG_STR = "(\()(.*)\s20"
AUTHOR_REG = re.compile(AUTHOR_REG_STR)


class Blamer:
    def __init__(self, path, file_name):
        self.blame_result = []
        self.path = path
        self.file_name = file_name

    def blame(self):
        cmd = 'cd /d {path} & git blame {filename}'.format(
                path=self.path,
                filename=self.path + "/" + self.file_name)

        with os.popen(cmd) as process:
            self.blame_result = process.readlines()

        return self.blame_result

    def get_author(self, line_num):
        match = AUTHOR_REG.search(self.blame_result[line_num])
        if match:
            return match.group(2)
        return ""
