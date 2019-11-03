import os
from main_functions import app
import config

app.run(host=config.address, port=int(config.port), debug=not config.production)
