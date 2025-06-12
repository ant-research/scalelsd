<div align="center">

# ScaleLSD: Scalable Deep Line Segment Detection Streamlined

<!-- <a href="https://code.alipay.com/kezeran.kzr/ScaleLSD"><img src="https://img.shields.io/static/v1?label=Project%20Page&message=Github&color=blue&logo=github-pages"></a>&ensp;<a href="https://code.alipay.com/kezeran.kzr/ScaleLSD"><img src="https://img.shields.io/badge/ArXiv-250x.xxxxx-brightgreen"></a>&ensp;<a href="https://code.alipay.com/kezeran.kzr/ScaleLSD"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Model_Card-Huggingface-orange"></a>&ensp;<a href="https://code.alipay.com/kezeran.kzr/ScaleLSD"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Gradio%20Demo-Huggingface-orange"></a> -->

<a href="https://ant-research.github.io/scalelsd"><img src="https://img.shields.io/static/v1?label=Project%20Page&message=Github&color=blue&logo=github-pages"></a>&ensp;<a href="https://arxiv.org/abs/2506.09369"><img src="https://img.shields.io/badge/ArXiv-2506.09369-brightgreen"></a>&ensp;<a href="https://huggingface.co/cherubicxn/scalelsd"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Model_Card-Huggingface-orange"></a>



[Zeran Ke](https://calmke.github.io/)<sup>1,2</sup>, [Bin Tan](https://icetttb.github.io/)<sup>2</sup>, [Xianwei Zheng](https://jszy.whu.edu.cn/zhengxianwei/zh_CN/index.htm)<sup>1</sup>,  [Yujun Shen](https://shenyujun.github.io/)<sup>2</sup>, [Tianfu Wu](https://research.ece.ncsu.edu/ivmcl/)<sup>3</sup>, [Nan Xue](https://xuenan.net/)<sup>2†</sup>

<sup>1</sup>Wuhan University &ensp;&ensp;<sup>2</sup>Ant Group&ensp;&ensp;<sup>3</sup>NC State University

</div>

<!-- <img src="assets/teaser.jpg" width="100%"> -->

![teaser](assets/teaser.jpg)


## ⚙️ Installtion

All codes are succefully tested on:

- Ubuntu 22.04.5 LTS
- CUDA 12.1
- Python 3.10
- Pytorch 2.5.1

First clone this repo:

```bash
git clone https://github.com/ant-research/scalelsd.git
```

Then create the conda eviroment and install the dependencies:
```bash
conda create -n scalelsd python=3.10
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt  
pip install -e .  # Install scalelsd locally
```

## 🔥🔍 Gradio Demo

### Line Segment Detection
Before you started, please download our pre-trained [models](https://huggingface.co/cherubicxn/scalelsd) and place them into the `models` folder. Then run the Gradio demo:
```bash
python -m gradio_demo.inference
```

### Line Matching
Because our line matching app is built on GlueStick with our ScaleLSD, you need to install [GlueStick](https://github.com/cvg/GlueStick) and download the weights of the GlueStick model. Then run the Gradio demo:
```bash
pythonb -m gradio_demo.line_mat_gluestick
```

## 🚗 Inference

Quickly start use our models for line segment detection by running the following command:
```bash
python -m predictor.predict --img $[IMAGE_PATH_OR_FODER]
```

You can also specify more params by:

```bash
python -m predictor.predict \
    --ckpt $[MODEL_PATH] \
    --img $[IMAGE_PATH_OR_FODER] \
    --ext $[png/pdf/json] \
    --threshold 10 \
    --junction-hm 0.1 \
    --disable-show
```

```bash
OPTIONS:
  --ckpt CKPT, -c CKPT
                        Path to the checkpoint file.
  --img IMG, -i IMG     Path to the image or folder containing images.
  --ext EXT, -e EXT     Output file extension (png/pdf/json).
  --threshold THRESHOLD, -t THRESHOLD
                        Threshold for line segment detection.
  --junction-hm JUNCTION_HM, -jh JUNCTION_HM
                        Junction heatmap threshold.
  --num-junctions NUM_JUNCTIONS, -nj NUM_JUNCTIONS
                        Max number of junctions to detect.
  --disable-show        Disable showing the results.
  --use_lsd             Use LSD-Rectifier for line segment detection.
  --use_nms             Use Non-Maximum Suppression (NMS) for junction detection.
```


## 📖 Related Third-party Projects

- [HAWPv3](https://github.com/cherubicXN/hawp/tree/main)
- [DeepLSD](https://github.com/cvg/DeepLSD)
- [Progressive-x](https://github.com/danini/progressive-x/tree/vanishing-points)
- [GlueStick](https://github.com/cvg/GlueStick)
- [GlueFactory](https://github.com/cvg/glue-factory)
- [LiMAP](https://github.com/cvg/limap)


## 📝 Citation

If you find our work useful in your research, please consider citing:

```bash
@inproceedings{ScaleLSD,
    title = {ScaleLSD: Scalable Deep Line Segment Detection Streamlined},
    author = {Zeran Ke and Bin Tan and Xianwei Zheng and Yujun Shen and Tianfu Wu and Nan Xue},
    booktitle = "IEEE Conference on Computer Vision and Pattern Recognition (CVPR)",
    year = {2025},
}
```
