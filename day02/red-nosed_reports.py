"""
--- Day 2: Red-Nosed Reports ---

https://adventofcode.com/2024/day/2

--------------------- Part I ---------------------
The number of safe reports is (269)

-------------------- Part II ---------------------
The number of safe-ish reports is (337)
"""


import pandas as pd


def detect_safe_reports(reports: pd.DataFrame) -> pd.Series:
    report_diffs = reports.diff()
    null_ok = report_diffs.isna()
    increases = (null_ok | (report_diffs > 0)).all()
    decreases = (null_ok | (report_diffs < 0)).all()
    diff_le_3 = (null_ok | (report_diffs.abs() <= 3)).all()
    safe_reports = (increases | decreases) & diff_le_3
    assert isinstance(safe_reports, pd.Series)
    return safe_reports


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType("r"), help="file input to run the code with")
    parser.add_argument("-v", action="store_true", help="verbose")
    parser.add_argument(
        "--test",
        action="store_true",
        help="ignores file input and runs test file `example`",
    )
    args = parser.parse_args()

    if args.test:
        filename = "example.txt"
        file = open(filename, "r")
    elif args.f:
        file = args.f
    else:
        raise Exception("File or test must be specified")

    print()
    print(" Part I ".center(50, "-"))
    raw_inputs = [tuple(map(int, line.split())) for line in file.readlines()]
    reports = pd.DataFrame(raw_inputs).T  # transpose b/c most methods use axis=0
    safe_reports = detect_safe_reports(reports)
    n_safe_reports = safe_reports.sum()
    print(f"The number of safe reports is ({n_safe_reports})")

    if args.test:
        ans = 2
        assert n_safe_reports == ans, f"The number of safe reports doesn't match the expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    dropout_results = []
    for i in range(reports.shape[0]):
        dropout = reports.drop(i)
        safe_dropout = detect_safe_reports(dropout)
        dropout_results.append(safe_dropout)
    safeish_reports = pd.DataFrame(dropout_results).any()
    n_safeish_reports = safeish_reports.sum()
    print(f"The number of safe-ish reports is ({n_safeish_reports})")

    if args.test:
        ans = 4
        assert n_safeish_reports == ans, f"The number of safe-ish reports doesn't match the expected ({ans})"

