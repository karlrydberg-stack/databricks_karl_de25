import dlt
from pyspark.sql.types import StructType

BASE_DIR = "/Volumes/supply_chain_demo/default/raw/"

# Infer schema from CSV outside the streaming table
schema = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{BASE_DIR}/data/DataCoSupplyChainDataset.csv")
    .schema
)

@dlt.table(
    name="raw_supply_chain",                        # no catalog/schema prefix here
    comment="Raw orders data as the bronze layer in medallion architecture",
    table_properties={
        "delta.columnMapping.mode": "name",
        "delta.minReaderVersion": "2",
        "delta.minWriterVersion": "5",
    },
)
def raw_supply_chain():
    return (
        spark.readStream.format("csv")
        .option("header", "true")
        .option("encoding", "UTF-8")
        .schema(schema)
        .load(f"{BASE_DIR}")
    )