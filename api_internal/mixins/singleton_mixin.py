import threading


class SingletonMixin:
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    print('Initializing {class_name}'.format(class_name=cls.__name__))
                    cls.__singleton_instance = cls(*args, **kwargs)
        return cls.__singleton_instance
