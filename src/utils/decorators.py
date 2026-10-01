def EventTrigger(function):
    """Decorate a function so it notifies registered subscribers when called.

    The wrapped function runs first. If it completes successfully, each
    subscriber is called without arguments, and its return value is returned.
    """
    subscribers = []
    def wrapper(*args,**kwargs):
        """Run the event function and then invoke its subscribers."""
        response = function(*args,**kwargs)
        # Notify listeners only after the event function has completed.
        for subscriber in wrapper.subscribers:
            subscriber()
        return response
    # Keep the callbacks on the wrapper so subscribe() can register them.
    wrapper.subscribers = subscribers
    return wrapper

def OnEvent(event):
    """Return a decorator that registers a function for the given event.

    The decorated function is returned unchanged, so registration does not
    alter how that function can otherwise be used.
    """
    def wrapper(function):
        """Append the function to the event's subscriber list."""
        event.subscribers.append(function)
        return function
    return wrapper