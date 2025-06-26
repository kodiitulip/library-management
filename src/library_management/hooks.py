from __future__ import annotations

from functools import wraps

from click import Context


def savemutation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = kwargs.get("ctx")
        if not isinstance(ctx, Context):
            raise RuntimeError(
                "Missing Typer context (`ctx`) in auto_save-wrapped command"
            )
        result = func(*args, **kwargs)
        ctx.obj.book_storage.to_file(ctx.obj.storage_path)
        return result

    return wrapper
