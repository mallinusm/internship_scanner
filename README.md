# Web vulnerability scanner for SeCloud

## Security-driven Engineering of Cloud-based applications

### Demonstration

Watch the tool live in action [here](https://vimeo.com/259124091).

## Installation

### Requirements

- Python 2
- Pip 2
- Python virtual environment

#### Makefile installation
```
make install
```

### Manual installation

You can install the required Linux packages on Debian using the following command.

```
sudo apt-get install python2 python2-pip
```

Next, use pip2 to install the virtualenv package.
```
sudo pip2 install virtualenv
```



After the packages are installed, create the Python virtual environment.

```
virtualenv --no-site-packages --distribute .env
. .env/bin/activate
```

Finally, install the Python packages (make sure pip2 is sourced/activated).

```
pip2 install -r requirements.txt
```

## Run

### Arguments and options

#### Usage

[-h] [--delay [Delay]] [Path]

#### Positional arguments

* Path (the path to the SeCloud project)

#### Optional arguments

* -h, --help (show the help message and exit)
* --delay (the delay in seconds when sending web requests)

### Using make
```
make run ~/web/project/to/scan
```

### Using CLI python
```
./.env/bin/python2 -m Scanner.Application
```

## Screenshots

![Vulnerable Web Application](Capture.PNG "Vulnerable Web Application")

![Safe Web Application](Safe.PNG "Safe Web Application")

## Documentation

### Security Policy definition

#### General

Security policies are defined in the policies folder. You can add, edit and remove them as pleased.

Definitions of security policies are stored in files with the extension sp, which stands for security policy. 

The sp files are evaluated and executed by the scanner. The language used for implementing the security policies (sp files) is Python 2. 

All valid Python code is valid inside sp files.

When the scanner is started, it will call all OpenAPI specified endpoints of the web application and execute HTTP calls against each endpoint. 

The resulting response and the original request are available in the security policies (sp files).

#### Variables 

Inside the security policies (sp files) you have access to several pre-defined variables. 

- request (see [here](http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects))
- response (see [here](http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects))
- count of type int (the amount of security flaws identified)
- Message of type Scanner.Message (with functions for printing info, success, error and debug)

The sent request as well as the received response are accessible from within a security policy (*.sp) in order to check headers, HTTP status codes, etc.

#### Example

Example of a security policy (xss.sp):
```python
header = 'X-XSS-Protection'

if not response.headers.get(header):
    Message.error('%s HTTP header is missing' % header)

    count += 1
else:
    Message.success('%s protected' % header)
```

It is recommended to increment the count variable whenever a security issue is found. This will be reflected in the total count of (potential) flaws at the end of the scan.

It is also recommended to print using the Message object whether a security policy passes or fails. Make the message as clear as possible, this will be printed out in the commandline interface during the scan.