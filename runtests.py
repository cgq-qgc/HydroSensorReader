"""
File for running tests programmatically.
"""

import pytest


def main():
    """
    Run pytest tests.
    """
    errno = pytest.main(['-x', 'hydsensread',  '-v', '-rw', '--durations=10',
                         '--cov=hydsensread'])
    if errno != 0:
        raise SystemExit(errno)


if __name__ == '__main__':
    main()
