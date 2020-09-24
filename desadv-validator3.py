import argparse, unittest
from colorama import init, Fore, Back, Style
from pydifact.segmentcollection import SegmentCollection
collection = SegmentCollection.from_file("G:\\GitHub\\desadv-validator\\tests\\DESADV_line_break.txt")
# collection = SegmentCollection.from_str("UNA:+,? 'UNH+1+ORDERS:D:96A:UN:EAN008'")

# for segment in collection.segments:
#     print('{}: {}'.format(segment.tag, segment.elements))

for each in collection.get_segments('RFF'):
    print(each)
print('----')
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

unt_counter = 0

class DESADVFehler():
    # pass
    UNB_RCV = False
    UNB_REF = False
    UNB_REF_C = ''
    UNB_TST = False
    UNH_VER = ''
    BGM_TYP = ''
    BGM_NO = ''
    BGM_NO_C = ''
    RFF_DQ = False
    RFF_DQ_C = ''
    LIN_QLF = False
    LIN_QLF_C = ''
    LIN_GTIN = False
    LIN_GTIN_C = ''
    GIN_BJ = False
    GIN_BJ_C = ''
    UNT_CNT = False
    UNT_CNT_C = ''
    UNZ_REF = False
    UNZ_REF_C = ''



def CheckDESADV(self, err):

    unt_counter = 0
    # Tests for DESADV quality
    # - correct receiver GLN in UNB
    # - BGM+351 present and filled
    # - RFF+DQ vorhanden?
    # - LIN filled with GTIN and correct qualifier (96A vs 01B)
    # - GIN+BJ with NVE (required for GH)
    # - correct counter in UNT
    # - correct reference in UNZ
    
    for segment in collection.segments:   
        if segment.tag == 'UNB':
            rcv = segment.elements[2][0]
            ref = segment.elements[4]
            # print('UNB Content: {}'.format(segment.elements))
            # print('UNB Receiver: {}'.format(segment.elements[2][0]))
            # print('UNB Reference: {}'.format(segment.elements[4]))
            if rcv == '4311501990018':
                err.UNB_RCV = True 
            
            
            print(fail_msg + 'EDI-Center GLN in UNB, "{}"'.format(rcv)) if rcv != '4311501990018' else print(success_msg + 'EDI-Center GLN in UNB, "{}"'.format(rcv))
            # print(fail_msg + 'UNB-Referenz fehlt, "{}"'.format(ref)) if not ref else print(success_msg + 'UNB-Referenz vorhanden, "{}"'.format(ref))

            continue

        elif segment.tag == 'UNH':
            unh_version = segment.elements[1][2]
            # print('UNH Version: {}'.format(segment.elements[1][2]))
            unt_counter = unt_counter + 1

        elif segment.tag == 'BGM':
            bgm_no = segment.elements[1]
            bgm_type = segment.elements[0][0]
            if bgm_type == 'YC5':
                # print('BGM+{} found.'.format(bgm_type))
                # print(fail_msg + 'DESADV-Nr fehlt, "{}"'.format(bgm_no)) if not bgm_no else print(success_msg + 'DESADV-Nr vorhanden, "{}"'.format(bgm_no))
                print(info_msg + 'Crossdocking Qualifier gefunden "{}"'.format(bgm_type))
            elif bgm_type == '351':
                pass
            else:
                print(fail_msg + 'Unbekannter Qualifier gefunden in "{}"'.format(segment))
            print(fail_msg + 'DESADV-Nr fehlt, "{}"'.format(bgm_no)) if not bgm_no else print(success_msg + 'DESADV-Nr vorhanden, "{}"'.format(bgm_no))
                
                
            unt_counter = unt_counter + 1

        # elif segment.tag == 'RFF':
        #     unt_counter = unt_counter + 1

        #     if segment.elements[2][0]:
        #         lin_gtin = segment.elements[2][0]
        #         lin_qualifier = segment.elements[2][1]


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

fehler = DESADVFehler()
CheckDESADV(collection, fehler)

print(fail_msg + 'falsch "{}"'.format(fehler.UNB_RCV)) if fehler.UNB_RCV else print(success_msg + 'richtig "{}"'.format(rcfehler.UNB_RCVv))
