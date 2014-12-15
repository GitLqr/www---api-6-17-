
print """#!/usr/bin/env python
# -*- coding: utf8 -*-

reason_desc = ["""


for line in open('reason_desc.txt'):
    line = line.rstrip(' \n')
    if not line:
        break
    items = line.split()
    assert(len(items) == 7)
    print '    (%s),' % (','.join(['"%s"' % item for item in items]))

print "]"
