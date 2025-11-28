import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import io

LABEL_COLUMNS = ['DR', 'ARMD', 'MH', 'DN', 'MYA', 'BRVO', 'TSLN', 'ERM', 'LS', 'MS', 'CSR', 'ODC', 
                 'CRVO', 'TV', 'AH', 'ODP', 'ODE', 'ST', 'AION', 'PT', 'RT', 'RS', 'CRS', 'EDN', 
                 'RPEC', 'MHL', 'RP', 'CWS', 'CB', 'ODPM', 'PRH', 'MNF', 'HR', 'CRAO', 'TD', 'CME', 
                 'PTCR', 'CF', 'VH', 'MCA', 'VS', 'BRAO', 'PLQ', 'HPED', 'CL']

IMG_SIZE = 380
THRESHOLD = 0.5
NUM_CLASSES = len(LABEL_COLUMNS)

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def load_model(model_path='model/best_model.pth'):
    model = models.efficientnet_b4(pretrained=False)
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, NUM_CLASSES)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model

def predict_image(image_bytes, model):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = transform(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = model(image)
        probs = torch.sigmoid(output).cpu().numpy()[0]
    predictions = []
    for i, p in enumerate(probs):
        predictions.append({
            "label": LABEL_COLUMNS[i],
            "probability": float(round(p, 4)),
            "status": "✅" if p > THRESHOLD else ""
        })
    predictions.sort(key=lambda x: x["probability"], reverse=True)
    return predictions
