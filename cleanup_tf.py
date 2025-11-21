import os
import shutil

def cleanup_tensorflow_cache():
    cache_dirs = [
        os.path.expanduser("~/.keras"),
        os.path.expanduser("~/.cache/keras"),
        os.path.expanduser("~/.cache/tensorflow"),
        os.path.expanduser("~/.nv"),
    ]

    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            print(f"Removing: {cache_dir}")
            shutil.rmtree(cache_dir, ignore_errors=True)
        else:
            print(f"Not found: {cache_dir}")

if __name__ == "__main__":
    cleanup_tensorflow_cache()
    print("Cleanup completed successfully!")
