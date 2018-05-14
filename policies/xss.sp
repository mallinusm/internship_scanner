header = 'X-XSS-Protection'

if not response.headers.get(header):
    Message.error('%s HTTP header is missing' % header)

    count += 1
else:
    Message.success('%s protected (reflected cross-site scripting detection enabled)' % header)
