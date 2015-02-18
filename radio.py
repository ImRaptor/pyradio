import os
from subprocess import call, Popen, PIPE

class Radio:

        def __init__(self):
                self.placeHolder = None

        def check_running(self):
                FNULL = open(os.devnull, 'w')
                output = Popen(['screen', '-list'],stdout=PIPE)
                op, err = output.communicate()
                if op is not None and 'station' in op:
                        return True
                else:
                        return False

        def play_station(self, address, type):
                if type == "SC":
                        self._sc_station(address)
                elif type == "F4M":
                        self._f4m_station(address)

        def _kill_screen(self):
                # Kill screen session if it is running
                tim = 0
                while self.check_running() and tim < 10:
                        call(['screen', '-XS', 'station', 'kill'])
                        output = Popen(['screen', '-list'],stdout=PIPE)
                        op, err = output.communicate()
                        tim += 1

        def _sc_station(self, address):
                self._kill_screen()
                #create stream
                stream = '/usr/bin/omxplayer "%s"' % address
                Popen(['screen','-dmS','station','sh','-c',stream])

        def _f4m_station(self,address):
                #Kill screen session
                self._kill_screen()
                stream = '/usr/local/bin/livestreamer %s best -np omxplayer' % address
                Popen(['screen','-dmS','station','sh','-c',stream])