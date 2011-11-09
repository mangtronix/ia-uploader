#!/opt/local/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)

web = QWebView()
web.load(QUrl("http://www-mang.archive.org/upload/app/"))
web.show()
web.raise_()

sys.exit(app.exec_())

