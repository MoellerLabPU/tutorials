#!/usr/bin/env python3

import argparse
import logging
import time
from multiprocessing import Pool, cpu_count


def parse_args():
    parser = argparse.ArgumentParser(
        description="A simple multiprocessing script that calculates squares and logs the output."
    )
    parser.add_argument(
        "--cpus",
        type=int,
        default=4,
        help="Number of CPU processes to use (default: 4).",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="results.csv",
        help="Path to the CSV file where results will be stored (default: results.csv).",
    )
    return parser.parse_args()


def calculate_square(number):
    """Function to calculate the square of a number."""
    result = number**2
    # Log to stderr (default logging)
    logging.info(f"Calculated square of {number}: {result}")
    time.sleep(1)  # simulate some longer-running task
    return result


def main():
    args = parse_args()

    # Configure logging WITHOUT specifying a filename, so logs go to stderr by default.
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [Process %(processName)s] %(message)s"
    )

    logging.info("Starting the multiprocessing example script.")

    # Generate a list of 720 tasks so the job takes ~2–3 minutes with 4 processes.
    # (720 / 4 processes = 180 tasks per process, each sleeping 1s => ~3 minutes)
    numbers = list(range(1, 300))

    # Use either the user-specified number of CPUs or the system's max
    num_processes = min(args.cpus, cpu_count())
    logging.info(f"Using {num_processes} processes.")

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Map the calculate_square function across the numbers
        results = pool.map(calculate_square, numbers)

    logging.info("All processes have completed. Writing results to CSV...")

    # Write final results to a CSV file (the user-specified output file)
    with open(args.output_file, "w") as f:
        f.write("number,square\n")
        for n, sqr in zip(numbers, results):
            f.write(f"{n},{sqr}\n")

    logging.info(f"Results written to {args.output_file}")
    logging.info("Done.")


if __name__ == "__main__":
    main()
