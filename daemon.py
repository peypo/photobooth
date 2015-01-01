# -*-coding:Utf-8 -*
#!/usr/bin/python3

"""Generic linux daemon base class for python 3.x."""

import sys, os, time, atexit, signal

class daemon:
	"""A generic daemon class.

	Usage: subclass the daemon class and override the run() method."""

	def __init__(self, pidfile): self.pidfile = pidfile
	#def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
	#	self.stdin = stdin
	#	self.stdout = stdout
	#	self.stderr = stderr
	#	self.pidfile = pidfile

	def daemonize(self):
		"""Deamonize class. UNIX double fork mechanism."""

		try: 
			pid = os.fork() 
			if pid > 0:
				# exit first parent
				sys.exit(0) 
		except OSError as err: 
			sys.stderr.write('fork #1 failed: {0}\n'.format(err))
			sys.exit(1)
	
		# decouple from parent environment
		os.chdir('/') 
		os.setsid() 
		os.umask(0) 
	
		# do second fork
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit from second parent
				sys.exit(0) 
		except OSError as err: 
			sys.stderr.write('fork #2 failed: {0}\n'.format(err))
			sys.exit(1) 
	
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = open(os.devnull, 'r')
		so = open(os.devnull, 'a+')
		se = open(os.devnull, 'a+')

		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# write pidfile
		atexit.register(self.delpid)

		pid = str(os.getpid())
		with open(self.pidfile,'w+') as f:
			f.write(pid + '\n')
	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""Start the daemon."""

		# Check for a pidfile to see if the daemon already runs
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())

		except IOError:
			pid = None
	
		if pid:
			message = "pidfile {0} already exist. " + \
					"Daemon already running?\n"
			sys.stderr.write(message.format(self.pidfile))
			sys.exit(1)
		
		# Start the daemon
		self.daemonize()
		self.run()

	def stop(self):
		"""Stop the daemon."""

		# Get the pid from the pidfile
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			pid = None
	
		if not pid:
			message = "pidfile {0} does not exist. " + \
					"Daemon not running?\n"
			sys.stderr.write(message.format(self.pidfile))
			return # not an error in a restart

		# Try killing the daemon process	
		try:
			while 1:
				os.kill(pid, signal.SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			e = str(err.args)
			if e.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print (str(err.args))
				sys.exit(1)

	def restart(self):
		"""Restart the daemon."""
		self.stop()
		self.start()

	def status(self):
		"""
		Get status of daemon.
		(draft version -- to be improved)
		"""
		try:
			#pf = open(self.pidfile,'r')
			#pid = int(pf.read().strip())
			#pf.close()
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			message = "There is not PID file. Daemon already running?\n"
			sys.stderr.write(message)
			sys.exit(1)

		try:
			#procfile = open("/proc/{}/status".format(pid), 'r')
			#procfile.close()
			with open("/proc/{}/status".format(pid),'r') as procfile:
				message = "There is a process with the PID {}\n".format(pid)
				sys.stdout.write(message)
		except IOError:
			message = "There is not a process with the PID {}\n".format(self.pidfile)
			sys.stdout.write(message)

	def run(self):
		"""You should override this method when you subclass Daemon.
		
		It will be called after the process has been daemonized by 
		start() or restart()."""
