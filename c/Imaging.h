/*
 * The Python Imaging Library
 * $Id$
 * 
 * declarations for the imaging core library
 *
 * Copyright (c) 1997-2005 by Secret Labs AB
 * Copyright (c) 1995-2005 by Fredrik Lundh
 *
 * See the README file for information on usage and redistribution.
 */

#include "Python.h"

/* Check that we have an ANSI compliant compiler */
#ifndef HAVE_PROTOTYPES
#error Sorry, this library requires support for ANSI prototypes.
#endif
#ifndef STDC_HEADERS
#error Sorry, this library requires ANSI header files.
#endif

#if defined(_MSC_VER)
#ifndef WIN32
#define WIN32
#endif
/* VC++ 4.0 is a bit annoying when it comes to precision issues (like
   claiming that "float a = 0.0;" would lead to loss of precision).  I
   don't like to see warnings from my code, but since I still want to
   keep it readable, I simply switch off a few warnings instead of adding
   the tons of casts that VC++ seem to require.  This code is compiled
   with numerous other compilers as well, so any real errors are likely
   to be catched anyway. */
#pragma warning(disable: 4244) /* conversion from 'float' to 'int' */
#endif

#if defined(_MSC_VER)
#define inline __inline
#elif !defined(USE_INLINE)
#define inline
#endif

#if SIZEOF_SHORT == 2
#define	INT16 short
#elif SIZEOF_INT == 2
#define	INT16 int
#else
#define	INT16 short /* most things works just fine anyway... */
#endif

#if SIZEOF_SHORT == 4
#define	INT32 short
#elif SIZEOF_INT == 4
#define	INT32 int
#elif SIZEOF_LONG == 4
#define	INT32 long
#else
#error Cannot find required 32-bit integer type
#endif

#if SIZEOF_LONG == 8
#define	INT64 long
#elif SIZEOF_LONG_LONG == 8
#define	INT64 long
#endif

/* assume IEEE; tweak if necessary (patches are welcome) */
#define	FLOAT32 float
#define	FLOAT64 double

#define	INT8  signed char
#define	UINT8 unsigned char

#define	UINT16 unsigned INT16
#define	UINT32 unsigned INT32


#if defined(__cplusplus)
extern "C" {
#endif


#ifndef M_PI
#define	M_PI	3.14159265359
#endif


/* -------------------------------------------------------------------- */

/*
 * Image data organization:
 *
 * mode	    bytes	byte order
 * -------------------------------
 * 1	    1		1
 * L	    1		L
 * P	    1		P
 * I        4           I (32-bit integer, native byte order)
 * F        4           F (32-bit IEEE float, native byte order)
 * RGB	    4		R, G, B, -
 * RGBA	    4		R, G, B, A
 * CMYK	    4		C, M, Y, K
 * YCbCr    4		Y, Cb, Cr, -
 *
 * experimental modes (incomplete):
 * LA       4           L, -, -, A
 * PA       4           P, -, -, A
 * I;16     2           I (16-bit integer, native byte order)
 *
 * "P" is an 8-bit palette mode, which should be mapped through the
 * palette member to get an output image.  Check palette->mode to
 * find the corresponding "real" mode.
 *
 * For information on how to access Imaging objects from your own C
 * extensions, see http://www.effbot.org/zone/pil-extending.htm
 */

/* Handles */

typedef struct ImagingMemoryInstance* Imaging;

typedef struct ImagingAccessInstance* ImagingAccess;
typedef struct ImagingHistogramInstance* ImagingHistogram;
typedef struct ImagingOutlineInstance* ImagingOutline;
typedef struct ImagingPaletteInstance* ImagingPalette;

/* handle magics (used with PyCObject). */
#define IMAGING_MAGIC "PIL Imaging"

/* pixel types */
#define IMAGING_TYPE_UINT8 0
#define IMAGING_TYPE_INT32 1
#define IMAGING_TYPE_FLOAT32 2
#define IMAGING_TYPE_SPECIAL 3 /* check mode for details */

struct ImagingMemoryInstance {

    /* Format */
    char mode[4+1];	/* Band names ("1", "L", "P", "RGB", "RGBA", "CMYK") */
    int type;		/* Data type (IMAGING_TYPE_*) */
    int depth;		/* Depth (ignored in this version) */
    int bands;		/* Number of bands (1, 2, 3, or 4) */
    int xsize;		/* Image dimension. */
    int ysize;

    /* Colour palette (for "P" images only) */
    ImagingPalette palette;

    /* Data pointers */
    UINT8 **image8;	/* Set for 8-bit images (pixelsize=1). */
    INT32 **image32;	/* Set for 32-bit images (pixelsize=4). */

    /* Internals */
    char **image;	/* Actual raster data. */
    char *block;	/* Set if data is allocated in a single block. */

    int pixelsize;	/* Size of a pixel, in bytes (1, 2 or 4) */
    int linesize;	/* Size of a line, in bytes (xsize * pixelsize) */

    /* Virtual methods */
    void (*destroy)(Imaging im);
};


#define IMAGING_PIXEL_1(im,x,y) ((im)->image8[(y)][(x)])
#define IMAGING_PIXEL_L(im,x,y) ((im)->image8[(y)][(x)])
#define IMAGING_PIXEL_LA(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_P(im,x,y) ((im)->image8[(y)][(x)])
#define IMAGING_PIXEL_PA(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_I(im,x,y) ((im)->image32[(y)][(x)])
#define IMAGING_PIXEL_F(im,x,y) (((FLOAT32*)(im)->image32[y])[x])
#define IMAGING_PIXEL_RGB(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_RGBA(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_CMYK(im,x,y) ((im)->image[(y)][(x)*4])
#define IMAGING_PIXEL_YCbCr(im,x,y) ((im)->image[(y)][(x)*4])

#define IMAGING_PIXEL_UINT8(im,x,y) ((im)->image8[(y)][(x)])
#define IMAGING_PIXEL_INT32(im,x,y) ((im)->image32[(y)][(x)])
#define IMAGING_PIXEL_FLOAT32(im,x,y) (((FLOAT32*)(im)->image32[y])[x])

struct ImagingAccessInstance {
  const char* mode;
  void* (*line)(Imaging im, int x, int y);
  void (*get_pixel)(Imaging im, int x, int y, void* pixel);
  void (*put_pixel)(Imaging im, int x, int y, const void* pixel);
};

struct ImagingHistogramInstance {

    /* Format */
    char mode[4+1];	/* Band names (of corresponding source image) */
    int bands;		/* Number of bands (1, 3, or 4) */

    /* Data */
    long *histogram;	/* Histogram (bands*256 longs) */

};


struct ImagingPaletteInstance {

    /* Format */
    char mode[4+1];	/* Band names */

    /* Data */
    UINT8 palette[1024];/* Palette data (same format as image data) */

    INT16* cache;	/* Palette cache (used for predefined palettes) */
    int keep_cache;	/* This palette will be reused; keep cache */

};

#if defined(__cplusplus)
}
#endif
