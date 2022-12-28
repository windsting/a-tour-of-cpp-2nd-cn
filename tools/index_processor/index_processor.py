#!/usr/bin/env python3

"""A tool to convert page number in index to a link.
"""

from io import TextIOWrapper
import sys
import argparse

def rreplace(s:str, old:str, new:str, occurrence:int = 1) -> str:
    li = s.rsplit(old, occurrence)
    return new.join(li)

class PageNumberConvertor():
    def __init__(self, chapter_start_from_page: list[int]) -> None:
        self.chapter_start_from_page = chapter_start_from_page
        pass
    def chapter_of_page(self, page_number:int):
        csfp = self.chapter_start_from_page
        if page_number < csfp[0]:
            raise ValueError(f'page_number {page_number} is smaller than start page number of any chapter?')
        for index,value in enumerate(csfp):
            if page_number < value:
                return index
        raise ValueError(f'page_number {page_number} is larger or equal than end page number of last chapter?')
    def gen_link(page: int, chapter:int) -> str:
        return f"[{page}](ch{str(chapter).zfill(2)}.md#{page})"
    def convert_page_number(self, page_string: str) -> str:
        page_number = int(page_string)
        chapter = self.chapter_of_page(page_number)
        link = PageNumberConvertor.gen_link(page_number, chapter)
        return link
    def convert_page_numbers(self, page_strings: list[str]) -> str:
        cp = self.convert_page_number
        links = [cp(word) for word in page_strings]
        return ','.join(links)
    def convert_line(self, line:str) -> str:
        words = line.split()
        if len(words) <= 1:
            return line
        last_word = words[len(words)-1]
        last_words = None
        if not last_word.isdigit():
            last_words = last_word.split(',')
            if not all(w.isdigit() for w in last_words):
                return line
        cp = self.convert_page_number
        cps = self.convert_page_numbers
        link = cp(last_word) if last_words is None else cps(last_words)
        new_line = rreplace(line, last_word, link)
        return new_line
    def convert_file(self, infile: TextIOWrapper, outfile: TextIOWrapper):
        for line in infile:
            new_line = self.convert_line(line)
            outfile.write(new_line)
    pass

def parse_args(arg_list=None):
    default_chapter_start_from_page = [1,21,29,47,65,79,93,107,111,123,137,149,163,187,195,207,227]

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    parser.add_argument('-c', '--chapter-start-from-page', nargs="*",
                        type=int, default=default_chapter_start_from_page)
    parser.add_argument('-o', '--outfile', help="Output file",
                        default=sys.stdout, type=argparse.FileType('w'))

    args = parser.parse_args(arg_list) if arg_list else parser.parse_args()
    return args

def main():
    args = parse_args()
    # print(args)
    convertor = PageNumberConvertor(args.chapter_start_from_page)
    convertor.convert_file(args.infile, args.outfile)

if __name__ == '__main__':
    sys.exit(main())
