import collections
dict1 = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}
dict2 = {'abc': 456}
dict3 = {'abc': 123, 10: 20}
dict4 = {} #定义空字典
dict5 = dict() #定义空字典
bag = ['apple', 'orange', 'cherry', 'apple','apple', 'cherry', 'blueberry']
count = collections.defaultdict(int)
for fruit in bag:
    count[fruit] += 1
print(count)