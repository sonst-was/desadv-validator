import argparse
import os
from typing import BinaryIO, Iterable, Iterator, Tuple, Dict, Union
import sys
from io import BufferedReader, BytesIO, FileIO
from collections.abc import Iterable
from collections import OrderedDict


def lprint(line: str, lineno: int, line_numbers: bool = False) -> None:
    """Print a line with optional line number"""
    if line_numbers:
        print("{0: >6}\t{1}".format(lineno + 1, line))
    else:
        print(line)


def openfiles(filenames: Iterable) -> Tuple[str, Iterator[BinaryIO]]:
    """Take an iterable of filenames and yields (filename, file object) tuples"""
    if not filenames:
        filenames = ['-']
    for filename in filenames:
        if filename == '-':
            yield 'stdin', sys.stdin.buffer
        else:
            with open(filename, 'rb') as file:
                yield filename, file


def output(filenames: Iterable, line_numbers: bool = False) -> int:
    ret_code = 0
    lineno = 0
    try:
        for filename, file in openfiles(filenames):
            for lineno, line in enumerate(readdocument(file, filename)):
                lprint(line, lineno, line_numbers)
            ret_code = ret_code or int(lineno == 0)
    except BrokenPipeError:
        sys.stdout = os.fdopen(1)  # suppress "Exception ignored in: [...]" when pager terminates.
    return ret_code

# ISA has fixed width elements. These should all be equal. 103 is official sep.element position
# isa_element_sep = [3, 6, 17, 20, 31, 34, 50, 53, 69, 76, 81, 83, 89, 99, 101, 103]
# isa_example = "ISA*00*          *00*          *ZZ*SOMEBODYELSE   *ZZ*MAYBEYOU       *171231*2359*U*00401*000012345*0*P*:~"  # noqa


def readdocument(edi: Union[str, BinaryIO], filename: str = 'stream', encoding: str ='latin-1') -> Iterator[str]:
    """Splits text on a line_break character (unless preceeded by an escape character)."""
    if isinstance(edi, str):
        sep = detect(edi)
        edi = BytesIO(edi.encode(encoding))
    else:
        edi = BufferedReader(edi)
        sep = detect(str(edi.peek(), encoding))
    if not sep:
        print("Skipping...%s" % filename, file=sys.stderr)
        return

    line_break = bytes(sep['segment'], 'ascii')
    escape = bytes(sep['escape'], 'ascii') if 'escape' in sep else None
    blacklist = {b'\r', b'\n'} if sep.get('hard_wrap') else set()
    last = ''
    buf = []

    while True:
        character = edi.read(1)  # EOF returns b''
        if character in blacklist:
            continue
        buf.append(str(character, encoding))
        if (character == line_break and last != escape) or character == b'':
            line = "".join(buf).strip()
            buf[:] = []
            if line:
                yield line
            if character == b'':
                break
        last = character  # previously read character


def detect(text: str) -> Dict[str, str]:
    """Takes an EDI string and returns detected separators as a dictionary."""

    sep = {}
    # EDI X12: begins with ISA (106 chars) followed by a GS segment
    # if text.startswith('ISA'):
    #     if 'GS' in text[106:110] and len(set([text[pos] for pos in isa_element_sep])) == 1:
    #         sep = {'element': text[103],
    #                'subelement': text[104],
    #                'segment': text[105],
    #                'suffix': text[106:text.find('GS')]}
    #         if text[82] != 'U':  # X12 before repetition has 'U' here.
    #             sep['repetition'] = text[82]
    #     else:
    #         print("Invalid X12 ISA Header (expected 16 fixed width fields, 106 characters wide)",
    #               "Expected: %s" % isa_example,
    #               "Received: %s" % (text[:106]),
    #               file=sys.stderr, sep="\n")

    # Edifact UNA: begins with UNA followed by UNB or UNG
    # elif 
    if text.startswith('UNA') and 'UN' in text[3:13]:
        # ex: """UNA:+.? '\r\nUN..."""
        sep = {'subelement': text[3],
               'element': text[4],
               'release': text[6],
               'segment': text[8],
               'suffix': text[9:text.find('UN')]}
        if text[7] != ' ':  # Edifact before repetition has ' ' here.
            sep['repetition'] = text[7]
    # Edifact no UNA: begins with UNB followed by UNH
    elif text.startswith('UNB') and 'UN' in text[3:13]:
        sep = {'subelement': ':',
               'element': '+',
               'segment': "'",
               'release': '?',
               'repetition': '*',
               'suffix': text[text.find("'") + 1:text.find('UN', 3)]}
    else:
        print("Found something that doesn't look like EDI: %r" % text[:8], file=sys.stderr)

    # This detects "hard wrapped" EDI files where a CRLF is inserted every 80 chars
    # TODO: Potentially support LF (\n) only hard wrap.
    if (len(text) > 246 and
        text[80] == text[162] == text[244] == '\r' and
        text[81] == text[163] == text[245] == '\n'):
        sep['hard_wrap'] = True
    return sep


filename = 'C:\\Users\\jharms\\OneDrive - primeXchange\\8. Github\\desadv-validator\\desadv_linebreak.txt'
filename = 'G:\\GitHub\\desadv-validator\\tests\\DESADV_line_break.txt'

data = {}
data['RECEIVER_GLN'] = ''
data['REFERENZ'] = ''
data['TESTKENNZEICHEN'] = False

my_file = open(filename, 'rb')
file_content = OrderedDict()

for line_no, line in enumerate(readdocument(my_file)):
    file_content[line_no] = line
    print(str(line_no) + '\t' + line)

    if line.startswith('UNB'):
        data['RECEIVER_GLN'] = line.split(':')[2].split('+')[1]
        if data['RECEIVER_GLN'] != '123':
            print('falsch, line {}'.format(line_no + 1))
        data['REFERENZ'] = line.split(':')[4].split('+')[1]
        try:
            data['TESTKENNZEICHEN'] = True if line.split(':')[4].split('+')[6] else False
        except IndexError:
            data['TESTKENNZEICHEN'] = False
        print('Empfänger: {}, REFERENZ: {}, Kennz: {}'.format(data['RECEIVER_GLN'], data['REFERENZ'], data['TESTKENNZEICHEN']))
        # print('Found UNA at line {}.'.format(line_no))
print('----')
print(file_content[0])
my_file.close()


if data['RECEIVER_GLN'] != '123':
    print('Receiver-GLN falsch')

# def split_desadv(segment: str):

