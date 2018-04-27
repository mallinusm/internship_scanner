# Web vulnerability scanner for SeCloud

## SeCloud

### Security-driven Engineering of Cloud-based applications

Cloud computing is a delivery model of computing as a service rather than a product. Services (i.e., resources, software and data) are provided to computers and other devices as utilities over a network. The services themselves are referred as Cloud services. Applications that use these cloud services by means of APIs are referred to as Cloud-based applications. Cloud-based applications are designed in a distributed and multi-party environment: they consume a multitude of third-party Cloud services and rely on infrastructures and/or platforms hosted in external data centers. The multi-party and distributed nature of cloud-based applications requires particular care with respect to security; the authentication and authorisation of users, as well as the confidentiality and integrity of their data.

Although several technologies and solutions are now emerging both in academia and in the industry, they only address parts of the security problems for Cloud-based applications. As a result, Cloud-based application providers are faced with difficulties when linking and bundling them into a workable security solution for their specific context.

Security of Cloud-based applications requires a holistic and proactive approach. The approach lies in good knowledge of security risks specific to Cloud-based applications. This knowledge must be built upon different aspects of the security problems; not only technical aspects but also organizational and societal ones.

The overall goal is to research whether it is feasible to address the above needs by:

- Performing scientific research with respect to the conception of a holistic & coherent set of tools, technologies and techniques that will allow the software industry to proactively think about security in their Cloud-based applications whether SaaS or Mobile. The four considered perspectives are architecture, infrastructure, programming and process.
- Conceiving a dedicated security risk management model targeted towards Cloud-based application builders (e.g., risk evaluation, mitigation responses to critical risks, vulnerabilities and threats).
- Involving the industry as validator of the two above goals through a dedicated industrial platform. The platform consists of different deliverables with objectives ranging from awareness creation up to adoption of the project results in 2 industrial target groups: software companies and technology providers and consultancies.

The SeCloud consortium consists of 11 multi-disciplinary partners. All partners have strong references as regards their scientific contribution to one perspective, and they will all contribute to realize the common goals in this project (risk management and industrial platform).

### Live

See the tool in action [here](https://vimeo.com/259124091).

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

Security policies are defined in the policies folder. You can remove, add and edit them as you please.

Definitions of security policies are stored in files with the extension *.sp, which stands for security policy. 

The *.sp files are evaluated and executed by the scanner. The language used for implementing the definition of security policies is Python 2. The *.sp files are evaluated and executed by the scanner. 

When the scanner is started, it will call all OpenAPI specified endpoints of a web application and execute HTTP calls against each endpoint. 

Inside the *.sp files you have access to several pre-defined variables. 
- request (see [here](http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects))
- response (see [here](http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects))
- count of type int

The sent request as well as the received response are accessible from within a security policy (*.sp) in order to check headers, HTTP status codes, etc.

Example of a security policy (xss.sp):
```python
header = 'X-XSS-Protection'

if not response.headers.get(header):
    print '[+] %s HTTP header is missing' % header

    count += 1
else:
    print '[+] X-XSS-Protection protected'
```

It is recommended to increment the count variable whenever a security issue is found. This will be reflected in the total count of (potential) flaws at the end of the scan.