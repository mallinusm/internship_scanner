header = 'X-XSS-Protection'

if not response.headers.get(header):
    print '[+] %s HTTP header is missing' % header

    count += 1
else:
    print '[+] X-XSS-Protection protected'
