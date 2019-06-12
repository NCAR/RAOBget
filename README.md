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
> python3 RAOBget.py <-h>
```
The -h option lists and identifies the parameters you can pass to the code, like requested station id and dates. So for example, **python3 RAOBget.py --raobtype TEXT:LIST --now --stnm DNR** will download the latest 12-hour sounding from Denver/Stapleton.

### Developer Notes ###

For complete documentation on each class/method, useful if you need to modify the code, use pydoc to extract embedded documentation from each file:
```
> python3 -m pydoc <filename_minus_.py>
```
e.g. python3 -m pydoc rwget. 

To manually run all unittests:
```
> python3 -m unittest -v
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
