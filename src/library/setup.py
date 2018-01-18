#!/usr/bin/env python

"""
setup.py file for CountingPRU
"""


from setuptools import setup


dist = setup (name = 'CountingPRU',
              version = '1.0',
              description = """Counting interface via Beaglebone PRU""",
              author      = "Patricia Nallin",
              author_email= "patricia.nallin@lnls.br",
              url         = "https://git.cnpem.br/patricia.nallin/CountingPRU.git",
              packages    = ["CountingPRU"],
              license     = "BSD",
              platforms   = ["Debian Beaglebone"],
)
