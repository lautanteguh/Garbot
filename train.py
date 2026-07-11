from ultralytics import YOLO
import torch

def main():
    # Clear GPU cache (prevents random OOM)
    torch.cuda.empty_cache()

    # Load model (use small model for stability)
    model = YOLO("yolo26m.pt")

    # Train with safe, stable settings
    model.train(
        data="dataset_custom.yaml",   # your dataset config
        epochs=50,
        imgsz=384,
        batch=1,
        workers=1,
        cache=False,
        val=True
    )

    model.val()

if __name__ == "__main__":
    main()