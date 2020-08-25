import argparse, unittest
from colorama import init, Fore, Back, Style
from pydifact.segmentcollection import SegmentCollection
collection = SegmentCollection.from_file("G:\\GitHub\\desadv-validator\\tests\\DESADV_long.txt")
# collection = SegmentCollection.from_str("UNA:+,? 'UNH+1+ORDERS:D:96A:UN:EAN008'")

# for segment in collection.segments:
#     print('{}: {}'.format(segment.tag, segment.elements))

# for each in collection.get_segments('NAD'):
#     print(each)
# print('----')
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


class DESADV():
    pass

def CheckDESADV(collection):

    unb_receiver = ''
    unb_reference = ''
    unb_test_indicator = ''
    unh_version = ''
    unt_counter = 0

    # Tests for DESADV quality
    # - correct receiver GLN in UNB
    # - BGM+351 present and filled
    # - LIN filled with GTIN and correct qualifier (96A vs 01B)
    # - GIN+BJ with NVE (required for GH)
    # - correct counter in UNT
    # - correct reference in UNZ



    for segment in collection.segments:   
        if segment.tag == 'UNB':
            # print('UNB Content: {}'.format(segment.elements))
            # print('UNB Receiver: {}'.format(segment.elements[2][0]))
            # print('UNB Reference: {}'.format(segment.elements[4]))
            print(fail_msg + 'EDI-Center GLN in UNB') if segment.elements[2][0] == '4311501990018' else print(success_msg + 'EDI-Center GLN in UNB')


        #     unb_receiver = segment.elements[2][0]
        #     unb_reference = segment.elements[4]
        #     continue

        # elif segment.tag == 'UNH':
        #     unh_version = segment.elements[1][2]
        #     print('UNH Version: {}'.format(segment.elements[1][2]))
        #     unt_counter = unt_counter + 1

        # elif segment.tag == 'BGM':
        #     if segment.elements[0][0] == '351':
        #         print('BGM+{} found.'.format(segment.elements[0][0]))
        #         bgm_despatch_advice_no = segment.elements[1]
        #     unt_counter = unt_counter + 1

        # elif segment.tag == 'LIN':
        #     unt_counter = unt_counter + 1
        #     if segment.elements[2][0]:
        #         lin_gtin = segment.elements[2][0]
        #         lin_qualifier = segment.elements[2][1]

        # elif segment.tag == 'GIN':
        #     unt_counter = unt_counter + 1

        # elif segment.tag == 'UNT':
        #     if segment.elements[0] == str(unt_counter):
        #         print('unt counter ok')
        #     else:
        #         print('unt counter not ok, found {}, expected {}'.format(segment.elements[0], unt_counter))
        #     pass

        # elif segment.tag == 'UNZ':
        #     pass

        # else:
        #     unt_counter = unt_counter + 1
        # try:
        #     print('Test marker: {}'.format(bool(segment.elements[10])))
        # except:
        #     print('No test marker')

        # print('{}, {}'.format(segment.tag, segment.elements))

    # print(unt_counter)



CheckDESADV(collection)