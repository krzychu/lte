import unittest
import numpy
import os
import os.path
import lte.infrastructure as inf


class NumpyArrayIO(unittest.TestCase):
    def test_what_was_saved_can_be_read(self):
        array = numpy.random.rand(5, 5)
        serialized = inf.dump_to_string(array)
        deserialized = inf.load_from_string(serialized)


class SqlStorageTest(unittest.TestCase):
    tempfile = 'abc.sql'

    def setUp(self):
        if os.path.isfile(self.tempfile):
            os.unlink(self.tempfile)

    def test_creates_database(self):
        with inf.SqlStorage(self.tempfile) as storage:
            pass

    def test_adds_simulation(self):
        sim = inf.Simulation()
        sim.channel = int
        sim.scheduler = str

        with inf.SqlStorage(self.tempfile) as storage:
            storage.add_simulation(sim)


if __name__ == "__main__":
    unittest.main()
