import asyncio
from shared_client import start_client
import importlib
import os

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir)
               if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        fn_name = f"run_{plugin}_plugin"
        if hasattr(module, fn_name):
            print(f"Running {plugin} plugin...")
            await getattr(module, fn_name)()

async def main():
    task = asyncio.create_task(load_and_run_plugins())
    try:
        await asyncio.Event().wait()  # Keep running
    except asyncio.CancelledError:
        pass
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
