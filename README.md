# Assigning static IP address and DNS servers with a Flask app

## How it works
The application assigns static IP address and DNS servers by modifying the _yaml_ files in the _/etc/netplan_ directory.

# Using the application
## Requirements
* `python` 3.x
* `pip`
* `virtualenv`



## Cloning the git repository

Assuming you have git configured, the following command will clone this repository to the present working directory

``` sh
$ git clone https://github.com/prajwal-annigeri/staticIP-ubuntu.git
```


## Creating a new virtual environment 
Navigate to the directory where you want the virtual environment.

The following command creates a new virtual environment named _venv_ in the current directory. This will be the project's directory.

``` sh
$ virtualenv venv
```

## Activating the virtual environment
The virtual environment can be activated with the following command.
Assuming _venv_ is the name of the virtual environment created

``` sh
$ source venv/bin/activate
```

Once the virtual environment has been activated, the console cursor might show the name of the virtual environment as shown below.
```sh
(venv)$ echo 'Hello'
```

## Deactivating the virtual environment
After execution/installing dependencies, the following command should be used to deactivate the current virtual environment. Any dependency installed after this command will be installed globally.

```sh
(venv)$ deactivate
```


## Installing Python packages
This repository has a _requirements.txt_ file. This file contains a list of all the dependencies needed for the project to work.

To install dependencies in the current environment from a _requirements.txt_ file, the command below can be used.
```sh
(venv)$ pip install -r requirements.txt
```

## Usage
The application works by modifying the _yaml_ files in the _/etc/netplan_ directory. The user running this will need _write_ access to files in the _/etc/netplan_ directory and also needs to provide a password when the script runs the `sudo netplan apply` command.

To run the app, the following command can be used
``` sh
(venv)$ python3 app.py
```

To bypass typing in the password and assigning file permissions, the app can be run using 
``` sh 
(venv)$ sudo python3 app.py
```
However, this can be dangerous if the `app.py` file is tampered with.

