header = 'Content-Security-Policy'

if not response.headers.get(header):
    print '[+] %s HTTP header is missing' % header

    count += 1
else:
    print '[+] Content-Security-Policy protected'
