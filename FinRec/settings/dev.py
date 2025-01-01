'''
devlopment environment settings initializer.
'''

from decouple import config, Csv
from kombu.utils.url import safequote

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('dev_debug', cast = bool)

ALLOWED_HOSTS = config('dev_allowed_hosts', cast = Csv())

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config('dev_database_engine'),
        'HOST': config('dev_database_host'),
        'PORT': config('dev_database_port'),
        'USER': config('dev_database_user'),
        'PASSWORD': config('dev_database_password'),
        'NAME': config('dev_database_name'),
        'OPTIONS': {
            # 'read_default_file': os.path.join(BASE_DIR, 'my.cnf'),
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}

# Email settings
EMAIL_BACKEND = config('dev_email_backend')
EMAIL_HOST = config('dev_email_host')
EMAIL_PORT = config('dev_email_port')
EMAIL_HOST_USER = config('dev_email_host_user')
EMAIL_HOST_PASSWORD = config('dev_email_host_passcode')
EMAIL_USE_TLS = True    # 587
EMAIL_USE_SSL = False   # 465

# Celery Amazon SQS settings
aws_access_key = safequote(config('dev_celery_broker_aws_sqs_access_key_id'))
aws_secret_key = safequote(config('dev_celery_broker_aws_sqs_secret_access_key'))
CELERY_BROKER_URL = f"sqs://{aws_access_key}:{aws_secret_key}@"
CELERY_RESULT_BACKEND = config('dev_celery_broker_aws_sqs_result_backend')
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-east-1',
    'polling_interval': 0.3,
    'visibility_timeout': 60,
    'queue_name_prefix': 'finrec-',
    'wait_time_seconds': 15
}

# Celery Redis settings
# CELERY_BROKER_URL = config('dev_celery_broker_url')
# CELERY_RESULT_BACKEND = config('dev_celery_result_backend')

# Celery common settings
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

# S3 Bucket file upload settings
AWS_ACCESS_KEY_ID = config('dev_aws_access_key_id')
AWS_SECRET_ACCESS_KEY = config('dev_aws_secret_access_key')
AWS_STORAGE_BUCKET_NAME = config('dev_aws_storage_bucket_name')
DEFAULT_FILE_STORAGE = config('dev_default_file_storage')
# ACL means Access Control List. by default inherits the bucket permissions.
AWS_DEFAULT_ACL = config('dev_aws_default_acl')
# By default files with the same name will overwrite each other.True by default.
AWS_S3_FILE_OVERWRITE = config('dev_aws_s3_file_overwrite')
AWS_S3_REGION_NAME = config('dev_aws_s3_region_name') # Change to your region
AWS_S3_SIGNATURE_VERSION = config('dev_aws_s3_signature_version')
#STATICFILES_STORAGE = storages.backends.s3boto3.S3Boto3Storage
