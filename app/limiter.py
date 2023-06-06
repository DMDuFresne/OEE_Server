from flask_limiter import Limiter

limiter = Limiter(key_func=lambda: 'global')
