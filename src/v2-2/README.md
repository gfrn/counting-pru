## CountingPRU - _SIRIUS_
_PRU-based Counters_  



_Author:_

Patricia H. Nallin ( _patricia.nallin@lnls.br_ )

_____


### Building the library

Run the script ´library_build.sh´. This will compile PRU and host codes, install it to your Beaglebone and create a Python module to use these libraries.



_____

### Using the library


_**Before using it**_

1. Apply the Device Tree Overlay (DTO) to configure Beaglebone pins to PRU. Run `DTO_CountingPRU.sh` script.

2. In your python code, you can just:
```python
import CountingPRU
```  

---


_**Available Methods**_

- ```Init()```

PRU initialization. Shared memory configuration and loading binaries into both PRUs.  


- ```Counting(time_base)```

Starts counting during time_base period, in seconds. This method will be blocking until the end of counting.  
Returns: list of 8 itens (32-bit integer each), corresponding to a channel counter value


- ```Close()```

Closes PRUs and memory mapping.