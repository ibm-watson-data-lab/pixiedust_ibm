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
from pixiedust.utils.shellAccess import ShellAccess
from pixiedust.utils import Logger
from . import WMLMessage

@Logger()
class WMLModelPublish(WMLMessage):
    @route(widget="WMLModelPublish")
    def wmlModelPublish(self):
        wrapperid = 'pd_app' + self.getPrefix()
        if not hasattr(self, 'currentmodel') or not self.currentmodel:
            self.renderMessage(message='A Model is required', targetid=wrapperid, btnid='modelerror')
        if not hasattr(self, 'modelformfields'):
            self.renderMessage(message='Missing required fields', targetid=wrapperid, btnid='modelerror')
        else:
            from repository.mlrepositoryartifact import MLRepositoryArtifact
            self.debug('WMLModelPublish.modelformfields: ' + str(self.modelformfields))
            message = None

            try:
                self.ml_repository_client = WMLUtil.getMLRepositoryClient(self.currentservice['credentials'])
                modelnamefield = 'modelname' + self.getPrefix()
                modeldescfield = 'modeldesc' + self.getPrefix()
                newname = self.modelformfields[modelnamefield] if modelnamefield in self.modelformfields and self.modelformfields[modelnamefield] else 'mlModel'
                newdesc = self.modelformfields[modeldescfield] if modeldescfield in self.modelformfields and self.modelformfields[modeldescfield] else ''

                title = 'Publish model <code>' + self.currentmodel.name + '</code>'
                message = 'Model successfully published as <code>{}</code>.'.format(newname)
                model = ShellAccess[self.currentmodel.name]

                if len(newdesc):
                    from repository.mlrepository import MetaNames, MetaProps
                    artifact = MLRepositoryArtifact(model, name=newname, meta_props=MetaProps({ MetaNames.DESCRIPTION: newdesc }))
                else:
                    artifact = MLRepositoryArtifact(model, name=newname)

                self.ml_repository_client.models.save(artifact)

                self.renderMessage(title=title, message=message, targetid=wrapperid, btnid='gotoservices')
            except Exception as e:
                self.renderMessage(message=str(e))
