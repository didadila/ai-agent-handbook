"""Each nonempty stdin line contains exactly two integers; print each sum."""
import sys
from algorithms import read_pairs


def solve(data):
    return "\n".join(str(a + b) for a, b in read_pairs(data))


if __name__ == "__main__":
    output = solve(sys.stdin.read())
    if output:
        sys.stdout.write(output + "\n")
