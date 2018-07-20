
import ptvsd
ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))

from .main import app
if __name__ == "__main__":
    app.run()
