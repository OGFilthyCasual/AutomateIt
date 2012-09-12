'''
Michael Allen C. Isaac <michael@thedevel.com>
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
http://creativecommons.org/licenses/by-nc-sa/3.0/
'''

import sys
import datetime
import pprint
import ctypes
import urllib.request
import ast
import os

from subprocess import call

class AutomateIt():

    sysBit = None
    dictConfig = None

    def __init__( self ):
        self.sysBit = (ctypes.sizeof(ctypes.c_voidp) * 8)

        if( (not(self.sysBit == 32)) and (not (self.sysBit == 64)) ):
            print('Unable to determine architecture.  Exiting.')
            sys.exit(0)

        fsize = os.path.getsize('ast.txt')
        if((fsize == 0) or (fsize == None)):
            print('Unable to locate ast.txt.  Exiting.')
            sys.exit(0)
        else:
            self.dictConfig = ast.literal_eval( self.ReadStringFromFile( 'ast.txt' ) )

        return

    def ReadStringFromFile( self, file ):
        f = open (file, "r")
        data = f.read()
        f.close()
        return data

    def Execute( self ):

        print( 'Working on a %sbit system.' % self.sysBit )

        for item in list(self.dictConfig.keys()):
            fname = ('%s.exe' % item)
            bitz = self.dictConfig[item][0]
            furl = self.dictConfig[item][1]
            farg = self.dictConfig[item][2]

            #check architecture compatiability
            if ((self.sysBit & bitz) == self.sysBit):
                print(([fname, farg]))

                # Or you can do it like this:
                with open(fname, 'wb') as fhandle:
                    #read the url bytes into a file
                    bytez = urllib.request.urlopen( furl ).read()
                    fhandle.write( bytez )

                call('%s %s' % (fname, farg), shell=True)

        return

app = AutomateIt()
app.Execute()

