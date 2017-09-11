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
from .dialogs import WMLModelDetail, WMLModelDownload, WMLModelPublishForm, WMLModelsList, WMLServices

@PixieApp
@Logger()
class WMLPixieApp(WMLServices, WMLModelsList, WMLModelDetail, WMLModelDownload, WMLModelPublishForm):
    def getDialogOptions(self):
        return {
            'title': 'Loading WMLPixieApp'
        }

    def pdButtonClicked(self, btnid):
        self.debug('WMLPixieApp.pdButtonClicked: {}'.format(btnid))
        self.action = btnid
        if btnid in ['downloadservice', 'publishservice', 'gotomodels', 'modelerror']:
            self.view = 'modelslist'
        elif btnid in ['gotoservices', 'serviceerror']:
            self.view = 'mlservices'
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
        
    @route(view="modelpublishform")
    def publishModelFormScreen(self):
        return '<div pd_widget="WMLModelPublishForm" style="height:100%"></div>'
        
    @route(view="modelslist")
    def listModelsScreen(self):
        return '<div pd_widget="WMLModelsList" style="height:100%"></div>'
        
    @route(view="mlservices")
    def mlServicesScreen(self):
        return '<div pd_widget="WMLServices" style="height:100%"></div>'
        
    @route()
    def startScreen(self):
        self._addHTMLTemplate('dialog.html')
