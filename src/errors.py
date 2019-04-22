class GetTemplateError(Exception):
    def __init__(self, name):
        self.value = name
    def __str__(self):
        return repr(self.value)

class InitialTemplateEngineError(Exception):
    def __init__(self, name):
        self.value = name
    def __str__(self):
        return repr(self.value)

class TemplateRenderingError(Exception):
    def __init__(self, name):
        self.value = name
    def __str__(self):
        return repr(self.value)