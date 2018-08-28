#!/usr/bin/env python3
import argparse
import bubblecheckpdf
import pdf2image
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
    bubblecheckpdf.create_pdf(
        exam_format=args.exam_format,
        output_file=args.output_file,
        exam_id=123,
        exam_name='Final Exam', 
        teacher_name='Mr. Smith', 
        show_points_possible=True,
        answers=args.answers
    )

# =========================================================================================
def convert_pdf(args):
    bubblecheckpdf.convert_pdf(input_file=args.input_file, output_directory=args.output_directory, dpi=args.dpi)

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
    create_pdf_parser.add_argument('exam_format', help='Format of the exam')
    create_pdf_parser.add_argument('--answers', help='Answers for the exam')
    create_pdf_parser.add_argument('--output-file', help='File to write out to', required=True)
    create_pdf_parser.set_defaults(func=create_pdf)

    # -----------------------
    # Convert PDF -> PNG
    # -----------------------
    convert_pdf_parser = add_standard_subparser('convert', help='Convert .pdf to .png files', add_help=False)
    convert_pdf_parser.add_argument('input_file', help='PDF file to convert')
    convert_pdf_parser.add_argument('output_directory', help='Directory to which we will write files')
    convert_pdf_parser.add_argument('--dpi', help='Resolution of the conversion', default=200)
    convert_pdf_parser.set_defaults(func=convert_pdf)


    help_parser = subparsers.add_parser('help', help='Command-specific help', add_help=False)
    help_parser.add_argument('help_for', action='store', nargs='*')
    help_parser.set_defaults(func=help)

    return parser.parse_args()

# =========================================================================================
def main():
    args = parse_args()
    if args.subparser_name:
        args.func(args)
    else:
        print_help()

# =========================================================================================
if __name__ == '__main__':
    main()
