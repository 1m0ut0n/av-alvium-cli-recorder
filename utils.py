def cleanup_after_exception(func):
    """Decorator to cleanup a class if an exeption occured."""

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.__exit__(None, None, None)
            raise e

    return wrapper
