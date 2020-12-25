import netmiko

from netmiko import ConnectHandler
cse01=('192.1.1.254')
#cse02=('135.241.247.102')
#rse01=('135.241.247.103')
#rse02=('135.241.247.104')

#cse03=('135.241.247.201')
#cse04=('135.241.247.202')
#rse03=('135.241.247.203')
#rse04=('135.241.247.204')

device=cse01

alcatel_sros = {
    'device_type': 'alcatel_sros',
    'ip':   device,
    'username': 'admin',
    'password': 'admin',
    'port' : 22,          # optional, defaults to 22
    'secret': '',     # optional, defaults to ''
    'verbose': False,       # optional, defaults to False
}

net_connect = ConnectHandler(**alcatel_sros)

print('Control Plane Counting Device under Check')
print(device)
print ('---')
print ('---')
print ('---')


print('version:')
version = net_connect.send_command('show version')
print(version)
print ('---')
print ('---')

showCP = net_connect.send_command('/show service service-using vpls | match vpls-martini | match "Up   Up" | count')
print(showCP)

print('CSE: BGPv4 Table: Total: 1,658,000 Active: 829,000:')
print('RSE: BGPv4 Table: Total: 200,000 Active: 100,000:')

showCP = net_connect.send_command('/show router bgp summary | match "Total IPv4 Remote Rts"')
print(showCP)
print('-------')
print('-------')

print('CSE: BGPv6 Table: Total: 200,000 Active: 100,000')
print('RSE: BGPv6 Table: Total: 50,000 Active: 25,000')
showCP = net_connect.send_command('/show router bgp summary | match "Total IPv6 Remote Rts"')
print(showCP)
print('-------')
print('-------')

print('CSE: VPNv4 Table: Total: 520,000 Active: 260,000')
print('RSE: VPNv4 Table: Total: 100,000 Active: 50,000')
showCP = net_connect.send_command('/show router bgp summary | match "Total VPN-IPv4 Rem. Rts"')
print(showCP)
print('-------')
print('-------')

print('CSE: L2VPN Table: Total: 50,000 Active:50,000')
print('RSE: L2VPN Table: Total: 50,000 Active:50,000')
showCP = net_connect.send_command('/show router bgp summary | match "Total L2-VPN Rem. Rts"')
print(showCP)
print('-------')

print('CSE: VPNv6 Table: Total: 50,000 Active: 25,000')
print('RSE: VPNv6 Table: Total: 50,000 Active: 25,000')
showCP = net_connect.send_command('/show router bgp summary | match "Total VPN-IPv6 Rem. Rts"')
print(showCP)
print('-------')
print('-------')

print('CSE: MVPNv4: Total: 50,000 Active: 25,000')
print('RSE: MVPNv4: Total: 50,000 Active: 25,000')
showCP = net_connect.send_command('/show router bgp summary | match "Total MVPN-IPv4 Rem Rts"')
print(showCP)
print('-------')
print('-------')

print('CSE: Route Target: Total: 20,000 Active: 10,000')
print('RSE: Route Target: Total: 20,000 Active: 10,000')
showCP = net_connect.send_command('/show router bgp summary | match "Total RouteTgt Rem Rts"')
print(showCP)
print('-------')

print('CSE: OSPF v4 Total: 20,000 Active: 20,000')
print('RSE: OSPF v4 Total: 20,000 Active: 20,000')
showCP = net_connect.send_command('/show router route-table ipv4 summary | match "OSPF"')
print(showCP)
print('-------')
print('-------')

print('CSE: ISIS V4 Total: 10,000 Active: 10,000')
print('RSE: ISIS V4 Total: 5,000 Active: 5,000')
showCP = net_connect.send_command('/show router route-table ipv4 summary | match "ISIS"')
print(showCP)
print('-------')
print('-------')

print('CSE: Static v4: 200')
print('RSE: Static v4: 200')
showCP = net_connect.send_command('/show router route-table ipv4 summary | match "Static"')
print(showCP)
print('-------')
print('-------')

print('CSE: Others v4 (Direct, etc) 300')
print('RSE: Others v4 (Direct, etc) 300')
showCP = net_connect.send_command('/show router route-table ipv4 summary | match "Direct"')
print(showCP)
print('-------')
print('-------')

print('CSE: OSPF v6 Total: 20,000 Active: 20,000')
print('RSE: OSPF v6 Total: 500 Active: 500')

showCP = net_connect.send_command('/show router route-table ipv6 summary | match "OSPFv3"')
print(showCP)
print('-------')
print('-------')

print('CSE: ISIS V6 Total: 1,000 Active: 1,000')
print('RSE: ISIS V6 Total: 10,000 Active: 10,000')

showCP = net_connect.send_command('/show router route-table ipv6 summary | match "ISIS"')
print(showCP)
print('-------')
print('-------')

print('CSE: Static v6: 200')
print('RSE: Static v6: 200')
showCP = net_connect.send_command('/show router route-table ipv6 summary | match "Static"')
print(showCP)
print('-------')
print('-------')

print('CSE: Direct v6: 200')
print('RSE: Direct v6: 200')
showCP = net_connect.send_command('/show router route-table ipv6 summary | match "Direct"')
print(showCP)
print('-------')

print('CSE: RSVP: 500 Sessions')
print('RSE: RSVP: 500 Sessions')
showCP = net_connect.send_command('/show router mpls lsp | match "Up   Up" | count')
print(showCP)
print('-------')
print('-------')

print('CSE/RSE LDP:')
print ('-5,000 IPv4 resolved prefixes')
print ('-500 sessions')
showCP = net_connect.send_command('/show router ldp bindings active summary')
print(showCP)
showCP = net_connect.send_command('/show router ldp session | match Established | count')
print(showCP)
print('-------')
print('-------')

print('NSR:')
showCP = net_connect.send_command('show redundancy synchronization | match "Standby Status"')
print(showCP)
showCP = net_connect.send_command('show card | match "A"')
print(showCP)
showCP = net_connect.send_command('show card | match "B"')
print(showCP)
print('-------')

print('CSE/RSE: 2000 local L3VPNv4 and 2000 local L3VPNv6 count:')
showCP = net_connect.send_command('/show service service-using vprn | match "Up   Up" | count')
print(showCP)
print('-------')
print('-------')

print('CSE/RSE: 8000 local vpls kompella:')
showCP = net_connect.send_command('/show service service-using vpls | match vpls-kompella | match "Up   Up" | count')
print(showCP)
print('-------')
#print('output for CSE03:')
#showCP = net_connect.send_command('/show service service-using vpls | match 40001 post-lines 8000 | match "Up   Up" | count')
#print(showCP)
print('-------')
print('-------')

print('CSE/RSE: 17000 local vpls martini:')
showCP = net_connect.send_command('/show service service-using vpls | match vpls-martini | match "Up   Up" | count')
print(showCP)
#print('CSE03')
#showCP = net_connect.send_command('/show service service-using vpls | match expression ^100*. | count')
#print(showCP)
#print('RSE03')
#showCP = net_connect.send_command('/show service service-using vpls | match 50001 post-lines 8000 | match "Up   Up" | count')
#print(showCP)
print('-------')
print('-------')

print('CSE/RSE: 10 NG-MVPN Head-ends count:')
showCP = net_connect.send_command('/show service service-using vprn | match mvpn | match "Up   Up" | count')
print(showCP)
print('-------')
print('-------')

print('CSE/RSE: 100 Area 0 OSPFv4 neighbors:')
showCP = net_connect.send_command('/show router ospf neighbor | match Full | count')
print(showCP)
print('-------')
print('-------')

print('CSE/RSE: IPv4 prefix export limit to OSPFv4 is 20k:')
config_commands = ['/config router ospf','info | match export-limit']
showCP = net_connect.send_config_set(config_commands)
print(showCP)
print('-------')

print('CSE/RSE: 10 Area 0 OSPFv6 neighbors:')
showCP = net_connect.send_command('/show router ospf3 neighbor | match Full | count')
print(showCP)
print('-------')
print('-------')

print('CSE/RSE: 10 Area 0 OSPFv6 neighbors:')
showCP = net_connect.send_command('/show router ospf3 neighbor | match Full | count')
print(showCP)
print('-------')
print('-------')

print('CSE/RSE: 100 ISISv4 adjacencies:')
showCP = net_connect.send_command('/show router isis  adjacency | match Up | count')
print(showCP)
print('-------')
print('-------')

print('CSE: ISIS with BFD (100ms 3) 20 L2 adjacencies:')
showCP = net_connect.send_command('show router bfd session | match L2 ignor | match IPv4 ignor | match Up | match 100 | match 3 | count')
print(showCP)
print('-------')
print('-------')

print('CSE: ISIS with BFD (100ms 3) 80 L1 adjacencies:')
print('RSE: ISIS with BFD (100ms 3) 50 L1 adjacencies:')
showCP = net_connect.send_command('/show router bfd session | match L1 ignor | match IPv4 ignor | match Up | match 100 | match 3 | count')
print(showCP)
print('-------')
print('-------')

print('CSE: ISISv6 with BFD (100ms 3) 80 L2 adjacencies:')
showCP = net_connect.send_command('/show router bfd session | match L2 ignor | match IPv6 ignor | match Up | match 100 | match 3 | count')
print(showCP)
print('-------')
print('-------')

print('CSE: ISISv6 with BFD (100ms 3) 80 L1 adjacencies:')
print('RSE: ISISv6 with BFD (100ms 3) 50 L1 adjacencies:')
showCP = net_connect.send_command('show router bfd session | match L1 ignor | match IPv6 ignor | match Up | match 100 | match 3 | count')
print(showCP)
print('-------')
print('-------')

print('-Reference bandwidth 100G')
print('-Wide metrics only')
print('-Prefixes exported to ISIS domain is limited to 20k')
print('-Point to Point only CSE=200 RSE=100')
print('-Authentication for IIH only (HMAC-MD5) enabled')

config_commands = ['/config router isis','info | match reference-bandwidth']
config_commands = ['/config router isis','info | match wide-metric pre 1']
config_commands = ['/config router isis','info | match point-to-point | count']
config_commands = ['/config router isis','info | match hello-auth-keychain | count']
config_commands = ['show system security keychain "ISIS-AUTH" detail  | match Algori']

showCP = net_connect.send_config_set(config_commands)
print(showCP)
print('-------')
print('-------')



#===

print('CSE/RSE:200 single-hop LSPs, primary LSP with strict path and hop-limit of 2. Backup: active secondary (standby) LSP with strict-path and hop-limit:')
showCP = net_connect.send_command('/show router mpls lsp detail | match Standby | match Up | count')
print(showCP)
print('-------')
print('-------')

print('CSE/RSE: 200 single-hop LSPs, primary LSP with strict path and hop-limit of 2, with fast reroute:')
showCP = net_connect.send_command('/show router mpls lsp | match Yes | count')
print(showCP)
print('-------')
print('-------')

print('500 LSPs total with:')
print ('-Adaptive')
print ('-SE reservation style')
print ('-least fill')
print ('-revert-timer 5 mins:')
print ('Adaptive:')
showCP = net_connect.send_command('/show router mpls lsp detail | match "Adaptive" | count')
print(showCP)
print('-------')
print ('SE:')
showCP = net_connect.send_command('/show router mpls lsp detail | match ": SE" | count')
print(showCP)
print('-------')
print ('Least Fill:')
showCP = net_connect.send_command('/show router mpls lsp detail | match "Least Fill      : Enabled" | count')
print(showCP)
print('-------')
print ('Revert Timer:')
showCP = net_connect.send_command('/show router mpls lsp detail | match "Revert Timer" | count')
print(showCP)

print('RSVP neighbors are -authenticated (hmac- md5)')
print('-hello interval 9s -LDP tunneling -implicit null -no-propagate TTL -6PE')
print('-icmp-tunneling')
print('- RSVP PATH/RESV messages refresh timeout:45s')
print('-Keep multiplier x3')
showCP = net_connect.send_command('/show router rsvp interf    ace detail | match ISIS-AUTH')
print(showCP)
showCP = net_connect.send_command('/show router rsvp interface detail | match "9000 ms"')
print(showCP)
config_commands = ['/configure router ttl-propagate', 'info']
showCP = net_connect.send_config_set(config_commands)
print(showCP)
showCP = net_connect.send_command('/show router rsvp status | match "Admin Status"')
print(showCP)
showCP = net_connect.send_command('/show router rsvp status | match "Keep Multiplier"')
print(showCP)
showCP = net_connect.send_command('show router mpls lsp detail | match LdpOverRsvp | count')
print(showCP)

print('LDP:')
print('-LDP Hello-interval: 5 seconds for link hello messages and 15 seconds for targeted hello messages.')
print('-LDP Hold-time: 3 times the Hello-interval ')
print('-Tunneled through RSVP-signaled LSPs ')
print('-LDP session keepalive- interval: 10 seconds. ')
print('-LDP session keepalive- timeout: 3 times the keepalive-interval')

showCP = net_connect.send_command('/show router ldp targ-peer | match "LDP IPv4 Targeted Peers" post-lines 5')
print(showCP)
config_commands = ['/configure router ldp', 'info | match prefer']
showCP = net_connect.send_config_set(config_commands)
print(showCP)

print('-------')
print('-------')
print('-------')
print('-------')

print('Point-to-multipoint LSPs to support NG-MVPN, with link protection enabled:')
print('p2mp-lsp, 10:')
showCP = net_connect.send_command('/show router mpls p2mp-lsp | match 20000 | match "Up   Up" | count')
print(showCP)
print('p2mp-lsp info type terminate:')
showCP = net_connect.send_command('/show router mpls p2mp-info type terminate')
print(showCP)
print('p2mp-lsp facility count, 10:')
showCP = net_connect.send_command('/show router mpls p2mp-lsp detail | match Facility | count')
print(showCP)
print('p2mp-lsp bypass tunnle count, 11:')
showCP = net_connect.send_command('/show router mpls bypass-tunnel p2mp detail')
print(showCP)
print('-------')
print('-------')

print('200 Staticv4 routes with BFD (300ms 3):')
showCP = net_connect.send_command('show router bfd session | match static pre-lines 1 | match Up post-lines 1 | match . | count')
print(showCP)
print('-------')
print('-------')

print('200 Staticv4 routes with BFD (300ms 3):')
showCP = net_connect.send_command('show router bfd session | match static pre-lines 1 | match Up post-lines 1 | match : | co')
print(showCP)
print('-------')
print('-------')

print('50 MP-iBGP peers')
if device == cse01 :
    showCP = net_connect.send_command('/show router bgp summary | match 0.59 post-lines 10')
    print(showCP)
if device == cse02 :
    showCP = net_connect.send_command('/show router bgp summary | match 0.58 post-lines 10')
    print(showCP)
if device == rse01 :
    showCP = net_connect.send_command('/show router bgp summary | match 0.61 post-lines 10')
    print(showCP)
if device == rse02 :
    showCP = net_connect.send_command('/show router bgp summary | match 0.60 post-lines 10')
    print(showCP)

print('-------')
print('-------')

print('CSE as RR for RSE')
if device == cse01 :
    config_commands = ['/configure router bgp', 'info | match cluster']
    showCP = net_connect.send_config_set(config_commands)    
    print(showCP)
if device == cse02 :
    config_commands = ['/configure router bgp', 'info | match cluster']
    showCP = net_connect.send_config_set(config_commands)    
    print(showCP)
if device == rse01 :   
    print('not applicable')
if device == rse02 :   
    print('not applicable')
 
print('-------')
print('-------')
   
print('CSE as client of IP Core RR')
showCP = net_connect.send_command('show router bgp neighbor 10.233.254.130 | match Recd.')
print(showCP)

print('-------')
print('-------')

print('50 MP-iBGP peers authenticated using HMAC-SHA-1-96')
showCP = net_connect.send_command('show router bgp auth-keychain | count')
print(showCP)

print('-------')
print('-------')

print('50 MP-iBGP peerings with 300s holdtime')
config_commands = ['/configure router bgp', 'info | match "Active Hold Time" ']
showCP = net_connect.send_config_set(config_commands)
print(showCP)

print('LLDP')
showCP = net_connect.send_command('show system lldp neighbor')
print(showCP)

print('-------')
print('-------')

print('RSE EBGP GRT:')
if device == cse01 :
    print ('not applicable')
if device == cse01 :
    print ('not applicable')
if device == rse01 :
    print('RSE EBGP GRT IPv4-2b-asn peer number:')
    showCP = net_connect.send_command(' /show router bgp summary group "CP-EBGP-IPv4-2b-asn" | match "0/0/0" | count')
    print(showCP)
    print('-------')
    print('RSE EBGP GRT IPv4-4b-asn peer number:')
    showCP = net_connect.send_command(' /show router bgp summary group "CP-EBGP-IPv4-4b-asn" | match "0/0/0" | count')
    print(showCP)
    print('-------')
    print('RSE EBGP GRT IPv6-2b-asn peer number:')
    showCP = net_connect.send_command(' /show router bgp summary group "CP-EBGP-IPv6-2b-asn" | match "0/0/0" | count')
    print(showCP)
    print('-------')
    print('RSE EBGP GRT IPv6-4b-asn peer number:')
    showCP = net_connect.send_command(' /show router bgp summary group "CP-EBGP-IPv6-4b-asn" | match "0/0/0" | count')
    print(showCP)
    print('       ')
    print('-------')
    print('-------')
if device == rse02 :
    print('RSE EBGP GRT IPv4-2b-asn peer number:')
    showCP = net_connect.send_command(' /show router bgp summary group "CP-EBGP-IPv4-2b-asn" | match "0/0/0" | count')
    print(showCP)
    print('-------')
    print('RSE EBGP GRT IPv4-4b-asn peer number:')
    showCP = net_connect.send_command(' /show router bgp summary group "CP-EBGP-IPv4-4b-asn" | match "0/0/0" | count')
    print(showCP)
    print('-------')
    print('RSE EBGP GRT IPv6-2b-asn peer number:')
    showCP = net_connect.send_command(' /show router bgp summary group "CP-EBGP-IPv6-2b-asn" | match "0/0/0" | count')
    print(showCP)
    print('-------')
    print('RSE EBGP GRT IPv6-4b-asn peer number:')
    showCP = net_connect.send_command(' /show router bgp summary group "CP-EBGP-IPv6-4b-asn" | match "0/0/0" | count')
    print(showCP)
    print('       ')
    print('-------')
    print('-------')



print('RSE EBGP GRT-BFD:')
print('RSE EBGP GRT-BFD IPv4-ebgp-2b:')
showCP = net_connect.send_command(' /show router bfd session | match IPv4-ebgp-2b | count')
print(showCP)
print('-------')
print('RSE EBGP GRT-BFD IPv4-ebgp-4b:')
showCP = net_connect.send_command(' /show router bfd session | match IPv4-ebgp-4b | count')
print(showCP)
print('-------')
print('RSE EBGP GRT-BFD IPv6-ebgp-2b:')
showCP = net_connect.send_command(' /show router bfd session | match IPv6-ebgp-4b | count')
print(showCP)
print('-------')
print('RSE EBGP GRT-BFD IPv6-ebgp-4b:')
showCP = net_connect.send_command(' /show router bfd session | match IPv6-ebgp-2b | count')
print(showCP)
print('-------')
print('-------')


print('50k VPNv4 from 100 EBGPs:')
print('25 peers with 2 bytes ASN:')
showCP = net_connect.send_command(' /show router 2 bgp summary | match 65001 | count')
print(showCP)
print('25 peers with 4 bytes ASN:')
showCP = net_connect.send_command(' /show router 2 bgp summary | match 42949 | count')
print(showCP)
print('25 peers with 2 bytes ASN BFD:')
showCP = net_connect.send_command(' /show router 2 bfd session | match vprn-bgp-2b | match "100       100" | count')
print(showCP)
print('25 peers with 4 bytes ASN BFD:')
showCP = net_connect.send_command(' /show router 2 bfd session | match vprn-bgp-4b | match "100       100" | count')
print(showCP)


print('50k VPNv6 from 100 EBGPs:')
print('25 peers with 2 bytes ASN:')
showCP = net_connect.send_command(' /show router 3 bgp summary | match 65001 | count')
print(showCP)
print('25 peers with 4 bytes ASN:')
showCP = net_connect.send_command(' /show router 3 bgp summary | match 42949 | count')
print(showCP)
print('25 peers with 2 bytes ASN BFD:')
showCP = net_connect.send_command(' /show router 3 bfd session | match IPv6-bgp-2b-asn | match "100       100" | count')
print(showCP)
print('25 peers with 4 bytes ASN BFD:')
showCP = net_connect.send_command(' /show router 3 bfd session | match IPv6-bgp-4b-asn | match "100       100" | count')
print(showCP)

print('---HABIS----')
print('---HABIS----')





