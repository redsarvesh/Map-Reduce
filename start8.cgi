#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys
cgitb.enable()
print  "content-type:text/html"
print  ""
x=cgi.FieldStorage()
nn_ip=x.getvalue("nnip")
directory=x.getvalue("dirname")

jobtracker=x.getlist('my_list')





################################################################# NAMENODE ##########################################################################


commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

file1=open("/var/www/cgi-bin/hdfs-site.xml","w")
s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>"+"/"+directory+"</value>\n</property>\n</configuration>"
file1.write(s1)
file1.close()

commands.getoutput("sudo -i touch /var/www/cgi-bin/core-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/core-site.xml")


file2=open("/var/www/cgi-bin/core-site.xml","w")
s2="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://ipaddr:10001</value>\n</property>\n</configuration>"
file2.write(s2)
file2.close()


commands.getoutput("sudo -i touch /var/www/cgi-bin/mapred-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/mapred-site.xml")


file3=open("/var/www/cgi-bin/mapred-site.xml","w")
s3="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n\n</configuration>"
file3.write(s3)
file3.close()

namenode=nn_ip


commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/hdfs-site.xml root@"+namenode+":/etc/hadoop/")

commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/core-site.xml root@"+namenode+":/etc/hadoop/")

commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/mapred-site.xml root@"+namenode+":/etc/hadoop/")

		

	
commands.getoutput("sudo -i sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+namenode+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")

#####################################################################################################################################################

cpu_check="lscpu   |  grep -i 'CPU(s):'   |   head  -1  |  cut -d:   -f2"
mem_check="cat /proc/meminfo | grep -i MemFree:"

print "SELECT JOBTRACKER"
print ""
print "</br>"
print  "<form  action='http://192.168.122.1/cgi-bin/hadoopproject/start9.cgi' method='POST'>"
for i   in  jobtracker:
	ignore_exit_value, cpu_core=commands.getstatusoutput('sudo -i sshpass -p "q" ssh -o StrictHostKeyChecking=no root@'+i+" "+cpu_check)
	cpu=cpu_core.strip()
			
	ignore1,memory_value=commands.getstatusoutput('sudo -i sshpass -p "q" ssh root@'+i+" "+mem_check)
	
	mem=memory_value.replace(" ","")
	mem_strip=mem.lstrip("MemFree:")
	mem_rstrip=mem_strip.rstrip("kB")
	print  "<input  type='radio' name='setup' value="+i+" >"+i +"  " +"RAM= "+mem_strip +"  " +"CPU core= "+cpu+ "<br/>"
	
#converting string to list
nn=namenode.split(' ')	
for element in nn:
	print '<input type="hidden" name="nn" value="%s">' % (cgi.escape(element),)
	
		
	
for element in jobtracker:
	print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element),)
print '<input type="submit" name="submit" value="Submit" />'
print "</form>"

