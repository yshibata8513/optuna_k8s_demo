import torch
import torch.nn as nn

class KineticModel(nn.Module):
    def __init__(self):
        super(KineticModel, self).__init__()

    def forward(self,state_action):
        M  = 2500.0 
        Lf = 1.5
        Lr = 1.5
        L  = 3.0

        x     = state_action[0]
        y     = state_action[1]
        head  = state_action[2]
        v     = state_action[3]
        delta = state_action[4]

        beta  = Lr/L*delta
        gamma = v/L*delta  

        dx_dt    = v*torch.cos(head + beta)
        dy_dt    = v*torch.sin(head + beta)
        dhead_dt = gamma

        return torch.cat([dx_dt.view(1),dy_dt.view(1),dhead_dt.view(1)],dim=0)

model = KineticModel()

dummy_input = torch.zeros(5)

onnx_file_name = "kinematic_model_test.onnx"

torch.onnx.export(
    model,
    dummy_input,
    onnx_file_name,
    verbose=True,
    input_names=["input"],
    output_names=["output"],
)