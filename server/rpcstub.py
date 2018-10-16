class RPCStub(object):
    def __init__(self):
        pass

    def foo(self, a, b, c):
        self
        print('foo:', a, b, c)

    def bar(self, *args, **kwargs):
        self
        print("bar:")
        print('args', args)
        print('kwargs', kwargs)

    def __getattr__(self, item):
        self
        def _(*args, **kwargs):
            print('function_name', item)
            print('function_args', args)
            print('function_kwargs', kwargs)
        return _