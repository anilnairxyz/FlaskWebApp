# -*- coding: utf-8 -*-
import math
from scipy import stats


def _sample_loss(crash_rate, mean, stddev):
    '''
    Generate a loss using a Poisson-LogNormal assumption.
    '''
    crashes = stats.poisson.rvs(crash_rate)
    loss = 0
    for crash in range(crashes):
        loss += stats.lognorm.rvs(stddev, math.exp(mean))
    return loss


def _sample_market_crash_annual(macroevent_rate, macroevent_mean, macroevent_stddev,
                                selfevent_rate, selfevent_mean, selfevent_stddev):
    '''
    Sample the annual loss due to market events using a
    very simple model of Poisson-LogNormals for Macro and Company Specific events.
    '''
    macro_loss = _sample_loss(macroevent_rate, macroevent_mean, macroevent_stddev)
    self_loss = _sample_loss(selfevent_rate, selfevent_mean, selfevent_stddev)
    return macro_loss + self_loss


def estimate_annual_loss(num_samples, macroevent_rate, macroevent_mean,
                         macroevent_stddev, selfevent_rate,
                         selfevent_mean, selfevent_stddev):
    '''
    Generate a Monte-Carlo estimate of the annual market loss due to
    Macroeconomic events using a very simple model of Poisson-LogNormals
    for Marco and COmpany Specific events.
    '''
    total_loss = 0
    for sample in range(num_samples):
        total_loss += _sample_market_crash_annual(macroevent_rate, macroevent_mean,
                                                  macroevent_stddev, selfevent_rate,
                                                  selfevent_mean, selfevent_stddev)
    return total_loss / num_samples


if __name__ == '__main__':
    print (estimate_annual_loss(500, 10, 1, 1.5, 20, 2, 1.5))
