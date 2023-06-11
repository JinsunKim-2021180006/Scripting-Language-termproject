#include "python.h"
#include <stdio.h>

static PyObject* pFileIn(PyObject* self, PyObject* args)
{
    const char* filename;
    FILE* file;
    char buffer[256];
    PyObject* result;

    if (!PyArg_ParseTuple(args, "s", &filename))
        return NULL;

    file = fopen(filename, "r");
    if (!file) {
        PyErr_SetString(PyExc_FileNotFoundError, "Failed to open the file");
        return NULL;
    }

    if (fgets(buffer, sizeof(buffer), file) == NULL) {
        PyErr_SetString(PyExc_IOError, "Failed to read from the file");
        fclose(file);
        return NULL;
    }

    fclose(file);
    result = Py_BuildValue("s", buffer);
    return result;
}

static PyObject* pFileOut(PyObject* self, PyObject* args)
{
    const char* filename;
    const char* content;
    FILE* file;

    if (!PyArg_ParseTuple(args, "ss", &filename, &content))
        return NULL;

    file = fopen(filename, "w");
    if (!file) {
        PyErr_SetString(PyExc_FileNotFoundError, "Failed to open the file");
        return NULL;
    }

    if (fputs(content, file) == EOF) {
        PyErr_SetString(PyExc_IOError, "Failed to write to the file");
        fclose(file);
        return NULL;
    }

    fclose(file);
    Py_RETURN_NONE;
}

static PyMethodDef SpamMethods[] = {
    {"pFileIn", pFileIn, METH_VARARGS, "Read content from a file."},
    {"pFileOut", pFileOut, METH_VARARGS, "Write content to a file."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "CModule",
    "Module for file I/O",
    -1,
    SpamMethods
};

PyMODINIT_FUNC
PyInit_Cmodule(void)
{
    return PyModule_Create(&spammodule);
}
