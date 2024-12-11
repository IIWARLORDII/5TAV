from ultralytics import YOLO

model = YOLO('yolo11m.pt')

model.train(data = 'dataset_cupins.yaml', 
            imgsz = 640, 
            batch = 16, 
            epochs = 100,
            lr0=0.001,
            augment=True,
            workers = 4,
            verbose = True,
            show_conf = False, 
            device = 0)