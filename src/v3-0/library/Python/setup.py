from distutils.core import setup, Extension

def main():
    setup(name="CountingPRU",
          version="1.0.0",
          description="Python interface for the CountingPRU's counting function",
          author="Guilherme F. de Freitas",
          author_email="guilherme.freitas@cnpem.br",
          ext_modules=[Extension("CountingPRU", ["count.c"])])

if __name__ == "__main__":
    main()

