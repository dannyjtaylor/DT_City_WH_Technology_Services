try:
    print("alpha"[4/0])
except ZeroDivisionError:
    print("zero")
except IndexError:
    print("index")
except:
    print("some")