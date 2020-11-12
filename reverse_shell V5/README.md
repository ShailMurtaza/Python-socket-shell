# Python Socket Reverse Shell Version 5
<h3>Single file RAT Features ::</h3>
<ul>
  <li>Gives you reverse shell of any Operating System</li>
  <li>Socket have limit of reveiving data at a time using <b>"recv()"</b> function. But you can receive unlimited data using <b>"recvall()"</b> function. It can receive almost 9.90 GB of data but you can change size in <b>"add_header()"</b> funtion of scripts. Default header size in 10.</li>
  <li>You can upload files to client computer using <b>"upload"</b> command.</li>
  <li>You can upload directory to client computer using <b>"uploaddir"</b> command.</li>
  <li>You can download files from client computer using <b>"download"</b> command.</li>
  <li>You can download directory from client computer using <b>"downloaddir"</b> command.</li>
  <li>You can take screenshot of client computer using <b>"screenshot"</b> command.</li>
  <li>You can attach file to StartUp of Windows using<b>"attach_startup"</b> command.</li>
</ul>
<hr color=red>
<h3>Some Help ::</h3>
<h2>How to upload files to client computer?</h2>
<!--To upload file to client computer you will have to follow this format:<br>
<b>upload  file_path_with_name,,file_path_with_name_to_save_in_client</b><br>-->

I wants to upload a file named file.txt which is in C:/users/ path in current working directory of client then I wil use: <br>
<b>upload,,C:/users/file.txt,,file.txt</b> <br>
If I wants to upload this file to C:/ drive of client then i will use: <br>
<b>upload,,C:/users/file.txt,,C:/file.txt</b> <br>
If file is in current working directory of server computer then I can use : <br>
<b>upload,,file.txt,,C:/file.txt</b>


<h2>How to upload folder to client computer?</h2>

I wants to upload a folder named folder.dir which is in C:/users/ path in current working directory of client then I wil use: <br>
<b>uploaddir,,C:/users/folder.dir,,folder.dir</b> <br>
If I wants to upload this file to C:/ drive of client then i will use: <br>
<b>uploaddir,,C:/users/folder.dir,,C:/folder.dir</b> <br>
If file is in current working directory of server computer then I can use : <br>
<b>uploaddir,,folder.dir,,C:/folder.dir</b>


<h2>How to download files from client computer?</h2>
I wants to download a file named file.txt which is in C:/users/ path in current working directory of my computer then I wil use: <br>
<b>download,,C:/users/file.txt,,file.txt</b> <br>
If I wants to download this file to C:/ drive in my computer then i will use: <br>
<b>download,,C:/users/file.txt,,C:/file.txt</b> <br>

If file is in current working directory of client computer then I can use : <br>
<b>download,,file.txt,,C:/file.txt</b>


<h2>How to download folder from client computer?</h2>
I wants to download a folder named folder.dir which is in C:/users/ path in current working directory of my computer then I wil use: <br>
<b>downloaddir,,C:/users/folder.dir,,folder.dir</b> <br>
If I wants to download this file to C:/ drive in my computer then i will use: <br>
<b>downloaddir,,C:/users/folder.dir,,C:/folder.dir</b> <br>

If folder is in current working directory of client computer then I can use : <br>
<b>downloaddir,,folder.dir,,C:/folder.dir</b>


<h2>How to take screenshot of client computer?</h2>
If I wants to take screeshot and save it with name screen.png thenn I can use: <br>
<b>screenshot,,sreen</b>
Else if I wants to save screenshot to my desktop then i can use this:
<b>screenshot,,C:/users/your_user_name/desktop/screen</b>

<h2>How to take attach client file to Windows StartUp?</h2>
Use attach_startup command

<h2>How to use this single file?</h2>
Use help command to take help