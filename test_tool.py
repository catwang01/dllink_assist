from tool import lru_cache
import functools
import numpy as np

class TestTool:

    def test_lru_cache(self):

        i = 0

        @lru_cache()
        def haha(a):
            nonlocal i
            i += 1
            return a

        for _ in range(10):
            haha(np.array(1))

        @lru_cache(maxsize=10)
        def haha(a):
            nonlocal i
            i += 1
            return a

        for _ in range(10):
            haha(np.array(1))

        assert i == 2

        for _ in range(10):
            haha(np.array(2))

        assert i == 3