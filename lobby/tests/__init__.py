import os


class PostMock():
    def __init__(self, fixture=''):
        self.status_code = 200
        self.content = ''
        if fixture:
            script_dir = os.path.dirname(__file__)
            f = open(os.path.join(script_dir, 'fixtures/' + fixture), 'r')
            self.content = f.read()
