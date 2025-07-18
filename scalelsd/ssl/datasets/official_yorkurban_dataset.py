""" YorkUrban dataset for VP estimation evaluation. """

import os
import numpy as np
import torch
import cv2
import scipy.io
from skimage.io import imread
from torch.utils.data import Dataset, DataLoader
from pathlib import Path

from ..config.project_config import Config as cfg



class YorkUrban(torch.utils.data.Dataset):
    def __init__(self, mode='train', config=None):

        assert mode in ['train', 'val', 'test']

        # Extract the image names
        self.root_dir = cfg.official_yorkurban_dataroot
        self.img_names = [name for name in os.listdir(self.root_dir)
                          if os.path.isdir(os.path.join(self.root_dir, name))]
        assert len(self.img_names) == 102 ## 102 categories in total

        # Separate validation and test
        split_file = os.path.join(self.root_dir,
                                    'ECCV_TrainingAndTestImageNumbers.mat')
        split_mat = scipy.io.loadmat(split_file)
        if mode == 'test':
            valid_set = split_mat['testSetIndex'][:, 0] - 1
        else:
            valid_set = split_mat['trainingSetIndex'][:, 0] - 1
        self.img_names = np.array(self.img_names)[valid_set]
        assert len(self.img_names) == 51

        # Load the intrinsics
        K_file = os.path.join(self.root_dir, 'cameraParameters.mat')
        K_mat = scipy.io.loadmat(K_file)
        f = K_mat['focal'][0, 0] / K_mat['pixelSize'][0, 0]
        p_point = K_mat['pp'][0] - 1  # -1 to convert to 0-based conv
        self.K = torch.tensor([[f, 0, p_point[0]],
                               [0, f, p_point[1]],
                               [0, 0, 1]])

    def __len__(self):
        return len(self.img_names)
    
    def __getitem__(self, idx):
        img_path = os.path.join(self.root_dir, self.img_names[idx],
                                f'{self.img_names[idx]}.jpg')
        name = str(Path(img_path).stem)
        img = cv2.imread(img_path)

        # Load the GT lines and VP association
        lines_file = os.path.join(self.root_dir, self.img_names[idx],
                                  f'{self.img_names[idx]}LinesAndVP.mat')
        lines_mat = scipy.io.loadmat(lines_file)
        lines = lines_mat['lines'].reshape(-1, 2, 2)[:, :, [1, 0]] - 1
        vp_association = lines_mat['vp_association'][:, 0] - 1

        # Load the VPs (non orthogonal ones)
        vp_file = os.path.join(
            self.root_dir, self.img_names[idx],
            f'{self.img_names[idx]}GroundTruthVP_CamParams.mat')
        vps = scipy.io.loadmat(vp_file)['vp'].T
        
        # Keep only the relevant VPs
        unique_vps = np.unique(vp_association)
        vps = vps[unique_vps]
        for i, index in enumerate(unique_vps):
            vp_association[vp_association == index] = i

        # Convert to torch tensors
        # img = torch.tensor(img[None], dtype=torch.float)
        lines = torch.tensor(lines.astype(float), dtype=torch.float)
        vps = torch.tensor(vps, dtype=torch.float)
        vp_association = torch.tensor(vp_association, dtype=torch.int)

        data = {'image': img, 
                'image_path': img_path, 
                'name': name, 
                'gt_lines': lines,
                'vps': vps, 
                'vp_association': vp_association, 
                'K': self.K
                }  

        return  data

    # Overwrite the parent data loader to handle custom collate_fn
    def get_data_loader(self, split, shuffle=False):
        """Return a data loader for a given split."""
        assert split in ['val', 'test']
        batch_size = self.conf.get(split+'_batch_size')
        num_workers = self.conf.get('num_workers', batch_size)
        return DataLoader(self.get_dataset(split), batch_size=batch_size,
                          shuffle=False, pin_memory=True,
                          num_workers=num_workers)
