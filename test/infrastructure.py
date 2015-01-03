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


if __name__ == "__main__":
    unittest.main()
