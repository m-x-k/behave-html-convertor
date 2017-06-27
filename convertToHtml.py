import math
import argparse
from jinja2 import Template, Environment, FileSystemLoader
from os.path import split
from json import loads


def render(tpl_path, results, report_stats, css_content, general_content):
    path, filename = split(tpl_path)
    return Environment(
        loader=FileSystemLoader(path or './')
    ).get_template(filename).render(results=results,
                                    report_stats=report_stats,
                                    css_content=css_content,
                                    general=general_content)

def get_report_stats(results):
    features = []
    for result in results:
        features.append(get_feature(result))

    stats = {
        "features": features
    }

    return stats

def get_feature(result):
    scenarios = result.get("elements")

    duration = 0
    total = len(scenarios)
    passed = 0
    failed = 0
    skipped = 0

    for scenario in scenarios:
        if scenario.get('keyword', '').lower() == "scenario":
            for step in scenario.get('steps', []):
                duration += step.get('result', {}).get('duration', 0)
                status = step.get('result', {}).get('status', 'skipped')
                if status:
                    if status == "passed":
                        passed += 1
                    elif status == "failed":
                        failed += 1
                    elif status == "skipped":
                        skipped += 1

    feature = {
        "name": result.get("name"),
        "scenarios": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped
        },
        "duration": int(math.ceil(duration)),
        "status": result.get('status')
    }
    return feature


def read(filename):
    read_data = []
    with open(filename, 'r') as f:
        read_data = f.read()
    f.closed
    return read_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        default="Test Report",
                        help="Title for test report")
    parser.add_argument("-i",
                        default="testresults.json",
                        help="Behave json input file")
    parser.add_argument("-c",
                        default="light-style.css",
                        help="Override css")
    args = parser.parse_args()
    inputfile = args.i
    cssfile = args.c

    general_content = {
        "title": args.t
    }

    css_content = read(filename=cssfile)
    results = loads(read(filename=inputfile))
    report_stats = get_report_stats(results)
    result = render('results_template.html',
                    results,
                    report_stats,
                    css_content,
                    general_content)
    print(result)
