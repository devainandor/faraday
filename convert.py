import os
import markdown2
import codecs
import sys

SOURCE_DIR = sys.argv[1] or 'site/source'
DEST_DIR = 'site/html'


def convert_file(path):
    with codecs.open(path, 'r', 'utf-8') as markdown_file:
        html = markdown2.markdown(
            '\n'.join(markdown_file.readlines()),
            extras=['fenced-code-blocks', 'metadata', 'strike'])
    return template_substitute(get_title(path), html)


def get_title(path):
    return path.rsplit('/', 1)[1].rsplit('.txt', 1)[0]


def template_substitute(title, content):
    with codecs.open('site/templates/page.html', 'r', 'utf-8') as template:
        return '\n'.join(template.readlines()).format(
            title=title,
            content=content,
            categories=content.metadata.get('categories', '').strip('[]'),
            tags=content.metadata.get('tags', '').strip('[]'))


def write_file(path, content):
    with codecs.open(convert_path(path), 'w', 'utf-8') as html_file:
        html_file.write(content)


def get_source_paths():
    return [os.path.join(SOURCE_DIR, f) for f in os.listdir(SOURCE_DIR) if f.endswith('.md')]


def convert_path(path):
    return path.replace(SOURCE_DIR, DEST_DIR).rsplit('.txt', 1)[0] + '.html'


[write_file(f, convert_file(f)) for f in get_source_paths()]
