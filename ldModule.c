

#include <Python.h>
#include <string.h>

//http://rosettacode.org/wiki/Levenshtein_distance#C
/* s, t: two strings; ls, lt: their respective length */
int levenshtein(const char *s, int ls, const char *t, int lt)
{
        int a, b, c;
 
        /* if either string is empty, difference is inserting all chars 
         * from the other
         */
        if (!ls) return lt;
        if (!lt) return ls;
 
        /* if last letters are the same, the difference is whatever is
         * required to edit the rest of the strings
         */
        if (s[ls] == t[ls])
                return levenshtein(s, ls - 1, t, lt - 1);
 
        /* else try:
         *      changing last letter of s to that of t; or
         *      remove last letter of s; or
         *      remove last letter of t,
         * any of which is 1 edit plus editing the rest of the strings
         */
        a = levenshtein(s, ls - 1, t, lt - 1);
        b = levenshtein(s, ls,     t, lt - 1);
        c = levenshtein(s, ls - 1, t, lt    );
 
        if (a > b) a = b;
        if (a > c) a = c;
 
        return a + 1;
}

/*
 * Function to be called from Python
 */
static PyObject* py_myFunction(PyObject* self, PyObject* args)
{
  char *s = "Hello from C!";
  return Py_BuildValue("s", s);
}

/*
 * Bind Python function names to our C functions
 */
static PyMethodDef ldModule_methods[] = {
  {"ld", py_myFunction, METH_VARARGS},
  {NULL, NULL}
};

/*
 * Python calls this to let us initialize our module
 */
void initldModule()
{
  (void) Py_InitModule("ldModule", ldModule_methods);
}


