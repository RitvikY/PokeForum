import certifi

# Stores all configuration values
SECRET_KEY = b'\xb6\xa2\xb2$P)\xbe9\xf7+"b\x9f\x1eoS'
MONGODB_HOST = 'mongodb+srv://ritviky:YqKdfS35RTaiY4OP@cluster0.prt5asg.mongodb.net/cluster0?retryWrites=true&w=majority&tlsCAFile=' + certifi.where()
