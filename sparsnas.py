#!/usr/bin/env python

import pigpio, time, sys, os, re 
from datetime import datetime, timedelta




# -----------------------------------------------------------------------------------------------
#   SOME SETTINGS
# -----------------------------------------------------------------------------------------------

sparsnas_pulse_setting = 10000
gpiopin = 17

# Fine tune to get correct values on the display. This is to offset the time spent calling datetime. Depends on computer performance and load.
offset = 0.0008

settingsfile = 'sparsnas.display'
filepollingseconds = 5
pulsewidth = 0.1
verbose = False   # Override with option "-v"





# -----------------------------------------------------------------------------------------------
#   MAIN LOOP: sparsnas()
# -----------------------------------------------------------------------------------------------

def sparsnas ():

	display = readsettingsfile()
	pi = pigpio.pi() 
	pi.set_mode(gpiopin,pigpio.OUTPUT) 

	prevstart = datetime.now()

	while True:  # Loop forever

		start = datetime.now()
		pi.write(gpiopin,1)
		time.sleep(pulsewidth)
		pi.write(gpiopin,0)

		# --------- Time insensitive section -------- #

		uncorrected = getlooptime(display)
		looptime = uncorrected - offset		# For fine tuning displayed number
		nexttime = start + timedelta(seconds=looptime)
		
		verboseprint(start, prevstart, display, uncorrected)
		prevstart = start

		display, nexttime = pollsettingsfile(display, start, nexttime)
	
		delay = (nexttime-datetime.now()).total_seconds()
		if delay < 0.01:
			delay = 0.01

		# ------------------------------------------- #

		time.sleep(delay)
	
	pi.stop()






# -----------------------------------------------------------------------------------------------
#   SUBROUTINES
# -----------------------------------------------------------------------------------------------

def pollsettingsfile(display, start, nexttime):

	prevdisplay = display

	while True:

		display = readsettingsfile()
		
		# Ah! display has changed!
		if display != prevdisplay:

			uncorrected = getlooptime(display)
			looptime = uncorrected - offset
			nexttime = start + timedelta(seconds=looptime)

			verboseprint(nexttime, start, display, uncorrected)

			# Prevent getting negative sleep time when changing to a much lower looptime
			if (nexttime-datetime.now()).total_seconds() <= 1:
				return display, datetime.now() + timedelta(seconds=1)

		prevdisplay = display
		
		
		if (nexttime-datetime.now()).total_seconds() < filepollingseconds:
			# If less than a couple of seconds to next blink break out and go set exact sleep time to next blink in main loop
			return display, nexttime
		else:
			# Else run file poll loop again in a couple of seconds
			time.sleep(filepollingseconds-1)	
	





# -----------------------------------------------------------------------------------------------

def readsettingsfile():

	display = ''

	if not os.path.isfile(settingsfile):
		errormsg('No settings file found: {}'.format(settingsfile))
		return 0
	else:
		try:
			with open(settingsfile) as file:
				for line in file.readlines():
					if re.search(r"[0-9]", line):
						display = re.sub(r'[^0-9]', '', line)
		except:
			errormsg('Could not open settings file: {}'.format(settingsfile))
			return 0
			
	if display == '':
		errormsg('No display value found in settings file: {}'.format(settingsfile))
		return 0
	else:
		return display



# -----------------------------------------------------------------------------------------------

def getlooptime(display):

	if int(display) <= 0:
		return 9999.9999	# Long dummy looptime. To display "0" equals infinite looptime.
	else:
		try:
			looptime = (1/float(display)) * 360 * (10000/float(sparsnas_pulse_setting))
		except:
			errormsg('Invalid display number.')
			return 9999.9999
				
		return looptime
	


# -----------------------------------------------------------------------------------------------

def verboseprint(start, prevstart, display, looptime):

	if verbose:
		print("{} {:>7} {:10.4f} {:11.4f}".format(str(start), display, looptime, (start-prevstart).total_seconds()))



# -----------------------------------------------------------------------------------------------

def errormsg(error):
	sys.stderr.write('ERROR: sparsnas.py: ' + error + '\n')
	return





# -----------------------------------------------------------------------------------------------

if __name__ == '__main__':

	os.chdir(os.path.dirname(sys.argv[0]))
	
	if len(sys.argv) == 2 and sys.argv[1] == '-v':
		verbose = True
		print("{:26} {:>7} {:10} {:10}".format('Timestamp', 'Display', 'Wanted loop', 'Actual loop'))
		
	
	sparsnas()


# -----------------------------------------------------------------------------------------------
