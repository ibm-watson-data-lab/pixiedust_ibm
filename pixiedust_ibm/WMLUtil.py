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
        from project_lib import Project
        proj_credentials = WMLUtil.checkCredentials(credentials)
        currentproject = Project(None, project_id = proj_credentials['project_id'], project_access_token = proj_credentials['access_token'])
        compute_entities = currentproject.get_metadata()['entity']['compute']
        ml_services = [entity for entity in compute_entities if entity['type'] == 'machine_learning']
        return ml_services

    @staticmethod
    def getMLRepositoryClient(credentials):
        ml_repository_client = None
        if credentials is not None:
            from repository.mlrepositoryclient import MLRepositoryClient
            ml_repository_client = MLRepositoryClient(credentials['url'])
            ml_repository_client.authorize(credentials['username'], credentials['password'])
        return ml_repository_client
