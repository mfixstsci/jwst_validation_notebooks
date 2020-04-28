import argparse
import os, sys, stat

def change_permissions(files_to_convert):
    """Set permissions for files using os.chmod
    
    Parameters
    ----------
    files_to_convert : list like
        List of files to change permissions of.
    """
    for f in files_to_convert:
        os.chmod(f, stat.S_IREAD|
                    stat.S_IWRITE|
                    stat.S_IEXEC|
                    stat.S_IRGRP|
                    stat.S_IWGRP|
                    stat.S_IXGRP)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', default=None, dest='files',
                        nargs='+', help='Path of files')
    args = parser.parse_args()

    change_permissions(args.files)

if __name__ == '__main__':
    main()