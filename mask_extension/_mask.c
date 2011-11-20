/*
 Copyright (C) 2002-2007 Ulf Ekstrom except for the bitcount function.
  This wrapper code was originally written by Danny van Bruggen(?) for
  the SCAM library, it was then converted by Ulf Ekstrom to wrap the
  bitmask library, a spinoff from SCAM.

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Library General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Library General Public License for more details.

  You should have received a copy of the GNU Library General Public
  License along with this library; if not, write to the Free
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

*/

#include "_mask.h"
#include "structmember.h"
#include "bitmask.h"
#include <math.h>

#include "Imaging.h"

// helper struct/define to communicate with PIL images
typedef struct {
    UINT8 r;
    UINT8 g;
    UINT8 b;
    UINT8 a;
} RGBAPixel;
#define GET_RGBA_PIXEL(im,x,y) ((RGBAPixel*) (im)->image[(y)])[(x)]

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

static PyTypeObject PyMask_Type;

/* mask object methods */
static PyObject* mask_get_size(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);

    return Py_BuildValue("(ii)", mask->w, mask->h);
}

static PyObject* mask_copy(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    bitmask_t *newmask;
    PyMaskObject *newobj;
    
    newobj = PyObject_New(PyMaskObject, &PyMask_Type);
    newmask = bitmask_copy(mask);
    newobj->mask = newmask;

    return (PyObject*) newobj;
}

static PyObject* mask_get_at(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    int x, y, val;

    if (!PyArg_ParseTuple(args, "(ii)", &x, &y)) return NULL;

    if (x >= 0 && x < mask->w && y >= 0 && y < mask->h) {
        val = bitmask_getbit(mask, x, y);
    } else {
        PyErr_Format(PyExc_IndexError, "%d, %d is out of bounds", x, y);
        return NULL;
    }

    return PyInt_FromLong(val);
}

static PyObject* mask_set_at(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    int x, y, value = 1;

    if (!PyArg_ParseTuple(args, "(ii)|i", &x, &y, &value)) return NULL;

    if (x >= 0 && x < mask->w && y >= 0 && y < mask->h) {
        if (value) {
            bitmask_setbit(mask, x, y);
        } else {
            bitmask_clearbit(mask, x, y);
        }
    } else {
        PyErr_Format(PyExc_IndexError, "%d, %d is out of bounds", x, y);
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* mask_overlap(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    bitmask_t *othermask;
    PyObject *maskobj;
    int x, y, val;
    int xp, yp;

    if (!PyArg_ParseTuple(args, "O!(ii)", &PyMask_Type, &maskobj, &x, &y)) return NULL;

    othermask = PyMask_AsBitmap(maskobj);

    val = bitmask_overlap_pos(mask, othermask, x, y, &xp, &yp);

    if (val) {
        return Py_BuildValue("(ii)", xp, yp);
    } else {
        Py_INCREF(Py_None);
        return Py_None;
    }
}


static PyObject* mask_overlap_area(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    bitmask_t *othermask;
    PyObject *maskobj;
    int x, y, val;

    if (!PyArg_ParseTuple(args, "O!(ii)", &PyMask_Type, &maskobj, &x, &y)) {
        return NULL;
    }

    othermask = PyMask_AsBitmap(maskobj);

    val = bitmask_overlap_area(mask, othermask, x, y);
    return PyInt_FromLong(val);
}

static PyObject* mask_overlap_mask(PyObject* self, PyObject* args) {
    int x, y;
    bitmask_t *mask = PyMask_AsBitmap(self);
    bitmask_t *output = bitmask_create(mask->w, mask->h, 0);
    bitmask_t *othermask;
    PyObject *maskobj;
    PyMaskObject *maskobj2 = PyObject_New(PyMaskObject, &PyMask_Type);

    if (!PyArg_ParseTuple(args, "O!(ii)", &PyMask_Type, &maskobj, &x, &y)) {
        return NULL;
    }

    othermask = PyMask_AsBitmap(maskobj);

    bitmask_overlap_mask(mask, othermask, output, x, y);

    if (maskobj2) maskobj2->mask = output;

    return (PyObject*)maskobj2;
}

static PyObject* mask_fill(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);

    bitmask_fill(mask);

    Py_RETURN_NONE;
}

static PyObject* mask_clear(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);

    bitmask_clear(mask);

    Py_RETURN_NONE;
}

static PyObject* mask_invert(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);

    bitmask_invert(mask);

    Py_RETURN_NONE;
}

static PyObject* mask_scale(PyObject* self, PyObject* args) {
    int x, y;
    bitmask_t *input = PyMask_AsBitmap(self);
    bitmask_t *output;
    PyMaskObject *maskobj = PyObject_New(PyMaskObject, &PyMask_Type);

    if (!PyArg_ParseTuple(args, "ii", &x, &y)) {
        return NULL;
    }

    output = bitmask_scale(input, x, y);

    if (maskobj)
        maskobj->mask = output;

    return (PyObject*)maskobj;
}

static PyObject* mask_draw(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    bitmask_t *othermask;
    PyObject *maskobj;
    int x, y;

    if (!PyArg_ParseTuple(args, "O!(ii)", &PyMask_Type, &maskobj, &x, &y)) {
        return NULL;
    }

    othermask = PyMask_AsBitmap(maskobj);

    bitmask_draw(mask, othermask, x, y);

    Py_RETURN_NONE;
}

static PyObject* mask_erase(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    bitmask_t *othermask;
    PyObject *maskobj;
    int x, y;

    if (!PyArg_ParseTuple(args, "O!(ii)", &PyMask_Type, &maskobj, &x, &y)) {
        return NULL;
    }

    othermask = PyMask_AsBitmap(maskobj);

    bitmask_erase(mask, othermask, x, y);

    Py_RETURN_NONE;
}

static PyObject* mask_count(PyObject* self, PyObject* args) {
    bitmask_t *m = PyMask_AsBitmap(self);

    return PyInt_FromLong(bitmask_count(m));
}

static PyObject* mask_centroid(PyObject* self, PyObject* args) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    int x, y;
    long int m10, m01, m00;
    PyObject *xobj, *yobj;

    m10 = m01 = m00 = 0;

    for (x = 0; x < mask->w; x++) {
        for (y = 0; y < mask->h; y++) {
            if (bitmask_getbit(mask, x, y)) {
                m10 += x;
                m01 += y;
                m00++;
            }
        }
    }

    if (m00) {
        xobj = PyInt_FromLong(m10 / m00);
        yobj = PyInt_FromLong(m01 / m00);
    } else {
        xobj = PyInt_FromLong(0);
        yobj = PyInt_FromLong(0);
    }

    return Py_BuildValue("(NN)", xobj, yobj);
}

static PyObject* mask_convolve(PyObject* aobj, PyObject* args) {
    PyObject *bobj, *oobj = Py_None;
    bitmask_t    *a,    *b,    *o;
    int xoffset = 0, yoffset = 0;

    if (!PyArg_ParseTuple (args, "O!|O(ii)", &PyMask_Type, &bobj, &oobj, &xoffset, &yoffset))
        return NULL;

    a = PyMask_AsBitmap(aobj);
    b = PyMask_AsBitmap(bobj);

    if (oobj == Py_None) {
        PyMaskObject *result = PyObject_New(PyMaskObject, &PyMask_Type);

        result->mask = bitmask_create(a->w + b->w - 1, a->h + b->h - 1, 0);
        oobj = (PyObject*) result;
    } else
        Py_INCREF(oobj);

    o = PyMask_AsBitmap(oobj);

    bitmask_convolve(a, b, o, xoffset, yoffset);
    return oobj;
}

static PyObject* mask_rotate(PyObject* self, PyObject* args) {
    float angle;
    bitmask_t *input = PyMask_AsBitmap(self);
    bitmask_t *output;
    PyMaskObject *maskobj = PyObject_New(PyMaskObject, &PyMask_Type);

    if (!PyArg_ParseTuple(args, "f", &angle)) {
        return NULL;
    }

    output = bitmask_rotate(input, angle);

    if (maskobj) maskobj->mask = output;

    return (PyObject*)maskobj;
}


static PyMethodDef mask_methods[] = {
    { "get_size", mask_get_size, METH_NOARGS, DOC_MASKGETSIZE},
    { "get_at", mask_get_at, METH_VARARGS, DOC_MASKGETAT },
    { "set_at", mask_set_at, METH_VARARGS, DOC_MASKSETAT },
    { "overlap", mask_overlap, METH_VARARGS, DOC_MASKOVERLAP },
    { "overlap_area", mask_overlap_area, METH_VARARGS, DOC_MASKOVERLAPAREA },
    { "overlap_mask", mask_overlap_mask, METH_VARARGS, DOC_MASKOVERLAPMASK },
    { "fill", mask_fill, METH_NOARGS, DOC_MASKFILL },
    { "clear", mask_clear, METH_NOARGS, DOC_MASKCLEAR },
    { "invert", mask_invert, METH_NOARGS, DOC_MASKINVERT },
    { "scale", mask_scale, METH_VARARGS, DOC_MASKSCALE },
    { "rotate", mask_rotate, METH_VARARGS, DOC_MASKROTATE },
    { "draw", mask_draw, METH_VARARGS, DOC_MASKDRAW },
    { "erase", mask_erase, METH_VARARGS, DOC_MASKERASE },
    { "count", mask_count, METH_NOARGS, DOC_MASKCOUNT },
    { "centroid", mask_centroid, METH_NOARGS, DOC_MASKCENTROID },
    { "convolve", mask_convolve, METH_VARARGS, DOC_MASKCONVOLVE },
    { "copy", mask_copy, METH_NOARGS, DOC_MASKCOPY },

    { NULL, NULL, 0, NULL }
};

/*mask object internals*/
static void mask_dealloc(PyObject* self) {
    bitmask_t *mask = PyMask_AsBitmap(self);
    bitmask_free(mask);
    PyObject_DEL(self);
}

static PyTypeObject PyMask_Type = {
    PyObject_HEAD_INIT(NULL)
    0,
    "Mask",
    sizeof(PyMaskObject),
    0,
    mask_dealloc,
    0,
    0,
    0,
    0,
    0,
    0,
    NULL,
    0,
    (hashfunc)NULL,
    (ternaryfunc)NULL,
    (reprfunc)NULL,
    0L, 0L, 0L, 0L,
    DOC_MASKMASK,                 /* Documentation string */
    0,                                  /* tp_traverse */
    0,				        /* tp_clear */
    0,				        /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    0,				        /* tp_iter */
    0,				        /* tp_iternext */
    mask_methods,                       /* tp_methods */
    0,                                  /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,			                /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,					/* tp_dictoffset */
    0,                                  /* tp_init */
    0,					/* tp_alloc */
    0,                                  /* tp_new */
};

/*mask module methods*/
static PyObject* Mask(PyObject* self, PyObject* args) {
    bitmask_t *mask;
    int w, h, fill;
    PyMaskObject *maskobj;

    fill = 0;
    if (!PyArg_ParseTuple(args, "iii", &w, &h, &fill))
        return NULL;

    mask = bitmask_create(w, h, fill);

    if (!mask)
        return NULL; /*RAISE(PyExc_Error, "cannot create bitmask");*/

    /*create the new python object from mask*/
    maskobj = PyObject_New(PyMaskObject, &PyMask_Type);

    if (maskobj)
        maskobj->mask = mask;

    return (PyObject*)maskobj;
}

static PyObject* load_mask_from_image_PIL(PyObject* self, PyObject* args) {
    Imaging imIn;
    bitmask_t *mask;
    PyMaskObject *maskobj;
    int x, y;

    long idIn;
    int threshold = 127;
    if (!PyArg_ParseTuple(args, "li", &idIn, &threshold))
        return NULL;

    imIn = (Imaging) idIn;
    mask = bitmask_create(imIn->xsize, imIn->ysize, 0);
    
    if (!mask) return NULL; /*RAISE(PyExc_Error, "cannot create bitmask");*/
    
    maskobj = PyObject_New(PyMaskObject, &PyMask_Type);

    if (maskobj) maskobj->mask = mask;
    
    for (y = 0; y < imIn->ysize; y++) {
        for (x = 0; x < imIn->xsize; x++) {
            if (GET_RGBA_PIXEL(imIn, x, y).a > threshold) {
                bitmask_setbit(mask, x, y);
            }
        }
    }

    return (PyObject*) maskobj;
}

static PyObject* load_mask_from_image_threshold_PIL(PyObject* self, PyObject* args) {
    Imaging imIn;
    bitmask_t *mask;
    PyMaskObject *maskobj;
    int x, y;

    long idIn;
    int cr, cg, cb, ca;
    int tr, tg, tb, ta;
    
    tr = tg = tb = 0;
    ta = 255;
    if (!PyArg_ParseTuple(args, "l(iiii)(iiii)", &idIn, &cr, &cg, &cb, &ca, &tr, &tg, &tb, &ta)) return NULL;

    imIn = (Imaging) idIn;
    mask = bitmask_create(imIn->xsize, imIn->ysize, 0);
    
    if (!mask) return NULL; /*RAISE(PyExc_Error, "cannot create bitmask");*/
    
    maskobj = PyObject_New(PyMaskObject, &PyMask_Type);

    if (maskobj) maskobj->mask = mask;
    
    for (y = 0; y < imIn->ysize; y++) {
        for (x = 0; x < imIn->xsize; x++) {
            RGBAPixel px = GET_RGBA_PIXEL(imIn, x, y);
         
            if ((abs(px.r - cr) <= tr) &
                (abs(px.g - cg) <= tg) &
                (abs(px.b - cb) <= tb)) {
                /* this pixel is within the threshold of the color. */
                bitmask_setbit(mask, x, y);
            }
        }
    }

    return (PyObject*) maskobj;
}


static PyMethodDef _mask_methods[] = {
    { "Mask", Mask, METH_VARARGS, DOC_MASKMASK },
    { "load_mask_from_image_PIL", load_mask_from_image_PIL, METH_VARARGS, "__internal" },
    { "load_mask_from_image_threshold_PIL", load_mask_from_image_threshold_PIL, METH_VARARGS, "__internal" },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC init_mask(void) {
    PyObject *module, *dict, *apiobj;
    static void* c_api[MASK_LOCAL_NUMSLOTS];

    /* create the mask type */
    if (PyType_Ready (&PyMask_Type) < 0) {
        return;
    }

    /* create the module */
#if PY3
    static struct PyModuleDef _module = {
        PyModuleDef_HEAD_INIT,
        "_mask",
        DOC_MASKMODULE,
        -1,
        _mask_methods,
        NULL, NULL, NULL, NULL
    };

    module = PyModule_Create(&_module);
#else
    module = Py_InitModule3("_mask", _mask_methods, DOC_MASKMODULE);
#endif

    if (module == NULL) {
        return;
    }

    dict = PyModule_GetDict(module);
    if (PyDict_SetItemString(dict, "MaskType", (PyObject *) &PyMask_Type) == -1) {
        Py_DECREF(module);
        return;
    }

    /* export the c api */
    c_api[0] = &PyMask_Type;
    apiobj = PyCObject_FromVoidPtr(c_api, NULL);

    if (apiobj == NULL) {
        Py_DECREF (module);
        return;
    }

    if (PyModule_AddObject(module, MASK_LOCAL_ENTRY, apiobj) == -1) {
        Py_DECREF (apiobj);
        Py_DECREF (module);
        return;
    }
}
