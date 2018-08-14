#!/usr/bin/env python3
import argparse
import bubblecheckpdf
import sys
import traceback

# ==============================================================================
class G:
    parser = None
    subparsers = None
    args = None

# ==============================================================================
def print_help():
    G.parser.print_help()

#===============================================================================
def exit_with_error(msg, code=1, exception=None):
    if exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                limit=2, file=sys.stdout)
        print("Exception:", exception)
    print(msg)
    sys.exit(code)

# ==============================================================================
def create_pdf(args):
    bubblecheckpdf.create_pdf(format=args.format)

# =========================================================================================
def help(args):
    if args.help_for:
        for p in G.subparsers.choices:
            if p in args.help_for:
                G.subparsers.choices[p].print_help()
    else:
        print_help()
    sys.exit(0)
    
# ==============================================================================
def parse_args():
    parser = G.parser = argparse.ArgumentParser(description="Create or split PDF files for bubblecheck", add_help=False)
    parser.add_argument("-?", "--help", action="help")
    parser.add_argument("--debug", action='store_true', help="Print extra information.")

    subparsers = G.subparsers = parser.add_subparsers(title='subcommands', dest='subparser_name')
    
    def add_standard_subparser(*args, **kwargs):
        subparser = subparsers.add_parser(*args, **kwargs)
        subparser.add_argument("--debug", action='store_true', help="Print extra information.")
        subparser.add_argument("-?", "--help", action="help")
        return subparser
    
    # -----------------------
    # Create PDF
    # -----------------------
    create_pdf_parser = add_standard_subparser('create', help='Create a single-page PDF exam', add_help=False)
    create_pdf_parser.add_argument('--format', help='Format of the exam', required=True)
    create_pdf_parser.add_argument('--output-file', help='File to write out to', required=True)
    create_pdf_parser.set_defaults(func=create_pdf)

    help_parser = subparsers.add_parser('help', help='Command-specific help', add_help=False)
    help_parser.add_argument('help_for', action='store', nargs='*')
    help_parser.set_defaults(func=help)

    return parser.parse_args()

# =========================================================================================
def main():
    try:
        args = parse_args()
        if args.subparser_name:
            args.func(args)
        else:
            print_help()
    except Exception as e:
        exit_with_error('An unhandled exception occurred. That makes me sad.', exception=e)

# =========================================================================================
if __name__ == '__main__':
    main()
