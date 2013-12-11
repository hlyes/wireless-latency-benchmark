#-*- coding: utf-8 -*-

import unittest
import common
import time

class StopWatchTest(unittest.TestCase):
	def test_run(self):
		watch = common.StopWatch()
		time.sleep(1)
		dt = watch.stop()
		self.assertAlmostEqual(dt, 1.0, places=2)

class TimeHistoryContainer_get_stats_list_Test(unittest.TestCase):
	def test_remove_first_last_disable(self):
		container = common.TimeHistoryContainer()
		container.append(1)
		container.append(2)
		container.append(3)
		container.append(4)
		self.assertEqual([1, 2, 3, 4], container.get_stats_list(remove_first_last=False))

	def test_remove_first_last_enabled(self):
		container = common.TimeHistoryContainer()
		container.append(1)
		container.append(2)
		container.append(3)
		container.append(4)
		self.assertEqual([2, 3], container.get_stats_list(remove_first_last=True))

	def test_reverse_disabled(self):
		container = common.TimeHistoryContainer()
		container.append(1)
		container.append(3)
		container.append(2)
		self.assertEqual([1, 2, 3], container.get_stats_list(reverse=False))

	def test_reverse_enabled(self):
		container = common.TimeHistoryContainer()
		container.append(1)
		container.append(3)
		container.append(2)
		self.assertEqual([3, 2, 1], container.get_stats_list(reverse=True))

class EchoGeneratorTest(unittest.TestCase):
	def test_call(self):
		generator = common.EchoGenerator('%02d msg')
		self.assertEqual('01 msg', generator())
		self.assertEqual('02 msg', generator())
		self.assertEqual('03 msg', generator())

if __name__ == "__main__":
	unittest.main()