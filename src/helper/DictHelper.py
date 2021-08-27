class DictHelper:
    def get_or_def(self, source: dict, name, default):
        return source.get(name, default)

