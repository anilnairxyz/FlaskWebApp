# -*- coding: utf-8 -*-
import math
from scipy import stats


def _sample_loss(landfall_rate, mean, stddev):
    '''
    Generate a loss using a Poisson-LogNormal assumption.
    '''
    landfalls = stats.poisson.rvs(landfall_rate)
    loss = 0
    for landfall in range(landfalls):
        loss += stats.lognorm.rvs(stddev, math.exp(mean))
    return loss


def _sample_us_hurricane_annual_loss(florida_landfall_rate, florida_mean,
                                     florida_stddev, gulf_landfall_rate,
                                     gulf_mean, gulf_stddev):
    '''
    Sample the annual economic loss due to US hurricanes using a
    very simple model of Poisson-LogNormals for Florida and Gulf landfalls.
    '''
    florida_loss = _sample_loss(florida_landfall_rate, florida_mean,
                                florida_stddev)
    gulf_loss = _sample_loss(gulf_landfall_rate, gulf_mean, gulf_stddev)
    return florida_loss + gulf_loss


def estimate_us_hurricane_annual_loss(num_monte_carlo_samples,
                                      florida_landfall_rate, florida_mean,
                                      florida_stddev, gulf_landfall_rate,
                                      gulf_mean, gulf_stddev):
    '''
    Generate a Monte-Carlo estimate of the annual economic loss due to
    US hurricanes using a very simple model of Poisson-LogNormals
    for Floria and Gulf landfalls.
    '''
    total_loss = 0
    for sample in range(num_monte_carlo_samples):
        total_loss += _sample_us_hurricane_annual_loss(florida_landfall_rate,
                                                       florida_mean,
                                                       florida_stddev,
                                                       gulf_landfall_rate,
                                                       gulf_mean, gulf_stddev)
    return total_loss / num_monte_carlo_samples


if __name__ == '__main__':
    print (estimate_us_hurricane_annual_loss(500, 10, 1, 1.5, 20, 2, 1.5))
