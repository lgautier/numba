from numba import cuda
import numpy as np
from numba import unittest_support as unittest


class TestMultiGPUContext(unittest.TestCase):
    def test_multigpu_context(self):
        @cuda.jit("void(float64[:], float64[:])")
        def copy_plus_1(inp, out):
            i = cuda.grid(1)
            if i < out.size:
                out[i] = inp[i] + 1

        def check(inp, out):
            np.testing.assert_equal(inp + 1, out)


        N = 32
        A = np.arange(N, dtype=np.float64)
        B = np.arange(N, dtype=np.float64)

        with cuda.gpus[0]:
            copy_plus_1[1, N](A, B)

        print(A, B)
        check(A, B)

        copy_plus_1[1, N](A, B)
        print(A, B)
        check(A, B)

        print(len(cuda.gpus))

        if len(cuda.gpus) >= 2:
            with cuda.gpus[0]:
                A0 = np.arange(N, dtype=np.float64)
                B0 = np.arange(N, dtype=np.float64)
                copy_plus_1[1, N](A0, B0)

                with cuda.gpus[1]:
                    A1 = np.arange(N, dtype=np.float64)
                    B1 = np.arange(N, dtype=np.float64)
                    copy_plus_1[1, N](A1, B1)

            print(A0, A1)
            print(B0, B1)

            check(A0, B0)
            check(A1, B1)


            A = np.arange(N, dtype=np.float64)
            B = np.arange(N, dtype=np.float64)
            copy_plus_1[1, N](A, B)
            check(A, B)

if __name__ == '__main__':
    unittest.main()
