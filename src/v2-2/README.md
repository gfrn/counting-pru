## CountingPRU - _SIRIUS_
_PRU-based Counters_

___

_Author:_

Patricia H. Nallin ( _patricia.nallin@lnls.br_ )

_____


_Building the library_

Run the script ´library_build.sh´. This will compile PRU and host codes, install it to your Beaglebone and create a Python module to use these libraries.


_Using the library_

1. Apply the Device Tree Overlay (DTO) to configure Beaglebone pins to PRU. Run ´DTO_CountingPRU.sh´ script.

2. In your python code, you can just:
```python
import CountingPRU
```
