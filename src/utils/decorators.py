from typing import Any, Callable

def EventTrigger(function: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorates a function so it notifies registered subscribers when called.

    The wrapped function runs first. If it completes successfully, each
    subscriber is called without arguments, and the function's return value is returned.

    Args:
        function (Callable[..., Any]): The function to be decorated.

    Returns:
        Callable[..., Any]: The wrapped function with event triggering capabilities.
    """
    subscribers: list[Callable[[], Any]] = []

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Runs the event function and then invokes its subscribers.

        Args:
            *args (Any): Positional arguments for the original function.
            **kwargs (Any): Keyword arguments for the original function.

        Returns:
            Any: The response from the original function.
        """
        response = function(*args, **kwargs)
        # Notify listeners only after the event function has completed.
        for subscriber in wrapper.subscribers:
            subscriber()
        return response

    # Keep the callbacks on the wrapper so subscribe() can register them.
    wrapper.subscribers = subscribers
    return wrapper

def OnEvent(event: Callable[..., Any]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Returns a decorator that registers a function for the given event.

    The decorated function is returned unchanged, so registration does not
    alter how that function can otherwise be used.

    Args:
        event (Callable[..., Any]): The event function wrapped by EventTrigger.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]: A decorator that registers the function.
    """
    def wrapper(function: Callable[..., Any]) -> Callable[..., Any]:
        """
        Appends the function to the event's subscriber list.

        Args:
            function (Callable[..., Any]): The function to register as a subscriber.

        Returns:
            Callable[..., Any]: The original function unchanged.
        """
        event.subscribers.append(function)
        return function

    return wrapper