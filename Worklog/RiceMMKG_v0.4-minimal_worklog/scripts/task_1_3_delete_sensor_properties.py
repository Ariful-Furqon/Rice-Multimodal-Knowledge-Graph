#!/usr/bin/env python3
"""Task 1.3 — Checkpoint C2 resolved per the worklog's own recommendation:
delete the four sensor datatype properties (humidityValue, temperatureValue,
rainfallValue, soilMoistureValue). Their domain (SensorReading) was deleted
in Task 1.1, they hold zero assertions, and re-adding them alongside a
sensor modality later is trivial.
"""
import argparse
from rdflib import Graph, Namespace

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

PROPS_TO_REMOVE = ["humidityValue", "temperatureValue", "rainfallValue", "soilMoistureValue"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)

    removed = 0
    for local in PROPS_TO_REMOVE:
        p = RICE[local]
        assert sum(1 for _ in g.triples((None, p, None))) == 0, f"{local} has assertions, refusing to delete"
        for t in list(g.triples((p, None, None))):
            g.remove(t)
            removed += 1

    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Sensor datatype properties deleted: {len(PROPS_TO_REMOVE)}")
    print(f"Triples removed: {removed}")
    print(f"Triple count before: {before}, after: {after}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
