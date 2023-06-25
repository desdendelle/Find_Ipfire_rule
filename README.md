# Find_Ipfire_rule

This python program checks whether a specific suricata rule in an IPFire firewall prevents DNS resolution of a certain address.
It does so by turning all suricata rules off, then turning them on one at a time and testing whether DNS resolution fails. Once it's done, it restores the rules file from a backup.
