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
from .views import WMLModelDetail, WMLModelDownload, WMLModelPublish, WMLModelForm, WMLModelsList, WMLServices

@PixieApp
@Logger()
class WMLPixieApp(WMLServices, WMLModelsList, WMLModelDetail, WMLModelForm, WMLModelDownload, WMLModelPublish):
    def getDialogOptions(self):
        return {
            'title': 'Loading WMLPixieApp'
        }
    
    def pdFormUpdate(self, fieldid, fieldvalue):
        self.debug('WMLPixieApp.pdFormUpdate: {}, {}'.format(fieldid, fieldvalue))
        if (fieldid == 'mlservice' + self.getPrefix()):
            if fieldvalue:
                selectedservice = [ml for ml in self.ml_services if ml['guid'] == fieldvalue]
                self.currentservice = selectedservice[0]
            else:
                self.currentservice = None
        else:
            self.modelformfields[fieldid] = fieldvalue

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
        elif btnid == 'initpublish':
            self.view = 'modelpublish'
            pass


    @route(view="modelpublish")
    def modelPublishView(self):
        return '<div pd_widget="WMLModelPublish" style="height:100%"></div>'
    
    @route(view="modeldownload")
    def modelDownloadView(self):
        return '<div pd_widget="WMLModelDownload" style="height:100%"></div>'
        
    @route(view="modeldetail")
    def modelDetailView(self):
        return '<div pd_widget="WMLModelDetail" style="height:100%"></div>'
        
    @route(view="modelform")
    def modelFormView(self):
        return '<div pd_widget="WMLModelForm" style="height:100%"></div>'
        
    @route(view="modelslist")
    def listModelsView(self):
        return '<div pd_widget="WMLModelsList" style="height:100%"></div>'
        
    @route(view="mlservices")
    def mlServicesView(self):
        return '<div pd_widget="WMLServices" style="height:100%"></div>'
        
    @route()
    def appshellView(self):
        self._addHTMLTemplate('appshell.html')
        # self._addHTMLTemplateString(appshell)
