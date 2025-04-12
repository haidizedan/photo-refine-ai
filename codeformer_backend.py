import os
import torch
import numpy as np
from PIL import Image
from torchvision.transforms import ToTensor, ToPILImage
from CodeFormer.basicsr.archs.codeformer_arch import CodeFormer
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DnCNN(torch.nn.Module):
    def __init__(self, num_of_layers=17):
        super(DnCNN, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1)
        self.conv2 = torch.nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = torch.nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.conv4 = torch.nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.conv5 = torch.nn.Conv2d(64, 3, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = torch.relu(self.conv4(x))
        return self.conv5(x)

dncnn_model_path = 'models/DnCNN.pth'
dncnn_model = DnCNN()
dncnn_model.load_state_dict(torch.load(dncnn_model_path))
dncnn_model.eval()

weight_path = os.path.join("weights", "RealESRGAN_x2plus.pth")
bg_upsampler = RealESRGANer(
    scale=2,
    model_path=weight_path,
    model=None,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=False,
    device=device
)

def load_codeformer(model_path="CodeFormer/weights/codeformer.pth"):
    net = CodeFormer(
        dim_embd=512,
        codebook_size=1024,
        n_head=8,
        n_layers=9,
        connect_list=["32", "64", "128", "256"]
    )
    checkpoint = torch.load(model_path, map_location=device)
    net.load_state_dict(checkpoint["params_ema"])
    net.eval()
    net.to(device)
    return net

net = load_codeformer()

def remove_noise(image_tensor):
    with torch.no_grad():
        output = dncnn_model(image_tensor)
    return output

def restore_image(input_image, fidelity_weight=0.7):
    if input_image is None:
        return None

    image = input_image.convert("RGB")
    img_tensor = ToTensor()(image).unsqueeze(0).to(device)

    denoised_image = remove_noise(img_tensor)

    with torch.no_grad():
        output = net(denoised_image, w=fidelity_weight, adain=True)[0]
        output_image = ToPILImage()(output.squeeze(0).clamp(0, 1).cpu())

    restored_image, _ = bg_upsampler.enhance(np.array(output_image), outscale=1)
    return Image.fromarray(restored_image)
