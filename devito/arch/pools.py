from cached_property import cached_property

from devito.arch.archinfo import get_gpu_info
from devito.tools import Singleton

__all__ = ['device_pool']

FREE = 0
ACQUIRED = 1


class Pool(object, metaclass=Singleton):

    def __repr__(self):
        return "%s[ntotal=%d, navail=%d]" % (self.__class__.__name__,
                                             self.ntotal, self.navail)

    @cached_property
    def ntotal(self):
        """
        Total number of resources in this pool.
        """
        raise NotImplementedError

    @property
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

    @cached_property
    def info(self):
        return get_gpu_info()

    @cached_property
    def state(self):
        return [FREE]*self.info['ncards']

    @cached_property
    def ntotal(self):
        return len(self.state)

    @property
    def navail(self):
        return self.state.count(FREE)

    def acquire(self, rid=None, busy_wait=True):
        if rid is None:
            while True:
                try:
                    rid = self.state.index(FREE)
                    self.state[rid] = ACQUIRED
                    return rid
                except ValueError:
                    if busy_wait:
                        continue
                    raise ValueError("Unable to acquire device")
        else:
            while True:
                if self.state[rid] == ACQUIRED:
                    if busy_wait:
                        continue
                    else:
                        raise ValueError("Unable to acquire device")
                else:
                    self.state[rid] = ACQUIRED
                    return rid

    def release(self, rid):
        if self.state[rid] == FREE:
            raise ValueError("Cannot release unacquired device")
        self.state[rid] = FREE


device_pool = DevicePool()
