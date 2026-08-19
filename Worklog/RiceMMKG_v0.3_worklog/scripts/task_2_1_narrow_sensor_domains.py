#!/usr/bin/env python3
"""Task 2.1 — narrow the domain of the four sensor datatype properties from
rice:Observation to rice:SensorReading. observationDate, confidenceScore,
and severityScore keep their Observation domain.
"""
import argparse
from rdflib import Graph, Namespace, RDFS

RICE = Namespace("http://www.semanticweb.org/arifu/ontologies/2026/3/riceMMKG#")

SENSOR_PROPS = [
    "humidityValue", "temperatureValue", "rainfallValue", "soilMoistureValue",
]


def apply(g):
    changed = 0
    for name in SENSOR_PROPS:
        p = RICE[name]
        old = (p, RDFS.domain, RICE.Observation)
        new = (p, RDFS.domain, RICE.SensorReading)
        if old in g:
            g.remove(old)
            changed += 1
        if new not in g:
            g.add(new)
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.input, format="xml")
    before = len(g)
    changed = apply(g)
    after = len(g)
    g.bind("rice", RICE)
    g.serialize(destination=args.output, format="pretty-xml")
    print(f"Domain triples changed: {changed}")
    print(f"Triple count before: {before}, after: {after}, delta: {after - before}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
