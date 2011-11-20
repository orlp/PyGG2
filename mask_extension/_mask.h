#include <Python.h>
#include "bitmask.h"

typedef struct {
    PyObject_HEAD
    bitmask_t *mask;
} PyMaskObject;

#define PyMask_AsBitmap(x) (((PyMaskObject*)x)->mask)

#define MASK_LOCAL_NUMSLOTS 1
#define MASK_LOCAL_ENTRY "_BITMASK_PYINTERFACE"

#define DOC_MASKMODULE "module for 2d bitmasks"
#define DOC_MASKMASK "mask.Mask((width, height)): return Mask\nobject for representing 2d bitmasks"
#define DOC_MASKGETSIZE "Mask.get_size() -> width,height\nReturns the size of the mask."
#define DOC_MASKGETAT "Mask.get_at((x,y)) -> int\nReturns nonzero if the bit at (x,y) is set."
#define DOC_MASKSETAT "Mask.set_at((x,y),value)\nSets the position in the mask given by x and y."
#define DOC_MASKOVERLAP "Mask.overlap(othermask, offset) -> x,y\nReturns the point of intersection if the masks overlap with the given offset - or None if it does not overlap."
#define DOC_MASKOVERLAPAREA "Mask.overlap_area(othermask, offset) -> numpixels\nReturns the number of overlapping 'pixels'."
#define DOC_MASKOVERLAPMASK "Mask.overlap_mask(othermask, offset) -> Mask\nReturns a mask of the overlapping pixels"
#define DOC_MASKFILL "Mask.fill()\nSets all bits to 1"
#define DOC_MASKCLEAR "Mask.clear()\nSets all bits to 0"
#define DOC_MASKINVERT "Mask.invert()\nFlips the bits in a Mask"
#define DOC_MASKSCALE "Mask.scale(x, y) -> Mask\nResizes a mask"
#define DOC_MASKROTATE "Mask.rotate(anle) -> Mask\nRotates a mask"
#define DOC_MASKDRAW "Mask.draw(othermask, offset)\nDraws a mask onto another"
#define DOC_MASKERASE "Mask.erase(othermask, offset)\nErases a mask from another"
#define DOC_MASKCOUNT "Mask.count() -> pixels\nReturns the number of set pixels"
#define DOC_MASKCENTROID "Mask.centroid() -> (x, y)\nReturns the centroid of the pixels in a Mask"
#define DOC_MASKCONVOLVE "Mask.convolve(othermask, outputmask = None, offset = (0,0)) -> Mask\nReturn the convolution of self with another mask."
#define DOC_MASKCOPY "Mask.copy() -> Mask\nReturns a copy of self"