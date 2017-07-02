#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys,numpy,ast
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
#  here  setup  choice  will store 

jobtracker=x.getvalue('setup')

all_ip=x.getlist('my_list')

namenode_ip=x.getlist('nn')

#converting list to string(namenode)

namenode =''.join(namenode_ip)

#jobtracker=sort_cpu_core_ip[0]



############################################################## JOBTRACKER ###########################################################################

commands.getoutput("sudo -i touch /var/www/cgi-bin/mapred-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/mapred-site.xml")


file1=open("/var/www/cgi-bin/mapred-site.xml","w")
s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>jobip:90001</value>\n</property>\n</configuration>"
file1.write(s1)
file1.close()


commands.getoutput("sudo -i touch /var/www/cgi-bin/core-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/core-site.xml")


file2=open("/var/www/cgi-bin/core-site.xml","w")
s2="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://ipaddr:10001</value>\n</property>\n</configuration>"
file2.write(s2)
file2.close()


commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

file3=open("/var/www/cgi-bin/hdfs-site.xml","w")
s3="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n</configuration>"
file3.write(s3)
file3.close()



commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/hdfs-site.xml root@"+jobtracker+":/etc/hadoop/")

commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/core-site.xml root@"+jobtracker+":/etc/hadoop/")

commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/mapred-site.xml root@"+jobtracker+":/etc/hadoop/")
		

	
commands.getoutput("sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+jobtracker+" "+'\'sed -i \"s/jobip/'+jobtracker+"/"+"\" /etc/hadoop/mapred-site.xml\'")

commands.getoutput("sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+jobtracker+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")
	 


####################################################################################################################################################

######################################################## DATANODE AND TASKTRACKER ##################################################################

commands.getoutput("sudo -i touch /var/www/cgi-bin/mapred-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/mapred-site.xml")


file1=open("/var/www/cgi-bin/mapred-site.xml","w+")
s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>jobip:90001</value>\n</property>\n</configuration>"
file1.write(s1)
file1.close()


commands.getoutput("sudo -i touch /var/www/cgi-bin/core-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/core-site.xml")


file2=open("/var/www/cgi-bin/core-site.xml","w+")
s2="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://ipaddr:10001</value>\n</property>\n</configuration>"
file2.write(s2)
file2.close()


commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

file3=open("/var/www/cgi-bin/hdfs-site.xml","w")
s3="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>"+"/"+"directory"+"</value>\n</property>\n</configuration>"
file3.write(s3)
file3.close()


s=1

index1=[]


if jobtracker in all_ip:


	n_index=all_ip.index(jobtracker)
	index1.append(n_index)
	

new_ip_list=numpy.delete(all_ip,index1).tolist()

data_task=new_ip_list


for dn_ip in data_task:
	commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/hdfs-site.xml root@"+dn_ip+":/etc/hadoop/")

	commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/core-site.xml root@"+dn_ip+":/etc/hadoop/")

	commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/mapred-site.xml root@"+dn_ip+":/etc/hadoop/")

	
	commands.getoutput("sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/jobip/'+jobtracker+"/"+"\" /etc/hadoop/mapred-site.xml\'")

	commands.getoutput("sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")

	commands.getoutput("sudo -i sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/dfs.name.dir/dfs.data.dir/'+"\""+" /etc/hadoop/hdfs-site.xml\'")
	
	
	commands.getoutput("sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/directory/'+"number"+str(s)+"/"+"\" /etc/hadoop/hdfs-site.xml\'")

	s=s+1


time.sleep(2)
print "your cluster is ready"
print " cooooool :-) "
time.sleep(5)
print  "<meta http-equiv='refresh' content='2;url=http://192.168.122.1/hadoopproject/second.html'/>"

##################################################################### X X X X X #####################################################################

