from feast import FeatureView, ValueType, Entity, FileSource, Field
from feast.types import Array, Float32, String
from feast.data_format import ParquetFormat
from datetime import timedelta

document = Entity(
    name="id",
    description="Document ID",
    value_type=ValueType.INT64,
)

source = FileSource(
    file_format=ParquetFormat(),
    path="../scripts/rag-mini-wikipedia-embeddings.parquet",
    event_timestamp_column="event_timestamp",
)

# Define the view for retrieval
docs_embeddings_feature_view = FeatureView(
    name="docs_embeddings",
    entities=[document],
    schema=[
        Field(
            name="embedding",
            dtype=Array(Float32),
            vector_index=True,                # Vector search enabled
            vector_search_metric="L2",    # Distance metric configured
        ),
        Field(name="passage", dtype=String),
    ],
    source=source,
    ttl=timedelta(hours=2),
)