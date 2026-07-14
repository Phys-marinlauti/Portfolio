# Transfer-Market GNN

A message-passing neural network (MPNN / NNConv, PyTorch Geometric) that
models the global football transfer market as a directed complex network, with 
clubs as nodes, individual transfers as attributed edges, and predicts
whether a club will finish in the top or bottom half of its league table
in the season following a 3-year transfer window.

## Results

Evaluated under a strictly chronological protocol (train 2005–2016,
validate 2017–2019, test 2020–2022 → 2023 season; test set evaluated once;
temporal-leakage guards asserted at runtime), averaged over 5 seeds:

| Model | Accuracy | Stayers | Changers |
|---|---|---|---|
| Random baseline | 0.500 | 0.500 | 0.500 |
| Persistence baseline¹ | 0.610 | 1.000 | 0.000 |
| MPNN (this checkpoint) | 0.624 ± 0.008 | 0.814 | 0.329 |
| Graph Transformer | 0.620 ± 0.015 | 0.782 | 0.368 |

¹ Persistence = predict that every club repeats its previous-season half.
League position is strongly
autocorrelated (61% of clubs stay in their half year-over-year).

The MPNN beats persistence by **1.5 ± 0.4 points** (one-sample t-test over
seeds, *p* < 0.02) — a small but statistically significant edge. More
importantly, it detects **~a third of half-table transitions**, which the
persistence baseline cannot anticipate by construction. The central finding
mirrors weak-form market efficiency: transfer-market activity *reflects*
club quality far more than it *anticipates* changes in it.

## What's in this repo

- `checkpoint/mpnn_final.pt` — trained weights **plus** everything needed
  for inference: architecture config and the z-score normalization
  statistics of the training set (inputs must be normalized with these).
- `model.py` — the architecture, `load_model()` and `predict()`.

```python
from model import load_model, predict
model, ckpt = load_model()
probs = predict(model, graph, ckpt)   # graph: PyG Data with x [N,19], edge_attr [E,8]
```

**Requirements:** `torch`, `torch-geometric`.

## Features

Node (19, per club per 3-year window): international/lower/higher-division
signing ratios; total spend; in/out degree; betweenness centrality;
division change; yearly trends of spend, arrivals and departures;
loan/free/paid shares of arrivals and departures; observation coverage.

Edge (8, per transfer, seller → buyer): fee; loan/free-transfer indicators;
cross-border indicator; division gap; current-period table-half gap;
repeat-pair count; player's previous club count.

## Data & training code


Trained on ~130,000 transfers between 1,727 clubs across the leagues of 32
countries (2005–2022, data from Transfermarkt).


The raw data was scraped from [Transfermarkt](https://www.transfermarkt.com)
and is **not redistributed** here.
