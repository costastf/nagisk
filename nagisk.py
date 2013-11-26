#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: nagisk.py
# Copyright (c) 2013 by None
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__    = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'plaintext'
__date__      = '04/11/2013'


import optparse, os, sys
from subprocess import Popen, PIPE

class Asterisk(object):
    def __init__(self):
        output = Popen(['/usr/bin/sudo', '/usr/sbin/asterisk', '-Rvvvx', 'core show channels'], stdout=PIPE).stdout.read()  
        for line in output.splitlines():
            if 'active channel'  in line:
                self.channels = int(line.split()[0])
            if 'active call'  in line:
                self.calls = int(line.split()[0])
            if 'calls processed'  in line:
                self.processedCalls = int(line.split()[0])

parser = optparse.OptionParser()
parser.add_option('-s', '--channels', help='check active sip channels', dest='channels', action='store_true')
parser.add_option('-k', '--calls', help='check active calls', dest='calls', action='store_true')
parser.add_option('-w', '--warning', help='set warning theshold', dest='warning')
parser.add_option('-c', '--critical', help='set critical threshold', dest='critical')
(opts, args) = parser.parse_args()

if __name__=='__main__':
    if not (opts.warning and opts.critical):
        print '-w and -c are required options . Please give values\n'
        parser.print_help()
        raise SystemExit(10)

    try:
        opts.warning = int(opts.warning)
        opts.critical = int(opts.critical)    
    except:
        print('Warning and critical must be valid integers')
        raise SystemExit()
   
    if opts.warning >= opts.critical:
        print 'Warning threshold cannot be bigger or equal than Critical\n'
        parser.print_help()
        raise SystemExit(11)

    if opts.channels and opts.calls:
        print 'Cannot use --channels and --calls at the same time\n'
        parser.print_help()
        raise SystemExit(12)
       
    asterisk = Asterisk()
    for argument in ['calls', 'channels']:
        if opts.__dict__[argument]:
            if opts.warning <= asterisk.__dict__[argument] < opts.critical:
                print('WARNING %s #: %d' % (argument, asterisk.__dict__[argument]))
                raise SystemExit(1)
            elif asterisk.__dict__[argument] >= opts.critical:
                print('CRITICAL %s #: %d' % (argument, asterisk.__dict__[argument]))
                raise SystemExit(2)
            elif asterisk.__dict__[argument] < opts.warning:
                print('OK %s #: %d' % (argument, asterisk.__dict__[argument]))
                raise SystemExit(0)
            else:
                print('UNKNOWN %s #: %d' % (argument, asterisk.__dict__[argument]))
                raise SystemExit(3)


