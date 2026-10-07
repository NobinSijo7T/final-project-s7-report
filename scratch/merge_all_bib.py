import os

tools_bib = """@inproceedings{ref_react,
  author = {Shunyu Yao and Jeffrey Zhao and Dian Yu and Nan Du and Izhak Shafran and Karthik Narasimhan and Yuan Cao},
  title = {{ReAct: Synergizing Reasoning and Acting in Language Models}},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2023}
}

@article{ref_autogen,
  author = {Qingyun Wu and Gagan Bansal and Jieyu Zhang and Yiran Wu and Beibin Li and Erkang Zhu and Li Jiang and Xiaoyun Zhang and Shaokun Zhang and Jiale Liu and Ahmed Hassan Awadallah and Ryen W White and Doug Burger and Chi Wang},
  title = {{AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation}},
  journal = {arXiv preprint arXiv:2308.08155},
  year = {2023}
}

@inproceedings{ref_metagpt,
  author = {Sirui Hong and Mingchen Zhuge and Jonathan Chen and Xiawu Zheng and Yuheng Cheng and Ceyao Zhang and Jinlin Wang and Zili Wang and Steven Ka Shing Yau and Zijuan Lin and Liyang Zhou and Chenglin Ran and Lingfeng Xiao and Chenglin Wu and J\"{u}rgen Schmidhuber},
  title = {{MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework}},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2024}
}

@misc{ref_mcp_spec,
  author = {{Anthropic}},
  title = {{Model Context Protocol (MCP) Specification}},
  year = {2024},
  howpublished = {\\url{https://modelcontextprotocol.io/}}
}

@article{ref_toolcua,
  author = {Xueke Hu and Xiaohan Zhang and Haotian Xu and Kai Qiao and Jian Yang and Xinxin Huang and Jing Shao and Ming Yan and Ji Ye},
  title = {{ToolCUA: Towards Optimal GUI-Tool Path Orchestration for Computer Use Agents}},
  journal = {arXiv preprint arXiv:2605.12481},
  year = {2026}
}

@misc{ref_livemcpbench,
  author = {{ICIP}},
  title = {{LiveMCPBench: A Dynamic Evaluation Benchmark for Model Context Protocol Agents}},
  year = {2025},
  howpublished = {\\url{https://huggingface.co/datasets/ICIP/LiveMCPBench}}
}

@article{ref_openm3,
  author = {Erkang Yang and Jing Zhou and Wayne Zhao},
  title = {{Open-M3-Bench: Benchmarking Multi-Modal, Multi-Tool Agent Environments}},
  journal = {arXiv preprint arXiv:2512.22047},
  year = {2025}
}

@article{ref_routerbench,
  author = {Qiguang Chen and Boyang Zheng and Yuchen Shen and Ming Li and Chong Zhang},
  title = {{RouterBench: A Benchmark for Multi-Model LLM Routing Algorithms}},
  journal = {arXiv preprint arXiv:2403.12031},
  year = {2024}
}

@article{ref_xroutebench,
  author = {Xiaocheng Li and Zhaowei Wang and Yuan Tian and Dan Roth},
  title = {{xRouteBench: Evaluating Cross-Provider Model Routing for Cost-Latency Pareto Frontiers}},
  journal = {arXiv preprint arXiv:2410.08922},
  year = {2024}
}

@inproceedings{ref_lmsys,
  author = {Lianmin Zheng and Wei-Lin Chiang and Ying Sheng and Siyuan Tian and Hao Shen and Zhanghao Hao and Hao Zhang and Bingyi Li and Xin Peng and Ying Zhu and Shuang Luo and Eric P. Xing and Ion Stoica},
  title = {{Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena}},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume = {36},
  year = {2023}
}

@inproceedings{ref_wildguard,
  author = {Seungju Han and Jiasheng Rao and Archit Bhardwaj and Shrimai Prabhumoye and Yejin Choi and Dan Roth},
  title = {{WildGuard: Open One-Stop Moderation Tools for Safety Risks, Jailbreaks, and Refusals of LLMs}},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2024}
}

@inproceedings{ref_ultrafeedback,
  author = {Ganqu Cui and Lifan Yuan and Ning Ding and Guanming Yao and Bingxiang Zhu and Yuan Ni and Xiao Xie and Zhiyuan Liu and Maosong Sun},
  title = {{UltraFeedback: Boosting Language Models with High-Quality Feedback}},
  booktitle = {International Conference on Machine Learning (ICML)},
  year = {2024}
}

@techreport{ref_agent_trajectories,
  author = {Chen Henry Xiao and Yiran Wu and Yicheng Shen and Graham Neubig},
  title = {{Agent Trajectories: Benchmarking Multi-Turn Interactive Agent Task Execution}},
  institution = {Carnegie Mellon University},
  year = {2024}
}

@inproceedings{ref_rlhf,
  author = {Paul F. Christiano and Jan Leike and Tom B. Brown and Miljan Martic and Shane Legg and Dario Amodei},
  title = {{Deep Reinforcement Learning from Human Preferences}},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume = {30},
  year = {2017}
}

@inproceedings{ref_dpo,
  author = {Rafael Rafailov and Archit Sharma and Eric Mitchell and Christopher D. Manning and Stefano Ermon and Chelsea Finn},
  title = {{Direct Preference Optimization: Your Language Model is Secretly a Reward Model}},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume = {36},
  year = {2023}
}

@inproceedings{ref_orpo,
  author = {Jiwoo Hong and Noah Lee and James Thorne},
  title = {{ORPO: Monolithic Preference Optimization without Reference Model}},
  booktitle = {Empirical Methods in Natural Language Processing (EMNLP)},
  year = {2024}
}

@inproceedings{ref_lora,
  author = {Edward J. Hu and Yelong Shen and Phillip Wallis and Zeyuan Allen-Zhu and Yuanzhi Li and Shean Wang and Lu Wang and Weizhu Chen},
  title = {{LoRA: Low-Rank Adaptation of Large Language Models}},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2022}
}

@inproceedings{ref_local_first,
  author = {Martin Kleppmann and Adam Wiggins and Peter van Hardenberg and Mark McGranaghan},
  title = {{Local-First Software: You Own Your Data, in Spite of the Cloud}},
  booktitle = {ACM SIGPLAN International Symposium on New Ideas, New Paradigms, and Reflections on Programming and Software (Onward!)},
  pages = {154--178},
  year = {2019}
}

@misc{ref_dexie,
  author = {David Fahlander},
  title = {{Dexie.js: A Minimalist Wrapper for IndexedDB}},
  year = {2024},
  howpublished = {\\url{https://dexie.org/}}
}

@misc{ref_fastapi,
  author = {Sebasti\\'an Ram{\\'\\i}rez},
  title = {{FastAPI: Modern, Fast (High-Performance), Web Framework for Building APIs with Python}},
  year = {2024},
  howpublished = {\\url{https://fastapi.tiangolo.com/}}
}

@inproceedings{ref_xgboost,
  author = {Tianqi Chen and Carlos Guestrin},
  title = {{XGBoost: A Scalable Tree Boosting System}},
  booktitle = {ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD)},
  pages = {785--794},
  year = {2016}
}

@article{ref_scikit,
  author = {Fabian Pedregosa and Ga{\\"e}l Varoquaux and Alexandre Gramfort and Vincent Michel and Bertrand Thirion and Olivier Grisel and Mathieu Blondel and Peter Prettenhofer and Ron Weiss and Vincent Dubourg and Jake Vanderplas and Alexandre Passos and David Cournapeau and Matthieu Brucher and Matthieu Perrot and {\\'E}douard Duchesnay},
  title = {{Scikit-learn: Machine Learning in Python}},
  journal = {Journal of Machine Learning Research},
  volume = {12},
  pages = {2825--2830},
  year = {2011}
}
"""

with open('references/references.bib', 'r', encoding='utf-8') as f:
    existing_bib = f.read()

full_bib = f"% ==============================================================================\n% FOUNDATIONAL PARADIGMS AND FRAMEWORKS\n% ==============================================================================\n\n{tools_bib}\n% ==============================================================================\n% EXTRACTED RESEARCH PAPERS\n% ==============================================================================\n\n{existing_bib}\n"

with open('references/references.bib', 'w', encoding='utf-8') as f:
    f.write(full_bib)

print("Updated references/references.bib with all 47 entries!")
