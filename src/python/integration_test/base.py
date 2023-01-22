class BaseIntegrationTest:
    @classmethod
    def name(cls):
        return cls.__name__

    def run(self, args):
        self.__implementation__(args)

    def __implementation__(self, args):
        raise "Not implemented!"
