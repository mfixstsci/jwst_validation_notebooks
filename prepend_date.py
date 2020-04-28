import argparse
import datetime
import os

def prepend_date_to_report(reportfile):
    """Add date to filename
    
    Parameters
    ----------
    reportfile : str
        name of report to add date to
    """

    now = datetime.datetime.now().isoformat()

    if os.path.exists(reportfile):
        os.rename(reportfile, now + '-' + reportfile) 
    else:
        print("Path not provided, continuing")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reportfile', default=None, dest='report',
                        help='Path to report file')
    args = parser.parse_args()

    prepend_date_to_report(args.report)

if __name__ == '__main__':
    main()