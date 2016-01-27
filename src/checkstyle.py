import os
import re

from fileinspector import FileInspector, BlamingFileInspector
from reportgenerator import ReportGenerator
from timing import timing

GOSU_FILE_NAME_REG_STR = '\.(gs|gsx)$'
GOSU_FILE_NAME_REG = re.compile(GOSU_FILE_NAME_REG_STR)


class Checkstyle:
    def __init__(self, strategy):
        self.report_generator = ReportGenerator(strategy)

    @timing
    def perform_checkstyle(self, inspected_dir):
        issues = []
        for root, directories, file_names in os.walk(inspected_dir):
            for filename in file_names:
                file_name_match = GOSU_FILE_NAME_REG.search(filename)
                if file_name_match:

					#use one of below
                    inspector = FileInspector(root, filename)
                    #inspector = BlamingFileInspector(root, filename)

                    issues += inspector.inspect()

        self.report_generator.generate(issues)
