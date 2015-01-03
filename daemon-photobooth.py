# -*-coding:Utf-8 -*
#!/usr/bin/python3

"""
This is a photobooth.
When the button is pushed, it takes 4 pictures, merge them, then (if requested) print the result.
"""

import RPi.GPIO as GPIO, sys, time, os, subprocess, logging, logging.handlers
from daemon import daemon
import photobooth as pb
 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
filehandler = logging.handlers.TimedRotatingFileHandler('/tmp/daemon-photobooth.log',when='midnight',interval=1,backupCount=10)
filehandler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(filehandler)

class MyDaemon(daemon):
	def run(self):
		logger.info('.... run .... :-)')
		pb.gpio_setup()
		pb.remove_tmp_content()
		# Run the loop function to keep script running
		try:			
			while True:
				time.sleep(1)

		except KeyboardInterrupt:
			logger.exception('Exit using CTRL+C')

		except Exception as e:  
			logger.exception('Error or exception occurred! (%s)',str(e))

		finally:
			GPIO.cleanup() # this ensures a clean exit on a GPIO point of view
			logger.info('clean exit')


if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-photobooth.pid')
	if len(sys.argv) == 2:
		logger.info('{} {}'.format(sys.argv[0],sys.argv[1]))
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'status' == sys.argv[1]:
			daemon.status()
		else:
			print("Unknown command")
			sys.exit(2)
		sys.exit(0)
	else:
		logger.warning('show cmd deamon usage')
		print("usage: %s start|stop|restart" % sys.argv[0])
		sys.exit(2)