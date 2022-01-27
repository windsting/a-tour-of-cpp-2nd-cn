#!/usr/bin/env python3

import index_processor as ip
import unittest

class Test(unittest.TestCase):
    chapter_start_from_page = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        args = ip.parse_args()
        self.convertor = ip.PageNumberConvertor(args.chapter_start_from_page)

    def test_chapter_of_page(self):
        valid_values = {1:1,117:9,147:11,226:16}
        for p,c in valid_values.items():
            cc = self.convertor.chapter_of_page(p)
            self.assertEqual(cc,c,f"chapter of page:{p} should be {c}, got {cc}")
        self.assertRaises(ValueError,self.convertor.chapter_of_page,0)
        self.assertRaises(ValueError,self.convertor.chapter_of_page,227)

    def test_convert_line(self):
        cases = {
            '## Token':'## Token',
            '    - container 147':'    - container [147](ch11.md#147)',
            '- `%=`, operator    7':'- `%=`, operator    [7](ch01.md#7)'
        }
        for l,nl in cases.items():
            new_line = self.convertor.convert_line(l)
            self.assertEqual(new_line,nl,f"result of \t[{l}] \nshould be\t[{nl}], \ngot\t\t[{new_line}]")

    def test_get_link(self):
        cases = {
            (147,11):'[147](ch11.md#147)'
        }
        for pc,link in cases.items():
            got_link = ip.PageNumberConvertor.gen_link(pc[0],pc[1])
            self.assertEqual(got_link,link,f"result of \t[{pc}] \nshould be\t[{link}], \ngot\t\t[{got_link}]")

    def test_rreplace(self):
        cases = [
            ('something old', 'old', 'new', 'something new')
        ]
        for case in cases:
            new_str = ip.rreplace(case[0],case[1],case[2])
            self.assertEqual(new_str,case[3])

if __name__ == '__main__':
    unittest.main()
