import os
import sys
import shutil
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'nepali_platform.settings_production'))
django.setup()

MEDIA_SYMLINK = settings.MEDIA_SYMLINK_PATH
MEDIA_TARGET = settings.MEDIA_TARGET_PATH

if not MEDIA_SYMLINK or not MEDIA_TARGET:
    raise SystemExit('MEDIA_SYMLINK_PATH and MEDIA_TARGET_PATH must be set in the environment.')

def main():
    # Delete existing media folder or symlink
    if os.path.islink(MEDIA_SYMLINK) or os.path.exists(MEDIA_SYMLINK):
        try:
            if os.path.islink(MEDIA_SYMLINK):
                os.unlink(MEDIA_SYMLINK)
            elif os.path.isdir(MEDIA_SYMLINK):
                shutil.rmtree(MEDIA_SYMLINK)
            else:
                os.remove(MEDIA_SYMLINK)
            print(f"Deleted existing: {MEDIA_SYMLINK}")
        except Exception as e:
            print(f"Error deleting {MEDIA_SYMLINK}: {e}")
            sys.exit(1)

    # Create symlink
    try:
        os.symlink(MEDIA_TARGET, MEDIA_SYMLINK)
        print(f"Symlink created: {MEDIA_SYMLINK} -> {MEDIA_TARGET}")
    except Exception as e:
        print(f"Error creating symlink: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
