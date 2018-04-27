import abc

from ... import IO

_MUST_IMPLEMENT = 'This method must be implemented'


class IOWrite(IO):
    '''Base class writing Field constructs to a dataset.

    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write(self, *args, **kwargs):
        '''Write fields to a netCDF file.
        '''
        raise NotImplementedError(_MUST_IMPLEMENT)
#--- End: class

