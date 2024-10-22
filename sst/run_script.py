import argparse
import logging
from security_baseline_tester import SecurityBaselineTester
import os

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description="AWS Security Baseline Tester")
    parser.add_argument("--profile", default="default", help="AWS IAM user profile")
    parser.add_argument("--language", choices=["ENG", "KOR", "JPN"], default="ENG", help="Language for the report")
    return parser.parse_args()

def main():
    setup_logging()
    args = parse_arguments()
    tester = SecurityBaselineTester(args.profile, args.language)
    tester.run()

if __name__ == "__main__":
    main()