from checkstyle.checkstyle import Checkstyle
from checkstyle.reportgenerator import HTMLStrategy, PrintStrategy

# directory to be checkstyle inspected
INSPECTED_DIR = "D:/dir"

# uncomment one from below strategies
STRATEGY = HTMLStrategy()
# STRATEGY = PrintStrategy()


Checkstyle(STRATEGY).perform_checkstyle(INSPECTED_DIR)
