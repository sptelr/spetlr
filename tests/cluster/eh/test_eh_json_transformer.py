import json

from atc_tools.testing import DataframeTestCase
from atc_tools.time import dt_utc
from pyspark.sql.types import BinaryType, StructField, StructType, TimestampType

from atc import Configurator
from atc.delta import DeltaHandle
from atc.orchestrators.ehjson2delta.EhJsonToDeltaTransformer import (
    EhJsonToDeltaTransformer,
)
from atc.spark import Spark


class JsonEhTransformerUnitTests(DataframeTestCase):
    tc: Configurator
    capture_eventhub_output_schema = StructType(
        [
            StructField("Body", BinaryType(), True),
            StructField("pdate", TimestampType(), True),
            StructField("EnqueuedTimestamp", TimestampType(), True),
        ]
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.tc = Configurator()
        cls.tc.set_debug()
        cls.tc.clear_all_configurations()

        cls.tc.register("TblPdate1", {"name": "TablePdate1{ID}"})
        cls.tc.register("TblPdate2", {"name": "TablePdate2{ID}"})
        cls.tc.register("TblPdate3", {"name": "TablePdate3{ID}"})

        spark = Spark.get()

        spark.sql(f"DROP TABLE IF EXISTS {cls.tc.table_name('TblPdate1')}")
        spark.sql(f"DROP TABLE IF EXISTS {cls.tc.table_name('TblPdate2')}")
        spark.sql(f"DROP TABLE IF EXISTS {cls.tc.table_name('TblPdate3')}")

        spark.sql(
            f"""
                CREATE TABLE {cls.tc.table_name('TblPdate1')}
                (id int, name string, BodyJson string, pdate timestamp,
                EnqueuedTimestamp timestamp)
                PARTITIONED BY (pdate)
            """
        )

        spark.sql(
            f"""
                CREATE TABLE {cls.tc.table_name('TblPdate2')}
                (id int, name string, pdate timestamp, EnqueuedTimestamp timestamp)
                PARTITIONED BY (pdate)
            """
        )

        spark.sql(
            f"""
                CREATE TABLE {cls.tc.table_name('TblPdate3')}
                (id int, name string, pdate timestamp, EnqueuedTimestamp timestamp,
                Unknown string)
                PARTITIONED BY (pdate)
            """
        )

    def test_transformer_w_body(self):
        """Tests whether the body is saved as BodyJson"""
        dh = DeltaHandle.from_tc("TblPdate1")

        df_in = Spark.get().createDataFrame(
            [
                (
                    json.dumps(
                        {
                            "id": "1234",
                            "name": "John",
                        }
                    ).encode("utf-8"),
                    dt_utc(2021, 10, 31, 0, 0, 0),  # pdate
                    dt_utc(2021, 10, 31, 0, 0, 0),  # EnqueuedTimestamp
                ),
            ],
            self.capture_eventhub_output_schema,
        )

        expected = Spark.get().createDataFrame(
            [
                (
                    1234,
                    "John",
                    json.dumps(
                        {
                            "id": "1234",
                            "name": "John",
                        }
                    ),
                    dt_utc(2021, 10, 31, 0, 0, 0),
                    dt_utc(2021, 10, 31, 0, 0, 0),
                ),
            ],
            dh.read().schema,
        )

        df_result = EhJsonToDeltaTransformer(target_dh=dh).process(df_in)

        # Check that data is correct
        self.assertDataframeMatches(df_result, None, expected)

    def test_transformer(self):
        """Test if the data is correctly extracted"""
        dh = DeltaHandle.from_tc("TblPdate2")

        df_in = Spark.get().createDataFrame(
            [
                (
                    json.dumps(
                        {
                            "id": "1234",
                            "name": "John",
                        }
                    ).encode("utf-8"),
                    dt_utc(2021, 10, 31, 0, 0, 0),  # pdate
                    dt_utc(2021, 10, 31, 0, 0, 0),  # EnqueuedTimestamp
                )
            ],
            self.capture_eventhub_output_schema,
        )

        expected = Spark.get().createDataFrame(
            [
                (
                    1234,
                    "John",
                    dt_utc(2021, 10, 31, 0, 0, 0),
                    dt_utc(2021, 10, 31, 0, 0, 0),
                ),
            ],
            dh.read().schema,
        )

        df_result = EhJsonToDeltaTransformer(target_dh=dh).process(df_in)

        # Check that data is correct
        self.assertDataframeMatches(df_result, None, expected)

    def test_transformer_unknown_target_field(self):
        """This should test what happens if the target
        schema has a field that does not exist in the source dataframe."""
        dh = DeltaHandle.from_tc("TblPdate3")

        df_in = Spark.get().createDataFrame(
            [
                (
                    json.dumps(
                        {
                            "id": "1234",
                            "name": "John",
                        }
                    ).encode("utf-8"),
                    dt_utc(2021, 10, 31, 0, 0, 0),  # pdate
                    dt_utc(2021, 10, 31, 0, 0, 0),  # EnqueuedTimestamp
                )
            ],
            self.capture_eventhub_output_schema,
        )

        expected = Spark.get().createDataFrame(
            [
                (
                    1234,
                    "John",
                    dt_utc(2021, 10, 31, 0, 0, 0),
                    dt_utc(2021, 10, 31, 0, 0, 0),
                    None,
                ),
            ],
            dh.read().schema,
        )

        df_result = EhJsonToDeltaTransformer(target_dh=dh).process(df_in)

        # Check that data is correct
        self.assertDataframeMatches(df_result, None, expected)
