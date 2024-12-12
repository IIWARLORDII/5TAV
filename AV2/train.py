from ultralytics import YOLO

model = YOLO('yolo11m.pt')

model.train(data = 'dataset_cupins.yaml', 
            imgsz = 1024, 
            batch = 16, 
            epochs = 200,
            workers = 0,
            device = 0)