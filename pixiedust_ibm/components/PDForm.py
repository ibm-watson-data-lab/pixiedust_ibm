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
class PDForm():
    def __init__(self):
        self._pdform = []
        
    def pdFormRender(self, formfields=[]):
        self._pdform = formfields
        self._addHTMLTemplateString('<div pd_widget="pdForm"></div>')
    
    def pdFormUpdate(self, field, value):
        self.debug('pdFormUpdate: {}, {}'.format(field, value))
    
    @route(widget="pdForm")
    def pdForm(self):
        # form = [{'id': 'fieldid', 'label': 'fieldname', 'required': True, 'type': 'select', 'options': [('optid', 'optlabel')], 'placeholder': 'select a value', 'value':'default value', 'disabled': False}]
        return """
<script>
    function onform{{ prefix }}(input) {
        $(input).trigger('click')
    }
</script>
{% for formfield in this._pdform %}
    <div class="formField">
        <label for="{{ formfield['id'] }}" class="formLabel">{{ formfield['label'] }}{% if formfield['required'] is defined and formfield['required'] %}<span class="redText">*</span>{% endif %}</label>
        {% if formfield['type'] == 'select' %}
        <select id="{{ formfield['id'] }}" pd_script="self.pdFormUpdate('{{ formfield['id'] }}', '$val({{ formfield['id'] }})')" pd_norefresh
            {% if formfield['required'] is defined and formfield['required'] %}required{% endif %}
            {% if formfield['disabled'] is defined and formfield['disabled'] %}disabled="disabled"{% endif %}>
            <option selected="selected" disabled>{{ formfield['placeholder'] }}</option>
            {% for option in formfield['options'] %}
            <option value="{{ option[0] }}">{{ option[1] }}</option>
            {% endfor %}
        </select>
        {% elif formfield['type'] == 'textarea' %}
        <textarea id="{{ formfield['id'] }}" placeholder="{{ formfield['placeholder'] }}"
            pd_script="self.pdFormUpdate('{{ formfield['id'] }}', '$val({{ formfield['id'] }})')" pd_norefresh
            onchange="onform{{ prefix }}(this)"
            {% if formfield['required'] is defined and formfield['required'] %}required{% endif %}
            {% if formfield['disabled'] is defined and formfield['disabled'] %}disabled="disabled"{% endif %}></textarea>
        {% else %}
        <input id="{{ formfield['id'] }}" value="{{ formfield['value'] }}" type="{{ formfield['type'] }}" placeholder="{{ formfield['placeholder'] }}"
            pd_script="self.pdFormUpdate('{{ formfield['id'] }}', '$val({{ formfield['id'] }})')" pd_norefresh
            onchange="onform{{ prefix }}(this)"
            {% if formfield['required'] is defined and formfield['required'] %}required{% endif %}
            {% if formfield['disabled'] is defined and formfield['disabled'] %}disabled="disabled"{% endif %}>
        {% endif %}
    </div>
{% endfor %}
"""
