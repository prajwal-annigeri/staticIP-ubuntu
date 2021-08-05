This is a Flask application to set a static IP address and change DNS servers

The application works by modifying the yaml files in the /etc/netplan directory
The user running this will need write access to files in the /etc/netplan directory and also needs a password when the script runs the "sudo netplan apply" command.

These can be bypassed if the app is run using "sudo python3 app.py" however this can be dangerous if the app.py is tampered with.
