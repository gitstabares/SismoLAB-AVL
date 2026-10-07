"""Decorators for subscribing to and notifying event handlers."""

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
    subscribers = []

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Run the event function and then notify its subscribers.

        Args:
            *args: Positional arguments passed to the original function.
            **kwargs: Keyword arguments passed to the original function.

        Returns:
            The return value from the original function.
        """
        response = function(*args, **kwargs)

        for subscriber in wrapper.subscribers:
            subscriber()
        return response

    wrapper.subscribers = subscribers
    return wrapper

def OnEvent(event: Callable[..., Any]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Return a decorator that registers a function as an event subscriber.

    Args:
        event: The event function wrapped by :func:`EventTrigger`.

    Returns:
        A decorator that appends a function to the event's subscriber list.
    """

    def wrapper(function: Callable[..., Any]) -> Callable[..., Any]:
        """Register a function as a subscriber for the given event.

        Args:
            function: The function to register as a subscriber.

        Returns:
            The original function unchanged.
        """
        event.subscribers.append(function)
        return function

    return wrapper