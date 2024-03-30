import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets

# Define the AlexNet architecture
class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()

        # Convolutional layers
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )

        # Fully connected layers
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), 256 * 6 * 6)
        x = self.classifier(x)
        return x

# Set device (GPU if available, else CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Hyperparameters
num_epochs = 10
batch_size = 128
learning_rate = 0.01

# Data transformations
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# Load and transform the dataset
train_dataset = datasets.ImageFolder(root='path/to/training/data', transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Initialize the model
model = AlexNet(num_classes=len(train_dataset.classes)).to(device)

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)

# Training loop
for epoch in range(num_epochs):
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

# Save the trained model
torch.save(model.state_dict(), "alexnet.pth")



# In this simplified implementation:
# 1. We define the AlexNet architecture using PyTorch's nn.Module class. The architecture consists of convolutional layers (self.features) followed by fully connected layers (self.classifier).
# 2. We set the device to GPU if available, otherwise CPU.
# 3. We define the hyperparameters such as the number of epochs, batch size, and learning rate.
# 4. We apply data transformations to the input images, including resizing, center cropping, converting to tensors, and normalizing.
# 5. We load the dataset using datasets.ImageFolder and create a data loader with the specified batch size and shuffling.
# 6. We initialize the AlexNet model with the appropriate number of output classes based on the dataset.
# 7. We define the loss function (cross-entropy loss) and optimizer (SGD with momentum).
# 8. We start the training loop, iterating over the specified number of epochs and the training data loader.
# 9. For each batch of images and labels, we perform a forward pass, calculate the loss, perform a backward pass, and update the model parameters using the optimizer.
# 10. After each epoch, we print the current epoch and the corresponding loss.
# 11. Finally, we save the trained model parameters to a file named "alexnet.pth".

# Note: Make sure to replace 'path/to/training/data' with the actual path to your training dataset directory.
# This simplified implementation provides a basic understanding of how to define and train the AlexNet architecture using PyTorch. You can further extend and modify it based on your specific requirements.


# Extra:
# ImageNet Classification with Deep Convolutional Neural Networks (Paper Explained): https://www.youtube.com/watch?v=Nq3auVtvd9Q
# One weird trick for parallelizing convolutional neural networks (2014 Paper): https://arxiv.org/abs/1404.5997
# MLX Image Models: https://github.com/robertmccraith/mimm (can easily train + run on macs)
