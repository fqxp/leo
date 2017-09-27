#!/usr/bin/env python3

from colored import fg, attr
import re
import requests
import sys
import types
import xmltodict


WANTED_SECTIONS = (
    'abbrev',
    'adjadv',
    'praep',
    'subst',
    'verb',
)


def translate(word):
    xml_data = make_request(word)
    data = xmltodict.parse(xml_data)
    translation_data = extract_translations(data)

    print_result(translation_data)


def make_request(word):
    session = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Accept':'application/xml, text/xml, */*; q=0.01',
        'Referer': 'https://dict.leo.org/englisch-deutsch/inhibit'
        }
    xml_url = 'https://dict.leo.org/dictQuery/m-vocab/ende/query.xml?lp=ende&search=%s&side=both&order=basic&partial=show&sectLenMax=16&n=2&filtered=-1&trigger=null' % word
    response = session.get(xml_url, headers=headers)

    return response.text


def extract_translations(data):
    section_list = data['xml']['sectionlist']
    search_word = data['xml']['search']['@normalized']

    return {
        'search': search_word,
        'sections': [
            extract_section(section)
            for section in section_list.get('section', [])
            if section['@sctName'] in WANTED_SECTIONS]
        }


def extract_section(section):
    entries = section['entry'] if type(section['entry']) == list else [section['entry']]

    return {
        'title': section['@sctTitle'],
        'entries': [extract_entry(entry) for entry in entries],
        }


def extract_entry(entry):
    return [
        side['words']['word']
        for side in entry['side']]


def print_result(translation_data):
    search_word = translation_data['search']

    if len(translation_data['sections']) == 0:
        print('%sNo translation found for »%s«.%s' % (fg('red'), search_word, attr(0)))
        return

    for i, section in enumerate(translation_data['sections']):
        if i > 0:
            print()
        print('%s# %s %s' % (attr('bold'), section['title'].upper(), attr(0)))

        for entry in section['entries']:
            print('  %s%-50s     %s%s' % (
                attr(0),
                format_entry(entry[0], search_word),
                format_entry(entry[1], search_word),
                attr(0)))


def format_entry(entry, search_word):
    return highlight_word(
        ', '.join(entry) if type(entry) == list else entry,
        search_word)


def highlight_word(word, highlight_word):
    return re.sub(
        r'(%s)' % highlight_word,
        r'%s\1%s' % (fg('light_green'), attr(0)),
        word,
        flags=re.IGNORECASE)


def main():
    translate(' '.join(sys.argv[1:]))
