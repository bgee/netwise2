

#include <Python.h>
#include <string.h>
#include <stdio.h>
#include <string.h>

//http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#C
#define MIN3(a, b, c) ((a) < (b) ? ((a) < (c) ? (a) : (c)) : ((b) < (c) ? (b) : (c)))
int levenshtein(char *s1, char *s2) {
    unsigned int x, y, s1len, s2len;
    s1len = strlen(s1);
    s2len = strlen(s2);
    unsigned int matrix[s2len+1][s1len+1];
    matrix[0][0] = 0;
    for (x = 1; x <= s2len; x++)
        matrix[x][0] = matrix[x-1][0] + 1;
    for (y = 1; y <= s1len; y++)
        matrix[0][y] = matrix[0][y-1] + 1;
    for (x = 1; x <= s2len; x++)
        for (y = 1; y <= s1len; y++)
            matrix[x][y] = MIN3(matrix[x-1][y] + 1, matrix[x][y-1] + 1, matrix[x-1][y-1] + (s1[y-1] == s2[x-1] ? 0 : 1));
 
    return(matrix[s2len][s1len]);
}

//http://rosettacode.org/wiki/Levenshtein_distance#C
/* s, t: two strings; ls, lt: their respective length */


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
  //int ld = levenshtein(str1, len_str1, str2, len_str2);
  int ld = levenshtein(str1, str2);
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
  if (len_str1 <= len_str2){
    return Py_BuildValue("i", 0);
  }
  // the size of matrix indicates the possible ways to map
  // the shorter string onto the longer string
  int matrix_size = len_str1+1-len_str2;
  //return Py_BuildValue("i", matrix_size);
  //int matrix[matrix_size];
  int *matrix = malloc(matrix_size * sizeof(int));
  int i;
  for(i=0; i<matrix_size; i++){
    //char *match;
    //strncpy(match, str1+i, (size_t)len_str2);
    //sprintf(match, "%.*s", len_str2, str1+i);
    char *match = (char*) malloc(len_str2);
    strncpy(match, str1+i, len_str2);
    // return Py_BuildValue("s", match);
    matrix[i] = levenshtein(match, str2);
    free(match);
  }
  int min_ld = len_str2;
  int location = 0;
  for (i=0; i<matrix_size; i++){
    if (matrix[i] < min_ld){
      min_ld = matrix[i];
      location = i;
    }
    /*if (i==8){
       return Py_BuildValue("s", match);}*/
  }
  char *test;
  //strncpy(test, str2+location, len_str2);
  return Py_BuildValue("i", location);
}

/*
 * Bind Python function names to our C functions
 */
static PyMethodDef ldModule_methods[] = {
  {"levenshtein", py_myFunction, METH_VARARGS},
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


