from abc import ABCMeta, abstractmethod

class AbstractTransit(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def getResponse(self, stopId):
        pass
