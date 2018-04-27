header = 'SET-X-CSRF-TOKEN'

protected = True

if not response.headers.get(header):
    Message.error('%s HTTP header is missing' % header)

    count += 1

    protected = False

if request.method.lower() == 'post' and response.status_code == 200:
    Message.error('HTTP status code is 200 (yet no CSRF token was sent) and should be 403')

    count += 1

    protected = False

if protected:
    Message.success('CSRF protected')
