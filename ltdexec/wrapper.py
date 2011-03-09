import threading
import uuid

_local = threading.local()
_local.key_stack = []

def create_envkey():
    if not _local.key_stack:
        key = uuid.uuid4().hex
    else:
        key = _local.key_stack[-1]
    _local.key_stack.append(key)
    return key

def pop_envkey(key):
    if key != _local.key_stack[-1]:
        raise RuntimeError('TODO')
    _local.key_stack.pop()


#==============================================================================#
class WrapperBase(object):
    def __init__(self):
        if _local.key_stack:
            self._LX_lock(_local.key_stack[-1])

    def _LX_lock(self, key):
        if not key:
            raise RuntimeError('TODO')
        if self._LX_key:
            raise RuntimeError('TODO')
        self._LX_key = key

    def _LX_unlock(self, other):
        if self._LX_key == other == _local.key_stack[-1]:
            self._LX_key = None
        else:
            raise RuntimeError('TODO')


#==============================================================================#

