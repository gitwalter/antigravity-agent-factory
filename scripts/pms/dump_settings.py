import os
import django
from django.conf import settings


def main():
    print(f"USE_MINIO='{getattr(settings, 'USE_MINIO', None)}'")
    print(f"AWS_S3_CUSTOM_DOMAIN='{getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)}'")
    print(f"AWS_S3_ENDPOINT_URL='{getattr(settings, 'AWS_S3_ENDPOINT_URL', None)}'")


if __name__ == "__main__":
    main()
