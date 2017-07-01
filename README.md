# Behave custom HTML report

[![Build Status](https://travis-ci.org/m-x-k/behave-html-convertor.svg?branch=master)](https://travis-ci.org/m-x-k/behave-html-convertor)

Using the behave json report format this script outputs a custom html report with useful stats on each feature, scenario and step.

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

usage: convertToHtml.py [-h] [-n N] [-i I] [-o O] [-c C] [-t T]

optional arguments:
  -h, --help  show this help message and exit
  -n N        Title for test report
  -i I        Behave json input file
  -o O        Output html file
  -c C        Override css
  -t T        jinja2 template

Example:

python convertToHtml.py -n "Test Report" -i testresults.json -c dark-style.css -t results_template.html -o results.html
```

