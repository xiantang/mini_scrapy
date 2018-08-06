from bitarray import bitarray

# 3rd party
import mmh3

import os

from mini_scrapy.untils.untils import request_fingerprint






class BloomFilter(set):

    def __init__(self, size, hash_count):
        super(BloomFilter, self).__init__()
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.size = size
        self.hash_count = hash_count

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.bit_array)



    def add(self, item):
        for ii in range(self.hash_count):
            index = mmh3.hash(item, ii) % self.size

            self.bit_array[index] = 1

        return self

    def __contains__(self, item):
        out = True
        for ii in range(self.hash_count):
            index = mmh3.hash(item, ii) % self.size
            if self.bit_array[index] == 0:
                out = False

        return out


class RFPDupeFilter(object):

    def __init__(self, size, hash_count,localizion,path):

        self.sbf = BloomFilter(
            size, hash_count
        )
        self.localizion = localizion
        self.path = path
        self.load()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        size = settings['BLOOMFILTER_SIZE']
        hash_count = settings['BLOOMFILTER_HASH_COUNT']
        localiztion = settings['LOCALIZTION']
        path = settings['LOCALIZTION_PAHT']
        return cls(size, hash_count,localiztion,path)

    def request_seen(self, request):
        """
        如果request是设置过避免过滤的 那就返回False
        request seen
        :param requests:
        :return:
        """

        finger = request_fingerprint(request)
        # print(finger)
        if request.dont_filter == True\
                or request.meta['retry_count']>0:
            # print("11111")
        #如果request 包含不被过滤或者retry_count>0的参数
        #就返回没有看到
            return False
        elif finger in self.sbf:
            return True
        # print(finger)
        self.add_to_text(finger)
        self.sbf.add(finger)
        return False

    def load(self):
        """
        TODO:load requests_seen from text/redis
        :return:
        """
        if os.path.exists(self.path):
            self.file = open(self.path,'a')
        else:
            self.file = open(self.path, 'w')


    def add_to_text(self,finger):
        self.file.write(finger+'\n')
if __name__ == '__main__':
    b = BloomFilter(1000,10)
    b.add("aaaaa")