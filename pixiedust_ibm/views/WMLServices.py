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
from ..components import PDButton, PDForm
from . import WMLMessage
from ..WMLUtil import WMLUtil

@Logger()
class WMLServices(PDForm, WMLMessage):
    def pdFormUpdate(self, fieldid, fieldvalue):
        self.debug('WMLServices.pdFormUpdate: {}, {}'.format(fieldid, fieldvalue))
    
    @route(widget="WMLServices")
    def wmlServices(self):
        message = None
        if not hasattr(self, 'currentservice'):
            self.currentservice = None
        
        if not hasattr(self, 'ml_services') or not self.ml_services:
            entity = self.getPixieAppEntity()
            self.serviceaction = None
            message = None

            try:
                self.ml_services = WMLUtil.getMLServices(entity)
            except Exception as e:
                message = str(e)

        if message is not None:
            self.renderMessage(message=message)
        else:
            PDButton.__init__(self)
            PDForm.__init__(self)
            return """
<div class="pd_title">Select a machine learning service to work with</div>
<div class="pd_main pd_mlservices">
    <div pd_widget="pdForm">
        <pd_script>
self._pdform = [{
    'type': 'select',
    'id':  'mlservice' + self.getPrefix(),
    'label': 'Machine Learning Service',
    'required': True,
    'options': [(service['guid'], service['name']) for service in self.ml_services],
{% if this.currentservice is defined and this.currentservice['guid'] is defined %}'selected': self.currentservice['guid'],{% endif %}
    'placeholder': 'Select a service'
}]
        </pd_script>
    </div>
</div>
<div class="pd_buttons">
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='downloadservice'
self._pdbutton['label']='Download from Service'
self._pdbutton['classes']='btn btn-default btn-primary btn-download'
self._pdbutton['targetid']='pd_app' + self.getPrefix()
{% if this.ml_services|length == 0 %}self._pdbutton['attributes']='disabled="disabled"'{% endif %}
        </pd_script>
    </div>
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='publishservice'
self._pdbutton['label']='Publish to Service'
self._pdbutton['classes']='btn btn-default btn-primary btn-publish'
self._pdbutton['targetid']='pd_app' + self.getPrefix()
{% if this.ml_services|length == 0 %}self._pdbutton['attributes']='disabled="disabled"'{% endif %}
        </pd_script>
    </div>
</div>
"""
