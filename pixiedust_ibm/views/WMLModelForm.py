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
from ..WMLUtil import WMLUtil

@Logger()
class WMLModelForm(WMLMessage):
    def publishForm(self):
        return [{
                'type': 'text',
                'id':  'modelname' + self.getPrefix(),
                'label': 'Model Name',
                'required': True,
                'placeholder': 'Enter a name for the model',
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
        pass
        
    def downloadForm(self):
        return [{
                'type': 'text',
                'id':  'modelname' + self.getPrefix(),
                'label': 'Variable Name',
                'required': True,
                'placeholder': 'Enter a name for the variable',
                'value': 'mlModel'
            # }, {
            #     'type': 'text',
            #     'id':  'servicename' + self.getPrefix(),
            #     'label': 'Machine Learning Service',
            #     'required': True,
            #     'disabled': True,
            #     'value': self.currentservice['name']
            }]
        pass
    
    def pdFormUpdate(self, fieldid, fieldvalue):
        self.debug('WMLModelForm.pdFormUpdate: {}, {}'.format(fieldid, fieldvalue))
        self.modelformfields[fieldid] = fieldvalue
    
    @route(widget="WMLModelForm")
    def wmlModelForm(self):
        wrapperid = 'pd_app' + self.getPrefix()
        self.modelformfields = {}
        if not hasattr(self, 'currentservice') or not self.currentservice:
            self.renderMessage(message='A machine learning service is required', targetid=wrapperid, btnid='serviceerror')
        if not hasattr(self, 'currentmodel') or not self.currentmodel:
            self.renderMessage(message='A Model is required', targetid=wrapperid, btnid='modelerror')
        else:
            PDButton.__init__(self)
            message = None

            try:
                self.ml_repository_client = WMLUtil.getMLRepositoryClient(self.currentservice['credentials'])
            except Exception as e:
                message = str(e)
            
            if message is not None:
                self.renderMessage(message=message)
            else:
                if self.serviceaction == 'publishservice':
                    self._pdform = self.publishForm()
                    title = 'Publish model <code>{}</code> to <strong>{}</strong>'.format(self.currentmodel.name, self.currentservice['name'])
                    btnid = 'initpublish'
                    btnlabel = 'Publish'
                    btnattr = ''
                else:
                    self._pdform = self.downloadForm()
                    title = 'Download model <code>{}</code> from <strong>{}</strong>'.format(self.currentmodel.name, self.currentservice['name'])
                    btnid = 'initdownload'
                    btnlabel = 'Download'
                    btnattr = ''

                return """
<div class="pd_title">{title}</div>
<div class="pd_main pd_modelform">
    <div pd_widget="pdForm"></div>
</div>
<div class="pd_buttons">
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='gotomodels'
self._pdbutton['label']='Return to Models'
self._pdbutton['classes']='btn btn-default btn-primary btn-back'
self._pdbutton['targetid']='{target}'
        </pd_scipt>
    </div>
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='{btnid}'
self._pdbutton['label']='{label}'
self._pdbutton['classes']='btn btn-default btn-primary btn-ok'
self._pdbutton['targetid']='{target}'
self._pdbutton['attributes']='{attr}'
        </pd_scipt>
    </div>
</div>
""".format(title=title, target=wrapperid, btnid=btnid, label=btnlabel, attr=btnattr)
