#!/usr/bin/env python
import sys
import os
import subprocess, threading, multiprocessing
import getopt
import signal

testname="test"
in_suffix=".in"
out_suffix=".out"
in_dir="in/"
expected_out_dir="out/"
prog_out_dir="prog_out/"
timer_file="tmp/timer"
diff_file="tmp/difference"
diff_tmp1_file="tmp/tmp1"
diff_tmp2_file="tmp/tmp2"

# Functions and utilities

class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None
	
	def run(self):
		def target():
			self.process = subprocess.Popen(self.cmd,shell=True,preexec_fn=os.setsid)
			self.process.communicate()
			
		thread = threading.Thread(target=target)
		thread.start()
		thread.join(time_limit)
		if thread.is_alive():
			os.killpg(self.process.pid,signal.SIGTERM)
			thread.join()
			return 1
		return 0

def run(com):
	command=Command(com)
	return command.run()

def run_test(prog,file_in,file_out_prog):
	command="time -f \"Time: %es\\nMemory: %MkB\" -o "+timer_file+" "+prog+" < "+file_in
	command=command+" > "+file_out_prog
	if run(command):
		print "Time Limit Exceeded"
		print ""
		return 1
	result=open(timer_file)
	txt=result.read()
	sys.stdout.write(txt)
	result.close()
	return 0

def compare(file_out,file_out_prog):
	command="tr '\\n' ' ' < "+file_out+" > "+diff_tmp1_file
	run(command)
	command="tr '\\n' ' ' < "+file_out_prog+" > "+diff_tmp2_file
	run(command)

	command ="diff -Bqb "+diff_tmp1_file+" "+diff_tmp2_file+" > "+diff_file
	run(command)
	result=open(diff_file)
	txt=result.read()
	if len(txt)>5:
		print "Wrong Answer"
		ret=0
	else:
		print "Correct"
		ret=1
	result.close()
	print ""
	return ret

def remove_files():
	files=os.listdir(prog_out_dir)
	for f in files:
		os.remove(prog_out_dir+f)
	files=os.listdir(in_dir)
	for f in files:
		os.remove(in_dir+f)
	files=os.listdir(expected_out_dir)
	for f in files:
		os.remove(expected_out_dir+f)

def usage():
	print ""
	print "Usage:"
	print sys.argv[0]+" [-ah] [-t time] [-i id] [-o eod] [-u pod] [-m mx] -g gen -p prog"
	print ""
	print "Flag explanation:"
	print "-a\trun all tests, whether some of them fail or not"
	print "-h\tdisplay this help"
	print "-t time"
	print "\tlimit the execution time to 'time' seconds; default: 2.0"
	print "-i id"
	print "\tset input directory to id; default: in/"
	print "-o eod"
	print "\tset expected output directory to eod; default: out/"
	print "-u pod"
	print "\tset program output directory to pod; default: prog_out/"
	print "\tNote that a '/' is needed at the end in i/o/d flags"
	print "-m mx"
	print "\tset maximum number of testcases to mx; default: 1000"
	print "-g gen"
	print "\tset a command that will generate testcases."
	print "\tNote that it will be called as follows: 'gen cnt if of', where:"
	print "\tcnt is current test number, and if and of are i/o files"
	print "-p prog"
	print "\tcommand used to run a tested program"
	print ""
	print "Example usage:"
	print sys.argv[0]+"-g generator.out -p program.out -m 10"




# Entry point

time_limit=2.0
generator_name=""
prog_name=""
max_cnt=1000
run_all=False

try:
	opts,args=getopt.getopt(sys.argv[1:],"aht:g:p:i:o:u:m:",[])
except getopt.GetoptError:
	usage()
	sys.exit(2)

for opt, arg in opts:
	if opt=="-a":
		run_all=True
	if opt=="-h":
		usage()
		sys.exit(2)
	if opt=="-t":
		time_limit=float(arg)
	if opt=="-g":
		generator_name=arg
	if opt=="-p":
		prog_name=arg
	if opt=="-i":
		in_dir=arg
	if opt=="-o":
		expected_out_dir=arg
	if opt=="-u":
		prog_out_dir=arg
	if opt=="-m":
		max_cnt=int(arg)

if generator_name=="":
	usage()
	sys.exit(2)
if prog_name=="":
	usage()
	sys.exit(2)



print ""
correct=0
wa=0
tle=0

end=False
cnt=0
remove_files()
first_wa=""
first_tle=""
while (not end or run_all) and cnt<max_cnt:
	fi=in_dir+testname+str(cnt)+in_suffix
	fo=expected_out_dir+testname+str(cnt)+out_suffix
	fop=prog_out_dir+testname+str(cnt)+out_suffix
	command=generator_name+" "+str(cnt)+" "+fi+" "+fo
	run(command)
	print "Testing "+testname+str(cnt)+":"
	cnt=cnt+1
	if run_test(prog_name,fi,fop):
		if first_tle=="":
			first_tle=fi
		tle=tle+1
		end=True
		continue
	if compare(fo,fop):
		correct=correct+1
	else:
		if first_wa=="":
			first_wa=fi
		wa=wa+1
		end=True

print "Statistics:"
print "========================"
print str(correct)+" x Correct"
print str(wa)+" x Wrong Answer"
if first_wa!="":
	print "(first at "+first_wa+")"
print str(tle)+" x Time Limit Exceeded"
if first_tle!="":
	print "(first at "+first_tle+")"
print "========================"
