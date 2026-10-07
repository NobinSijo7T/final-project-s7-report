import json

papers = [
    {
        "key": "ref_yue2026_cpnhrl",
        "authors": "Q.~Yue, L.~Tian, X.~Feng, Z.~Yuan, S.~Wei, J.~Xia, B.~Chen, X.~Song, Y.~Yao, and Y.~Liu",
        "title": "CPN-HRL: A hierarchical deep reinforcement learning approach for priority-aware task scheduling in CPN enabled by cloud-edge-end environments",
        "journal": "Journal of King Saud University -- Computer and Information Sciences",
        "volume": "38",
        "number": "",
        "pages": "art. 290",
        "year": "2026",
        "doi": "10.1007/s44443-026-00690-x"
    },
    {
        "key": "ref_cornalba2024_multiobj",
        "authors": "F.~Cornalba, C.~Disselkamp, D.~Scassola, and C.~Helf",
        "title": "Multi-objective reward generalization: Improving performance of deep reinforcement learning for applications in single-asset trading",
        "journal": "Neural Computing and Applications",
        "volume": "36",
        "number": "2",
        "pages": "619--637",
        "year": "2024",
        "doi": "10.1007/s00521-023-09033-7"
    },
    {
        "key": "ref_schneckenreither2025_aral",
        "authors": "M.~Schneckenreither and G.~Moser",
        "title": "Average reward adjusted discounted reinforcement learning",
        "journal": "Neural Computing and Applications",
        "volume": "37",
        "number": "35",
        "pages": "25663--25694",
        "year": "2025",
        "doi": "10.1007/s00521-024-10620-5"
    },
    {
        "key": "ref_aina2026_smadrl",
        "authors": "K.~O. Aina and S.~Ha",
        "title": "Deep reinforcement learning for multi-agent coordination",
        "journal": "Artificial Life and Robotics",
        "volume": "31",
        "number": "2",
        "pages": "484--494",
        "year": "2026",
        "doi": "10.1007/s10015-025-01089-z"
    },
    {
        "key": "ref_rother2025_openended",
        "authors": "D.~Rother, J.~Pajarinen, J.~Peters, and T.~H. Weisswange",
        "title": "Open-ended coordination for multi-agent systems using modular open policies",
        "journal": "Autonomous Agents and Multi-Agent Systems",
        "volume": "39",
        "number": "2",
        "pages": "art. 40",
        "year": "2025",
        "doi": "10.1007/s10458-025-09723-7"
    },
    {
        "key": "ref_liu2026_humanknowledge",
        "authors": "D.~Liu, F.~Ren, J.~Yan, G.~Su, W.~Gu, and S.~Kato",
        "title": "Improving scalability of multi-agent deep reinforcement learning with suboptimal human knowledge",
        "journal": "Autonomous Agents and Multi-Agent Systems",
        "volume": "40",
        "number": "1",
        "pages": "art. 2",
        "year": "2026",
        "doi": "10.1007/s10458-025-09729-1"
    },
    {
        "key": "ref_marzari2026_epsretrain",
        "authors": "L.~Marzari, C.~Liu, P.~L. Donti, and E.~Marchesini",
        "title": "$\\varepsilon$-retraining reinforcement learning algorithms",
        "journal": "Autonomous Agents and Multi-Agent Systems",
        "volume": "40",
        "number": "1",
        "pages": "art. 24",
        "year": "2026",
        "doi": "10.1007/s10458-026-09748-6"
    },
    {
        "key": "ref_wong2023_marlsurvey",
        "authors": "A.~Wong, T.~B{\\\"a}ck, A.~V. Kononova, and A.~Plaat",
        "title": "Deep multiagent reinforcement learning: Challenges and directions",
        "journal": "Artificial Intelligence Review",
        "volume": "56",
        "number": "6",
        "pages": "5023--5056",
        "year": "2023",
        "doi": "10.1007/s10462-022-10299-x"
    },
    {
        "key": "ref_niu2025_hiat",
        "authors": "B.~Niu, B.~Luo, Y.~Cui, X.~Xu, Y.~Zhao, and Y.~Feng",
        "title": "HIAT: Human-in-the-loop reinforcement learning with auxiliary task",
        "journal": "Artificial Intelligence Review",
        "volume": "58",
        "number": "10",
        "pages": "art. 273",
        "year": "2025",
        "doi": "10.1007/s10462-025-11260-4"
    },
    {
        "key": "ref_lee2025_instructpatentgpt",
        "authors": "J.-S. Lee",
        "title": "InstructPatentGPT: Training patent language models to follow instructions with human feedback",
        "journal": "Artificial Intelligence and Law",
        "volume": "33",
        "number": "3",
        "pages": "739--782",
        "year": "2025",
        "doi": "10.1007/s10506-024-09401-1"
    },
    {
        "key": "ref_zhuang2022_roltr",
        "authors": "S.~Zhuang, Z.~Qiao, and G.~Zuccon",
        "title": "Reinforcement online learning to rank with unbiased reward shaping",
        "journal": "Information Retrieval Journal",
        "volume": "25",
        "number": "4",
        "pages": "386--413",
        "year": "2022",
        "doi": "10.1007/s10791-022-09413-y"
    },
    {
        "key": "ref_ghazal2025_mecworkflow",
        "authors": "T.~M. Ghazal, A.~E. Awouda, M.~K. Hasan, A.~H.~A. Rahman, S.~Islam, R.~A. Saeed, H.~Elshafie, A.~Iqbal, and A.~H. Hussein",
        "title": "Knowledge learning for securing workflow scheduling algorithm in mobile edge computing",
        "journal": "Mobile Networks and Applications",
        "volume": "30",
        "number": "2",
        "pages": "395--413",
        "year": "2025",
        "doi": "10.1007/s11036-025-02465-6"
    },
    {
        "key": "ref_barredo2025_multifitness",
        "authors": "P.~Barredo and J.~Puente",
        "title": "Energy-aware cooperative multi-fitness evolutionary algorithm for workflow scheduling in cloud computing",
        "journal": "Natural Computing",
        "volume": "24",
        "number": "3",
        "pages": "557--570",
        "year": "2025",
        "doi": "10.1007/s11047-025-10023-y"
    },
    {
        "key": "ref_heirati2026_fogcloud",
        "authors": "A.~Heirati, M.~Fartash, and M.~Khalily-Dermany",
        "title": "Optimized task scheduling in fog-cloud computing using hybrid deep learning and metaheuristic algorithms",
        "journal": "Neural Processing Letters",
        "volume": "58",
        "number": "1",
        "pages": "art. 5",
        "year": "2026",
        "doi": "10.1007/s11063-025-11819-w"
    },
    {
        "key": "ref_abdi2024_edgecloud",
        "authors": "S.~Abdi, M.~Ashjaei, and S.~Mubeen",
        "title": "Cost-aware workflow offloading in edge-cloud computing using a genetic algorithm",
        "journal": "The Journal of Supercomputing",
        "volume": "80",
        "number": "16",
        "pages": "24835--24870",
        "year": "2024",
        "doi": "10.1007/s11227-024-06341-0"
    },
    {
        "key": "ref_skirzynski2024_humanplanning",
        "authors": "J.~Skirzy{\\'n}ski, Y.~R. Jain, and F.~Lieder",
        "title": "Automatic discovery and description of human planning strategies",
        "journal": "Behavior Research Methods",
        "volume": "56",
        "number": "3",
        "pages": "1049--1076",
        "year": "2024",
        "doi": "10.3758/s13428-023-02062-z"
    },
    {
        "key": "ref_zhang2023_dataintensive",
        "authors": "S.~Zhang, Z.~Zhao, C.~Liu, and S.~Qin",
        "title": "Data-intensive workflow scheduling strategy based on deep reinforcement learning in multi-clouds",
        "journal": "Journal of Cloud Computing",
        "volume": "12",
        "number": "1",
        "pages": "art. 125",
        "year": "2023",
        "doi": "10.1186/s13677-023-00504-9"
    },
    {
        "key": "ref_wang2023_ecofriendly",
        "authors": "Z.~Wang, S.~Chen, L.~Bai, J.~Gao, J.~Tao, R.~R. Bond, and M.~D. Mulvenna",
        "title": "Reinforcement learning based task scheduling for environmentally sustainable federated cloud computing",
        "journal": "Journal of Cloud Computing",
        "volume": "12",
        "number": "1",
        "pages": "art. 174",
        "year": "2023",
        "doi": "10.1186/s13677-023-00553-0"
    },
    {
        "key": "ref_subashree2025_dssso",
        "authors": "S.~Subashree, M.~Rajakumaran, G.~Pushpa, and S.~Senthilkumar",
        "title": "Hybrid dolphin swarm sparrow search optimization based multi-objective cloud workflow scheduling",
        "journal": "Journal of Cloud Computing",
        "volume": "14",
        "number": "1",
        "pages": "art. 80",
        "year": "2025",
        "doi": "10.1186/s13677-025-00828-8"
    },
    {
        "key": "ref_xia2023_dynamic_roles",
        "authors": "Y.~Xia, J.~Zhu, and L.~Zhu",
        "title": "Dynamic role discovery and assignment in multi-agent task decomposition",
        "journal": "Complex \\& Intelligent Systems",
        "volume": "9",
        "number": "6",
        "pages": "6211--6222",
        "year": "2023",
        "doi": "10.1007/s40747-023-01071-x"
    },
    {
        "key": "ref_li2023_vcaes",
        "authors": "J.~Li, L.~Xing, W.~Zhong, Z.~Cai, and F.~Hou",
        "title": "Decision variable contribution based adaptive mechanism for evolutionary multi-objective cloud workflow scheduling",
        "journal": "Complex \\& Intelligent Systems",
        "volume": "9",
        "number": "6",
        "pages": "7337--7348",
        "year": "2023",
        "doi": "10.1007/s40747-023-01137-w"
    },
    {
        "key": "ref_yu2024_ghq",
        "authors": "X.~Yu, Y.~Lin, X.~Wang, S.~Han, and K.~Lv",
        "title": "GHQ: Grouped hybrid Q-learning for cooperative heterogeneous multi-agent reinforcement learning",
        "journal": "Complex \\& Intelligent Systems",
        "volume": "10",
        "number": "4",
        "pages": "5261--5280",
        "year": "2024",
        "doi": "10.1007/s40747-024-01415-1"
    },
    {
        "key": "ref_xu2024_dapm",
        "authors": "C.~Xu, J.~Wang, X.~Zhu, Y.~Yue, W.~Zhou, Z.~Liang, and D.~Wojtczak",
        "title": "Decentralized multi-agent cooperation via adaptive partner modeling",
        "journal": "Complex \\& Intelligent Systems",
        "volume": "10",
        "number": "4",
        "pages": "4989--5004",
        "year": "2024",
        "doi": "10.1007/s40747-024-01421-3"
    },
    {
        "key": "ref_vyhmeister2023_responsibleai",
        "authors": "E.~Vyhmeister, G.~Castane, P.-O. {\\\"O}stberg, and S.~Thevenin",
        "title": "A responsible AI framework: Pipeline contextualisation",
        "journal": "AI and Ethics",
        "volume": "3",
        "number": "1",
        "pages": "175--197",
        "year": "2023",
        "doi": "10.1007/s43681-022-00154-8"
    },
    {
        "key": "ref_siebert2023_humancontrol",
        "authors": "L.~C. Siebert, M.~L. Lupetti, E.~Aizenberg, N.~Beckers, A.~Zgonnikov, H.~Veluwenkamp, D.~Abbink, E.~Giaccardi, G.-J. Houben, C.~M. Jonker, J.~van~den Hoven, D.~Forster, and R.~L. Lagendijk",
        "title": "Meaningful human control: Actionable properties for AI system development",
        "journal": "AI and Ethics",
        "volume": "3",
        "number": "1",
        "pages": "241--255",
        "year": "2023",
        "doi": "10.1007/s43681-022-00167-3"
    }
]

# Generate \bibitem entries
bibitem_entries = []
for p in papers:
    vol_str = f"vol.~{p['volume']}" if p['volume'] else ""
    no_str = f", no.~{p['number']}" if p['number'] else ""
    pp_str = f", pp.~{p['pages']}" if p['pages'] and not p['pages'].startswith('art') else (f", {p['pages']}" if p['pages'] else "")
    doi_str = f" [Online]. Available: \\url{{https://doi.org/{p['doi']}}}" if p['doi'] else ""
    
    entry = f"\\bibitem{{{p['key']}}}\n{p['authors']}, ``{p['title']},'' \\emph{{{p['journal']}}}, {vol_str}{no_str}{pp_str}, {p['year']}.{doi_str}\n"
    bibitem_entries.append(entry)

with open('references/extracted_bibitems.tex', 'w', encoding='utf-8') as f:
    f.write('\n'.join(bibitem_entries))

# Generate .bib file
bib_entries = []
for p in papers:
    vol_f = f"  volume = {{{p['volume']}}},\n" if p['volume'] else ""
    no_f = f"  number = {{{p['number']}}},\n" if p['number'] else ""
    pp_f = f"  pages = {{{p['pages']}}},\n" if p['pages'] else ""
    doi_f = f"  doi = {{{p['doi']}}},\n" if p['doi'] else ""
    j_clean = p['journal'].replace('\\&', '&')
    
    b = f"""@article{{{p['key']},
  author = {{{p['authors']}}},
  title = {{{{{p['title']}}}}},
  journal = {{{j_clean}}},
{vol_f}{no_f}{pp_f}  year = {{{p['year']}}},
{doi_f}}}"""
    bib_entries.append(b)

with open('references/references.bib', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(bib_entries))

print("Regenerated cleanly!")
