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

from .WMLPixieApp import WMLPixieApp
from .WMLUtil import WMLUtil
from repository.mlrepositoryartifact import MLRepositoryArtifact

class WMLModel(object):
    def __init__(self, credentials=None):
        cred = WMLUtil.checkCredentials(credentials)
        WMLPixieApp().run(cred, runInDialog='true')

class listWMLModels(object):
    def __new__(cls, credentials=None):
        allservices = []
        try:
            allservices = WMLUtil.getMLServices(credentials)
        except Exception as e:
            print(str(e))

        if len(allservices) == 0:
            print('No services found')
        else:
            for service in allservices:
                cred = service['credentials']
                servicemodels = []
                try:
                    client = WMLUtil.getMLRepositoryClient(cred)
                    servicemodels = client.models.all()
                    print('Service: {} ({})'.format(service['name'], service['guid']))
                except Exception as e:
                    print(str(e))

                if len(servicemodels) == 0:
                    print('  - No models available')
                else:
                    for model in servicemodels:
                        print('  - Model: {} ({})'.format(model.name, model.uid))

class downloadWMLModel(object):
    def __new__(cls, modelNameOrUID, serviceNameOrGUID=None, credentials=None):
        possiblemodels = []
        allservices = []
        try:
            allservices = WMLUtil.getMLServices(credentials)
        except Exception as e:
            print(str(e))

        if len(allservices):
            services = allservices if serviceNameOrGUID is None else [s for s in allservices if s['name'] == serviceNameOrGUID or s['guid'] == serviceNameOrGUID]
            if len(services) == 0:
                print('No services found')
            for service in services:
                try:
                    cred = service['credentials']
                    client = WMLUtil.getMLRepositoryClient(cred)
                    servicemodels = client.models.all()
                    possiblemodels += [m for m in servicemodels if m.name == modelNameOrUID or m.uid == modelNameOrUID]
                except Exception as e:
                    print(str(e))

        if len(possiblemodels):
            # using the first model only
            model = possiblemodels[0]
            return model.model_instance()
        else:
            print('No models found with the name "{}"'.format(modelNameOrUID))

class publishWMLModel(object):
    def __new__(cls, model, modelName, serviceNameOrGUID=None, credentials=None):
        savedmodel = None
        service = None
        allservices = []
        try:
            allservices = WMLUtil.getMLServices(credentials)
        except Exception as e:
            print(str(e))

        if len(allservices):
            services = allservices if serviceNameOrGUID is None else [s for s in allservices if s['name'] == serviceNameOrGUID or s['guid'] == serviceNameOrGUID]
            if len(services):
                try:
                    service = services[0]
                    cred = service['credentials']
                    client = WMLUtil.getMLRepositoryClient(cred)
                    artifact = MLRepositoryArtifact(model, name=modelName)
                    savedartifact = client.models.save(artifact)
                    savedmodel = savedartifact.model_instance()
                except Exception as e:
                    print(str(e))
            else:
                print('No services found')
        if savedmodel is not None and service is not None:
            print('Model {} saved in service "{}"'.format(savedmodel.name if hasattr(savedmodel, 'name') else '', service['name']))
            return savedmodel
        else:
            print('Model could not be saved')
