import json
from importlib import import_module

from mini_scrapy.conf import default_settings


class Attribute(object):

    def __init__(self,value):
        self.value = value

    def __str__(self):
        return "<Attribute value=%s>" %self.value

    __repr__ = __str__



class Settings(object):

    def __init__(self, value=None):
        self.attrs = {}
        self.load_config(default_settings)
        # 加载默认setting
        if value is not None:
            self.set_dict(value)

    def __getitem__(self, key):

        return self.attrs[key].value if key in self.attrs else None

    def load_config(self, module):
        if isinstance(module, str):
            #如果是字符串 就导入这个模块
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                #是否是大写的 如果是的话就导入
                self.set(key, getattr(module, key))

    def set(self, key, value):
        self.attrs[key] = Attribute(value)

    def set_dict(self, values):
        # set 到自己的attrs中
        for key, value in values.iteritems():
            self.set(key, value)

    def get(self, key, default=None):
        """

        :param key:
        :param default:
        :return:
        """
        return self[key] or default

    def get_int(self, key, default=0):
        return int(self.get(key, default))

    def get_float(self, key, default=0.0):
        return float(self.get(key, default))

    def get_list(self, key, default=None):
        value = self.get(key, default or None)
        if isinstance(value, str):
            value = value.split(",")
        return value

    def get_dict(self, key, default=None):
        value = self.get(key,default or None)
        if isinstance(value,str):
            value = json.loads(value)
        return value
