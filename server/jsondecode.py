import json


class JSONRPC(object):
    def __init__(self):
        self.data = None

    def from_data(self, data):
        print('from data ({})'.format(data))
        self.data = json.loads(data.decode('utf-8'))

    def call_method(self):
        method_name = self.data['method_name']
        method_args = self.data['method_args']
        method_kwargs = self.data['method_kwargs']

        my_method = getattr(self, method_name)
        my_method(*method_args, **method_kwargs)
        print(dir(my_method))
