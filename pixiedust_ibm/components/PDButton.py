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
import re

@Logger()
class PDButton():
    def __init__(self):
        self._pdbutton = {
            'label': 'Button',
            'classes': 'btn btn-default',
            'attributes': 'pd_norefresh',
            'btnid': 'defaultbutton',
            'targetid': ''
        }
        
    def pdButtonRender(self, btnid='defaultbutton', label='Button', classes='btn btn-default', attributes='pd_norefresh', targetid=''):
        self._pdbutton = {
            'label': label,
            'classes': classes,
            'attributes': attributes,
            'btnid': btnid,
            'targetid': targetid
        }
        self._addHTMLTemplateString('<div pd_widget="pdButton"></div>')
    
    def pdButtonClicked(self, btnid):
        self.debug('pdButtonClicked: {}'.format(btnid))
    
    @route(widget="pdButton")
    def pdButton(self):
        label = self._pdbutton['label']
        classes = self._pdbutton['classes']
        attributes = self._pdbutton['attributes']
        btnid = re.sub(r'\W+', '', self._pdbutton['btnid']).lower()
        targetid =  '' if len(self._pdbutton['targetid']) == 0 else '<target pd_target="' + str(self._pdbutton['targetid']) + '"/>'

        return """
<button class="{}" pd_script="self.pdButtonClicked('{}')" {}>{} {}</button>
""".format(classes, btnid, attributes, label, targetid)
