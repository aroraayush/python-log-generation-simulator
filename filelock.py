import fcntl
import os
from contextlib import contextmanager

MODE_NAMES = {
    fcntl.LOCK_SH: 'shared',
    fcntl.LOCK_EX: 'exclusive',
}

class FileLock:
    def __init__(self, filename):
        self.filename = filename
        self.reader = self.shared = _FileLock(self, fcntl.LOCK_SH)
        self.writer = self.exclusive = _FileLock(self, fcntl.LOCK_EX)

        self.held = False
        self.mode = None
        self._handle = None

    @property
    def handle(self):
        if self._handle is None or self._handle.closed:
            self._handle = open(self.filename, 'w+')
        return self._handle

    def close(self):
        if self.held:
            raise RuntimeError("Can't close held lock, release it first")
        if self._handle and not self._handle.closed:
            self._handle.close()
        self._handle = None

    def delete(self):
        self.close()
        os.remove(self.filename)

    def _acquire(self, mode):
        self.held = True
        self.mode = mode

    def _release(self):
        self.held = False
        self.mode = None

    # Object representation
    def __repr__(self):
        if self.held:
            mode = MODE_NAMES[self.mode]
        else:
            mode = 'not held'
        return f'<{type(self).__name__}: {self.filename} ({mode})>'


class _FileLock:
    """
    Helper class that locks a file with a mode (exclusive or shared). Should be
    used through a FileLock instance.
    """
    def __init__(self, file_lock, mode):
        self.file_lock = file_lock
        self.mode = mode

    def acquire(self, blocking=True):
        """Acquire this lock."""
        if self.file_lock.held:
            raise RuntimeError(
                f"Lock is already held as {MODE_NAMES[self.file_lock.mode]}")
        flags = self.mode | (0 if blocking else fcntl.LOCK_NB)
        fcntl.flock(self.file_lock.handle, flags)
        self.file_lock._acquire(self.mode)

    def release(self):
        """Release this lock."""
        if not self.file_lock.held:
            raise RuntimeError("Lock is not held")
        elif self.file_lock.mode != self.mode:
            raise RuntimeError("Lock is held as {held} not {desired}".format(
                held=MODE_NAMES[self.file_lock.mode],
                desired=MODE_NAMES[self.mode]))
        fcntl.flock(self.file_lock.handle, fcntl.LOCK_UN)
        self.file_lock._release()

    @contextmanager
    def __call__(self, blocking=True):
        self.acquire(blocking=blocking)
        try:
            yield
        finally:
            self.release()
