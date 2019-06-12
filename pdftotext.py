from subprocess import Popen


PDFTOTXT_BIN = "bin/pdftotext.exe"
TEMP_FILE = '.temp'


def _invoke_bin(args, executable, timeout=None, verbose=False):
    # TODO 1: Handle standard output and errors
    # TODO 2[SECURITY]: Implement hash checking for security

    if verbose:
        print("Executing {} {}".format(executable, " ".join(args)))

    with Popen(args, executable=PDFTOTXT_BIN) as proc:
        try:
            return proc.wait(timeout=timeout)
        except:
            proc.kill()
            raise


def _invoke_pdftotext(args, timeout=None, verbose=False):
    return _invoke_bin(args, PDFTOTXT_BIN, timeout, verbose)


def convert(pdf_file, output=None, start=None, end=None, simple=True, layout=False,
            table=False, lineprinter=False, raw=False, fixed_pitch=None, linespacing=None,
            clip=False, no_diag=False, encoding=None, eol=None, no_pgbreak=False,
            bom=False, opw=None, upw=None, no_error_msg=True, cfg_file=None, verbose=False):
    # TODO: Lot of work, process all the arguments properly

    # NOTE: FIX: Adding " " in arguments list as popen is ignoring first
    # argument in the list probably due to a BUG
    args = [" "]

    # Optional Args
    if start:
        args.append('-f')
        args.append(str(start))

    if end:
        args.append('-l')
        args.append(str(end))

    if simple:
        args.append('-simple')

    if table:
        args.append('-table')

    if layout:
        args.append('-layout')

    # Required Args
    args.append(pdf_file)

    # TODO: Handle errors and return properly
    if output is None:
        # If output==None, then return the extracted text
        args.append(TEMP_FILE)
        _invoke_pdftotext(args, verbose=verbose)
        # Read temp file
        with open(TEMP_FILE, 'r', encoding="utf-8") as fp:
            return fp.read()

    elif isinstance(output, str):
        # if output is filename
        args.append(output)
        _invoke_pdftotext(args, verbose=verbose)
        return

    else:
        # if output is none of the above the assuming it to be a file handler
        try:
            output.write(convert(pdf_file, None, start, end, simple, layout,
                                 table, lineprinter, raw, fixed_pitch, linespacing,
                                 clip, no_diag, encoding, eol, no_pgbreak,
                                 bom, opw, upw, no_error_msg, cfg_file, verbose))

        except AttributeError:
            raise AttributeError(
                "'output' should be either a file name or file handler capable of handling write.")


def bin_version():
    """Not Implemented"""
    # TODO: Func should return version number of binary
    pass

def update():
    """Not Implemented"""
    # TODO: Implement binary update, retrive changelog and new binary from their website and check hashes for security
    pass



