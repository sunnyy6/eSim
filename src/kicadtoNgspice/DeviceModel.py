from PyQt6 import QtWidgets, QtCore
import os
from xml.etree import ElementTree as ET
from . import TrackWidget


class DeviceModel(QtWidgets.QWidget):
    """
    - This class creates Device Library Tab in KicadtoNgspice Window
      It dynamically creates the widget for device like diode,mosfet,
      transistor and jfet.
    - Same function as the subCircuit file, except for
      this takes different parameters in the if block
        - q   TRANSISTOR
        - d   DIODE
        - j   JFET
        - m   MOSFET
        - s   SWITCH
        - tx  single lossy transmission line
    - Other 2 functions same as the ones in subCircuit
        - trackLibrary
        - trackLibraryWithoutButton
    """

    def __init__(self, schematicInfo, clarg1):

        self.clarg1 = clarg1
        kicadFile = self.clarg1
        (projpath, filename) = os.path.split(kicadFile)
        project_name = os.path.basename(projpath)

        try:
            f = open(
                os.path.join(
                    projpath,
                    project_name +
                    "_Previous_Values.xml"),
                'r')
            tree = ET.parse(f)
            parent_root = tree.getroot()
            for child in parent_root:
                if child.tag == "devicemodel":
                    root = child
        except BaseException:
            print("Device Model Previous XML is Empty")

        QtWidgets.QWidget.__init__(self)

        # Creating track widget object
        self.obj_trac = TrackWidget.TrackWidget()

        # Row and column count
        self.row = 0
        self.count = 1  # Entry count
        self.entry_var = {}

        # For MOSFET
        self.widthLabel = {}
        self.lengthLabel = {}
        self.multifactorLable = {}
        self.devicemodel_dict_beg = {}
        self.devicemodel_dict_end = {}
        # List to hold information about device
        self.deviceDetail = {}

        # Set Layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        # print("Reading Device model details from Schematic")

        for eachline in schematicInfo:
            print("=========================================")
            print(eachline)
            words = eachline.split()
            if eachline[0] == 'q':
                # print("Device Model Transistor: ", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                transbox = QtWidgets.QGroupBox()
                transgrid = QtWidgets.QGridLayout()
                transbox.setTitle(
                    "Add library for Transistor " +
                    words[0] +
                    " : " +
                    words[4])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                global path_name

                try:
                    for child in root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                    path_name = child[0].text
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of device " +
                                      "model transistor :", str(e))
                except BaseException:
                    pass

                transgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                transgrid.addWidget(self.addbtn, self.row, 2)
                transbox.setLayout(transgrid)

                # CSS
                transbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(transbox)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 'd':
                # print("Device Model Diode:", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                diodebox = QtWidgets.QGroupBox()
                diodegrid = QtWidgets.QGridLayout()
                diodebox.setTitle(
                    "Add library for Diode " +
                    words[0] +
                    " : " +
                    words[3])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                # global path_name
                try:
                    for child in root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    path_name = child[0].text
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of device " +
                                      "model diode :", str(e))
                except BaseException:
                    pass

                diodegrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                diodegrid.addWidget(self.addbtn, self.row, 2)
                diodebox.setLayout(diodegrid)

                # CSS
                diodebox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(diodebox)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 'j':
                # print("Device Model JFET:", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                jfetbox = QtWidgets.QGroupBox()
                jfetgrid = QtWidgets.QGridLayout()
                jfetbox.setTitle(
                    "Add library for JFET " +
                    words[0] +
                    " : " +
                    words[4])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                # global path_name
                try:
                    for child in root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                    path_name = child[0].text
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of Device " +
                                      "Model JFET :", str(e))
                except BaseException:
                    pass

                jfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                jfetgrid.addWidget(self.addbtn, self.row, 2)
                jfetbox.setLayout(jfetgrid)

                # CSS
                jfetbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius:\
                 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(jfetbox)

                # Adding Device Details #
                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 's':
                # print("Device Model Switch:", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                switchbox = QtWidgets.QGroupBox()
                switchgrid = QtWidgets.QGridLayout()
                switchbox.setTitle(
                    "Add library for Switch " +
                    words[0] +
                    " : " +
                    words[5])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                # global path_name
                try:
                    for child in root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    path_name = child[0].text
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of device " +
                                      "model switch :", str(e))
                except BaseException:
                    pass

                switchgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                switchgrid.addWidget(self.addbtn, self.row, 2)
                switchbox.setLayout(switchgrid)

                # CSS
                switchbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(switchbox)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 'ytxl':
                # print("Device Model ymod:", words[0])
                self.devicemodel_dict_beg[words[0]] = self.count
                ymodbox = QtWidgets.QGroupBox()
                ymodgrid = QtWidgets.QGridLayout()
                ymodbox.setTitle(
                    "Add library for ymod " +
                    words[0] +
                    " : " +
                    words[4])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                # global path_name
                try:
                    for child in root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            try:
                                if child[0].text \
                                   and os.path.exists(child[0].text):
                                    path_name = child[0].text
                                    self.entry_var[self.count] \
                                        .setText(child[0].text)
                                else:
                                    self.entry_var[self.count].setText("")
                            except BaseException as e:
                                print("Error when set text of device " +
                                      "model ymod :", str(e))
                except BaseException:
                    pass

                ymodgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                self.deviceDetail[self.count] = words[0]

                if self.entry_var[self.count].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(self.count, path_name)

                ymodgrid.addWidget(self.addbtn, self.row, 2)
                ymodbox.setLayout(ymodgrid)

                # CSS
                ymodbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius: \
                9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left:\
                 10px; padding: 0 3px 0 3px; } \
                ")

                self.grid.addWidget(ymodbox)

                # Adding Device Details #

                # Increment row and widget count
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1

            elif eachline[0] == 'm':

                self.devicemodel_dict_beg[words[0]] = self.count
                mosfetbox = QtWidgets.QGroupBox()
                mosfetgrid = QtWidgets.QGridLayout()
                i = self.count
                beg = self.count
                mosfetbox.setTitle(
                    "Add library for MOSFET " +
                    words[0] +
                    " : " +
                    words[4])
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setReadOnly(True)
                mosfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.addbtn = QtWidgets.QPushButton("Add")
                self.addbtn.setObjectName("%d" % self.count)
                self.addbtn.clicked.connect(self.trackLibrary)
                mosfetgrid.addWidget(self.addbtn, self.row, 2)

                # Adding Device Details
                self.deviceDetail[self.count] = words[0]

                # Increment row and widget count
                self.row = self.row + 1
                self.count = self.count + 1

                # Adding to get MOSFET dimension
                self.widthLabel[self.count] = QtWidgets.QLabel(
                    "Enter width of MOSFET " + words[0] + "(default=100u):")
                mosfetgrid.addWidget(self.widthLabel[self.count], self.row, 0)
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.row = self.row + 1
                self.count = self.count + 1

                self.lengthLabel[self.count] = QtWidgets.QLabel(
                    "Enter length of MOSFET " + words[0] + "(default=100u):")
                mosfetgrid.addWidget(self.lengthLabel[self.count], self.row, 0)
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.row = self.row + 1
                self.count = self.count + 1

                self.multifactorLable[self.count] = QtWidgets.QLabel(
                    "Enter multiplicative factor of MOSFET " +
                    words[0] + "(default=1):")
                mosfetgrid.addWidget(
                    self.multifactorLable[self.count], self.row, 0)
                self.entry_var[self.count] = QtWidgets.QLineEdit()
                self.entry_var[self.count].setText("")
                end = self.count
                self.entry_var[self.count].setMaximumWidth(150)
                mosfetgrid.addWidget(self.entry_var[self.count], self.row, 1)
                self.row = self.row + 1
                self.devicemodel_dict_end[words[0]] = self.count
                self.count = self.count + 1
                mosfetbox.setLayout(mosfetgrid)

                # global path_name
                try:
                    for child in root:
                        if child.tag == words[0]:
                            # print("DEVICE MODEL MATCHING---", \
                            #       child.tag, words[0])
                            while i <= end:
                                self.entry_var[i].setText(child[i - beg].text)
                                if (i - beg) == 0:
                                    if os.path.exists(child[0].text):
                                        self.entry_var[i] \
                                            .setText(child[i - beg].text)
                                        path_name = child[i - beg].text
                                    else:
                                        self.entry_var[i].setText("")
                                i = i + 1
                except BaseException:
                    pass
                # CSS
                mosfetbox.setStyleSheet(" \
                QGroupBox { border: 1px solid gray; border-radius:\
                 9px; margin-top: 0.5em; } \
                QGroupBox::title { subcontrol-origin: margin; left: \
                10px; padding: 0 3px 0 3px; } \
                ")
                if self.entry_var[beg].text() == "":
                    pass
                else:
                    self.trackLibraryWithoutButton(beg, path_name)

                self.grid.addWidget(mosfetbox)

            self.show()

    def trackLibrary(self):
        """
        This function is use to keep track of all Device Model widget
        """
        print("Calling Track Device Model Library funtion")
        sending_btn = self.sender()
        self.widgetObjCount = int(sending_btn.objectName())

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        self.libfile = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Library Directory",
                init_path + "library/deviceModelLibrary", "*.lib"
            )[0]
        )

        if not self.libfile:
            return

        # Setting Library to Text Edit Line
        self.entry_var[self.widgetObjCount].setText(self.libfile)
        self.deviceName = self.deviceDetail[self.widgetObjCount]

        # Storing to track it during conversion
        if self.deviceName[0] == 'm':
            width = str(self.entry_var[self.widgetObjCount + 1].text())
            length = str(self.entry_var[self.widgetObjCount + 2].text())
            multifactor = str(self.entry_var[self.widgetObjCount + 3].text())
            if width == "":
                width = "100u"
            if length == "":
                length = "100u"
            if multifactor == "":
                multifactor = "1"

            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile + \
                ":" + "W=" + width + " L=" + length + " M=" + multifactor

        else:
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile

    def trackLibraryWithoutButton(self, iter_value, path_value):
        """
        This function is use to keep track of all Device Model widget
        """
        print("Calling Track Library function Without Button")
        self.widgetObjCount = iter_value
        print("self.widgetObjCount-----", self.widgetObjCount)
        self.libfile = path_value
        print("PATH VALUE", path_value)

        # Setting Library to Text Edit Line
        self.entry_var[self.widgetObjCount].setText(self.libfile)
        self.deviceName = self.deviceDetail[self.widgetObjCount]

        # Storing to track it during conversion
        if self.deviceName[0] == 'm':
            width = str(self.entry_var[self.widgetObjCount + 1].text())
            length = str(self.entry_var[self.widgetObjCount + 2].text())
            multifactor = str(self.entry_var[self.widgetObjCount + 3].text())
            if width == "":
                width = "100u"
            if length == "":
                length = "100u"
            if multifactor == "":
                multifactor = "1"
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile + \
                ":" + "W=" + width + " L=" + length + " M=" + multifactor
        else:
            self.obj_trac.deviceModelTrack[self.deviceName] = self.libfile
