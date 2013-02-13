"""
Proxy objects for any library, that allow you to add hooks before or after
methods on a specific object.
"""

__author__ = "Martin Blais <blais@furius.ca>"

import types
from pprint import pformat

class ProxyMethodWrapper:
    """ Wrapper object for a method to be called """ 
    def __init__(self, obj, func, name):
        self.obj, self.func, self.name = obj, func, name
        assert obj is not None
        assert func is not None
        assert name is not None

    def __call__(self, *args, **kwds):
        return self.obj._method_call(self.name, self.func, *args, **kwds)

class HookProxy(object):
    """
    Proxy object that delegates methods and attributes that don't start with _.
    You can derive from this and add appropriate hooks where needed.
    Override _pre/_post to do something before/afer all method calls.
    Override _pre_<name>/_post_<name> to hook before/after a specific call.
    """

    def __init__(self, objname, obj):
        self._objname, self._obj = objname, obj

    def __getattribute__(self, name):
        """ Return a proxy wrapper object if this is a method call """
        if name.startswith('_'):
            return object.__getattribute__(self, name)

        att = getattr(self._obj, name)
        if callable(att):
            return ProxyMethodWrapper(self, att, name)
        return att

    def __setitem__(self, key, value):
        """ Delegate [] syntax """
        name = '__setitem__'
        att = getattr(self._obj, name)
        pmeth = ProxyMethodWrapper(self, att, name)
        pmeth(key, value)

    def _call_str(self, name, *args, **kwds):
        """
        Returns a printable version of the call.
        This can be used for tracing.
        """
        pargs = [pformat(x) for x in args]
        for k, v in kwds.iteritems():
            pargs.append('%s=%s' % (k, pformat(v)))
        return '%s.%s(%s)' % (self._objname, name, ', '.join(pargs))

    def _method_call(self, name, func, *args, **kwds):
        """ This method gets called before a method is called """
        self._call_method('_pre', True, *args, **kwds)
        self._call_method('_pre_%s' % name, False, *args, **kwds)
        rval = func(*args, **kwds)
        self._call_method('_post_%s' % name, False, *args, **kwds)
        self._call_method('_post', True, *args, **kwds)
        return rval

    def _call_method(self, name, incName, *args, **kwds):
        try:
            postfunc = getattr(self, name)
            if incName: postfunc(name, *args, **kwds)
            else: postfunc(*args, **kwds)
        except AttributeError: pass
