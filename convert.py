import os
import markdown
import codecs

SOURCE_DIR = 'site/source'
DEST_DIR = 'site/html'


def convert_file(path):
    with codecs.open(path, 'r', 'utf-8') as markdown_file:
        md = markdown.markdown('\n'.join(markdown_file.readlines()))
    return template_substitute(get_title(path), md)


def get_title(path):
    return path.rsplit('/', 1)[1].rsplit('.txt', 1)[0]


def template_substitute(title, content):
    with codecs.open('site/templates/page.html', 'r', 'utf-8') as template:
        return '\n'.join(template.readlines()).format(title=title, content=content)


def write_file(path, content):
    with codecs.open(convert_path(path), 'w', 'utf-8') as html_file:
        html_file.write(content)


def get_source_paths():
    return [os.path.join(SOURCE_DIR, f) for f in os.listdir(SOURCE_DIR) if f.endswith('.txt')]


def convert_path(path):
    return path.replace(SOURCE_DIR, DEST_DIR).rsplit('.txt', 1)[0] + '.html'


[write_file(f, convert_file(f)) for f in get_source_paths()]
