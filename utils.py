import os, time
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%H:%M.%S")
    open("find_rule.log", "a").write(f"{timestamp} {message}\n")

class Rules(object):
    def __init__(self):
        pass
    def set_rule_file(self, fn):
        if not os.path.isfile(fn):
            log("ERROR: the file '{fn}' does not exist - Aborting")
            exit()
        self.rule_file = fn
    def set_modifications_file(self, fn):
        if not os.path.isfile(fn):
            log("ERROR: the file '{fn}' does not exist - Aborting")
            exit()
        self.mod_file = fn
    def get_rules(self):
       ignore = True
       rules = {}
       for l in open(self.rule_file).read().split("\n"):
           if not l.startswith("#"):
               ignore = False
           if ignore: continue
           l = l.strip()
           if l=="": continue

           sid = l.split("sid:")[1].split(";")[0]
           msg = l.split('msg:"')[1].split('"')[0]
           active = (not l.startswith("#"))
           rules[sid] = { "msg": msg, "active": active }
           #log(sid, rules[sid])
#       mods = open(self.mod_file).read().split("\n")
#       for mod in mods:
#           if mod=="": continue
#           log(mod)
#           sid = mod.split("=")[0]
#           active = (mod.split("=")[1]=="enabled")
#           log(sid, active, rules[sid]["active"])
       return rules

    def disable_rule(self, sid):
        cmd = f"sed -i '/sid:{sid};/ s/^/#/' {self.rule_file}"
        os.system(cmd)
        cmd = "/etc/init.d/suricata restart"
        os.system(cmd)
        log('Waiting three seconds.')
        time.sleep(3)
        log('Done disabling rule')
    def enable_rule(self, sid):
        cmd = f"sed -i '/sid:{sid};/ s/^#//' {self.rule_file}"
        os.system(cmd)
        cmd = "/etc/init.d/suricata restart"
        os.system(cmd)
        log('Waiting three seconds.')
        time.sleep(3)
        log('Re-enabled previously disabled rule.')
