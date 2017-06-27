from jinja2 import Template, Environment, FileSystemLoader
from os.path import split
from json import loads


def render(tpl_path, context):
    path, filename = split(tpl_path)
    return Environment(
        loader=FileSystemLoader(path or './')
    ).get_template(filename).render(results=context)


if __name__ == '__main__':
    read_data = []
    with open('testresults.json', 'r') as f:
        read_data = f.read()
    f.closed

    read_data = loads(read_data)
    result = render('results_template.html', read_data)
    print(result)
