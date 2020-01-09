import re
def rank_titul(string):
    if not isinstance(string, str):
        return 0
    if re.match('(Ph.D|DSc|CSc|Dr\.)', string):
        return 4
    if re.match('(Mgr|Ing|MUDr|MDDr|MVDr|JUDr|PhDr|RNDr|ThLic|ThDr|PharmDr)', string):
        return 3
    if re.match('(Bc|BcA)', string):
        return 2
    if re.match('DiS', string):
        return 1
    return 0

