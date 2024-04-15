# paper-source-trace

## Prerequisites
- Linux
- Python 3.9
- PyTorch 1.10.0+cu111

## Getting Started

### Installation

Clone this repo.

```bash
git clone https://github.com/THUDM/paper-source-trace.git
cd paper-source-trace
```

Please install dependencies by

```bash
pip install -r requirements.txt
```

## PST Dataset
The dataset can be downloaded from [BaiduPan](https://pan.baidu.com/s/1I_HZXBx7U0UsRHJL5JJagw?pwd=bft3) with password bft3, [Aliyun](https://open-data-set.oss-cn-beijing.aliyuncs.com/oag-benchmark/kddcup-2024/PST/PST.zip) or [DropBox](https://www.dropbox.com/scl/fi/namx1n55xzqil4zbkd5sv/PST.zip?rlkey=impcbm2acqmqhurv2oj0xxysx&dl=1).
The paper XML files are generated by [Grobid](https://grobid.readthedocs.io/en/latest/Introduction/) APIs from paper pdfs.

## Run Baselines for [KDD Cup 2024](https://www.biendata.xyz/competition/pst_kdd_2024/)
First, download DBLP dataset from [AMiner](https://opendata.aminer.cn/dataset/DBLP-Citation-network-V16.zip).
Put the unzipped PST directory into ``data/`` and unzipped DBLP dataset into ``data/PST/``.

```bash
cd $project_path
export CUDA_VISIBLE_DEVICES='?'  # specify which GPU(s) to be used
export PYTHONPATH="`pwd`:$PYTHONPATH"

# Method 1: Random Forest
python rf/process_kddcup_data.py
python rf/model_rf.py  # output at out/kddcup/rf/

# Method 2: Network Embedding
python net_emb.py  # output at out/kddcup/prone/

# Method 3: SciBERT
python bert.py  # output at out/kddcup/scibert/
```

## Results on Valiation Set

|  Method  | MAP   |
|-------|-------|
| Random Forest  | 0.21420 |
| ProNE | 0.21668 |
| SciBERT  | 0.29489 |

## Citation

If you find this repo useful in your research, please cite the following papers:

```
@article{zhang2024pst,
  title={PST-Bench: Tracing and Benchmarking the Source of Publications},
  author={Fanjin Zhang and Kun Cao and Yukuo Cen and Jifan Yu and Da Yin and Jie Tang},
  journal={arXiv preprint arXiv:2402.16009},
  year={2024}
}

@article{zhang2024oag,
    title={OAG-Bench: A Human-Curated Benchmark for Academic Graph Mining},
    author={Fanjin Zhang and Shijie Shi and Yifan Zhu and Bo Chen and Yukuo Cen and Jifan Yu and Yelin Chen and Lulu Wang and Qingfei Zhao and Yuqing Cheng and Tianyi Han and Yuwei An and Dan Zhang and Weng Lam Tam and Kun Cao and Yunhe Pang and Xinyu Guan and Huihui Yuan and Jian Song and Xiaoyan Li and Yuxiao Dong and Jie Tang},
    journal={arXiv preprint arXiv:2402.15810},
    year={2024}
}
```
