import os.path
import sys
from os import rename

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

from mainwindow import Ui_MainWindow


# TODO: file name parse
# TODO: CJM file save
# TODO: CJM file parsing
# TODO: invalid combinations

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionE_xit.triggered.connect(self.file_exit)
        self.action_Open.triggered.connect(self.file_open)
        self.actionRename.triggered.connect(self.file_rename)
        self.model.currentIndexChanged.connect(self.rebuild_cjm)
        self.model2.currentIndexChanged.connect(self.rebuild_cjm)
        self.joystick.currentIndexChanged.connect(self.rebuild_cjm)
        self.mouse.currentIndexChanged.connect(self.rebuild_cjm)
        self.diskmode.currentIndexChanged.connect(self.rebuild_cjm)
        self.reu.currentIndexChanged.connect(self.rebuild_cjm)
        self.setmorejoy.toggled.connect(self.rebuild_cjm)
        self.setfh.toggled.connect(self.rebuild_cjm)
        self.setdi.toggled.connect(self.rebuild_cjm)
        self.setns.toggled.connect(self.rebuild_cjm)
        self.bank0.toggled.connect(self.rebuild_cjm)
        self.bank1.toggled.connect(self.rebuild_cjm)
        self.bank2.toggled.connect(self.rebuild_cjm)
        self.bank3.toggled.connect(self.rebuild_cjm)
        self.bank5.toggled.connect(self.rebuild_cjm)

        self.path = ""
        self.basename = ""
        self.extension = ""
        self.original = ""
        self.cjm_type = False
        self.rebuild_cjm("")

    def file_exit(self, s):
        self.close()

    def file_open(self, s):
        name = QFileDialog.getOpenFileName(self, "Open file", filter=self.tr(
            "CJM files (*.cjm);;virtual disk file (*.d64 *.g64 *d81);;virtual cartridge file (*.crt);;standard virtual tape file (*.tap *.t64);;stand-alone virtual program file (*.prg *.p00);;all files (*.*) "))
        if name[0] != "":
            self.clear_form()
            self.original = name[0]
            self.path = os.path.dirname(name[0])
            (self.basename, self.extension) = os.path.splitext(os.path.basename((name[0])))
            self.cjm_type = self.extension == ".cjm"
            self.rebuild_cjm("")

    def file_rename(self, s):
        new_name = os.path.join(os.path.abspath(self.path), self.get_filename())
        rename(self.original, new_name)
        self.original = new_name

    def get_filename(self) -> str:
        inner = ""
        result = self.basename
        if self.model.currentIndex() > 0:
            inner += ("", "M6", "MV")[self.model.currentIndex()]
        if self.model2.currentIndex() > 0:
            inner += ("", "TP", "TN")[self.model2.currentIndex()]
        if self.joystick.currentIndex() > 0:
            inner += ("", "J1", "J2")[self.joystick.currentIndex()]
        if self.diskmode.currentIndex() > 0:
            inner += ("", "AD", "RO", "CD")[self.diskmode.currentIndex()]
        if self.reu.currentIndex() > 0:
            inner += ("", "R5", "R2", "RM")[self.diskmode.currentIndex()]

        if self.setfh.isChecked():
            inner += "FH"
        if self.setdi.isChecked():
            inner += "NI"
        if self.setns.isChecked():
            inner += "NS"
        if self.bank0.isChecked():
            inner += "B0"
        if self.bank1.isChecked():
            inner += "B1"
        if self.bank2.isChecked():
            inner += "B2"
        if self.bank3.isChecked():
            inner += "B3"
        if self.bank5.isChecked():
            inner += "B5"
        if inner != "":
            result += "_" + inner
        result += self.extension
        return result

    def get_cjm(self) -> str:
        result = ""
        tmp = []
        if self.model.currentIndex() > 0:
            tmp.append(("", "64", "vic")[self.model.currentIndex()])
        if self.model2.currentIndex() > 0:
            tmp.append(("", "pal", "ntsc")[self.model2.currentIndex()])
        if self.diskmode.currentIndex() > 0:
            tmp.append(("", "accuratedisk", "readonly", "")[self.diskmode.currentIndex()])
        if self.setfh.isChecked():
            tmp.append("fullheight")
        if self.setdi.isChecked():
            tmp.append("driveicon")
        if self.setns.isChecked():
            tmp.append("noaudioscale")
        if self.bank0.isChecked():
            tmp.append("bank0")
        if self.bank1.isChecked():
            tmp.append("bank1")
        if self.bank2.isChecked():
            tmp.append("bank2")
        if self.bank3.isChecked():
            tmp.append("bank3")
        if self.bank5.isChecked():
            tmp.append("bank5")
        if "" in tmp:
            tmp.remove("")
        if len(tmp) > 0:
            result = "X:" + ",".join(tmp)
        return result

    def rebuild_cjm(self, value) -> None:
        self.fileName.setText(self.get_filename())
        self.cjmcontent.setPlainText(self.get_cjm())
        self.actionRename.setEnabled(not self.cjm_type and self.original != "")

    def clear_form(self) -> None:
        for item in [self.model, self.model2, self.joystick, self.diskmode]:
            item.setCurrentIndex(0)
        for item in [self.setfh, self.setdi, self.setns, self.bank0, self.bank1, self.bank2, self.bank3, self.bank5]:
            item.setChecked(False)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
