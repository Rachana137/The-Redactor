import argparse
from project1 import project1 as p1
import glob

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=glob.glob, required=True, help="Source File location", nargs='*',
                        action='store')
    parser.add_argument("--names", required=False, help="Redacts Names", action='store_true')
    parser.add_argument("--dates", required=False, help="Redacts dates", action='store_true')
    parser.add_argument("--phones", required=False, help="Redacts phone numbers", action='store_true')
    parser.add_argument("--genders", required=False, help="Redacts genders and gender references", action='store_true')
    parser.add_argument("--address", action="store_true", help='Redacts Addresses')
    parser.add_argument("--concept", type=str, required=True, help="Concept word removal")
    parser.add_argument("--output", action='store', required=True, help="Output File location")
    parser.add_argument("--stats", required=False,
                        help="Gives statistics for redacted files")
#, choices=("stdout", "stderr")
    args = parser.parse_args()
    files = []

    for i in args.input:
        files.extend(i)

    for i in range(0, len(files)):
        filename = (files[i])
        data = p1.input(filename)

        if (args.names):
            r_data = p1.names_(data)[0]

        if (args.dates):
            r_data = p1.Dates(r_data)[0]

        if (args.genders):
            r_data = p1.genders(r_data)[0]

        if (args.phones):
            r_data = p1.extract_phone_number(r_data)[0]

        if args.address:
            r_data = p1.address(r_data)[0]

        if (args.concept):
            r_data= p1.concept(r_data, args.concept)[0]

        if (args.stats):
            p1.stats(data, args.concept, args.stats, i)

        if args.output:
            path = args.output
            name = filename
            p1.output(r_data, name, path)

