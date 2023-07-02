#ifndef M4RI_M4RI_CONFIG_H
#define M4RI_M4RI_CONFIG_H

// Defines determined during configuration of m4ri.
#define __M4RI_HAVE_MM_MALLOC		1
#define __M4RI_HAVE_POSIX_MEMALIGN	1
#define __M4RI_HAVE_SSE2		1
#define __M4RI_HAVE_OPENMP		0
#define __M4RI_CPU_L1_CACHE		32768
#define __M4RI_CPU_L2_CACHE		1310720
#define __M4RI_CPU_L3_CACHE		31457280
#define __M4RI_DEBUG_DUMP		(0 || 0)
#define __M4RI_DEBUG_MZD		0
#define __M4RI_HAVE_LIBPNG              1

#define __M4RI_CC                       "gcc"
#define __M4RI_CFLAGS                   " -mmmx -msse -msse2 -msse3 -mssse3 -msse4.1 -msse4.2 -msha -maes -mavx -mfma -mavx2  -g -O2"
#define __M4RI_SIMD_CFLAGS              " -mmmx -msse -msse2 -msse3 -mssse3 -msse4.1 -msse4.2 -msha -maes -mavx -mfma -mavx2"
#define __M4RI_OPENMP_CFLAGS            ""

// Helper macros.
#define __M4RI_USE_MM_MALLOC		(__M4RI_HAVE_MM_MALLOC && __M4RI_HAVE_SSE2)
#define __M4RI_USE_POSIX_MEMALIGN	(__M4RI_HAVE_POSIX_MEMALIGN && __M4RI_HAVE_SSE2)
#define __M4RI_DD_QUIET			(0 && !0)

#define __M4RI_ENABLE_MZD_CACHE         1
#define __M4RI_ENABLE_MMC               1

#endif // M4RI_M4RI_CONFIG_H
