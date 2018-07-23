
class Repository:
    def create_snippet(self, snippet_id):
        raise NotImplementedError()

    def get_snippet(self, snippet_id):
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()
