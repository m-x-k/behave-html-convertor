# Behave custom HTML report

Using the behave json report format this script outputs a custom html report.

## Requirements

* Python

## Source code outline

* convertToHtml.py: main python script to convert json into custom html report
* results_template.html: jinja2 template used to build custom html report

## Setup

```
mkvirtualenv behave-custom-html-report
pip install -r requirements.txt
```

## Run

As input you should take the report produced from a behave test run: `behave --format json ...`.

```
python convertToHtml.py -h

usage: convertToHtml.py [-h] [-t T] [-i I] [-c C]

optional arguments:
  -h, --help  show this help message and exit
  -n N        Title for test report
  -i I        Behave json input file
  -o O        Output html file
  -c C        Override css
  -t T        jinja2 template

Example:

python convertToHtml.py -t "Test Report" -i testresults.json -c dark-style.css -o results.html
```

