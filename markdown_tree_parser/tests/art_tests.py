import unittest

from parser import parse_string


class TestParser(unittest.TestCase):

    def test_parse(self):
        with open('example_1.md') as f:
            text = f.read()

        out = parse_string(text)

        with open('out.md', 'w') as f:
            f.write(out.full_source)

        self.assertEqual(out.title, 'Title')
        self.assertEqual(out.source, None)

        self.assertEqual(out.root.text, 'Title')
        self.assertEqual(out.root.source, '')

        self.assertEqual(out.root[0].text, 'Sub Title')
        self.assertEqual(out.root[0].source, '')

        self.assertEqual(out[0].text, 'Hello')
        self.assertEqual(out[0].source, 'Some text\n')

        self.assertEqual(out[1].text, 'Hello 2')
        self.assertEqual(out[1].source, '')

        self.assertEqual(out[1][0].text, 'Hello 3')
        self.assertEqual(out[1][0].source, 'Hello from Russia\n')

        part1 = out[2]
        self.assertEqual(part1.text, 'Part 1')
        self.assertEqual(part1.source, '\nThis is the main part\n')
        chapter1 = part1[0]
        self.assertEqual(chapter1.text, 'Chapter 1')
        self.assertEqual(chapter1.source, '\nLong ago, somewhere in a distant faraway galaxy.\n\nSome text...\n')
        self.assertEqual(chapter1[0].text, 'Sub Chapter 1.1')
        self.assertEqual(chapter1[0].source, '\nDance With th Dead - Sunset\n')
        chapter2 = part1[1]
        self.assertEqual(chapter2.text, 'Chapter 2')
        self.assertEqual(chapter2.source, '\nThis is the middle chapter\n')
        self.assertEqual(chapter2[0].text, 'Sub Chapter 2.1')
        self.assertEqual(chapter2[0].source, '\nDocument your code\n')
        self.assertEqual(chapter2[1].text, 'Sub Chapter 2.2')
        self.assertEqual(chapter2[1].source, '\nComponents File Manager\n')

        self.assertEqual(out.full_source, text)

    def test_heading_diff(self):
        text = '''

## Heading 3

# Heading 2
'''
        out = parse_string(text)
        self.assertEqual(out[0].text, 'Heading 3')
        self.assertEqual(out.root.text, 'Heading 2')

    def test_code_block(self):
        text = '''
Title
=====

# Code

Code 1
------
Some text
```
# TODO
```

Code 2
------
```python
# TODO
print('test')
```

# Heading
'''
        out = parse_string(text)
        self.assertEqual(out.title, 'Title')
        self.assertEqual(out[0][0].text, 'Code 1')
        self.assertEqual(out[0][0].source, 'Some text\n```\n# TODO\n```\n')
        self.assertEqual(out[0][1].text, 'Code 2')
        self.assertEqual(out[0][1].source, "```python\n# TODO\nprint('test')\n```\n")
        self.assertEqual(out[1].text, 'Heading')


if __name__ == '__main__':
    unittest.main()