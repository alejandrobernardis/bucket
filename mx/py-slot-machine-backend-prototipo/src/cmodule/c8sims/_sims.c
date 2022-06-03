#include <Python.h>

static PyObject *SimsError;
static PyObject *sims_getmatrix(PyObject *self, PyObject *args);
static PyObject *sims_getfactor(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
	{"getmatrix", sims_getmatrix, METH_VARARGS, "Get Matrix"},
	{"getfactor", sims_getfactor, METH_VARARGS, "Get Factor"},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_sims(void) {
	PyObject *pymod = Py_InitModule("_sims", module_methods);
	if (pymod == NULL)
		return;
	SimsError = PyErr_NewException("_sims.error", NULL, NULL);
	Py_INCREF(SimsError);
	PyModule_AddObject(pymod, "error", SimsError);
}

// Return str, len 15 alpha-chars

static PyObject * sims_getmatrix(PyObject *self, PyObject *args) {
	const int *mid, *lines;
	const float *bet;
	
	if(!PyArg_ParseTuple(args, "iif", &mid, &lines, &bet))
		return NULL;
	
	// Pocho ...
	
	return Py_BuildValue("s", "AAAAABBBBBCCCCC");
}

// Return float, 0.0

static PyObject * sims_getfactor(PyObject *self, PyObject *args) {
	const int *mid, *lines;
	const float *bet;
	
	if(!PyArg_ParseTuple(args, "iif", &mid, &lines, &bet))
		return NULL;
	
	// Pocho ...
	
	return Py_BuildValue("f", 4.5);
}