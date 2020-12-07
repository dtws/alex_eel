"""===============================================================================

        FILE: alex_eel/__init__.py

       USAGE: (not intended to be directly executed)

 DESCRIPTION:

     OPTIONS: ---
REQUIREMENTS: ---
        BUGS: ---
       NOTES: ---
      AUTHOR: Alex Leontiev (nailbiter@dtws-work.in)
ORGANIZATION: Datawise Inc.
     VERSION: ---
     CREATED: 2020-11-18T15:49:54.605548
    REVISION: ---

==============================================================================="""

import graphviz
from uuid import uuid4
import logging
import numpy as np


def _add_logger(f):
    logger = logging.getLogger(f.__name__)

    def _f(*args, **kwargs):
        return f(*args, logger=logger, **kwargs)
    _f.__name__ = f.__name__
    return _f


def _vertices(chain):
    vertices = set.union(*[{s, d} for s, d, r in chain])
    vertices = {v: f"v_{str(uuid4()).replace('-','_')}" for v in vertices}
    return vertices


def print_chain(chain, output_format="svg"):
    """
    param `chain` -- array [(src_1,dst_1,resistance_1),(src_2,dst_2,resistance_2),...,(src_N,dst_N,resistance_N)]
    describing the edges of the electrical network graph
    """
    assert output_format in ["svg", "graphviz"]
    dot = graphviz.Graph(graph_attr={"rankdir": "LR", "splines": "ortho"})
    vertices = _vertices(chain)

    for v, u in vertices.items():
        dot.node(str(u), str(v), shape="ellipse")
    for i,(s,d,r) in enumerate(chain):
        dot.node(f"r_{i}", str(r), shape="box")
    for i,(s, d, r) in enumerate(chain):
        dot.edge(vertices[s], f"r_{i}")
        dot.edge(f"r_{i}", vertices[d])

    if output_format == "graphviz":
        return dot.source
    elif output_format == "svg":
        dot.format = "svg"
        fn = f"/tmp/{uuid4()}"
        dot.render(filename=fn)
        with open(f"{fn}.svg") as f:
            res = f.read()
        return res


@_add_logger
def compute_currents(chain, src, dst, logger=None, voltage=1):
    """
    param `chain` -- same is and `print_chain`
    param `src`, `dst` -- source and destination
    param `voltage` voltage difference applied to `src` and `dst`
    """
    assert voltage != 0
    vertices = _vertices(chain)
    assert src in vertices and dst in vertices

    sorted_vertices = sorted([v for v in vertices])
    sorted_vertices = {v: i for i, v in enumerate(sorted_vertices)}
    for i, (s, d, r) in enumerate(chain):
        if sorted_vertices[s] > sorted_vertices[d]:
            chain[i] = (d, s, r)

    sorted_vertices = sorted([v for v in vertices if v != src and v != dst])

    A, b = [], np.zeros(len(chain)+len(sorted_vertices))
    # setting up equations corresponding to definition of resistance: $i_{src\to dst} \cdot r = u_{dst}-u_{src}$
    for i, (s, d, r) in enumerate(chain):
        a = np.zeros(len(chain)+len(sorted_vertices))
        a[i] = r
        for sign, sd in zip([-1, 1], [s, d]):
            if sd == src:
                pass
            elif sd == dst:
                b[i] = sign*voltage
            else:
                a[len(chain)+sorted_vertices.index(sd)] = -sign
        A.append(a)

    # setting up equations corresponding to [Kirchhoff's current law](https://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws#Kirchhoff's_current_law): $\forall dst: \sum_{src} i_{src\to\dst} = 0$
    for v in sorted_vertices:
        a = np.zeros(len(chain)+len(sorted_vertices))
        for i, (s, d, r) in enumerate(chain):
            for sign, sd in zip([-1, 1], [s, d]):
                if sd == v:
                    a[i] = sign
        A.append(a)
    logger.info(f"A: {A}")
    A = np.array(A)
    logger.info(f"b: {b}")
    x = np.linalg.solve(A, b)

    return {
        "currents": list(x[0:len(chain)]),
        "voltages": {v: u for v, u in zip(sorted_vertices, x[len(chain):])},
        "equivalent_resistance": voltage/sum([i for i, (_, d, _) in zip(x[0:len(chain)], chain) if d == dst])
    }
