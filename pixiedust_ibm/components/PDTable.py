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

@Logger()
class PDTable():
    def __init__(self):
        self._pdtable = {
            'columns': [],
            'rows': [],
            'actions': [],
            'header': True
        }
        
    def pdTableRender(self, columns=[], rows=[], actions=[], header=True):
        self._pdtable = {
            'columns': columns,
            'rows': rows,
            'actions': actions,
            'header': header
        }
        self._addHTMLTemplateString('<div pd_widget="pdTable"></div>')
    
    def pdActionClicked(self, action, row):
        self.debug('pdActionClicked: {}, {}'.format(action, row))
    
    @route(widget="pdTable")
    def pdTable(self):
        return """
<table>
    {% if this._pdtable.header is not defined or this._pdtable.header %}
    <thead>
        <tr>
        {% for col in this._pdtable.columns %}
            <th>{{ col }}</th>
        {% endfor %}
        {% if this._pdtable.actions|length > 0 %}
            <th>Action{% if this._pdtable.actions|length > 1 %}s{% endif %}</th>
        {% endif %}
        </tr>
    </thead>
    {% endif %}
    <tbody>
    {% for row in this._pdtable.rows %}
        <tr>
        {% for col in this._pdtable.columns %}
            <td>{% if row[col] is defined %}{{ row[col] }}{% endif %}</td>
        {% endfor %}
        {% if this._pdtable.actions|length > 0 %}
            <td>
                {% if this._pdtable.actions|length > 1 %}
                <div class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"> &#8943; </a>
                    <ul class="dropdown-menu">
                        {% for action in this._pdtable.actions %}
                        <li>
                            <a href="#"> {{ action['name'] }}
                                {% if action['targetid'] is defined %}
                                <target pd_target="{{ action['targetid'] }}"/>
                                {% endif %}
                                <pd_script>self.pdActionClicked("{{ action['name'] }}", "{% if row['id'] is defined %}{{ row['id'] }}{% else %}{{ row['name'] }}{% endif %}")</pd_script>
                            </a>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
                {% else %}
                <a href="#"> {{ this._pdtable.actions[0]['name'] }}
                    {% if this._pdtable.actions[0]['targetid'] is defined %}
                    <target pd_target="{{ this._pdtable.actions[0]['targetid'] }}"/>
                    {% endif %}
                    <pd_script>self.pdActionClicked("{{ this._pdtable.actions[0]['name'] }}", "{% if row['id'] is defined %}{{ row['id'] }}{% else %}{{ row['name'] }}{% endif %}")</pd_script>
                </a>
                {% endif %}
            </td>
        {% endif %}
        </tr>
    {% endfor %}
    </tbody>
</table>
"""
