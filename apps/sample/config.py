# api
PREFIX_API = 'api_sample'
URL_INDEX_API = '/' + PREFIX_API

# view
VIEW_PREFIX = 'sample'
APP_DIR = VIEW_PREFIX + '/'
URL_INDEX_VIEW = '/' + VIEW_PREFIX
APP_NAME = 'app_' + VIEW_PREFIX

# app config

## file download
CSV_MIMETYPE = 'text/csv'

## file upload
UPLOAD_DIR = 'data/'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

## simulation
NUMBER_OF_SCENARIO = 8
ALLOWED_EXTENSIONS = {'xlsx'}

# request form key

## upload.html
FORM_KEY_UPLOAD_DATADIR = 'datadir'
FORM_KEY_UPLOAD_FILES = 'files'

## download.html
FORM_KEY_DL_FILEPATH ='filepath' 

# session key
SESSION_KEY_DATADIR = 'datadir'
SESSION_KEY_FLASH = '_flashes'