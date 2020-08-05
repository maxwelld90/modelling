class SimpleFilter(object):

    def __init__(self, context, document_count=100):
        self._context = context
    
    def include(self, log_entry):
        return True