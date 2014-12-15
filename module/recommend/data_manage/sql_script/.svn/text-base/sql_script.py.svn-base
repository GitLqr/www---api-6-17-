import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("usage:%s database_name\n" % sys.argv[0])
        sys.exit(1)
    fin = sys.stdin
    print fin.read() % {'database':sys.argv[1]}
