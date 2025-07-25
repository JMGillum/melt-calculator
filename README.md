See https://git-scm.com/book/en/v2/Git-Tools-Submodules for information on submodules


Invoke the script by callling it from the command line. Either:
`python3 main.py` or `python main.py`

pass `--help` as a command line argument to get a list of supported arguments.

Completed:
* Filtering by bullion is possible
* refactored setup and project structure
* Renamed CountryName to AlternativeNames and applied across denomination names
* Able to search for bullion by "face_value" (decimal of ounce ex: 1/4 oz would be 0.25 face value)
* Able to provide a division operation as a face value ex: 1/4 instead of 0.25
