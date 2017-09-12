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
from ..components import PDButton, PDTable
from . import WMLMessage
from ..WMLUtil import WMLUtil

@Logger()
class WMLModelsList(PDButton, PDTable, WMLMessage):
    def initWatsonML(self, credentials):
        if credentials is None:
            return "You must provide credentials to your Watson ML Service"
        self.ml_repository_client = MLRepositoryClient(credentials['url'])
        self.ml_repository_client.authorize(credentials['username'], credentials['password'])

    
    def pdActionClicked(self, action, rowid):
        self.debug('pdActionClicked: {}, {}'.format(action, rowid))
        self.currentmodel = self.ml_repository_client.models.get(rowid)
        if action == 'Publish' or action == 'Download':
            self.view = 'modelform'
        elif action == 'Detail':
            self.view = 'modeldetail'
    
    @route(widget="WMLModelsList")
    def wmlModelsList(self):
        wrapperid = 'pd_app' + self.getPrefix()
        if not hasattr(self, 'currentservice') or not self.currentservice:
            self.renderMessage(message='An ML service is required', targetid=wrapperid, btnid='serviceerror')
        else:
            PDButton.__init__(self)
            actions = []
            rows = []
            message = None

            try:
                self.ml_repository_client = WMLUtil.getMLRepositoryClient(self.currentservice['credentials'])
            except Exception as e:
                message = str(e)
            
            if message is not None:
                self.renderMessage(message=message)
            else:
                if self.serviceaction == 'publishservice':
                    # TODO: get notebook models
                    models = []
    #                 models = self.ml_repository_client.models.all()
                    actions = [{
                        'name': 'Publish',
                        'targetid': wrapperid
                    }]
                else:
                    models = self.ml_repository_client.models.all()
                    actions = [{
                        'name': 'Detail',
                        'targetid': wrapperid
                    }, {
                        'name': 'Download',
                        'targetid': wrapperid
                    }]

                for model in models:
                    rows.append({
                        'id': model.uid,
                        'name': model.name,
                        'type': model.meta.prop('modelType')
                    })
                
                self._pdtable = {
                    'columns': ['name', 'status', 'type'],
                    'rows': rows,
                    'actions': actions
                }
                template = """
<div class="pd_title">Models in <strong>{{ service }}</strong></div>
<div class="pd_main pd_listmodel">
    <div pd_widget="pdTable"></div>
</div>
<div class="pd_buttons">
    <button class="btn btn-default btn-cancel" data-dismiss="modal">Cancel</button>
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='gotoservices'
self._pdbutton['label']='Start Over'
self._pdbutton['classes']='btn btn-default btn-primary btn-back'
self._pdbutton['targetid']='pd_app{{ prefix }}'
        </pd_scipt>
    </div>
</div>
"""
                self._addHTMLTemplateString(template, service='notebook' if self.serviceaction == 'publishservice' else self.currentservice['name'])
