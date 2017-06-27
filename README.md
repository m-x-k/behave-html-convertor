# Behave custom HTML report

THIS IS A WORK IN PROGRESS!!!

Based on the standard behave report format this script outputs a custom html report.

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

* A sample testresults.json file has been provided but this would typically come from running behave with the necessary parameter setting.

```
python convertToHtml.py > results.html
```
