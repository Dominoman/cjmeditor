import os.path
import sys
from os import rename

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

from mainwindow import Ui_MainWindow

MODES = ("", "M6", "MV")
MODES2 = ("", "TP", "TN")
JOY = ("", "J1", "J2")
MOUSE = ("", "P1", "P2")
DISKMODE = ("", "AD", "RO", "CD")
REU = ("", "R5", "R2", "RM")

JOYKEYS = ["JU", "JD", "JL", "JR", "JF", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "A", "B", "C", "D", "E", "F",
           "G",
           "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3",
           "4", "5", "6", "7", "8", "9", "0", "AL",
           "AU", "CM", "CO", "CT", "CU", "CD", "CL", "CR", "DL", "EN", "HM", "RS", "RE", "SL", "SR", "SS", "SP", "PO"]
JOYLABELS = ["Joy Up", "Joy Down", "Joy Left", "Joy Right", "Joy Fire", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
             "A", "B", "C", "D", "E",
             "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Arrow Left",
             "Arrow Up", "CBM", ",", "CTRL", "Cursor Up", "Cursor Down", "Cursor Left", "Cursor Right", "Ins/Del",
             "RETURN", "Clr/Home", "Run/Stop", "RESTORE", "Left Shift", "Right Shift", "Shift Lock", "SPACE",
             "£"]

VIC20BANKS = {"3 kB":("B0"),"4 kB":(),"8 kB":("B1"),"16 kB":("B1","B2"),"24 kB":("B1","B2","B3"),"32 kB":("B1","B2","B3","B5"),"35 kB":("B0","B1","B2","B3","B5")}


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionE_xit.triggered.connect(self.file_exit)
        self.action_Open.triggered.connect(self.file_open)
        self.actionRename.triggered.connect(self.file_rename)
        self.action_Save_cjm.triggered.connect(self.file_save)
        self.model.currentIndexChanged.connect(self.form_change)
        self.model2.currentIndexChanged.connect(self.form_change)
        self.joystick.currentIndexChanged.connect(self.form_change)
        self.mouse.currentIndexChanged.connect(self.form_change)
        self.diskmode.currentIndexChanged.connect(self.form_change)
        self.reu.currentIndexChanged.connect(self.form_change)
        self.chbxs = {"JA": self.setmorejoy, "FH": self.setfh, "NI": self.setdi, "NS": self.setns, "B0": self.bank0,
                      "B1": self.bank1, "B2": self.bank2, "B3": self.bank3, "B5": self.bank5}
        for cb in self.chbxs.values():
            cb.toggled.connect(self.form_change)
        self.ramsetting.currentIndexChanged.connect(self.ram_change)
        self.joy1.clicked.connect(self.joystick_config)
        self.joy2.clicked.connect(self.joystick_config)
        self.joy3.clicked.connect(self.joystick_config)
        self.joy4.clicked.connect(self.joystick_config)

        self.path = ""
        self.basename = ""
        self.extension = ""
        self.original = ""
        self.cjm_type = True
        self.form_change("")

    def file_exit(self, value):
        self.close()

    def file_open(self, value):
        name = QFileDialog.getOpenFileName(self, "Open file", filter=self.tr(
            "CJM files (*.cjm);;virtual disk file (*.d64 *.g64 *d81);;virtual cartridge file (*.crt);;standard virtual tape file (*.tap *.t64);;stand-alone virtual program file (*.prg *.p00);;all files (*.*) "))
        if name[0] != "":
            self.clear_form()
            self.original = name[0]
            self.path = os.path.dirname(name[0])
            (self.basename, self.extension) = os.path.splitext(os.path.basename((name[0])))
            self.cjm_type = self.extension == ".cjm"
            if self.cjm_type:
                pass
            else:
                self.parse_filename()
            self.form_change("")
            self.statusbar.showMessage(f"File {name[0]} loaded.", 2000)

    def file_save(self, value):
        if self.cjm_type:
            pass
        else:
            pass

    def file_rename(self, value):
        new_name = os.path.join(os.path.abspath(self.path), self.get_filename())
        rename(self.original, new_name)
        self.statusbar.showMessage(f"File {self.original} renamed to {new_name}", 2000)
        self.original = new_name

    def ram_change(self, value):
        value = self.ramsetting.currentText()
        if value in VIC20BANKS:
            for bank in ["B0","B1","B2","B3","B5"]:
                if bank in VIC20BANKS[value]:
                    self.chbxs[bank].setChecked(True)
                else:
                    self.chbxs[bank].setChecked(False)
        self.ramsetting.setCurrentIndex(0)

    def joystick_config(self):
        pass

    def form_change(self, value) -> None:
        self.fileName.setText(self.get_filename())
        self.cjmsource.setPlainText(self.get_cjm())
        self.actionRename.setEnabled(not self.cjm_type and self.original != "")

    def get_filename(self) -> str:
        flags = ""
        if self.model.currentIndex() > 0:
            flags += MODES[self.model.currentIndex()]
        if self.model2.currentIndex() > 0:
            flags += MODES2[self.model2.currentIndex()]
        if self.joystick.currentIndex() > 0:
            flags += JOY[self.joystick.currentIndex()]
        if self.mouse.currentIndex() > 0:
            flags += MOUSE[self.mouse.currentIndex()]
        if self.diskmode.currentIndex() > 0:
            flags += DISKMODE[self.diskmode.currentIndex()]
        if self.reu.currentIndex() > 0:
            flags += REU[self.reu.currentIndex()]

        for key, cb in self.chbxs.items():
            if cb.isChecked():
                flags += key

        result = self.basename
        if flags != "":
            result += "_" + flags
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
        if self.reu.currentIndex() > 0:
            tmp.append(("", "reu512", "reu2048", "reu16384")[self.reu.currentIndex()])
        if self.setfh.isChecked():
            tmp.append("fullheight")
        if not self.setdi.isChecked():
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
        while "" in tmp:
            tmp.remove("")
        if len(tmp) > 0:
            result = "X:" + ",".join(tmp) + "\n"

        return result

    def clear_form(self) -> None:
        for item in [self.model, self.model2, self.joystick, self.mouse, self.diskmode, self.reu]:
            item.setCurrentIndex(0)
        for item in [self.setmorejoy, self.setfh, self.setdi, self.setns, self.bank0, self.bank1, self.bank2,
                     self.bank3, self.bank5]:
            item.setChecked(False)

    def parse_filename(self) -> None:
        items = self.basename.split('_')
        if len(items) < 2:
            return
        flags = [items[-1][i:i + 2].upper() for i in range(0, len(items[-1]), 2)]
        for flag in flags:
            if flag in MODES:
                self.model.setCurrentIndex(MODES.index(flag))
            elif flag in MODES2:
                self.model2.setCurrentIndex(MODES2.index(flag))
            elif flag in JOY:
                self.joystick.setCurrentIndex(JOY.index(flag))
            elif flag in MOUSE:
                self.mouse.setCurrentIndex(MOUSE.index(flag))
            elif flag in DISKMODE:
                self.diskmode.setCurrentIndex(DISKMODE.index(flag))
            elif flag in REU:
                self.reu.setCurrentIndex(REU.index(flag))
            elif flag in self.chbxs:
                self.chbxs[flag].setChecked(True)
            else:
                print("Unknown flag")
        self.basename = self.basename[:-len(items[-1]) - 1]


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
