import argparse
import asyncio
import logging
import signal
import sys
from .daemon import ZeroTabDaemon

logger = logging.getLogger(__name__)

async def run_daemon(daemon: ZeroTabDaemon):
    """Run the daemon in an asyncio event loop with signal handling."""
    loop = asyncio.get_running_loop()
    
    # Setup graceful shutdown
    stop_event = asyncio.Event()
    
    def shutdown_handler():
        logger.info("Shutdown signal received.")
        daemon.stop()
        stop_event.set()

    if sys.platform != "win32":
        try:
            loop.add_signal_handler(signal.SIGINT, shutdown_handler)
            loop.add_signal_handler(signal.SIGTERM, shutdown_handler)
        except NotImplementedError:
            pass

    # Start the daemon
    daemon_task = asyncio.create_task(daemon.start())
    
    # Wait for the shutdown event
    try:
        if sys.platform == "win32":
            await daemon_task
        else:
            await stop_event.wait()
            await daemon_task
    except asyncio.CancelledError:
        pass

def main():
    parser = argparse.ArgumentParser(description="ZeroTab - Zero-dependency LRU tab eviction daemon.")
    parser.add_argument("--browser", type=str, default="chrome", help="Target browser (chrome, safari, edge, brave, opera). Default: chrome")
    parser.add_argument("--timeout", type=int, default=300, help="Tab idle timeout in seconds before eviction (default: 300).")
    parser.add_argument("--max-ram", type=int, default=4096, help="Maximum RAM in MB before aggressive eviction (default: 4096).")
    parser.add_argument("--poll", type=int, default=5, help="Polling interval in seconds (default: 5).")
    
    args = parser.parse_args()
    
    daemon = ZeroTabDaemon(
        browser=args.browser,
        timeout_seconds=args.timeout,
        max_ram_mb=args.max_ram,
        poll_interval=args.poll
    )
    
    try:
        asyncio.run(run_daemon(daemon))
    except KeyboardInterrupt:
        logger.info("ZeroTab shut down gracefully (KeyboardInterrupt).")

if __name__ == "__main__":
    main()
