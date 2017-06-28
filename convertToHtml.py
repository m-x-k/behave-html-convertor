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
    overall_status = "passed"
    total_scenarios = 0
    total_scenarios_passed = 0
    total_scenarios_failed = 0
    total_scenarios_skipped = 0
    total_steps = 0
    total_steps_passed = 0
    total_steps_failed = 0
    total_steps_skipped = 0
    total_duration = 0
    features = []
    for result in results:
        feature = get_feature(result)
        features.append(feature)
        total_duration += feature.get('duration')
        status = feature.get('status')
        if status == "failed":
            overall_status = "failed"

        scenarios = feature.get('scenarios', {})
        total_scenarios += scenarios.get('total', 0)
        total_scenarios_failed += scenarios.get('failed', 0)
        total_scenarios_passed += scenarios.get('passed', 0)
        total_scenarios_skipped += scenarios.get('skipped', 0)

        steps = scenarios.get('steps', {})
        total_steps += steps.get('total', 0)
        total_steps_failed += steps.get('failed', 0)
        total_steps_passed += steps.get('passed', 0)
        total_steps_skipped += steps.get('skipped', 0)

    stats = {
        "features": features,
        "overall_status": overall_status,
        "total_scenarios": total_scenarios,
        "total_scenarios_passed": total_scenarios_passed,
        "total_scenarios_failed": total_scenarios_failed,
        "total_scenarios_skipped": total_scenarios_skipped,
        "total_steps": total_steps,
        "total_steps_passed": total_steps_passed,
        "total_steps_failed": total_steps_failed,
        "total_steps_skipped": total_steps_skipped,
        "total_duration": total_duration,
        "total_features": len(features)
    }
    return stats


def get_feature(result):
    scenarios = result.get("elements")

    duration = 0

    total_scenarios = 0
    passed_scenarios = 0
    failed_scenarios = 0
    skipped_scenarios = 0

    total_steps = 0
    passed_steps = 0
    failed_steps = 0
    skipped_steps = 0

    for scenario in scenarios:
        if scenario.get('keyword', '').lower() == "scenario":
            total_scenarios += 1
            # Default to passed unless skipped
            passed = True
            skipped = False
            for step in scenario.get('steps', []):
                result = step.get('result', {})
                duration += result.get('duration', 0)
                status = result.get('status', 'skipped')
                if status:
                    total_steps += 1
                    if status == "passed":
                        passed_steps += 1
                    elif status == "failed":
                        failed_steps += 1
                        passed = False
                    elif status == "skipped":
                        skipped_steps += 1
                        skipped = True

            if skipped:
                skipped_scenarios += 1
            elif passed:
                passed_scenarios += 1
            else:
                failed_scenarios += 1

    feature = {
        "name": result.get("name"),
        "scenarios": {
            "steps": {
                "total": total_steps,
                "passed": passed_steps,
                "failed": failed_steps,
                "skipped": skipped_steps
            },
            "total": total_scenarios,
            "passed": passed_scenarios,
            "failed": failed_scenarios,
            "skipped": skipped_scenarios
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
