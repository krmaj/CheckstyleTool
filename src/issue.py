import re

import fileinspector

FILE_PATH_REG_STR = "(dir)(.*)"
FILE_PATH_REG = re.compile(FILE_PATH_REG_STR)


def get_short_path(file_path):
    match = FILE_PATH_REG.search(file_path)
    if match:
        return match.group(2)
    return file_path


class Issue(object):
    """Abstract class representing Coding Standard Issue"""

    def __init__(self, file_path, line, code):
        self.author = ""
        self.short_path = get_short_path(file_path)
        self.line = line
        self.code = code
        self.description = ""


class LineLengthIssue(Issue):
    def __init__(self, file_path="", line=-1, code=""):
        super(LineLengthIssue, self).__init__(file_path, line, code)
        self.description = "Line cannot be longer than %s" % fileinspector.MAX_LINE_SIZE


class ClassSizeIssue(Issue):
    def __init__(self, file_path="", line=-1, code=""):
        super(ClassSizeIssue, self).__init__(file_path, line, code)
        self.description = "File cannot be longer than %s lines" % fileinspector.MAX_FILE_SIZE


class IllegalBooleanOperator(Issue):
    def __init__(self, file_path="", line=-1, code=""):
        super(IllegalBooleanOperator, self).__init__(file_path, line, code)
        self.description = "Illegal boolean operator"
