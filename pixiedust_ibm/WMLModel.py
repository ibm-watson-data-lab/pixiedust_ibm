from WMLPixieApp import WMLPixieApp
import os

class WMLModel(object):
    def __init__(self, credentials=None):
        if credentials is None:
            credentials = {}

        if not hasattr(credentials, 'project_id'):
            pid = os.environ.get('PROJECT_ID', None)
            if pid:
                credentials['project_id'] = pid

        if not hasattr(credentials, 'access_token'):
            pat = os.environ.get('PROJECT_ACCESS_TOKEN', None)
            if pat:
                credentials['access_token'] = pat

        WMLPixieApp().run(credentials, runInDialog='true')

class downloadWMLModel(object):
    def __init__(self, modelName, fromService, newName, credentials=None):
        # TODO: implement direct download (minus UI)
        print 'not yet implemented'

class publishWMLModel(object):
    def __init__(self, modelName, toService, newName, credentials=None):
        # TODO: implemnt direct publish (minus UI)
        print 'not yet implemented'
