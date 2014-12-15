import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("usage:%s resource_type\n" % sys.argv[0])
        sys.exit(1)
    fin = sys.stdin
    print fin.read() % {'resource_type':sys.argv[1]}
