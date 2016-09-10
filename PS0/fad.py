import sys

python_version = sys.version
numpy_installed = False
matplotlib_installed = False

try:
    import numpy
    numpy_installed = True
except:
    pass

try:
    import matplotlib
    matplotlib_installed = True
except:
    pass

print("Version:", python_version)
if numpy_installed:
    print("Numpy installed")
else:
    print("Numpy NOT installed")
if matplotlib_installed:
    print("Matplotlib installed")
else:
    print("Matplotlib NOT installed")