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

@Logger()
class WMLMessage(PDButton):
    def renderMessage(self, title='Attention', message='Action failed', targetid='', btnid='msgbackbtn'):
        self._wmlmessage = {
            'title': title,
            'message': message,
            'targetid': targetid,
            'btnid': btnid
        }
        self._addHTMLTemplateString('<div pd_widget="WMLMessage"></div>')

    @route(widget="WMLMessage")
    def wmlMessage(self):
        backtarget = ''
        if 'targetid' in self._wmlmessage and len(self._wmlmessage['targetid']) > 0:
            PDButton.__init__(self)
            backtarget = """
    <div pd_widget="pdButton">
        <pd_script>
self._pdbutton['btnid']='{}'
self._pdbutton['label']='Back'
self._pdbutton['classes']='btn btn-default btn-primary btn-msg'
self._pdbutton['targetid']='{}'
        </pd_scipt>
    </div>
""".format(self._wmlmessage['btnid'], self._wmlmessage['targetid'])
    
        return """
<div class="pd_title">{}</div>
<div class="pd_main pd_wmlmessage">
    <h4>{}</h4>
</div>
<div class="pd_buttons">
    <button class="btn btn-default btn-cancel" data-dismiss="modal">Cancel</button>
    {}
</div>
""".format(self._wmlmessage['title'], self._wmlmessage['message'], backtarget)
