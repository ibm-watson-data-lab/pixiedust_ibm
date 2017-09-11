# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2017
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------

from pixiedust.display.app import *
from pixiedust.utils import Logger
from .views import WMLModelDetail, WMLModelDownload, WMLModelForm, WMLModelsList, WMLServices

@PixieApp
@Logger()
class WMLPixieApp(WMLServices, WMLModelsList, WMLModelDetail, WMLModelForm, WMLModelDownload):
    def getDialogOptions(self):
        return {
            'title': 'Loading WMLPixieApp'
        }
    
    def pdFormUpdate(self, fieldid, fieldvalue):
        self.debug('WMLServices.pdFormUpdate: {}, {}'.format(fieldid, fieldvalue))
        if (fieldid == 'mlservice' + self.getPrefix()):
            if fieldvalue:
                selectedservice = [ml for ml in self.ml_services if ml['guid'] == fieldvalue]
                self.currentservice = selectedservice[0]
            else:
                self.currentservice = None
        elif (fieldid == 'variablename' + self.getPrefix()) or (fieldid == 'modelname' + self.getPrefix()):
            self.newmodelname = fieldvalue

    def pdButtonClicked(self, btnid):
        self.debug('WMLPixieApp.pdButtonClicked: {}'.format(btnid))
        if btnid in ['downloadservice', 'publishservice']:
            self.serviceaction = btnid
            self.view = 'modelslist'
        elif btnid in ['gotoservices', 'serviceerror']:
            self.view = 'mlservices'
        elif btnid in ['gotomodels', 'modelerror']:
            self.view = 'modelslist'
        elif btnid == 'gotodetails':
            self.view = 'modeldetail'
        elif btnid == 'gotoform':
            self.view = 'modelform'
        elif btnid == 'initdownload':
            self.view = 'modeldownload'
#         elif btnid == 'initpublish':
#             # TODO
#             pass


    @route(view="modeldownload")
    def modelDownloadScreen(self):
        return '<div pd_widget="WMLModelDownload" style="height:100%"></div>'
        
    @route(view="modeldetail")
    def modelDetailScreen(self):
        return '<div pd_widget="WMLModelDetail" style="height:100%"></div>'
        
    @route(view="modelform")
    def modelFormScreen(self):
        return '<div pd_widget="WMLModelForm" style="height:100%"></div>'
        
    @route(view="modelslist")
    def listModelsScreen(self):
        return '<div pd_widget="WMLModelsList" style="height:100%"></div>'
        
    @route(view="mlservices")
    def mlServicesScreen(self):
        return '<div pd_widget="WMLServices" style="height:100%"></div>'
        
    @route()
    def startScreen(self):
        self._addHTMLTemplate('appshell.html')
        # self._addHTMLTemplateString(appshell)
