def testfunc(*args, **kwargs):
    for num in args:
        print (num)
    for key, value in kwargs.items():
        print("The value of {} is {}".format(key, value))