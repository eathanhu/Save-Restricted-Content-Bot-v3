# main.py (minimal)
import asyncio
from shared_client import start_client, stop_client
import importlib, os

async def load_and_run_plugins():
    await start_client()
    print("Clients started")
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]
    for plugin in plugins:
        m = importlib.import_module(f"plugins.{plugin}")
        fn = f"run_{plugin}_plugin"
        if hasattr(m, fn):
            print("Running", plugin)
            await getattr(m, fn)()

async def main():
    task = asyncio.create_task(load_and_run_plugins())
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        await stop_client()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down")
