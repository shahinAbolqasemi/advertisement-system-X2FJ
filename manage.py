import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1:
        if args[0] == 'runserver':
            import uvicorn
            from settings import get_settings

            settings = get_settings()

            uvicorn.run(
                'app.main:app',
                host=settings.host,
                port=settings.port,
                reload=settings.debug
            )
