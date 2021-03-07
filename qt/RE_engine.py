# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RE_engine.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_re_manager(object):
    def setupUi(self, re_manager):
        re_manager.setObjectName("re_manager")
        re_manager.resize(702, 722)
        self.centralwidget = QtWidgets.QWidget(re_manager)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.animsTreeView = QtWidgets.QTreeView(self.centralwidget)
        self.animsTreeView.setObjectName("animsTreeView")
        self.verticalLayout_2.addWidget(self.animsTreeView)
        self.animLoadSelectedBtn = QtWidgets.QPushButton(self.centralwidget)
        self.animLoadSelectedBtn.setObjectName("animLoadSelectedBtn")
        self.verticalLayout_2.addWidget(self.animLoadSelectedBtn)
        self.timeEditorBtn = QtWidgets.QPushButton(self.centralwidget)
        self.timeEditorBtn.setObjectName("timeEditorBtn")
        self.verticalLayout_2.addWidget(self.timeEditorBtn)
        self.loadSequencerBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loadSequencerBtn.setObjectName("loadSequencerBtn")
        self.verticalLayout_2.addWidget(self.loadSequencerBtn)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.renameBonesBtn = QtWidgets.QPushButton(self.groupBox)
        self.renameBonesBtn.setObjectName("renameBonesBtn")
        self.verticalLayout.addWidget(self.renameBonesBtn)
        self.injectAnimBtn = QtWidgets.QPushButton(self.groupBox)
        self.injectAnimBtn.setObjectName("injectAnimBtn")
        self.verticalLayout.addWidget(self.injectAnimBtn)
        self.verticalLayout_2.addWidget(self.groupBox)
        re_manager.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(re_manager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 702, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRecent_Files = QtWidgets.QMenu(self.menuFile)
        self.menuRecent_Files.setObjectName("menuRecent_Files")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        re_manager.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(re_manager)
        self.statusbar.setObjectName("statusbar")
        re_manager.setStatusBar(self.statusbar)
        self.actionImport_motlist = QtWidgets.QAction(re_manager)
        self.actionImport_motlist.setCheckable(False)
        self.actionImport_motlist.setObjectName("actionImport_motlist")
        self.actionAbout = QtWidgets.QAction(re_manager)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionImport_motlist)
        self.menuFile.addAction(self.menuRecent_Files.menuAction())
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(re_manager)
        QtCore.QMetaObject.connectSlotsByName(re_manager)

    def retranslateUi(self, re_manager):
        _translate = QtCore.QCoreApplication.translate
        re_manager.setWindowTitle(_translate("re_manager", "RE Engine Motion Tool"))
        self.animLoadSelectedBtn.setText(_translate("re_manager", "Load Selected"))
        self.timeEditorBtn.setText(_translate("re_manager", "Load All into Time Editor (WIP)"))
        self.loadSequencerBtn.setText(_translate("re_manager", "Load Mcamlist into Camera Sequencer (WIP)"))
        self.groupBox.setTitle(_translate("re_manager", "Utils"))
        self.renameBonesBtn.setToolTip(_translate("re_manager", "Renames selected bones from the RE2 naming scheme to the DMC5 one, or vice versa."))
        self.renameBonesBtn.setText(_translate("re_manager", "RE2 <--> DMC5"))
        self.injectAnimBtn.setToolTip(_translate("re_manager", "Creates a new motlist with the selected animation replaced by the scene timeline."))
        self.injectAnimBtn.setText(_translate("re_manager", "Inject Animation (WIP)"))
        self.menuFile.setTitle(_translate("re_manager", "File"))
        self.menuRecent_Files.setTitle(_translate("re_manager", "Recent Files"))
        self.menuAbout.setTitle(_translate("re_manager", "Help"))
        self.actionImport_motlist.setText(_translate("re_manager", "Add .mlist"))
        self.actionAbout.setText(_translate("re_manager", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    re_manager = QtWidgets.QMainWindow()
    ui = Ui_re_manager()
    ui.setupUi(re_manager)
    re_manager.show()
    sys.exit(app.exec_())
