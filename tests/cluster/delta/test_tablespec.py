import unittest

from spetlr import Configurator
from spetlr.configurator.sql.parse_sql import parse_sql_code_to_config
from spetlr.delta.table_spec import DbSpec
from spetlr.spark import Spark


class TestTableSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        c = Configurator()
        c.clear_all_configurations()
        c.set_debug()

    def test_DbSpecFromDisk(self):
        c = Configurator()
        c.clear_all_configurations()
        master_sql = """
            -- SPETLR.CONFIGURATOR key: MyDbAlias
            CREATE DATABASE IF NOT EXISTS my_db_name{ID}
            COMMENT "Really great db"
            LOCATION "/tmp/my_db{ID}";
            """
        config = parse_sql_code_to_config(master_sql)

        k, v = config.popitem()
        self.assertEqual(k, "MyDbAlias")
        c.register(k, v)
        db_parsed = DbSpec.from_tc(k)
        Spark.get().sql(master_sql)
        db_read = DbSpec.from_spark(db_parsed.name)

        self.assertEqual(db_parsed, db_read)

        Spark.get().sql(f"DROP DATABASE {db_parsed.name} CASCADE")
