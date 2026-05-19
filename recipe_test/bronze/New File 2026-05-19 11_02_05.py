from pyspark import pipelines as dp

BASE_DIR = "/Volumes/test/landing/raw/"

schema = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .option("multiLine", "true")
    .option("escape", '"')
    .load(f"{BASE_DIR}recipes.csv")
    .schema
)

@dp.table(
    name="test.bronze.raw_recipes",
    comment="Raw recipes data as the bronze layer in medallion architecture",
    table_properties={
        "delta.columnMapping.mode": "name",
        "delta.minReaderVersion": "2",
        "delta.minWriterVersion": "5",
    },
)
def raw_recipes():
    return (
        spark.readStream.format("csv")
        .options(header="true", encoding="UTF-8")
        .option("multiLine", "true")
        .option("escape", '"')
        .schema(schema)
        .load(BASE_DIR)
    )