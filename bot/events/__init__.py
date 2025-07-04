from telethon import events

client = None
db = None
_registry = []

def register(*event_args, **event_kwargs):
    def decorator(func):
        _registry.append((event_args, event_kwargs, func))
        return func
    return decorator

def register_all():
    from . import channel_events

    for args, kwargs, func in _registry:
        if not client:
            raise RuntimeError("client не инициализирован до register_all()")
        client.on(*args, **kwargs)(func)
