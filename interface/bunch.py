class bunch:
    def __init__(self, **args):
        self.__dict__.update(args)
    def __len__(self):
        return len(self.__dict__)
    def has(self, key):
        return self.__dict__.__contains__(key)
