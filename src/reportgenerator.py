import sys

from mako.lookup import TemplateLookup

REPORT_DIR = "report"
REPORT_FILE_NAME = "CheckstyleReport.html"


class ReportGenerator:
    def __init__(self, generation_strategy):
        self.generation_strategy = generation_strategy

    def generate(self, issues):
        self.generation_strategy.generate(issues)
        print "Generated report for %s issues" % len(issues)


class GenerationStrategy(object):
    def generate(self, issues):
        pass


class PrintStrategy(GenerationStrategy):
    def generate(self, issues):
        print "Using PrintStrategy"
        for issue in issues:
            print "author: %s, class: %s, line: %s, code: %s, description: %s" % (
                issue.author, issue.short_path, issue.line, issue.description, issue.code)


class HTMLStrategy(GenerationStrategy):
    template_lookup = TemplateLookup(
            directories=['templates'],
            module_directory='tmp/mako_modules',
            input_encoding='utf-8',
            output_encoding='utf-8',
            encoding_errors='replace')

    def serve_template(self, template_name, **kwargs):
        template = self.template_lookup.get_template(template_name)
        return template.render(**kwargs)

    def generate(self, issues):
        print "Using HTMLStrategy"
        reload(sys)
        sys.setdefaultencoding('utf-8')
        result = self.serve_template("template.txt", issues=issues)
        f = open("%s/%s" % (REPORT_DIR, REPORT_FILE_NAME), "w")
        f.write(result)
        f.close()
