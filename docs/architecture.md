# Architecture

The package is structured following the same structure as [CloudEvents spec](https://github.com/cloudevents/spec/tree/main)
in the following modules:

- `events` implements the base `CloudEvent` model, required fields and canonical data types serialization.
- `formats` implements the logic for serialization and deserialization between the `CloudEvent` model
  and formats ([JSON](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/json-format.md),
  [AVRO](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/avro-format.md), etc.). These are
  not usually used directly.
- `bindings` implements the logic for serialization and deserialization between the `CloudEvent` model
  and protocol bindings (HTTP, KAFKA, etc.). It reuses functions from `formats` when necessary (i.e. [HTTP in
  structured JSON mode](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md#32-structured-content-mode)
  will use the already implemented JSON format)
