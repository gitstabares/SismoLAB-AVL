def event(function):
    subs = []
    def wrapper(*args,**kwargs):
        response = function(*args,**kwargs)
        for sub in subs:
            sub() #IMPORTANTE