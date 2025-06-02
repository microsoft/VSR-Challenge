import torch
import torch.nn as nn
import time
from flopth import flopth
from fvcore.nn import FlopCountAnalysis, parameter_count
import torch.nn as nn

# Example model (use your own video model here)
# This is a placeholder 2D CNN for demonstration
class Simple2DCNN(nn.Module):
    def __init__(self):
        super(Simple2DCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 8, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, padding=1)
        self.gap = nn.AdaptiveAvgPool2d((4, 4))
        # The input size to the linear layer depends on the input image size
        # For demonstration, let's assume input is (3, 180, 320) -> after 2 poolings: (16, 45, 80)
        self.fc = nn.Linear(16 * 4 * 4, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = self.gap(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# sample code when using a model that requires specific kwargs
class WrapperModel(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x):
        # Call your original model with kwargs
        return self.model(lq=x, test_mode=True)

def main():
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        else:
            print("CUDA is not available.")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        
    model = Simple2DCNN().cuda()
    model = model.to(device)
    model.eval()

    data = [{
            'track': 'track1',
            'tensor': torch.randn(1, 3, 180, 320).to(device)
        },
        {
            'track': 'track2',
            'tensor': torch.randn(1,  3, 272, 480).to(device)
        },
        {
            'track': 'track3',
            'tensor': torch.randn(1, 3, 360, 640).to(device)
        }
    ]
    for d in data:
        print('==================== Processing track:', d['track'])
        input_tensor = d['tensor']
        
        # Dummy input: (batch, channels, height, width)    
        track = d['track']
        print(f"Processing {track} with shape {input_tensor.shape}")
        with torch.no_grad():
            flops, params = flopth(model, inputs=(input_tensor,))
            print(f"FLOPs: {flops}")
            print(f"Params: {params} ")

        # Warm-up (important for GPU to stabilize performance)
        for _ in range(10):
            with torch.no_grad():
                model(input_tensor)

        repeats = 1000
        latencies = []

        # Measure Latency
        start = time.time()
        with torch.no_grad():
            for _ in range(repeats):
                start = time.time()
                model(input_tensor)
                end = time.time()
                latencies.append(end - start)
        latencies_ms = [t * 1000 for t in latencies]  # Convert to ms

        print(f"Latency (mean over {repeats} runs): {sum(latencies_ms)/repeats:.2f} ms")


        # Measure Throughput
        n_frames = 1000
        start = time.time()
        with torch.no_grad():
            for _ in range(n_frames):
                model(input_tensor)
        end = time.time()
        total_time = end - start
        fps = n_frames / total_time
        print(f"Throughput: {fps:.2f} FPS")

if __name__ == '__main__':
    main()