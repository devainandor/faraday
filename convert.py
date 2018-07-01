import os
import markdown2
import codecs
import sys
import datetime

SOURCE_DIR = (len(sys.argv) > 1 and sys.argv[1]) or 'site/source'
DEST_DIR = 'site'


def convert_file(path):
    with codecs.open(path, 'r', 'utf-8') as markdown_file:
        html = markdown2.markdown(
            '\n'.join(markdown_file.readlines()),
            extras=['fenced-code-blocks', 'metadata', 'strike'])
    if html.metadata.get('draft') == 'true':
        return ''
    return template_substitute(get_title(path), html)


def get_title(path):
    return path.rsplit('/', 1)[1].rsplit('.md', 1)[0]


def template_substitute(title, content):
    with codecs.open('site/templates/page.html', 'r', 'utf-8') as template:
        return '\n'.join(template.readlines()).format(
            title=title.replace('-', ' '),
            content=content,
            categories=content.metadata.get('categories', '').strip('[]'),
            tags=generate_tags(content.metadata.get('tags', '')),
            published_on=get_date(content.metadata['published_on']))


def get_date(date):
    return datetime.datetime.strftime(
        datetime.datetime.fromisoformat(date),
        '%Y %B %d %A, %H:%M (%Z)'
    )


def generate_tags(raw_tags):
    return ' '.join(['#' + tag for tag in raw_tags.strip('[]').split(', ')])


def write_file(path, content):
    if content == '':
        return
    with codecs.open(convert_path(path), 'w', 'utf-8') as html_file:
        html_file.write(content)


def get_source_paths():
    return [os.path.join(SOURCE_DIR, f) for f in os.listdir(SOURCE_DIR) if f.endswith('.md')]


def convert_path(path):
    if path.endswith('.html'):
        return path
    return path.replace(SOURCE_DIR, DEST_DIR).rsplit('.md', 1)[0] + '.html'


def link_to(f):
    return '<a href="{path}">{title}</a>'.format(
        path=f,
        title=f.replace('-', ' ')[0:-5]
    )


def generate_index():
    with codecs.open('site/templates/index.html', 'r', 'utf-8') as template:
        return '\n'.join(template.readlines()) + '\n'.join([link_to(f) for f in os.listdir(DEST_DIR) if f != 'index.html' and f.endswith('.html')])


[write_file(f, convert_file(f)) for f in get_source_paths()]
[write_file(os.path.join(DEST_DIR, 'index.html'), generate_index())]
