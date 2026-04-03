# nihonmichi

This repository contains resources for the nihonmichi site.

# Routing

[GPX](https://grokipedia.com/page/GPS_Exchange_Format) files live in
[./gpx](./gpx). You can view these files in your favorite GPX viewer.
Intermediate points in tracks may seem arbitrary--they were added to assist
[OsmAnd](https://osmand.net/) in navigation.

# Tooling

[./tools/gpx-consolidator.py](./tools/gpx-consolidator.py) can combine multiple
GPX files into a single GPX file. See the tool's help text for usage details.
The combined file is meant for convenience; prefer the individual GPX files for
correctness.
