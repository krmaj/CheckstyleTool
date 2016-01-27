import os
import re
import sys

from blamer import Blamer
from issue import LineLengthIssue, ClassSizeIssue, IllegalBooleanOperator

MAX_LINE_SIZE = 120
MAX_FILE_SIZE = 400

MULTI_LINE_COMMENT_REG_STR = '/\*.*\*/'
SINGLE_LINE_COMMENT_REG_STR = '//.*'
MULTI_LINE_COMMENT_REG = re.compile(MULTI_LINE_COMMENT_REG_STR, re.DOTALL)
SINGLE_LINE_COMMENT_REG = re.compile(SINGLE_LINE_COMMENT_REG_STR)
NEW_LINE_REG_STR = '\n'
NEW_LINE_REG = re.compile(NEW_LINE_REG_STR)
OR_AND_REG_STR = '\s(and|or)\s'
OR_AND_REG = re.compile(OR_AND_REG_STR)
VAR_NAME_REG_STR = '(\svar)(\s)*(.*)(=|:)'
VAR_NAME_REG = re.compile(VAR_NAME_REG_STR)


class FileInspector(object):
    def __init__(self, root, filename):
        self.issues = []
        self.path = root
        self.file_name = filename
        self.file_full_path = os.path.join(root, filename)
        self.file_content = None
        self.lines = None

    def inspect(self):
        self.prepare_file()
        self.inspect_file()
        return self.issues

    def prepare_file(self):
        try:
            my_file = open(self.file_full_path, "r")
            self.file_content = my_file.read()
            my_file.close()
            self.remove_multi_line_comments()
        except IOError:
            print "There was an error reading from ", self.file_full_path
            sys.exit()
        return my_file

    def remove_multi_line_comments(self):
        match = MULTI_LINE_COMMENT_REG.search(self.file_content)
        if match:
            self.replace_comment_with_blank(match)

    def replace_comment_with_blank(self, match):
        to_be_deleted = match.group()
        new_line_count = "".join(NEW_LINE_REG.findall(to_be_deleted))
        self.file_content = re.sub(MULTI_LINE_COMMENT_REG, new_line_count, self.file_content)

    def inspect_file(self):
        self.lines = self.file_content.split(NEW_LINE_REG_STR)
        self.check_file_len()

        for line_number, line in enumerate(self.lines):
            line = self.remove_single_line_comments(line)
            self.check_line_len(line, line_number)
            self.check_and_or_symbols(line, line_number)
            #self.check_var_name(line, line_number)

    def check_file_len(self):
        if len(self.lines) > MAX_FILE_SIZE:
            issue = ClassSizeIssue(self.file_full_path)
            self.issues.append(issue)

    @staticmethod
    def remove_single_line_comments(line):
        match = SINGLE_LINE_COMMENT_REG.search(line)
        if match:
            line = re.sub(SINGLE_LINE_COMMENT_REG, "", line)
        return line

    def check_line_len(self, line, line_number):
        if len(line) > MAX_LINE_SIZE:
            issue = LineLengthIssue(self.file_full_path, line_number, line)
            self.issues.append(issue)

    def check_and_or_symbols(self, that_line, line_number):
        match = OR_AND_REG.search(that_line)
        if match:
            issue = IllegalBooleanOperator(self.file_full_path, line_number, that_line)
            self.issues.append(issue)

    # def check_var_name(self, that_line, line_number):
    #     match = VAR_NAME_REG.search(that_line)
    #     if match:
    #         print that_line
    #         print match.group(3)
    #         match2 = variable.NAME_REG.search(that_line)
    #         if match2:
    #
    #             issue = IllegalBooleanOperator(self.file_full_path, line_number, that_line)
    #             self.issues.append(issue)


class BlamingFileInspector(FileInspector):
    def __init__(self, root, filename):
        super(BlamingFileInspector, self).__init__(root, filename)

    def inspect_file(self):
        super(BlamingFileInspector, self).inspect_file()
        self.blame_issues()

    def blame_issues(self):
        if len(self.issues) > 0:
            blamer = Blamer(self.path, self.file_name)
            blamer.blame()
            for issue in self.issues:
                if issue.line > 0:
                    issue.author = blamer.get_author(issue.line)
