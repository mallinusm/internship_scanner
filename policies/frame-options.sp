header = 'X-Frame-Options'

if not response.headers.get(header):
    Message.error('%s HTTP header is missing' % header)

    count += 1
else:
    Message.success('HTML frames (<frame>, <iframe> and <object>) protected from rendering')
