class SimpleFilter(object):

    def __init__(self, context):
        self._context = context
    
    def include(self, log_entry):
        return True