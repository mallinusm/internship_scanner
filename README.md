# Web vulnerability scanner for SeCloud

## Security-driven Engineering of Cloud-based applications

### Demonstration

Watch the tool live in action [here](https://vimeo.com/259124091).

## Installation

### Manually
```
@TODO
```

#### Using Makefile
```
make install
```

## Run

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