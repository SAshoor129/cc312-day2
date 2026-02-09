import argparse

VALID_LEVELS = {"INFO", "WARN", "ERROR"}

def parse_args():
    parser = argparse.ArgumentParser(description="Filter cloud logs")

    parser.add_argument(
        "--level",
        type=str,
        help="Filter by level (INFO, WARN, ERROR)"
    )

    parser.add_argument(
        "--service",
        type=str,
        help="Filter by service (auth, api, db, billing, etc.)"
    )

    parser.add_argument(
        "--out",
        type=str,
        default="filtered_logs.txt",
        help="Output filename"
    )

    return parser.parse_args()


def is_valid_line(line):
    parts = line.strip().split("|")

    if len(parts) != 4:
        return False, None

    timestamp = parts[0].strip()
    level = parts[1].strip().upper()
    service = parts[2].strip()
    message = parts[3].strip()

    if level not in VALID_LEVELS:
        return False, None

    return True, (timestamp, level, service, message)


def main():
    args = parse_args()

    level_filter = args.level.upper() if args.level else None
    service_filter = args.service
    output_file = args.out

    valid_count = 0
    written_count = 0

    with open("logs.txt", "r") as infile, open(output_file, "w") as outfile:

        for line in infile:

            valid, data = is_valid_line(line)

            if not valid:
                continue

            valid_count += 1

            timestamp, level, service, message = data

            if level_filter and level != level_filter:
                continue

            if service_filter and service != service_filter:
                continue

            outfile.write(f"{timestamp} | {level} | {service} | {message}\n")

            written_count += 1

    print(f"Valid lines scanned: {valid_count}")
    print(f"Lines written: {written_count}")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()
