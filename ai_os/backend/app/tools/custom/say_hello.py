

async def say_hello(name: str):
    return f"Hello there, {name}!"


def register_tool(manager):
    manager.register("say_hello", say_hello, "Says hello")
