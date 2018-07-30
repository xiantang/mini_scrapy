### 使用unittest进行测试

unittest是Python 自带的测试框架 
unittest 最核心的四个概念分别是   
：TestCase,TestSuite,TestRunner,TestFixture

TestCase:就是测试用例,一个完整的测试
流程，包括测试前的环境搭建(setUp),执行测试代码   
以及测试后环境的还原(tearDown)。


TestSuite:就是多个测试用例集合在一起  
然后TestSuite内部也可以嵌套TestSuite   

TestLoader:用来从各个地方收集测试用例   
然后加入到TestCase中。     

TestRunner:执行测试用例   

我们来编写test实例:

mathfunc.py

```python
def add(a, b):
    return a+b

def minus(a, b):
    return a-b

def multi(a, b):
    return a*b

def divide(a, b):
    return a/b
```

test_mathfunc.py

```python
import unittest
from learn.mathfunc import *
class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    def test_add(self):
        """Test method add(a, b)"""
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        """Test method divide(a, b)"""
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))

if __name__ == '__main__':
    unittest.main()


#Ran 4 tests in 0.045s
#OK
```

我们需要注意的是：
每个的测试方法必须以test开头   
不然识别不了   

如果我们想要测试用例按照顺序执行怎么办？
我们需要新建应该test_suit.py文件

```python
import unittest
from learn.test_mathfunc import TestMathFunc

if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [TestMathFunc('test_add'),
             TestMathFunc('test_minus'),
             TestMathFunc('test_divide')]
    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
```

执行结果:

```text
test_add (learn.test_mathfunc.TestMathFunc) ... ok
test_minus (learn.test_mathfunc.TestMathFunc) ... ok
test_divide (learn.test_mathfunc.TestMathFunc) ... FAIL

======================================================================
FAIL: test_divide (learn.test_mathfunc.TestMathFunc)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/didi/repertory/mini_scrapy/learn/test_mathfunc.py", line 28, in test_divide
    self.assertEqual(3, divide(6, 3))
AssertionError: 3 != 2.0

----------------------------------------------------------------------
Ran 3 tests in 0.000s

FAILED (failures=1)
```

但是很多时候我们会遇到一些问题   
就是很多应用环境中我们要涉及到   
操作数据库，需要执行操作数据，还原，
断开链接等一系列操作。但是不能每次都要去准备还原环境。   
我们可以采用`setUp`和`tearDown`来创建和销毁环境

```python
import unittest
class TestMathFunc(unittest.TestCase):
    def setUp(self):
        print("do something before test.Prepare environment")

    def tearDown(self):
        print('do something after test.Clean up')

```