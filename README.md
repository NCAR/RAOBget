# RAOBget

This repository contains scripts to download RAOBS from the University of
Wyoming Radiosonde Archive by building URLs like:

 * for accessing TEXT:LIST data:
```
http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2019&MONTH=05&FROM=2812&TO=2812&STNM=72672
```
 * for accessing GIF:SKEWT images:
```
http://weather.uwyo.edu/upperair/images/2019052812.72672.skewt.parc.gif
```

To run the code, use the command:
```
> cd src
> python3 RAOBget.py <-h>
```
The -h option lists and identifies the parameters you can pass to the code, like requested station id and dates. So for example, **python3 RAOBget.py --raobtype TEXT:LIST --now --stnm DNR** will download the latest 12-hour sounding from Denver/Stapleton.

For use with the NCAR/EOL field catalog, use the command:
```
> cd src
> python3 RAOBget.py --config ../config/catalog.yml [--stnm <station number> or --rsl <station_list_file>] [--freq <[3,6,12]>]
```
(or edit the sample config file, config/catalog.yml, and add stnm or rsl keywords)

**NCAR/EOL users: To run on barolo, you need to use /opt/local/anaconda3/bin/python3.7 as
this is the only place PyQt5 is installed. Even if you are not using the
GUI mode, the code will look for the PyQt5 library and fail.**

For use with the NCAR/EOL MTP, use the GUI to set all the needed metadata:
```
python3 RAOBget.py --gui
```

If you need help reading skewT plots, a good reference is the COMET MetEd module:
https://www.meted.ucar.edu/training_module.php?id=225#.XXrMpZNKiwQ

### To run on a mac ###

 * pip3 install PyYAML

Either:
```
 * install conda
 * conda install -c conda-forge metpy
```
Or:
```
 * brew install geos
 * brew install proj
 * pip3 install cython
 * pip3 install git+https://github.com/SciTools/cartopy.git@master  (see http://louistiao.me/posts/installing-cartopy-on-mac-osx-1011/)
```

### Developer Notes ###

For complete documentation on each class/method, useful if you need to modify the code, use pydoc to extract embedded documentation from each file:
```
> cd src
> python3 -m pydoc <filename>
```
e.g. python3 -m pydoc lib/rwget.py 

To manually run all unittests:
```
> cd src
> python3 -m unittest discover -s ../test -v
```

A [linter](https://en.wikipedia.org/wiki/Lint_\(software\)) can be another useful tool. I used flake8
```
> python3 -m pip install flake8
> flake8 <path/to/code> or <path/to/file.py>
```
e.g
```
> flake8 .
```

### References ###
This code uses the SkewT plot function from metpy to display downloaded
TEXT:LIST-formatted data for visual QC:

May, R. M., Arms, S. C., Marsh, P., Bruning, E. and Leeman, J. R., 2017:
    MetPy: A Python Package for Meteorological Data.
    Unidata, Accessed 31 March 2017.
    [Available online at https://github.com/Unidata/MetPy.]
    doi:10.5065/D6WW7G29.
