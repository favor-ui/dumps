import os

basedir = os.path.abspath(os.path.dirname(__file__))


# creating a configuration class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'\

    MONGO_URI = os.environ.get('MONGO_URI') or  "mongodb+srv://facilities:cTf6dnzcqiHvLtRe@cluster0.zl0s3.mongodb.net/Facilities?retryWrites=true&w=majority"

    # MONGO_URI_1 = os.environ.get('MONGO_URI_1') or "mongodb+srv://idl:idl123@idl.hgmwm.mongodb.net/Enrollment?retryWrites=true&w=majority"

