# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------

# This file is part of Code_Saturne, a general-purpose CFD tool.
#
# Copyright (C) 1998-2013 EDF S.A.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.

#-------------------------------------------------------------------------------

"""
This module contains the following classes and function:
- LagrangianOutputView
"""

#-------------------------------------------------------------------------------
# Standard modules
#-------------------------------------------------------------------------------

import logging

#-------------------------------------------------------------------------------
# Third-party modules
#-------------------------------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

#-------------------------------------------------------------------------------
# Application modules import
#-------------------------------------------------------------------------------

from Pages.LagrangianOutputForm import Ui_LagrangianOutputForm
from Base.Toolbox import GuiParam
from Base.QtPage import ComboModel, IntValidator, DoubleValidator
from Pages.LagrangianOutputModel import LagrangianOutputModel

#-------------------------------------------------------------------------------
# log config
#-------------------------------------------------------------------------------

logging.basicConfig()
log = logging.getLogger("LagrangianOutputView")
log.setLevel(GuiParam.DEBUG)

#-------------------------------------------------------------------------------
# Main class
#-------------------------------------------------------------------------------

class LagrangianOutputView(QWidget, Ui_LagrangianOutputForm):
    """
    """
    def __init__(self, parent, case):
        """
        Constructor
        """
        QWidget.__init__(self, parent)

        Ui_LagrangianOutputForm.__init__(self)
        self.setupUi(self)

        self.case = case
        self.case.undoStopGlobal()
        self.model = LagrangianOutputModel(self.case)

        # Connections
        self.connect(self.checkBoxIVISV1, SIGNAL("clicked()"),    self.slotIVISV1)
        self.connect(self.checkBoxIVISV2, SIGNAL("clicked()"),    self.slotIVISV2)
        self.connect(self.checkBoxIVISTP, SIGNAL("clicked()"),    self.slotIVISTP)
        self.connect(self.checkBoxIVISDM, SIGNAL("clicked()"),    self.slotIVISDM)
        self.connect(self.checkBoxIVISTE, SIGNAL("clicked()"),    self.slotIVISTE)
        self.connect(self.checkBoxIVISMP, SIGNAL("clicked()"),    self.slotIVISMP)
        self.connect(self.checkBoxIVISDK, SIGNAL("clicked()"),    self.slotIVISDK)
        self.connect(self.checkBoxIVISCH, SIGNAL("clicked()"),    self.slotIVISCH)
        self.connect(self.checkBoxIVISCK, SIGNAL("clicked()"),    self.slotIVISCK)

        # initialize Widgets
        status = self.model.getFluidVelocityStatus()
        if status == "on":
            self.checkBoxIVISV1.setChecked(True)
        else:
            self.checkBoxIVISV1.setChecked(False)

        status = self.model.getParticlesVelocityStatus()
        if status == "on":
            self.checkBoxIVISV2.setChecked(True)
        else:
            self.checkBoxIVISV2.setChecked(False)

        status = self.model.getResidentTimeStatus()
        if status == "on":
            self.checkBoxIVISTP.setChecked(True)
        else:
            self.checkBoxIVISTP.setChecked(False)

        status = self.model.getParticleDiameterStatus()
        if status == "on":
            self.checkBoxIVISDM.setChecked(True)
        else:
            self.checkBoxIVISDM.setChecked(False)

        status = self.model.getParticleTemperatureStatus()
        if status == "on":
            self.checkBoxIVISTE.setChecked(True)
        else:
            self.checkBoxIVISTE.setChecked(False)

        status = self.model.getParticleMassStatus()
        if status == "on":
            self.checkBoxIVISMP.setChecked(True)
        else:
            self.checkBoxIVISMP.setChecked(False)

        # FIXME
        # check if coal model is activated
##         coalThermoChModel = CoalThermoChemistry.CoalThermoChemistryModel("dp_FCP", self.case)
##         coals = coalThermoChModel.getCoals()
##         CoalsNumber = coals.getNumber()
##         if CoalsNumber == 0:
##             self.lineEditIVISDK.setDisabled(True)
##             self.checkBoxIVISDK.setDisabled(True)
##             self.lineEditIVISCH.setDisabled(True)
##             self.checkBoxIVISCH.setDisabled(True)
##             self.lineEditIVISCK.setDisabled(True)
##             self.checkBoxIVISCK.setDisabled(True)

        status = self.model.getCoalParticleDiameterStatus()
        if status == "on":
            self.checkBoxIVISDK.setChecked(True)
        else:
            self.checkBoxIVISDK.setChecked(False)

        status = self.model.getCoalParticleMassStatus()
        if status == "on":
            self.checkBoxIVISCH.setChecked(True)
        else:
            self.checkBoxIVISCH.setChecked(False)

        status = self.model.getCokeParticleMassStatus()
        if status == "on":
            self.checkBoxIVISCK.setChecked(True)
        else:
            self.checkBoxIVISCK.setChecked(False)

        self.case.undoStartGlobal()


    @pyqtSignature("")
    def slotIVISV1(self):
        """
        Input IVISV1.
        """
        if self.checkBoxIVISV1.isChecked():
            self.model.setFluidVelocityStatus("on")
        else:
            self.model.setFluidVelocityStatus("off")


    @pyqtSignature("")
    def slotIVISV2(self):
        """
        Input IVISV2.
        """
        if self.checkBoxIVISV2.isChecked():
            self.model.setParticlesVelocityStatus("on")
        else:
            self.model.setParticlesVelocityStatus("off")


    @pyqtSignature("")
    def slotIVISTP(self):
        """
        Input IVISTP.
        """
        if self.checkBoxIVISTP.isChecked():
            self.model.setResidentTimeStatus("on")
        else:
            self.model.setResidentTimeStatus("off")


    @pyqtSignature("")
    def slotIVISDM(self):
        """
        Input IVISDM.
        """
        if self.checkBoxIVISDM.isChecked():
            self.model.setParticleDiameterStatus("on")
        else:
            self.model.setParticleDiameterStatus("off")


    @pyqtSignature("")
    def slotIVISTE(self):
        """
        Input IVISTE.
        """
        if self.checkBoxIVISTE.isChecked():
            self.model.setParticleTemperatureStatus("on")
        else:
            self.model.setParticleTemperatureStatus("off")


    @pyqtSignature("")
    def slotIVISMP(self):
        """
        Input IVISMP.
        """
        if self.checkBoxIVISMP.isChecked():
            self.model.setParticleMassStatus("on")
        else:
            self.model.setParticleMassStatus("off")


    @pyqtSignature("")
    def slotIVISDK(self):
        """
        Input IVISDK.
        """
        if self.checkBoxIVISDK.isChecked():
            self.model.setCoalParticleDiameterStatus("on")
        else:
            self.model.setCoalParticleDiameterStatus("off")


    @pyqtSignature("")
    def slotIVISCH(self):
        """
        Input IVISCH.
        """
        if self.checkBoxIVISCH.isChecked():
            self.model.setCoalParticleMassStatus("on")
        else:
            self.model.setCoalParticleMassStatus("off")


    @pyqtSignature("")
    def slotIVISCK(self):
        """
        Input IVISCK.
        """
        if self.checkBoxIVISCK.isChecked():
            self.model.setCokeParticleMassStatus("on")
        else:
            self.model.setCokeParticleMassStatus("off")


    def tr(self, text):
        """
        Translation
        """
        return text


#-------------------------------------------------------------------------------
# Testing part
#-------------------------------------------------------------------------------


if __name__ == "__main__":
    pass


#-------------------------------------------------------------------------------
# End
#-------------------------------------------------------------------------------
