#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys,numpy,ast
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
#  here  setup  choice  will store 

choice=x.getvalue('setup')

all_ip=x.getlist('my_list')


index1=[]


if choice in all_ip:


	n_index=all_ip.index(choice)
	index1.append(n_index)
	

new_ip_list=numpy.delete(all_ip,index1).tolist()

remaining_ip=new_ip_list



print  "<form  action='http://192.168.122.1/cgi-bin/hadoopproject/start8.cgi' method='POST'>"

print  "<input  type='radio' name='nnip' checked='checked' value="+choice+" >"+choice

for element in remaining_ip:
	print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element),)


print "Enter directory name for namenode:"
print "<input  type=\"text\" name=\"dirname\" placeholder=\"enter directory name here\"  >   <br/>"
print   "<input  type='submit' value='send'>"
print "</form >"

