
import base
errored = 0
for i in range(600):
    print i
    code = base.subscribe('t@example.com', 'mozilla-and-you')
    if code == 500:
        error = error + 1
print error


