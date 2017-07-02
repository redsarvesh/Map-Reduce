#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys,ast,numpy
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
#  here  setup  choice  will store 

choice=x.getvalue('select')


ip_list=["192.168.122.107","192.168.122.9","192.168.122.160"]

ip_listing=[]

cpu_check="lscpu   |  grep -i 'CPU(s):'   |   head  -1  |  cut -d:   -f2"
mem_check="cat /proc/meminfo | grep -i MemFree:"

for i in ip_list:
	
	check=commands.getstatusoutput('ping  -c 1 '+i)
	if  check[0] ==  0  :
	
		ip_listing.append(i)


#@@@@@@@@@@@@@@@@@@@@@@

if choice == "man":

#@@@@@@@@@@@@@@@@@@@@@@
	
	print  "<form  action='http://192.168.122.1/cgi-bin/hadoopproject/start7.cgi' method='POST'>"
	print "SELECT NAMENODE:"
	print "</br>"
	for i   in  ip_listing:
		ignore_exit_value, cpu_core=commands.getstatusoutput('sudo -i sshpass -p "q" ssh -o StrictHostKeyChecking=no root@'+i+" "+cpu_check)
		cpu=cpu_core.strip()
			
		ignore1,memory_value=commands.getstatusoutput('sudo -i sshpass -p "q" ssh root@'+i+" "+mem_check)
	
		mem=memory_value.replace(" ","")
		mem_strip=mem.lstrip("MemFree:")
		mem_rstrip=mem_strip.rstrip("kB")
		
		

		print  "<input  type='radio' name='setup' value="+i+" >"+i +"  " +"RAM= "+mem_strip +"  " +"CPU core= "+cpu+ "<br/>"

	for element in ip_listing:
	
		print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element),)
	print '<input type="submit" name="submit" value="Submit" />'
	print "</form>"


#@@@@@@@@@@@@@@@@@@@@@@@@@

if choice == "auto" :

#@@@@@@@@@@@@@@@@@@@@@@@@@
	cpu_core_ip={}
	F_ram_ip={}
	
	for i   in  ip_listing:
		ignore_exit_value, cpu_core=commands.getstatusoutput('sudo -i sshpass -p "q" ssh -o StrictHostKeyChecking=no root@'+i+" "+cpu_check)
		cpu=cpu_core.strip()
		
		ignore1,memory_value=commands.getstatusoutput('sudo -i sshpass -p "q" ssh root@'+i+" "+mem_check)
		
		mem=memory_value.replace(" ","")
		mem_strip=mem.lstrip("MemFree:")
		mem_rstrip=mem_strip.rstrip("kB")
	

		x1="{"+"\'"+i+"\'"+":"+mem_rstrip+"}"
	

		y1=ast.literal_eval(x1)


		F_ram_ip.update(y1)


		sort_F_ram_ip=sorted(F_ram_ip,key=F_ram_ip.get,reverse=True)




		x2="{"+"\'"+i+"\'"+":"+cpu+"}"
	

		y2=ast.literal_eval(x2)


		cpu_core_ip.update(y2)

		sort_cpu_core_ip=sorted(cpu_core_ip,key=cpu_core_ip.get,reverse=True)


	

############################################################### NAMENODE ############################################################################

	namenode=sort_F_ram_ip[0]


	if namenode in sort_F_ram_ip:



		commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
		commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

		file1=open("/var/www/cgi-bin/hdfs-site.xml","w")
		s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>"+"/"+"directory"+"</value>\n</property>\n</configuration>"
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




		commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/hdfs-site.xml root@"+namenode+":/etc/hadoop/")

		commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/core-site.xml root@"+namenode+":/etc/hadoop/")

		commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/mapred-site.xml root@"+namenode+":/etc/hadoop/")

		

	
		commands.getoutput("sudo -i sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+namenode+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")
	#commands.getoutput("sshpass -p 'q' ssh root@"+namenode+" "+"hadoop namenode -format")
	#commands.getoutput("sshpass -p 'q' ssh root@"+namenode+" "+"hadoop-daemon.sh start namenode")
	 



############################################################### X X X X X X #########################################################################


############################################################### JOBTRACKER ##########################################################################



	jobtracker=sort_cpu_core_ip[0]


	if jobtracker in sort_cpu_core_ip:
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
	 
		#commands.getoutput("sshpass -p 'q' ssh root@"+namenode+" "+"hadoop-daemon.sh start jobtracker")

############################################################ X X X X X X X X X ######################################################################



########################################################### DATANODE AND TASKTRACKER ################################################################
	s=1

	index=[]


	if namenode and jobtracker in ip_listing:

		n_index=ip_listing.index(namenode)
		index.append(n_index)
		j_index=ip_listing.index(jobtracker)
		index.append(j_index)

	new_ip_list=numpy.delete(ip_listing,index).tolist()

	datanodes=new_ip_list
		

		

	for dn_ip in datanodes:

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




		commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/hdfs-site.xml root@"+dn_ip+":/etc/hadoop/")
	
		commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/core-site.xml root@"+dn_ip+":/etc/hadoop/")

		commands.getoutput("sudo -i sshpass -p 'q' scp /var/www/cgi-bin/mapred-site.xml root@"+dn_ip+":/etc/hadoop/")

	
		commands.getoutput("sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/jobip/'+jobtracker+"/"+"\" /etc/hadoop/mapred-site.xml\'")

		commands.getoutput("sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")

		commands.getoutput("sudo -i sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/dfs.name.dir/dfs.data.dir/'+"\""+" /etc/hadoop/hdfs-site.xml\'")
	
	
		commands.getoutput("sshpass -p 'q' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/directory/'+"number"+str(s)+"/"+"\" /etc/hadoop/hdfs-site.xml\'")

		s=s+1





############################################################## x x x x x x x x x x x x ##############################################################



	
	

	print "IP with memory: %r"%(F_ram_ip)
	print "</br>"
	print "sorted IP =  %r"%(sort_F_ram_ip)
	print "</br>"
	print "##################################################################################################################"
	print "NAMENODE =====  %r" %(namenode)
	print "</br>"
	time.sleep(5)
	print "IP with cpu: %r"%(cpu_core_ip)
	print "</br>"
	print "sorted IP =  %r"%(sort_cpu_core_ip)
	print "</br>"
	print ""

	print "###################################################################################################################"
	print "</br>"	
	print "JOBTRACKER =====  %r" %(jobtracker)
	
	print "</br>"

	

	time.sleep(5)
	print "####################################################################################################################"
	print ""
	print "</br>"
	print "DATANODES and TASKTRACKER =====  %r" %(datanodes)
	

















