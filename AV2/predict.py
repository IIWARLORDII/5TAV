from ultralytics import YOLO

model = YOLO('yolo11m_train23.pt')

model.predict(source = './test/test.jpg', show = True, save = True)