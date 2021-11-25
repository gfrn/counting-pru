#include <unistd.h>
#include <fcntl.h>
#include <sys/poll.h>
#include <Python.h>
#include <stdint.h>

#define DEVICE_NAME0 "/dev/rpmsg_pru30"
#define DEVICE_NAME1 "/dev/rpmsg_pru31"
#define MAX_BUFFER_SIZE 512

char pru0_buf[MAX_BUFFER_SIZE];
char pru1_buf[MAX_BUFFER_SIZE];

static PyObject *count_pru(PyObject *self, PyObject *args) {
    struct pollfd pfd;
    uint8_t pru, wr_stat;
    uint32_t time_base;
    PyObject* py_counts = PyList_New(4);

    if(!PyArg_ParseTuple(args, "Ih", &time_base, &pru)) return NULL;

    if (pru > 1) {
        PyErr_SetString(PyExc_ValueError, "Invalid PRU selected (only PRUs 0 and 1 are available)");
        return NULL;
    }
 
    switch (pru) {
        case 0:
            pfd.fd = open(DEVICE_NAME0, O_RDWR);
            break;
        case 1:
            pfd.fd = open(DEVICE_NAME1, O_RDWR);
            break;
    }

    if (pfd.fd < 0) {
        PyErr_SetString(PyExc_IOError, "Cannot communicate with selected PRU");
        return NULL;
    }

    wr_stat = write(pfd.fd, "-", 2) == -1;
    usleep(time_base-400); // There is a 400 us offset
    if (wr_stat || write(pfd.fd, "-", 2) == -1) {
        PyErr_SetString(PyExc_IOError, "Cannot communicate with selected PRU");
        return NULL;
    }

    if (read(pfd.fd, pru0_buf, MAX_BUFFER_SIZE))
    {
        uint8_t offset = 0;
        uint32_t count = 0;
        for (int i = 0; i < 4; i++) {
            count = (pru0_buf[offset+3] << 24) | (pru0_buf[offset+2] << 16) | (pru0_buf[offset+1] << 8) | pru0_buf[offset];
            PyObject* py_count = Py_BuildValue("I", count);
            PyList_SetItem(py_counts, i, py_count);
            offset+=4;
        }
    }

    read(pfd.fd, pru0_buf, MAX_BUFFER_SIZE);
    close(pfd.fd);

    return py_counts;
}

static PyObject *count_both(PyObject *self, PyObject *args) {
    struct pollfd pfd0, pfd1;
    uint8_t wr_stat;
    uint32_t time_base;
    PyObject* py_counts = PyList_New(8);

    if(!PyArg_ParseTuple(args, "I", &time_base)) return NULL;

    pfd0.fd = open(DEVICE_NAME0, O_RDWR);
    pfd1.fd = open(DEVICE_NAME1, O_RDWR);

    if (pfd0.fd < 0 || pfd1.fd < 0) {
        PyErr_SetString(PyExc_IOError, "Cannot communicate with PRUs");
        return NULL;
    }

    wr_stat = write(pfd0.fd, "-", 2) == -1;
    wr_stat |= write(pfd1.fd, "-", 2) == -1;

    usleep(time_base-400); // There is a 400 us offset

    wr_stat |= write(pfd0.fd, "-", 2) == -1;
    wr_stat |= write(pfd1.fd, "-", 2) == -1;
    if (wr_stat) {
        PyErr_SetString(PyExc_IOError, "Cannot communicate with PRUs");
        return NULL;
    }

    if (read(pfd0.fd, pru0_buf, MAX_BUFFER_SIZE))
    {
        uint8_t offset = 0;
        uint32_t count = 0;
        for (int i = 0; i < 4; i++) {
            count = (pru0_buf[offset+3] << 24) | (pru0_buf[offset+2] << 16) | (pru0_buf[offset+1] << 8) | pru0_buf[offset];
            PyObject* py_count = Py_BuildValue("I", count);
            PyList_SetItem(py_counts, i, py_count);
            offset+=4;
        }
    }

    if (read(pfd1.fd, pru1_buf, MAX_BUFFER_SIZE))
    {
        uint8_t offset = 0;
        uint32_t count = 0;
        for (int i = 0; i < 4; i++) {
            count = (pru1_buf[offset+3] << 24) | (pru1_buf[offset+2] << 16) | (pru1_buf[offset+1] << 8) | pru1_buf[offset];
            PyObject* py_count = Py_BuildValue("I", count);
            PyList_SetItem(py_counts, i+4, py_count);
            offset+=4;
        }
    }


    read(pfd0.fd, pru0_buf, MAX_BUFFER_SIZE);
    read(pfd1.fd, pru1_buf, MAX_BUFFER_SIZE);
    close(pfd0.fd);
    close(pfd1.fd);

    return py_counts;
}

static PyMethodDef CountMethod[] = {
    {"count_pru", count_pru, METH_VARARGS, "Python interface for CountingPRU's counting function (single PRU)"},
    {"count_both", count_both, METH_VARARGS, "Python interface for CountingPRU's counting function (both PRUs)"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef countingpru_module = {
    PyModuleDef_HEAD_INIT,
    "CountingPRU",
    "Python interface for CountingPRU's counting function",
    -1,
    CountMethod
};

PyMODINIT_FUNC PyInit_CountingPRU(void) {
    return PyModule_Create(&countingpru_module);
}

