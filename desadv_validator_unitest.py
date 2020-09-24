import argparse, unittest
from colorama import init, Fore, Back, Style
from pydifact.segmentcollection import SegmentCollection
collection = SegmentCollection.from_file("G:\\GitHub\\desadv-validator\\tests\\DESADV_long.txt")

fail_msg = '[ ' + Fore.RED + '×' + Style.RESET_ALL + ' ] - '
success_msg = '[ ' + Fore.GREEN + '√' + Style.RESET_ALL + ' ] - '
info_msg = '[ ' + Fore.YELLOW + '●' + Style.RESET_ALL + ' ] - '
init(convert=True)
parser = argparse.ArgumentParser(description='Process some integers.')
group = parser.add_mutually_exclusive_group()

group.add_argument("-EH", help="Auswahl von EH, Standard", action="store_true")
group.add_argument("-GH", help="Auswahl von GH", action="store_true")
# parser.add_argument('-hs', '--handelsstufe', default='EH', choices=['EH', 'GH'], help='Zur Spezifikation der Handelsstufe (default: %(default)s)') 
args = parser.parse_args()

if args.GH:
    print('GH')
else:
    print('EH')


class MyTest(unittest.TestCase):
    def test_check_unb(self):
        self.assertNotEqual(segment.elements[2][0], '4311501990018',fail_msg)

    def test_check_bgm_non_emptiness(self, segment):
        self.assertIsNone(segment.elements[1])


for segment in collection.segments:
    if segment.tag == 'UNB':
        