import unittest
import numpy
import os
import os.path
import sqlite3
from contextlib import closing
import lte.infrastructure as inf


class NumpyArrayIO(unittest.TestCase):
    def test_what_was_saved_can_be_read(self):
        array = numpy.random.rand(5, 5)
        serialized = inf.dump_to_string(array)
        deserialized = inf.load_from_string(serialized)


class SqlStorageTest(unittest.TestCase):
    tempfile = 'abc.sql'

    def count(self):
        with closing(sqlite3.connect(self.tempfile)) as db:
            num_sim, num_exec = 0, 0

            with closing(db.execute('SELECT COUNT(*) FROM Simulation')) as c:
                num_sim = int(c.fetchone()[0])
            
            with closing(db.execute('SELECT COUNT(*) FROM Execution')) as c:
                num_exec = int(c.fetchone()[0])

            return (num_sim, num_exec)

    def assert_executions_equal(self, expected, actual):
        self.assertEqual(expected.seed, actual.seed)
        self.assertTrue(numpy.all(expected.rate_history == actual.rate_history))
        self.assertTrue(numpy.all(expected.selection_history == \
                actual.selection_history))

    def setUp(self):
        if os.path.isfile(self.tempfile):
            os.unlink(self.tempfile)

    def test_creates_database(self):
        with inf.SqlStorage(self.tempfile) as storage:
            pass

        self.assertEqual((0, 0), self.count())

    def test_adds_simulation(self):
        sim = inf.Simulation()
        with inf.SqlStorage(self.tempfile) as storage:
            storage.add_simulation(sim)

        self.assertEqual((1, 0), self.count())

    def test_adds_execution(self):
        sim = inf.Simulation()
        with inf.SqlStorage(self.tempfile) as storage:
            storage.add_simulation(sim)

            for i in xrange(10):
                ex = inf.Execution(i, numpy.random.rand(5, 5), numpy.random.rand(5, 5))
                storage.add_execution(sim, ex)
        
        self.assertEqual((1, 10), self.count())

    def test_retrieves_executions(self):
        sim = inf.Simulation()
        ex1, ex2 = None, None
        with inf.SqlStorage(self.tempfile) as storage:
            storage.add_simulation(sim)
            ex1 = inf.Execution(1, numpy.random.rand(5, 5), numpy.random.rand(5, 5))
            ex2 = inf.Execution(2, numpy.random.rand(5, 5), numpy.random.rand(5, 5))
            
            storage.add_execution(sim, ex1)
            storage.add_execution(sim, ex2)

        with inf.SqlStorage(self.tempfile) as storage:
            r1 = storage.get_execution(1)
            r2 = storage.get_execution(2)

            self.assert_executions_equal(ex1, r1)
            self.assert_executions_equal(ex2, r2)

if __name__ == "__main__":
    unittest.main()
