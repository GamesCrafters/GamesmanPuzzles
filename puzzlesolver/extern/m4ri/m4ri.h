/**
 * \file m4ri.h
 * \brief Main include file for the M4RI library.
 *
 * \author Gregory Bard <bard@fordham.edu>
 * \author Martin Albrecht <M.R.Albrecht@rhul.ac.uk>
 */
/******************************************************************************
 *
 *                 M4RI: Linear Algebra over GF(2)
 *
 *    Copyright (C) 2007 Gregory Bard <gregory.bard@ieee.org>
 *    Copyright (C) 2007,2008 Martin Albrecht <malb@informatik.uni-bremen.de>
 *
 *  Distributed under the terms of the GNU General Public License (GPL)
 *  version 2 or higher.
 *
 *    This code is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *    General Public License for more details.
 *
 *  The full text of the GPL is available at:
 *
 *                  http://www.gnu.org/licenses/
 ******************************************************************************/

#ifndef M4RI_M4RI_H
#define M4RI_M4RI_H

/**
 * \mainpage
 *
 * M4RI is a library to do fast arithmetic with dense matrices over
 * \f$\mathbb{F}_2\f$. M4RI is available under the GPLv2+ and used by the Sage
 * mathematics software and the PolyBoRi library. See
 * http://m4ri.sagemath.org for details.
 *
 * \example tests/test_multiplication.c
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#if defined(__M4RI_HAVE_SSE2) && __M4RI_HAVE_SSE2
#if !defined(__SSE2__) || !__SSE2__
#error                                                                                             \
    "Your current compiler and / or CFLAGS setting doesn't allow SSE2 code. Please change that or these to the setting(s) you used when compiling M4RI."
#endif
#endif

#if defined(__cplusplus) && !defined(_MSC_VER)
extern "C" {
#endif

#include <brilliantrussian.h>
#include <djb.h>
#include <echelonform.h>
#include <graycode.h>
#include <io.h>
#include <mp.h>
#include <mzd.h>
#include <mzp.h>
#include <parity.h>
#include <ple.h>
#include <ple_russian.h>
#include <solve.h>
#include <strassen.h>
#include <triangular.h>
#include <triangular_russian.h>

#if defined(__cplusplus) && !defined(_MSC_VER)
}
#endif

#endif  // M4RI_M4RI_H
