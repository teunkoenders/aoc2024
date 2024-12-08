import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--install_reactor_mounted_problem_dampener', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day2_red_nosed_reports/input.{'test' if args.test else 'prd'}") as f:
        lines = f.readlines()
    
    return [list(map(int, line.split())) for line in lines]

def assert_report_is_safe(report):
    diff_first_indexes = report[0] - report[1]    
    is_increasing = diff_first_indexes > 0
    for nr1, nr2 in zip(report, report[1:]):
        diff = nr1 - nr2
        assert diff > 0 if is_increasing else diff < 0
        assert abs(diff) >= 1 and abs(diff) <= 3

def assert_report_with_problem_dampener(report):
    try:
        return assert_report_is_safe(report)
    except AssertionError:
        pass
    
    for index in range(len(report)):
        try:
            tmp = report.copy()
            tmp.pop(index)
            return assert_report_is_safe(tmp)
        except AssertionError:
            pass
    assert False

def solve(reports):
    safe_reports = 0

    for report in reports:
        try:
            if args.install_reactor_mounted_problem_dampener:
                assert_report_with_problem_dampener(report)
            else: 
                assert_report_is_safe(report)
            safe_reports += 1
        except AssertionError:
            pass
    
    print(safe_reports)

if __name__ == "__main__":
    solve(read_input())