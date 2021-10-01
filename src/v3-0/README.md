# CountingPRU - SIRIUS (Remoteproc)

_PRU-based Counters_

Brazilian Synchrotron Light Laboratory (LNLS/CNPEM) IoT Group

## What's new?

This version aims to incorporate the new Remoteproc standard, utilizing it's messaging protocol instead of shared memory, fixed firmware and some changes to the Python C extension module that aims to improve QoL for future users.

This version contains:
- C library
- Python library
- Firmware (ASM/C)
- Pin config script

## Usage

### Installation (Python)
```sh
cd library/Python && python3 setup.py install
```

### Counting (Python)
```python
from count_pru import count_pru, count_both
count_pru(1000000, 0) # 1 second, PRU 0
count_both(1000000) # Returns data for both PRUs
```

### Counting (C)
```c
#include <stdio.h>
#include <stdint.h>
#include "count.h"

int main(void)
{
    uint32_t data[4];
    count_pru(1000000, 0, data); // 1 second, PRU 0

    for(int i = 0; i < 4; i++) printf("Count for %d: %d\n", i, data[i]);
    return 0;
}
```

## Compiling firmware

1. Copy either `LNLS` or `BergozLNLS` to your workspace
2. Copy the files from `Common/` to the root of your project
3. Download the [PRU support package](https://git.ti.com/cgit/pru-software-support-package/pru-software-support-package/tree?h=master)
4. Extract `include/` to a known location
5. Include the folders `include/` and `include/am335x` in your compilation if you're using CCS
6. Compile! (Preferrably with -O4 and speed optimizations, remoteproc is slower than UIO-PRUSS)
