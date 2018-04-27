header = 'Content-Security-Policy'

if not response.headers.get(header):
    Message.error('%s HTTP header is missing' % header)

    count += 1
else:
    Message.success('%s protected' % header)
