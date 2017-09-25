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
from repository.mlrepositoryclient import MLRepositoryClient
from project_lib import Project

class WMLUtil:

    @staticmethod
    def checkCredentials(credentials):
        import os
        if credentials is None:
            credentials = {}
        if 'project_id' not in credentials:
            credentials['project_id'] = os.environ.get('PROJECT_ID', '')
        if 'access_token' not in credentials:
            credentials['access_token'] = os.environ.get('PROJECT_ACCESS_TOKEN', '')
        return credentials

    @staticmethod
    def getMLServices(credentials):
        proj_credentials = WMLUtil.checkCredentials(credentials)
        currentproject = Project(None, project_id = proj_credentials['project_id'], project_access_token = proj_credentials['access_token'])
        compute_entities = currentproject.get_metadata()['entity']['compute']
        ml_services = [entity for entity in compute_entities if entity['type'] == 'machine_learning']
        return ml_services

    @staticmethod
    def getMLRepositoryClient(credentials):
        ml_repository_client = None
        if credentials is not None:
            ml_repository_client = MLRepositoryClient(credentials['url'])
            ml_repository_client.authorize(credentials['username'], credentials['password'])
        return ml_repository_client
    
    @staticmethod
    def fqName(entity):
        return (entity.__module__ + '.' if hasattr(entity, '__module__') else '') + (entity.__class__.__name__ if hasattr(entity, '__class__') else '')
