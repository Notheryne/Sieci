from scapy.all import *
from scapy.utils import hexdump
import time
import argparse
import atexit

TRANSLATOR = {
    'src': 'Source',
    'dst': 'Destination',
    'type': 'Type',
    'version': 'Version',
    'tc': 'Traffic Class',
    'fl': 'Flow Label',
    'plen': 'Packet Length',
    'nh': 'Next Header',
    'hlim': 'Hop Limit',
    'sport': 'Source Port',
    'dport': 'Destination Port',
    'seq': 'Sequence number',
    'ack': 'Acknowledgment number',
    'dataofs': 'Data offset',
    'reserved': 'Reserved',
    'flags': 'Flags',
    'window': 'Window Size',
    'chksum': 'Checksum',
    'urgptr': 'Urgent Pointer',
    'options': 'Options',
    'load': 'Load',
}
# choices=[''pcp', 'pop', 'icmp']
DESCRIPTIONS = {
    'ip':
        'IP - protokół internetowy (od ang. Internet Protocol) - protokół komunikacyjny warstwy internetu '
        'w modelu TCP/IP. Zbiór ścisłych reguł i kroków postępowania, które są automatycznie wykonywane przez '
        'urządzenia w celu nawiązania łączności i wymiany danych.',
    'ip4':
        'IPv4 - czwarta wersja protokołu komunikacyjnego IP (od ang. Internet Protocol version 4). Identyfikacja '
        'hostów opiera się na adresach IP, dane przesyłane są w postaci datagramów (pakietów telekomunikacyjnych). '
        'Dokładny opis protokołu znajduje się w RFC 791. '
        'Adres IPv4 w postaci dziesiętnej ma formę "x.x.x.x", gdzie x należy do przedziału [0, 255], '
        ' składa się z czterech oktetów (bajtów). Może utrzymać 4,295 mln unikalnych hostów, '
        'co obecnie nie wystarcza, jego następcą został IPv6.',
    'ip6':
        'IPv6 - (ang. Internet Protocol version 6) -protokół komunikacyjny, będący następca IPv4. Podstawowym '
        'zadaniem tej wersji jest rozwiązanie problemu małej puli dostępnych adresów w IPv4. Sposobem '
        'rozwiązania tego problemu jest zwiększenie długości adresu z 32 bitów do 128 bitów, uproszczenie '
        'nagłówka protkołu oraz zapewnienie jego elastyczności poprzez wprowadzenie rozszerzeń. '
        'Dokładne opisy protokołu można znaleźć w RFC 2460 oraz RFC 4291. '
        'Adres zapisuje się jako osiem 16-bitowych bloków zapisanych w systemie szesnastkowym, '
        'oddzielonych dwukropkami.',
    'tcp':
        'TCP - protokół kontroli transmisji lub protokół sterowania transmisją, (ang. '
        'Transmission Control Protocol) - połączeniowy, niezawodny, strumieniowy protokół '
        'komunikacyjny stosowany do przesyłania danych między procesami uruchomionymi'
        'na dwóch różnych maszynach, nalężącymi do wykorzystywanego obecnie stosu TCP/IP. '
        'Korzysta z usług protokołu IP do wysyłania i odbierania danych, a także '
        'w razie potrzeby z ich fragmentacji. Połączenie TCP może znajdować się w jednym '
        'z następujących stanów: LISTEN, SYN-SENT, SYN-RECEIVED, ESTABLISHED, FIN-WAIT-1, '
        'FIN-WAIT-2, CLOSE-WAIT, CLOSING, LAST-ACK, TIME-WAIT, CLOSED.',
    'ftp':
        'FTP - protokół transferu plików (ang. File Transfer Protocol) - protokół komunikacyjny '
        'typu klient-serwer wykorzystujący TCP weedług modelu TCP/IP, umożliwiający dwukierunkowy '
        'transfer plików w układzie serwer FTP - klient FTP. Zdefiniowany w dokumencie RFC 959.',
    'dns':
        'DNS - system nazw domen (ang. Domain Name System) - hierarhiczny, rozproszony system '
        'nazw sieciowych, który odpowiada na zapytania o nazwy domen. Dzięki DNS nazwa '
        'mnemoniczna (np. przyjazna użytkownikowy nazwa domeny) jest tłumaczona na odpowiadający '
        'jej adres. Np. "pl.wikipedia.org" -> "91.198.174.192".',
    'http':
        'HTTP - protokół przesyłania dokumentów hipertekstowych (ang. Hypertext Transfer Protocol) - '
        'protokół sieci WWW. Za jego pomocą przesyła się żadania udostępnienia dokumentów WWW oraz '
        'informacje o kliknięciu odnośnika i informacje z formularzy. Opisany dokładnie w '
        'dokumencie RFC 2616. Jest użyteczny, gdyż udostępnia znormalizowany sposób komunikowania '
        'się między sobą komputerów określając formę żądań oraz odpowiedzi. Metody HTTP to '
        'GET, HEAD, PUT, POST, DELETE, OPTIONS, TRACE, CONNECT, PATCH. Definiuje się także '
        'kody odpowiedzi, jak np:\n'
        '200 - OK,\n'
        '400 - Bad Request (nieprawidłowe zapytanie)\n'
        "418 - I'm a teapot (jestem czajnikiem).",
    'udp':
        'UDP - protokół pakietów użytkownika (ang. User Datagram Protocol) - protokół internetowy stosowany '
        'w warstwie transportowej modelu OSI, nie gwarantujący dostarczenia datagramu. Protokół '
        'bezpołączeniowy, bez mechanizmów kontroli przepływu i retransmisji, w porównaniu do TCP '
        'transmisja jest natomiast o wiele szybsza.',
    'pcp':
        'PCP - protokół kontroli portu (ang. Port Control Protocol) - protokół internetowy określający '
        'jak należy tłumaczyć i przekazać pakiety połączeń IPv4 oraz IPv6. Pozwala także '
        'określić hostowi przekierowywanie portów.',
    'pop':
        'POP - protokół pocztowy (ang. Post Office Protocol) - protokół internetowy z '
        'warstwy aplikacji pozwalający na odbiór poczty elektroniczinej ze zdalnego '
        'serwera do lokalnego komputera poprzez połączenie TCP/IP. Obecnie wykorzystujemy '
        'najczęściej POP3 (wersja 3). Wykorzystywany przez użytkowników do odbioru poczty email.',
    'icmp':
        'ICMP - internetowy protokół komunikatów kontrolnych (ang. Internet Control Message '
        'Protocol - protokół warstwy sieciowej modelu OSI, wykorzystywany w diagnostyce '
        'sieci oraz trasowaniu. Pełni przede wszystkim funkcję kontroli transmisji w sieci. '
        'Wykorzystują go takie programy jak ping i traceroute. Jest dokładnie opisany w RFC 792.'
}


def stringify(data):
    layers = []
    for protocol, headers in data.items():
        layer_description = 'Protocol: {0},'.format(protocol)
        for key, value in headers.items():
            if key in TRANSLATOR:
                if key == 'load' and DECRYPT:
                    add = ' {0}:\n {1}\n'.format(TRANSLATOR[key], hexdump(value, dump=True))
                else:
                    add = ' {0}: {1},'.format(TRANSLATOR[key], value)
            else:
                add = ' {0}: {1},'.format(key, value)
            layer_description += add
        layers.append(layer_description)
    result = ''
    for i in range(len(layers)):
        result += '\t' * i + layers[i] + '\n'
    return result[:-1]


def pkt_callback(pkt):
    PACKETS.append(pkt)
    if VERBOSE == 1:
        x = pkt.show(dump=True)
        x = x.split('###[ ')[1:]
        x = [y.replace('\n', ' ').replace(']###', '').split() for y in x]
        data = {}
        for i in x:
            key = i.pop(0)
            data[key] = {}
            for index in range(0, len(i), 3):
                d = i[index:index + 3]
                data[key].update({d[0]: d[-1]})
        result = stringify(data)
        print(result[:-1])
        print("#######################################")


def load_file():
    print('Ładuję plik...')
    file_name = LOAD
    if '.pcap' not in LOAD:
        file_name += '.pcap'
    pkts = sniff(offline=file_name)
    pkts.show()
    print("###########   PODSUMOWANIE:   ###########")
    print(pkts)


def clean_up():
    if SAVE and not STOP_SAVE:
        print('Zapisuję do pliku...')
        file_name = SAVE
        if '.pcap' not in file_name:
            file_name += '.pcap'
        wrpcap(file_name, PACKETS)


if __name__ == "__main__":
    atexit.register(clean_up)
    PACKETS = []
    parse_args = True
    SAVE = None
    STOP_SAVE = False
    if parse_args:
        parser = argparse.ArgumentParser(
            description='Pozwala zobaczyć i analizować komunikację urządzenia z internetem.'
        )
        parser.add_argument('-de', '--decrypt', default=0,
                            help='czy wyświetlać dane pakietu w formie rozszyfrowanej')
        parser.add_argument('-d', '--describe', default=None, choices=list(DESCRIPTIONS.keys()),
                            help='wyświetl opis danego protokołu')
        parser.add_argument('-c', '--count', default=0, type=int,
                            help='ilość pakietów do wyświetlenia')
        parser.add_argument('-s', '--save', default=None,
                            help='do jakiego pliku .pcap zapisać historię')
        parser.add_argument('-v', '--verbose', default=True, type=int,
                            help='czy opisy pakietów powinny być wyświetlane w konsoli')
        parser.add_argument('-l', '--load', default=None,
                            help='z jakiego pliku .pcap wczytać pakiety')
        args = parser.parse_args()
        DECRYPT = args.decrypt if args.decrypt == 0 else 1
        DESC = args.describe
        COUNT = args.count
        SAVE = args.save
        VERBOSE = 0 if args.verbose == 0 else 1
        LOAD = args.load
        if SAVE and LOAD:
            STOP_SAVE = True
            raise AttributeError("That is not possible.")
    else:
        DECRYPT = False
        DESC = 'ip4'
        COUNT = 3
        SAVE = None
        VERBOSE = 0
        LOAD = None
    if not DESC and not LOAD:
        sniff(prn=pkt_callback, store=0, count=COUNT)
    if DESC:
        print(DESCRIPTIONS[DESC])
    if LOAD:
        load_file()
