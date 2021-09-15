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
from count_pru import count_pru
count_pru.count_pru(1000000) # 1 second
```

### Counting (C)
```c
#include <stdio.h>
#include <stdint.h>
#include "cpru_userspace.h"

int main(void)
{
    uint32_t data[4];
    count_pru(1000000, data);

    for(int i = 0; i < 4; i++) printf("Count for %d: %d\n", i, data[i]);
    return 0;
}
```
