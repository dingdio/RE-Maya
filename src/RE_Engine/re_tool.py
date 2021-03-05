import os

#maya imports
import pymel.core as pm
from maya import cmds
from maya import OpenMayaUI as omui
import maya.mel as mel
from functools import partial

import settings
reload(settings)
import tree
reload(tree)
import re_motion
reload(re_motion)

import logging
logging.basicConfig()
logger = logging.getLogger('RE_Manager')
logger.setLevel(logging.DEBUG)

##Qt imports
import vendor.Qt
from vendor.Qt import QtWidgets, QtCore, QtGui
if vendor.Qt.__binding__.startswith('PyQt'):
    logger.debug('Using sip')
    from sip import wrapinstance as wrapInstance
    from vendor.Qt.QtCore import pyqtSignal as Signal
elif vendor.Qt.__binding__ == 'PySide':
    logger.debug('Using shiboken')
    from shiboken import wrapInstance
    from vendor.Qt.QtCore import Signal
else:
    logger.debug('Using shiboken2')
    from shiboken2 import wrapInstance
    from vendor.Qt.QtCore import Signal

#from vendor.Qt.QtCore import QSettings

class RE_Manager(QtWidgets.QWidget):
    def __init__(self, dock=False): 
        ## GET SETTINGS
        self.settings = settings.get()
        if not self.settings.DEFAULT_DIR_KEY:
            self.lastDir = self.getDirectory()
        else:
            self.lastDir = self.settings.DEFAULT_DIR_KEY

            
        if dock:
            parent = getDock()
        else:
            deleteDock()
            try:
                pm.deleteUI('re_manager')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QMainWindow(parent=getMayaMainWindow())
            parent.setObjectName('re_manager')
            parent.setWindowTitle('RE Engine Tool')
        super(RE_Manager, self).__init__(parent=parent)

        self.setupUi(parent)
        self.setup_buttons()
        self.parent().layout().addWidget(self)
        self.parent = parent

        
        self.recentFileActs = []

        for i in range(self.settings.RECENT_FILES_MAX):
            self.recentFileActs.append(
                    QtWidgets.QAction(parent, visible=False,
                            triggered=self.openRecentFile))
            self.menuRecent_Files.addAction( self.recentFileActs[i])


        self.recent_files_update()


        #self.lineEditRawDepo.setText(self.settings.repopath)
        #self.checkBoxImportFace.setChecked(self.settings.importFacePoses)
        directory = os.path.join(pm.internalVar(userAppDir=True), 're_engine_working')

        ##DEBUG
        #self.populate_animSet("F:\\RE3R_MODS\\maya files\\010 anims\\em0000_es_pl_bite.motlist.99")

        if not dock:
            parent.show()

    

    def recent_files_update(self):
        _translate = QtCore.QCoreApplication.translate
        numrecent = 0
        if self.settings.RECENT_FILES_MAX < len(self.settings.RECENT_FILES):
            numrecent = self.settings.RECENT_FILES_MAX
        else:
            numrecent = len(self.settings.RECENT_FILES)


        for i in range(0, numrecent):
            if self.settings.RECENT_FILES[i]:
                self.recentFileActs[i].setData(self.settings.RECENT_FILES[i])
                self.recentFileActs[i].setObjectName("recent_"+str(i))
                self.recentFileActs[i].setText(_translate("re_manager", self.settings.RECENT_FILES[i]))
                self.recentFileActs[i].setVisible(True)
            else:
                break

    def append_recent_file(self, path):
        if path in self.settings.RECENT_FILES:
            self.settings.RECENT_FILES.remove(path)
            self.settings.RECENT_FILES.insert(0, path)
        else:
            self.settings.RECENT_FILES.insert(0, path)
        self.recent_files_update()

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.load_motion_list(action.data())

    def setup_buttons(self):
        # self.importRigBtn.clicked.connect(self.importRig)
        # self.exportRigBtn.clicked.connect(self.exportRig)
        # self.importAnimBtn.clicked.connect(self.importAnims)
        # self.exportAnimBtn.clicked.connect(self.exportAnims)
        # self.importFacBtn.clicked.connect(self.importFac)
        # self.exportFacBtn.clicked.connect(self.exportFac)
        # self.addNS.clicked.connect(self.addNSFun)
        # self.remNS.clicked.connect(self.remNSFun)
        # self.attachRigBtn.clicked.connect(self.attachRig)
        self.actionImport_motlist.triggered.connect(self.actionImport_MOT_LIST)

        # self.pushButtonSaveSettings.clicked.connect(self.saveSettingsClicked)
        # self.btnExportCutscene.clicked.connect(self.exportCutsceneClicked)
        # self.toolButtonDepoSelect.clicked.connect(self.depoSelectClicked)
    
        self.animLoadSelectedBtn.clicked.connect(self.animLoadSelected)

        # self.loadAnimBtn.clicked.connect(self.importAnimsTree)
        # self.loadAllBtn.clicked.connect(self.importAnimsTree)
        # self.actorListWidget.clicked.connect(self.getActorValue)

    def setupUi(self, re_manager):
        re_manager.setObjectName("re_manager")
        re_manager.resize(630, 530)
        self.centralwidget = QtWidgets.QWidget(re_manager)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.animLoadSelectedBtn = QtWidgets.QPushButton(self.centralwidget)
        self.animLoadSelectedBtn.setObjectName("animLoadSelectedBtn")
        self.gridLayout.addWidget(self.animLoadSelectedBtn, 1, 0, 1, 1)
        self.animsTreeView = QtWidgets.QTreeView(self.centralwidget)
        self.animsTreeView.setObjectName("animsTreeView")
        self.gridLayout.addWidget(self.animsTreeView, 0, 0, 1, 1)
        re_manager.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(re_manager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 630, 21))
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
        self.menuFile.setTitle(_translate("re_manager", "File"))
        self.menuRecent_Files.setTitle(_translate("re_manager", "Recent Files"))
        self.menuAbout.setTitle(_translate("re_manager", "Help"))
        self.actionImport_motlist.setText(_translate("re_manager", "Add .mlist"))
        self.actionAbout.setText(_translate("re_manager", "About"))

    def getDirectory(self):
        directory = os.path.join(pm.internalVar(userAppDir=True), 're_engine_working')
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    def actionImport_MOT_LIST(self):
        directory = self.getDirectory()
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Select Entity", self.lastDir ,"Motlist (*.motlist.85 *.motlist.99 *.mcamlist.14 *.mcamlist.13);;All files (*.*)")
        if not fileName[0]:
            pass
        else:
            self.load_motion_list(fileName[0])

    def load_motion_list(self, path):
        print("Importing Animation Set")
        self.populate_animSet(path)
        self.settings.DEFAULT_DIR_KEY = os.path.dirname(path)
        self.lastDir = self.settings.DEFAULT_DIR_KEY
        self.append_recent_file(path)
        settings.save(self.settings)

    def animLoadSelected(self, all=False):
        #print("loading animation")
        #scene_actor = self.getSceneActor()
        #pm.select( scene_actor+"*", r=True, hi=True )
        if cmds.objExists("spine_2"):
            pm.select( "spine_2"+"*", r=True, hi=True )
        if cmds.objExists("root"):
            pm.select( "root"+"*", r=True, hi=True )
        pm.cutKey( )
        mel.eval("gotoBindPose;")
        SetEntry = self.getSelectedAnim(self.animsTreeView, self.loadedAnimSet)
        re_motion.import_mot(SetEntry, self.loadedAnimSet.filepath)
        #anims.import_w3_animation2(SetEntry.animation, scene_actor, type = "animation")
    
    def getValue(self, val):
        print(val.data())
        print(val.row())
        print(val.column())

    def getSelectedAnim(self, view_tree, animset):
        currentAnim = False
        for ix in view_tree.selectedIndexes():
            for anim in animset.header.POINTERS:
                if anim.motName == ix.data():
                    currentAnim = anim
        return currentAnim

    def populate_animSet(self, fileName):
        animSetTemplate = re_motion.read_mot_list(fileName)
        self.loadedAnimSet = animSetTemplate
        #load animSet object
        #animSet object is just animation set
        #read all the animations???
        #populate the tree with that object
        

        #animsTreeView
        treeModel = QtGui.QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        animSet = tree.StandardItem(animSetTemplate.filepath, 10, set_bold=True);
        animSet.setEditable(False)
        animSet.setSelectable(False)
        animSet.setCheckable(False)

        for animation in animSetTemplate.header.POINTERS:
            name = animation.motName
            animSet2 = tree.StandardItem(name, 10, pm_node=animation);
            animSet.appendRow(animSet2)

        rootNode.appendRow(animSet)

        self.animsTreeView.setHeaderHidden(True)
        self.animsTreeView.setModel(treeModel)
        self.animsTreeView.expandAll()
        #self.animsTreeView.doubleClicked.connect(self.getValue)
        self.animsTreeView.clicked.connect(self.getValue)

def getMayaMainWindow():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr

def getDock(name='RE_ManagerDock'):

    deleteDock(name)
    ctrl = pm.workspaceControl(name, dockToMainWindow=('right', 1), label="RE Engine Tools")
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr

def deleteDock(name='RE_ManagerDock'):
    if pm.workspaceControl(name, query=True, exists=True):
        pm.deleteUI(name)

