"""
Backend web server entry: use config HOST/PORT for deployment.
Frontend can call http://<HOST>:<PORT>/v1/...
"""
import sys
import uvicorn

if __name__ == "__main__":
    try:
        from config.base import HOST, PORT, DEBUG
    except ImportError:
        from video_distribution_tool.config.base import HOST, PORT, DEBUG
    print(f"Starting backend on http://{HOST}:{PORT} (DEBUG={DEBUG})", file=sys.stderr)
    print(f"  API: http://127.0.0.1:{PORT}/v1/  Health: http://127.0.0.1:{PORT}/health  Docs: http://127.0.0.1:{PORT}/docs", file=sys.stderr)
    try:
        uvicorn.run(
            "api.app:app",
            host=HOST,
            port=PORT,
            reload=DEBUG,
        )
    except OSError as e:
        if "address already in use" in str(e).lower() or "10048" in str(e):
            print(f"Port {PORT} already in use. Set PORT= another value or stop the other process.", file=sys.stderr)
        raise
