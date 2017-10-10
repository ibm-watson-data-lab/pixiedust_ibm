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
class WMLModelDetail(WMLMessage):
    @route(widget="WMLModelDetail")
    def wmlModelDetail(self):
        wrapperid = 'pd_app' + self.getPrefix()
        if not hasattr(self, 'currentmodel') or not self.currentmodel:
            self.renderMessage(message='A Model is required', targetid=wrapperid, btnid='modelerror')
        else:
            PDButton.__init__(self)
            props = [item for item in self.currentmodel.meta.available_props() if (item != "inputDataSchema" and item !="trainingDataSchema")]
            rows = []
            for prop in props:
                rows.append({ 'prop': prop, 'value': self.currentmodel.meta.prop(prop) })
            self._pdtable = {
                'columns': ['prop', 'value'],
                'rows': rows,
                'header': False
            }
            return """
<div class="pd_title">Details of Model: {}</div>
<div class="pd_main pd_modeldetail">
    <div pd_widget="pdTable"></div>
</div>
<div class="pd_buttons">
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='gotomodels'
self._pdbutton['label']='Return to Models'
self._pdbutton['classes']='btn btn-default btn-primary btn-back'
self._pdbutton['targetid']='{}'
        </pd_script>
    </div>
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='gotoform'
self._pdbutton['label']='Download this Model'
self._pdbutton['classes']='btn btn-default btn-primary btn-download'
self._pdbutton['targetid']='{}'
        </pd_script>
    </div>
</div>
""".format(self.currentmodel.name, wrapperid, wrapperid)
