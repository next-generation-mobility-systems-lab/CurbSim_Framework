# CurbSim_Framework
> This repo is the implementation of the paper **[A Microsimulation Study of Curb Space Operational Strategies and User Behaviors](https://www.researchgate.net/publication/383426054_A_Microsimulation_Study_of_Curb_Space_Operational_Strategies_and_User_Behaviors)** _(Accepted in Transportation Research Part E)_.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SUMO Version](https://img.shields.io/badge/SUMO-1.21.0-blue)](https://sumo.dlr.de)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green)](https://python.org)

## 📺 Simulation Demo
<a href="https://www.youtube.com/watch?v=voitCFogc6k" target="_blank">
  <img src="https://img.youtube.com/vi/voitCFogc6k/maxresdefault.jpg" 
       alt="Curb Space Microsimulation Demo" 
       style="width:100%; max-width:800px; border: 1px solid #eee; border-radius:8px;">
</a>

<div align="center">
  <a href="https://www.youtube.com/watch?v=voitCFogc6k" target="_blank" style="font-size:1.2em; display:inline-block; margin-top:12px;">
    ▶️ Overview of Curb Space Operation Simulation
  </a>
</div>

### More Demo Videos:
Please refer to the [Next Generation Mobility Systems (NGMS) Lab](https://public.websites.umich.edu/~nmasoud/) YouTube channel:   
[![NGMS YouTube Channel](https://img.shields.io/badge/YouTube-NGMS_Lab-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/channel/UCJjRMGo-pqZaudJTZU1PWyw?view_as=subscriber)

## 🔧 Quick Start

### Prerequisites
- **SUMO 1.21.0** ([Installation Guide](https://sumo.dlr.de/docs/Installing.html))
- **Python 3.8+** (Anaconda recommended)

```bash
conda create -n CurbSim python=3.8.19
conda activate CurbSim
```

```bash
git clone https://github.com/zhyuyang1023/CurbSim_Framework.git
cd CurbSim_Framework
```

```bash
pip install -r requirements.txt
```
```bash
python run_proportional.py  # Demand-proportional allocation
python run_random.py        # Random allocation
```

### Brief Description
- "run_proportional.py" and "run_random.py" execute the simulation with the corresponding curb allocation scheme
- "input" folder contains all input data required for the simulation
- "modules" folder contains script files that generate drivers and define driving behaviors (e.g., parking, cruising, illegal actions)
- "output_proportional" folder collects CSV files that report the simulation results under the demand proportional allocation scheme
- "output_random" folder collects CSV files that report the simulation results under the random allocation scheme

## 📑 Citation
If you use this code in your research, please cite our paper:
```bibtex
@article{zhao2025microsimulation,
  title={A Microsimulation Study of Curb Space Operational Strategies and User Behaviors},
  author={Zhao, Yuyang and Li, Chenhan and Lim, Jisoon and Masoud, Neda},
  journal={Transportation Research Part E: Logistics and Transportation Review},
  year={2025 (In press)}
}
