import time


def timing(f):
    def wrap(*args):
        st_time = time.time()
        ret = f(*args)
        end_time = time.time()
        print '\n%s function took %dms' % (f.func_name, (end_time - st_time) * 1000.0)
        return ret

    return wrap
