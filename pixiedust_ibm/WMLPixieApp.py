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
            'title': 'Loading WMLPixieApp',
            'hideHeader': 'true'
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
            self.view = 'WMLModelsList'
        elif btnid in ['gotoservices', 'serviceerror']:
            self.view = 'WMLServices'
        elif btnid in ['gotomodels', 'modelerror']:
            self.view = 'WMLModelsList'
        elif btnid == 'gotodetails':
            self.view = 'WMLModelDetail'
        elif btnid == 'gotoform':
            self.view = 'WMLModelForm'
        elif btnid == 'initdownload':
            self.view = 'WMLModelDownload'
        elif btnid == 'initpublish':
            self.view = 'WMLModelPublish'
            pass

    @route(view="*")
    def modelPublishView(self, view):
        return '<div pd_widget="{{view}}" style="height:100%"></div>'
        
    @route()
    def appshellView(self):
        self._addHTMLTemplate('appshell.html')
        # self._addHTMLTemplateString(appshell)
