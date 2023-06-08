import unittest
from unittest.mock import Mock

from spetlrtools.testing import DataframeTestCase

from spetlr.autoloader import AutoloaderHandle
from spetlr.delta import DeltaHandle
from spetlr.etl.loaders.stream_loader import StreamLoader
from spetlr.spark import Spark


# Tests are runned for spark versions lower than 10_4
# To ensure that the correct assertions are made.
@unittest.skipUnless(
    Spark.version() < Spark.DATABRICKS_RUNTIME_10_4,
    f"Sparkversion tests only applies for spark runtime versions lower than 10_4,"
    f"Your version {Spark.version()}. Skipping...",
)
class SparkVersionTests(DataframeTestCase):
    def test_01_streamloader(self):
        with self.assertRaises(AssertionError):
            StreamLoader(
                handle=Mock(),
                options_dict={},
                format="delta",
                await_termination=True,
                mode="append",
                checkpoint_path="testpath",
            ).save(Mock())

    def test_02_autoloader(self):
        with self.assertRaises(AssertionError):
            AutoloaderHandle(
                location="test", schema_location="test", data_format="test"
            ).read_stream()

    def test_03_deltahandle_read_stream(self):
        with self.assertRaises(AssertionError):
            DeltaHandle(name="test").read_stream()
