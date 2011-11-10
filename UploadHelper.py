from PyQt4 import QtCore, QtGui, QtWebKit

class UploadHelper(QtCore.QObject):  
    """Upload Helper"""  
 
    @QtCore.pyqtSlot(str)  
    def showMessage(self, msg):
        """Open a message box and display the specified message."""  
        QtGui.QMessageBox.information(None, "Info", msg)  
  
    def _pyVersion(self):  
        """Return the Python version."""  
        return sys.version  
  
    """Python interpreter version property."""  
    pyVersion = QtCore.pyqtProperty(str, fget=_pyVersion)  