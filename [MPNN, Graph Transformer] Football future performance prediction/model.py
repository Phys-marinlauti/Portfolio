"""
Usage:
    from model import load_model, predict

    model, ckpt = load_model("checkpoint/mpnn_final.pt")
    # `graph` is a torch_geometric.data.Data with .x [N,19] and .edge_attr [E,8]
    probs = predict(model, graph, ckpt)   # [N, 2] softmax probabilities
"""
import torch
import torch.nn.functional as F
from torch import nn
from torch_geometric.nn import NNConv


class MPNN(nn.Module):
    def __init__(self, node_features=19, edge_features=8,
                 hidden_channels=64, out_channels=2):
        super().__init__()
        self.edge_nn1 = nn.Sequential(nn.Linear(edge_features, 32), nn.ReLU(),
                                      nn.Linear(32, node_features * hidden_channels))
        self.conv1 = NNConv(node_features, hidden_channels, self.edge_nn1, aggr="mean")
        self.edge_nn2 = nn.Sequential(nn.Linear(edge_features, 32), nn.ReLU(),
                                      nn.Linear(32, hidden_channels * hidden_channels))
        self.conv2 = NNConv(hidden_channels, hidden_channels, self.edge_nn2, aggr="mean")
        self.edge_nn3 = nn.Sequential(nn.Linear(edge_features, 32), nn.ReLU(),
                                      nn.Linear(32, hidden_channels * hidden_channels))
        self.conv3 = NNConv(hidden_channels, hidden_channels, self.edge_nn3, aggr="mean")
        self.lin = nn.Linear(hidden_channels, out_channels)

    def forward(self, data):
        x, ei, ea = data.x, data.edge_index, data.edge_attr
        x = F.dropout(F.elu(self.conv1(x, ei, ea)), p=0.3, training=self.training)
        x = F.dropout(F.elu(self.conv2(x, ei, ea)), p=0.3, training=self.training)
        x = F.dropout(F.elu(self.conv3(x, ei, ea)), p=0.3, training=self.training)
        return self.lin(x)


def load_model(path="checkpoint/mpnn_final.pt"): #Rebuilds from the checkpoint config and loads weights.
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    cfg = ckpt["config"]
    model = MPNN(cfg["node_features"], cfg["edge_features"],
                 cfg["hidden_channels"], cfg["out_channels"])
    model.load_state_dict(ckpt["state_dict"])
    model.eval()
    return model, ckpt


def predict(model, graph, ckpt): 
    norm = ckpt["norm"]
    graph = graph.clone()
    graph.x = (graph.x - norm["x_mean"]) / norm["x_std"]
    graph.edge_attr = (graph.edge_attr - norm["e_mean"]) / norm["e_std"]
    with torch.no_grad():
        return F.softmax(model(graph), dim=1)
