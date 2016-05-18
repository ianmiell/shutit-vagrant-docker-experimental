"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule


class docker_experimental(ShutItModule):


	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches)
		#                                    - Returns True if any lines in output match any of
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		#
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#                                    - Delete text from file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#                                    - Replace text from file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		shutit.send('mkdir -p /tmp/shutit-vagrant-docker-experimental')
		shutit.send('cd /tmp/shutit-vagrant-docker-experimental')
		if shutit.file_exists('Vagrantfile'):
			shutit.send('git pull')
		else:
			shutit.send('cd ..')
			shutit.send('git clone --recursive https://github.com/ianmiell/shutit-vagrant-docker-experimental.git')
		shutit.send('cd /tmp/shutit-vagrant-docker-experimental')
		if shutit.send_and_match_output('vagrant status',['.*running.*','.*saved.*','.*poweroff.*','.*not created.*','.*aborted.*']):
			if not shutit.send_and_match_output('vagrant status',['.*running.*','.*not created.*']) and shutit.get_input('A vagrant setup already exists here. Do you want me to start up the existing instance (y) or destroy it (n)?',boolean=True):
				shutit.send('vagrant up',note='Start up the vagrant machine')
			elif not shutit.send_and_match_output('vagrant status',['.*not created.*']):
				shutit.send('vagrant up',note='Start up the vagrant machine')
			elif not shutit.send_and_match_output('vagrant status',['.*running.*']):
				shutit.send('vagrant destroy -f',note='Destroy the existing vagrant machine')
				shutit.send('vagrant up',note='Start up the vagrant machine')
		else:
			shutit.pause_point('error starting up Vagrant')
		shutit.login(command='vagrant ssh',note='Log into the Vagrant machine')
		shutit.login(command='sudo su -',note='Become root')
		shutit.install('curl')
		shutit.send('curl -sSL https://experimental.docker.com/ | sh',note='Install the experimental docker binary')
		shutit.send('nohup docker daemon &',note='Start up the Docker daemon')
		if shutit.cfg[self.module_id]['network']:
vagrant_ip = shutit.send_and_get_output("""hostname -i | awk '{print $1}'""")
			shutit.send('docker run -d --name nettest debian sleep infinity')
			shutit.send('docker network ls')
			bridge_id = shutit.send_and_get_output("""docker network ls --no-trunc | grep bridge | awk '{print $1}'""")
			shutit.send('docker network inspect bridge')
			shutit.send('docker disconnect bridge nettest')
docker network inspect bridge
docker exec -ti nettest bash
ip route
logout
docker network connect bridge nettest
docker exec -ti nettest bash
ip route
logout
https://sreeninet.wordpress.com/2015/07/20/docker-experimental-networking-1/
https://sreeninet.wordpress.com/2015/07/20/docker-experimental-networking-2/
https://sreeninet.wordpress.com/2015/07/20/docker-experimental-networking-3/
			shutit.send('docker rm -f nettest')

			
		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		shutit.get_config(self.module_id, 'network', default=False, boolean=True)
		return True

	def test(self, shutit):
		# For test cycle part of the ShutIt build.
		return True

	def finalize(self, shutit):
		# Any cleanup required at the end.
		return True
	
	def is_installed(self, shutit):
		return False


def module():
	return docker_experimental(
		'shutit.docker_experimental.docker_experimental.docker_experimental', 847062941.00,
		description='Sets up docker experimental for you in a vagrant/virtualbox VM',
		maintainer='ian.miell@gmail.com',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup','tk.shutit.vagrant.vagrant.vagrant','shutit-library.virtualbox.virtualbox.virtualbox']
	)

