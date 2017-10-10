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

from pixiedust.display.app import route
from pixiedust.utils import Logger
from pixiedust.utils.shellAccess import ShellAccess
from . import WMLMessage

@Logger()
class WMLModelDownload(WMLMessage):
    @route(widget="WMLModelDownload")
    def wmlModelDownload(self):
        wrapperid = 'pd_app' + self.getPrefix()
        if not hasattr(self, 'currentmodel') or not self.currentmodel:
            self.renderMessage(message='A Model is required', targetid=wrapperid, btnid='modelerror')
        if not hasattr(self, 'modelformfields'):
            self.renderMessage(message='Missing required fields', targetid=wrapperid, btnid='modelerror')
        else:
            self.debug('WMLModelDownload.modelformfields: ' + str(self.modelformfields))
            modelnamefield = 'modelname' + self.getPrefix()
            newname = self.modelformfields[modelnamefield] if modelnamefield in self.modelformfields and self.modelformfields[modelnamefield] else 'mlModel'
            
            ShellAccess[newname] = self.currentmodel.model_instance()
            title = 'Download model: ' + self.currentmodel.name
            message = 'Model successfully downloaded and stored in variable: {}'.format(newname)
            
            self.renderMessage(title=title, message=message, targetid=wrapperid, btnid='gotoservices')
