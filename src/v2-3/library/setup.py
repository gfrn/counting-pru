#!/usr/bin/env python-sirius

"""
setup.py file for CountingPRU
"""


from setuptools import setup



with open('VERSION','r') as _f:
    __version__ = _f.read().strip()



dist = setup (name = 'CountingPRU',
              version = __version__,
              description = """Counting interface via Beaglebone PRU""",
              author      = "Patricia Nallin",
              author_email= "patricia.nallin@lnls.br",
              url         = "https://gitlab.cnpem.br/patricia.nallin/counting-pru.git",
              packages    = ["CountingPRU"],
              package_data = {'CountingPRU': ['VERSION']},
              license     = "BSD",
              platforms   = ["Debian Beaglebone"],
)
