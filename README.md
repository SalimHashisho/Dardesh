## Objective

"Dardesh" is a simple peer-to-peer chat application that uses reliable UDP transfer for message exchange as well as TCP for file exchange.

## How it Works

In order for the two peers to start chatting. Each will launch their .py file. Hence, we launch "chat1.py" and "chat2.py". After entering their names, the two peers can immediately start exchanging messages through the GUI.

Sending a file is as simple as pressing the "File" button, browsing, and choosing the file needed. Once the file is received by the other peer, a "You've received a file" message will appear at his side to direct his attention to the newly created file on his pc.

In order to exit the application, "quit" should be typed into the chat box.

## Caution

Depending on the size and type of the file chosen, the user might have to wait a second or two to start sending messages again in order to avoid any crash. In case any error is encountered, just exit and relaunch the app.

## Next Steps

Several steps are to be taken in different aspects of the chat application.

- GUI: We plan on enhancing the GUI furthermore. The GUI right now is made with simple 'tkinter' functions. Hence, it's minimal.
- File Transfer: We plan on improving the file transfer functionality in order to avoid the possibility of crash when sending large files or complex file types.
- New Features: New features such as exporting chat logs, sending voice notes, and viewing images could've been easily added. To meet our deadlines and ensure stability, we delayed the launching of said features.
- Dynamic timeout values.: Depending on the measured values for the delays, we change the timeout value instead of it being a static 3 seconds timeout.
