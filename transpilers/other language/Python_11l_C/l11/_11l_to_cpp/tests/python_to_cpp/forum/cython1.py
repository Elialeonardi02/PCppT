import exs2sfz, sys

if __name__ == '__main__':

    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: {0} EXSfile.exs SFZfile.sfz [samplefolder]".format('1.exs2sfz.py'))
        print()
        print("    the samplefolder argument is optional; if not specified, the program will")
        print("    attempt to locate the samples by searching folders surrounding the exs file")
        print()

        sys.exit(64)

    samplefolder = sys.argv[3] if len(sys.argv) == 4 else ''
    try:
        exs = exs2sfz.EXSInstrument(sys.argv[1], samplefolder)
        exs.convert(sys.argv[2])
    except RuntimeError as rerr:
        sys.exit(rerr)
