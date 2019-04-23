import time

from scipy import stats


def chi2_random_delay(df=2):
    """Produces a random delay based on a chi-squared prob. distribution."""
    time.sleep(stats.chi2.rvs(df))


def norm_random_delay(mean=1, sd=2):
    """Produces a random delay based on a chi-squared prob. distribution."""
    time.sleep(abs(stats.norm.rvs(mean, sd)))


def parse_delay_args(**kwargs):
    """Processes and executes delay-related function parameters"""
    if kwargs.get('c2_delay_df', None) is not None:
        chi2_random_delay(df=kwargs['c2_delay_df'])

    if kwargs.get('norm_delay_m', None) is not None and \
            kwargs.get('norm_delay_sd', None) is not None:
        norm_random_delay(
            mean=kwargs['norm_delay_m'], sd=kwargs['norm_delay_sd'])
