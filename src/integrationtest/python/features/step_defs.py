# -*- coding: utf-8 -*-
import os

from lettuce import *
from hamcrest import *

import analyzer.main

TEST_HOST_METRICS_FILE_PATH = '../../../target/test_host_metrics.txt'

test_host_metrics = [
  'hostA,1366829460,1366831260,60|None,None,100.0,100.0,99.0,99.0',
  'hostB,1366829460,1366831260,60|37.0,65.0,87.0',
  'hostC,1366829460,1366831260,60|100.0,100.0'
]
analyzed_test_host_metrics = [
  'hostB: Average: 63.0 Max: 87.0 Min: 37.0',
  'hostA: Average: 99.5 Max: 100.0 Min: 99.0',
  'hostC: Average: 100.0 Max: 100.0 Min: 100.0'
]

# Create a temporary test data file so build is fully repeatable and doesn't have
# dependency on pre-existing data file
@step(u'Given a host metric file')
def given_a_host_metric_file(step):
  test_host_metrics_file = open(TEST_HOST_METRICS_FILE_PATH, 'w')

  for host_metric in test_host_metrics:
    test_host_metrics_file.write("%s\n" % host_metric)

  test_host_metrics_file.close()

@step(u'When I analyze the file')
def when_i_analyze_the_file(step):
  world.processed_metrics = analyzer.main.process_metrics(TEST_HOST_METRICS_FILE_PATH)

@step(u'Then I will get the computed min, max, and avg for each host')
def then_i_will_get_the_computed_min_max_and_avg_for_each_host(step):
  assert True, (world.processed_metrics.find(analyzed_test_host_metrics[0]) != -1)
  assert True, (world.processed_metrics.find(analyzed_test_host_metrics[1]) != -1)
  cleanup()

@step(u'Then I will see the analyzed metrics in descending order by average')
def then_i_will_see_the_analyzed_metrics_in_descending_order_by_average(step):
  sorted_metrics_as_arr = world.processed_metrics.split('\n')
  assert_that(sorted_metrics_as_arr[0], starts_with('hostC'))
  assert_that(sorted_metrics_as_arr[1], starts_with('hostA'))
  assert_that(sorted_metrics_as_arr[2], starts_with('hostB'))
  cleanup()

def cleanup():
  os.remove(TEST_HOST_METRICS_FILE_PATH)  
