from easydict import EasyDict as edict
from pathlib import Path
import torch
from torch.nn import CrossEntropyLoss
from torchvision import transforms as trans

def get_config(detector_name, model_name, training= True):
    conf = edict()
    conf.update_faces = False
    conf.data_path = Path('data')
    conf.work_path = Path('work_space/')
    conf.model_path = conf.work_path/'models'
    conf.log_path = conf.work_path/'log'
    conf.save_path = conf.work_path/'save'
    #conf.video_path = r"rtsp:/admin:Mb@c$123@192.168.0.210:554/Streaming/Channels/301"
    conf.video_path = r'videos\CAM2_MUNAM_ABDULLAH\munam_abdullah_front_cam2.mp4'
    conf.input_size = [112, 112]
    conf.embedding_size = 512

    conf.use_mobilfacenet = False
    conf.model_name = "model_name"
    conf.detector_name = "detector_name"
    conf.net_depth = 50
    conf.drop_ratio = 0.6
    conf.architecture = 'resnet18'  # resnet50/resnet18
    conf.net_mode = 'ir_se'  # or 'ir'
    conf.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    conf.test_transform = trans.Compose([
        trans.ToTensor(),
        trans.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    conf.data_mode = 'emore'
    conf.vgg_folder = conf.data_path/'faces_vgg_112x112'
    conf.ms1m_folder = conf.data_path/'faces_ms1m_112x112'
    conf.emore_folder = conf.data_path/'faces_emore'
    conf.batch_size = 200  # mobilefacenet
    # --------------------Training Config ------------------------
    if training:
        conf.log_path = conf.work_path/'log'
        conf.save_path = conf.work_path/'save'
        conf.lr = 1e-3
        conf.milestones = [12, 15, 18]
        conf.momentum = 0.9
        conf.pin_memory = True
        conf.num_workers = 4
        conf.ce_loss = CrossEntropyLoss()
    # --------------------Inference Config ------------------------
    else:
        conf.facebank_path = Path(r'data\facebank')
        conf.threshold = 1.5
        conf.face_limit = 50
        conf.min_face_size = 15  # the larger this value, the faster deduction, comes with tradeoff in small faces
        
    return conf
