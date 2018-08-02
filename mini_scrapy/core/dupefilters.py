from bitarray import bitarray

# 3rd party
import mmh3

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

    def load(self):
        """
        TODO:load requests_seen from text/redis
        :return:
        """
        pass

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

    def __init__(self, size, hash_count):

        self.sbf = BloomFilter(
            size, hash_count
        )

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        size = settings['BLOOMFILTER_SIZE']
        hash_count = settings['BLOOMFILTER_HASH_COUNT']
        return cls(size, hash_count)

    def request_seen(self, request):
        """
        如果request是设置过避免过滤的 那就返回False
        request seen
        :param requests:
        :return:
        """

        finger = request_fingerprint(request)

        if request.dont_filter == True or request.meta['retry_count']>0:
            # print("11111")

            return False
        elif finger in self.sbf:
            return True
        self.sbf.add(finger)
        return False
