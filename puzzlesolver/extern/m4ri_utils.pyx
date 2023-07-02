# distutils: sources = m4ri/brilliantrussian.c m4ri/debug_dump.c m4ri/djb.c m4ri/echelonform.c m4ri/graycode.c m4ri/misc.c m4ri/mmc.c m4ri/mp.c m4ri/mzd.c m4ri/mzp.c m4ri/ple_russian.c m4ri/ple.c m4ri/solve.c m4ri/strassen.c m4ri/triangular_russian.c m4ri/triangular.c
# distutils: include_dirs = m4ri/

from m4ri cimport mzd_t
from m4ri cimport mzd_init, mzd_free
from m4ri cimport mzd_read_bit, mzd_write_bit
from m4ri cimport mzd_inv_m4ri, mzd_mul_m4rm


cdef mzd_to_mat(mzd_t *A_mzd, m, n):
    return [[mzd_read_bit(A_mzd, i, j) for j in range(n)] for i in range(m)]


cdef mzd_t *mat_to_mzd(A, m, n):
    cdef mzd_t *A_mzd = mzd_init(m, n)

    for i in range(m):
        for j in range(n):
            mzd_write_bit(A_mzd, i, j, A[i][j])
    
    return A_mzd


def mat_inv_GF2(A):
    """Returns the inverse of A."""
    m = len(A)
    n = len(A[0])
    cdef mzd_t *A_mzd = mat_to_mzd(A, m, n)

    cdef mzd_t *A_inv_mzd = mzd_inv_m4ri(NULL, A_mzd, 0)
    A_inv = mzd_to_mat(A_inv_mzd, m, n)
    mzd_free(A_mzd)
    mzd_free(A_inv_mzd)

    return A_inv


def mat_mul_GF2(A, B):
    """Returns AB."""
    ma = len(A); na = len(A[0])
    mb = len(B); nb = len(B[0])
    cdef mzd_t *A_mzd = mat_to_mzd(A, ma, na)
    cdef mzd_t *B_mzd = mat_to_mzd(B, mb, nb)

    cdef mzd_t *C_mzd = mzd_mul_m4rm(NULL, A_mzd, B_mzd, 0)
    C = mzd_to_mat(C_mzd, ma, nb)
    mzd_free(A_mzd)
    mzd_free(B_mzd)
    mzd_free(C_mzd)

    return C
