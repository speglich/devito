from devito.tools import Singleton

__all__ = []


class Pool(object, metaclass=Singleton):

    @property
    def ntotal(self):
        """
        Total number of resources in this pool.
        """
        raise NotImplementedError

    def navail(self):
        """
        Number of currently available resources.
        """
        raise NotImplementedError

    def acquire(self):
        """
        Acquire a new resource.
        """
        raise NotImplementedError

    def release(self, rid):
        """
        Release the resource with the given `rid`.
        """
        raise NotImplementedError


class DevicePool(Pool):
    pass
