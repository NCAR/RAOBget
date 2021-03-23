
[![DOI](https://img.shields.io/badge/DOI-10.26023/5smy-qp26)](https://doi.org/10.26023/5smy-qp26)

# RAOBget

This repository contains scripts to download RAOBS from the [University of Wyoming Radiosonde Archive](http://weather.uwyo.edu/upperair/sounding.html) by building URLs like:

 * for accessing TEXT:LIST data:
```
http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2019&MONTH=05&FROM=2812&TO=2812&STNM=72672
```
 * for accessing GIF:SKEWT images:
```
http://weather.uwyo.edu/upperair/images/2019052812.72672.skewt.parc.gif
```

## Usage ##
To run on windows 10:

```
- open an xterm
> conda activate (to get the base environment where libraries have been installed)
> python RAOBget.py <-h> ...
```

or create a shortcut to windows10/RAOBget.bat and move it to the desktop and just click on it

To run on a mac:

```
- open an xterm
> python3 RAOBget.py <-h> ...
```

**NCAR/EOL users: To run on barolo, you need to use
/opt/local/anaconda3/bin/python3.7 as this is the only place PyQt5 and other
needed packages are installed. Even if you are not using the GUI mode, the code
will look for the PyQt5 library and fail.**

The -h option lists and identifies the parameters you can pass to the code, like requested station id and dates. So for example, **python3 RAOBget.py --raobtype TEXT:LIST --now --stnm DNR** will download the latest 12-hour sounding from Denver/Stapleton.

For use with the NCAR/EOL field catalog, use the command:

```
> cd src
> python3 RAOBget.py --config config/catalog.yml [--stnm <station number> or --rsl <station_list_file>] [--freq <[3,6,12]>]
```
(or edit the sample config file, config/catalog.yml, and add stnm or rsl keywords)

For use with the NCAR/EOL MTP, use the GUI to set all the needed metadata:
```
python3 RAOBget.py --gui
```
then save your config and for future runs:
```
python3 RAOBget.py --config <configfile>
```
If you need help reading skewT plots, a good reference is the COMET MetEd module:
https://www.meted.ucar.edu/training_module.php?id=225#.XXrMpZNKiwQ

## Dependencies ##

```
 * python3
 * pyqt5
 * PyYAML
 * metpy (which drags in cartopy, hopefully)
```

## Installation ##

### To install on a MAC ###
```
> brew upgrade python (to 3.7.x)
unset PYTHONPATH
> python3 -m pip install PyQt5
> pip3 install pyyaml
> pip3 install metpy
```

### To install on Windows ###
Use miniconda to install all needed packages:
 * https://docs.conda.io/en/latest/miniconda.html
   * download win 64 bit installer for python3.7 and install
 * (Optional) Add Miniconda3 and Miniconda3\condabin to your path
   * Windows search -> type "env" -> click "Edit the system environment variables"
   * In lower "System variables" window, click the "Path" row and click edit
   * Click "New" and add the new paths, e.g.
     * C:\Users\lroot\Miniconda3
     * C:\Users\lroot\Miniconda3\condabin
 * Activate a conda environment (I used the default base environment) - see - https://conda.io/activation 
```
   > conda activate
```
 * Update conda if warned following instructions
 * Install packages
```
   > conda install -c conda-forge metpy
     - Drags in pyqt5 and cartopy. If it doesn't...
   > conda install -c conda-forge pyqt
   > conda install -c conda-forge pyyaml
```
If the packages are not available via the conda-forge channel, you can search for alternative channels at https://anaconda.org

Then install Git (if not already there) and download RAOBget:
 * https://git-scm.com/ -> Download latest per automatic OS detection. Run .exe file to install. I used default settings as suggested by installer, except that I asked to install a desktop icon for “Git Bash”
 * Launch “Git Bash”
 * At the prompt 
```
    git clone http://github.com/NCAR/RAOBget
```
Copy Windows10 bat file from RAOBget/windows10 to desktop
```
cp RAOBget/windows10/RAOBget.bat /c/Users/lroot/Desktop/.
```

## Developer Notes ##

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

## References ##
This code uses the SkewT plot function from metpy to display downloaded
TEXT:LIST-formatted data for visual QC:

May, R. M., Arms, S. C., Marsh, P., Bruning, E. and Leeman, J. R., 2017:
    MetPy: A Python Package for Meteorological Data.
    Unidata, Accessed 31 March 2017.
    [Available online at https://github.com/Unidata/MetPy.]
    doi:10.5065/D6WW7G29.
    
## Other resources ##
If this tool doesn't provide what you need, here are a list of other potential resources:

* The Unidata Siphon Python utility collection can be used to write a simple Python script to download Wyoming Upper Air data into a PANDAS data frame.
https://unidata.github.io/siphon/latest/examples/upperair/Wyoming_Request.html#sphx-glr-examples-upperair-wyoming-request-py

* [Software Component Diagram](https://github.com/NCAR/RAOBget/blob/master/doc/RAOBget%20Component%20Diagram.png)
