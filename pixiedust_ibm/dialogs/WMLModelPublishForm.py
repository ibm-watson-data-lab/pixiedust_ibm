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
from ..components import PDButton
from . import WMLMessage

@Logger()
class WMLModelPublishForm(PDButton, WMLMessage):
    @route(widget="WMLModelPublishForm")
    def wmlModelPublishForm(self):
        wrapperid = 'pd_app' + self.getPrefix()
        if not hasattr(self, 'currentservice') or not self.currentservice:
            self.renderMessage(message='An ML service is required', targetid=wrapperid, btnid='serviceerror')
        if not hasattr(self, 'currentmodel') or not self.currentmodel:
            self.renderMessage(message='A Model is required', targetid=wrapperid, btnid='modelerror')
        else:
            PDButton.__init__(self)
            self.initWatsonML(self.currentservice['credentials'])
            # form = [{'id': 'fieldid', 'label': 'fieldname', 'required': True, 'type': 'select', 'options': [('optid', 'optlabel')], 'placeholder': 'select a value', 'value':'default value'}]
            self._pdform = [{
                'type': 'text',
                'id':  'modelname' + self.getPrefix(),
                'label': 'Name',
                'required': True,
                'placeholder': 'Enter a model name',
                'value': self.currentmodel.name
            }, {
                'type': 'textarea',
                'id':  'modeldesc' + self.getPrefix(),
                'label': 'Description',
                'placeholder': 'Type your description here'
            # }, {
            #     'type': 'text',
            #     'id':  'servicename' + self.getPrefix(),
            #     'label': 'Machine Learning Service',
            #     'required': True,
            #     'disabled': True,
            #     'value': self.currentservice['name']
            }]
            return """
<div class="pd_title">Publish model <code>{}</code> to <strong>{}</strong></div>
<div class="pd_main pd_publishmodelform">
    <div pd_widget="pdForm"></div>
</div>
<div class="pd_buttons">
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='gotomodels'
self._pdbutton['label']='Return to Models'
self._pdbutton['classes']='btn btn-default btn-primary btn-back'
self._pdbutton['targetid']='{}'
        </pd_scipt>
    </div>
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='initpublish'
self._pdbutton['label']='Publish'
self._pdbutton['classes']='btn btn-default btn-primary btn-ok'
self._pdbutton['targetid']='{}'
self._pdbutton['attributes']='data-dismiss="modal" disabled="disabled"'
        </pd_scipt>
    </div>
</div>
""".format(self.currentmodel.name, self.currentservice['name'], wrapperid, wrapperid)
