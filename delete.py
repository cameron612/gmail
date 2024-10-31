import ezgmail

def __main__():
    unreadThreads = ezgmail.unread(maxResults=500)
    while (len(unreadThreads) > 0):
        unreadThreads = ezgmail.unread(maxResults=500)
        print("got %d threads" % (len(unreadThreads)))
        for t in unreadThreads:
            t.trash()

print("test")
__main__()
