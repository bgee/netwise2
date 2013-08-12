

#include <Python.h>
#include <string.h>
#include <stdio.h>
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
 * Function to be called from Python, ld function wrapper
 */
static PyObject* py_myFunction(PyObject* self, PyObject* args)
{
  char *s = "Hello from C!";
  //return Py_BuildValue("s", s);
  char *str1, *str2;
  int len_str1, len_str2;
  
  if (!PyArg_ParseTuple(args, "ss", &str1, &str2)){
    exit(5);
  }
  len_str1 = strlen(str1);
  len_str2 = strlen(str2);
  //printf("%s", x);
  int ld = levenshtein(str1, len_str1, str2, len_str2);
  return Py_BuildValue("i", ld);
  
}

/* 
 * the function to find the match with smallest ld
 * assume str1 is longer than str2
 */
static PyObject* find_match(PyObject* self, PyObject* args)
{
  char *str1, *str2;
  int len_str1, len_str2;
  if (!PyArg_ParseTuple(args, "ss", &str1, &str2)){
    exit(5);
  }
  len_str1 = strlen(str1);
  len_str2 = strlen(str2);
  // the size of matrix indicates the possible ways to map
  // the shorter string onto the longer string
  int matrix_size = len_str1+1-len_str2;
  
  int matrix[matrix_size];
  int i;
  for(i=0; i<matrix_size; i++){
    char *match;
    //strncpy(match, str1+i, (size_t)len_str2);
    sprintf(match, "%.*s", len_str2, str1);
    matrix[i] = levenshtein(match, len_str2, str2, len_str2);
  }
  int min_ld = len_str2;
  int location;
  for (i=0; i<matrix_size; i++){
    if (matrix[i] < min_ld){
      min_ld = matrix[i];
      location = i;
    }
  }
  char *test;
  //strncpy(test, str2+location, len_str2);
  return Py_BuildValue("i", min_ld);
}

/*
 * Bind Python function names to our C functions
 */
static PyMethodDef ldModule_methods[] = {
  {"ld", py_myFunction, METH_VARARGS},
  {"find_match", find_match, METH_VARARGS},
  {NULL, NULL}
};

/*
 * Python calls this to let us initialize our module
 */
void initldModule()
{
  (void) Py_InitModule("ldModule", ldModule_methods);
}


