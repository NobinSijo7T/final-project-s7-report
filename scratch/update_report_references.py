import re

# Read extracted bibitems
with open('references/extracted_bibitems.tex', 'r', encoding='utf-8') as f:
    extracted_bibs = f.read().strip()

# Read main.tex
with open('main.tex', 'r', encoding='utf-8') as f:
    main_tex = f.read()

# Let's extract existing bibitems from main.tex
bib_match = re.search(r'(\\begin\{thebibliography\}\{99\})(.*?)(\\end\{thebibliography\})', main_tex, re.DOTALL)
if not bib_match:
    raise Exception("Could not find thebibliography in main.tex")

existing_bib_content = bib_match.group(2).strip()

# Combine existing and extracted bibitems
all_bibitems = f"""\\begin{{thebibliography}}{{99}}

% ==============================================================================
% FOUNDATIONAL PARADIGMS, TOOL PROTOCOLS, AND WORKSPACE FRAMEWORKS
% ==============================================================================

{existing_bib_content}

% ==============================================================================
% MULTI-AGENT SYSTEMS, REINFORCEMENT LEARNING, AND WORKFLOW SCHEDULING (EXTRACTED)
% ==============================================================================

{extracted_bibs}

\\end{{thebibliography}}"""

# Now let's craft an enriched Chapter 2 (Literature Review) incorporating all 25 extracted papers
new_chapter_2 = r"""\chapter{Literature Review}

The engineering of an autonomous developer operating environment and multi-agent orchestration platform sits at the convergence of multi-agent reinforcement learning (MARL), distributed workflow scheduling, standardized tool communication protocols, preference-guided language modeling, and local-first data systems. This chapter critically examines the theoretical foundations, algorithmic advancements, and empirical benchmarks established across recent literature, categorizing related works into eight principal dimensions.

\section{Multi-Agent Reinforcement Learning and Cooperative Intelligence}
Coordinating decentralized autonomous agents in dynamic and shared environments presents fundamental challenges, including environmental non-stationarity, exponential state-action state space growth, and coordination dilemmas. Wong et~al.~\cite{ref_wong2023_marlsurvey} provide a comprehensive survey of deep multi-agent reinforcement learning, categorizing modern paradigms into centralized training with decentralized execution (CTDE), opponent modeling, explicit inter-agent communication, and reward shaping. They demonstrate that without structured communication channels or behavioral abstractions, uncoordinated agent fleets suffer severely from the curse of dimensionality and non-stationarity.

To facilitate coordination without burdensome network synchronization, Aina and Ha~\cite{ref_aina2026_smadrl} introduce a stigmergic multi-agent deep reinforcement learning (S-MADRL) framework. Drawing inspiration from biological insect swarms, their model uses environmental traces (virtual pheromones) coupled with curriculum learning, enabling decentralized agents to self-organize into asymmetric workload distributions under severe communication constraints.

In open environments where team size and collaborator objectives vary dynamically, Rother et~al.~\cite{ref_rother2025_openended} propose open-ended coordination via modular open policies. By combining online partner-goal inference with maximum-entropy posterior policy blending, their system adapts dynamically without requiring joint retraining. Similarly, Liu et~al.~\cite{ref_liu2026_humanknowledge} address the scalability bottleneck of large-population multi-agent teams by integrating suboptimal human knowledge formatted in natural language into the action-selection policy.

Addressing heterogeneity across agent capability profiles, Yu et~al.~\cite{ref_yu2024_ghq} propose Grouped Hybrid Q-Learning (GHQ). By establishing Grouped Individual-Global-Max (GIGM) consistency and maximizing mutual information across group trajectories, GHQ overcomes local transition heterogeneity in asymmetric cooperative environments. Complementarily, Xu et~al.~\cite{ref_xu2024_dapm} formulate Decentralized Adaptive Partner Modeling (DAPM) using fictitious self-play (FSP) to construct predictive partner models, mitigating partner sample complexity by up to 28.5\% while maintaining robust convergence.

\section{Dynamic Role Discovery and Human Planning Strategies}
Decomposing complex, multi-stage engineering goals into discrete sub-tasks necessitates dynamic persona and role assignment. Xia et~al.~\cite{ref_xia2023_dynamic_roles} present a framework for dynamic role discovery and assignment in multi-agent task decomposition. By introducing action encoders to map behavioral vectors and regularizing policy drift to prevent excessive role switching, agents dynamically assume specialized roles aligned with task requirements, achieving significant performance gains over static baselines.

From a cognitive planning perspective, Skirzy\'nski et~al.~\cite{ref_skirzynski2024_humanplanning} introduce the Human-Interpret framework to automatically discover and verbalize planning heuristics from human process-tracing data. By converting sequential search operations into procedural formulas and generating natural language descriptions, their method elucidates how human problem solvers prioritize sub-goals under cognitive constraints.

These insights directly inform modern language agent architectures. The foundational paradigm for language model reasoning was established by Yao et~al.~\cite{ref_react} with the \textbf{ReAct} (Reasoning and Acting) framework, which interleaves textual reasoning traces with tool execution steps. Multi-agent collaborative frameworks such as AutoGen (Wu et~al.~\cite{ref_autogen}) and MetaGPT (Hong et~al.~\cite{ref_metagpt}) further demonstrated that decomposing complex software engineering objectives into specialized agent roles (e.g., Architect, Coder, Reviewer) substantially improves code quality and reduces hallucinations through Standardized Operating Procedures (SOPs).

\section{Workflow Scheduling, Multi-Cloud Offloading, and Resource Allocation}
Orchestrating agent workflows and computational jobs across distributed cloud and edge nodes mirrors the multi-objective workflow scheduling literature. Yue et~al.~\cite{ref_yue2026_cpnhrl} formulate CPN-HRL, a hierarchical deep reinforcement learning approach for Computing Power Networks (CPNs) spanning cloud-edge-end environments. Their architecture decomposes scheduling into a high-level LSTM-PPO priority-weight generator and a low-level GAT-PPO topology-aware node selector, augmented with a dual-queue mechanism for latency-critical tasks.

In mobile edge computing (MEC) environments, Ghazal et~al.~\cite{ref_ghazal2025_mecworkflow} develop a knowledge-learning workflow scheduling algorithm that incorporates real-time trust evaluation, security normalization, and adaptive allocation to prevent malicious nodes from executing mission-critical tasks. Addressing infrastructure energy overhead, Barredo and Puente~\cite{ref_barredo2025_multifitness} formulate an energy-aware cooperative multi-fitness evolutionary algorithm for Directed Acyclic Graph (DAG) scientific workflow scheduling in cloud environments, revealing vital Pareto trade-offs between completion makespan and power expenditure.

Hybrid metaheuristic optimization has also demonstrated strong utility for task offloading. Heirati et~al.~\cite{ref_heirati2026_fogcloud} combine feedforward neural network workload prediction, reinforcement learning offloading policies, and hybrid Harris Hawk Optimization with Genetic Algorithms (HHO-GA) for fog-cloud environments. Abdi et~al.~\cite{ref_abdi2024_edgecloud} formulate non-linear mathematical models and genetic algorithms for cost-aware workflow offloading across the edge-cloud continuum under strict QoS and deadline bounds.

For data-intensive workflows, Zhang et~al.~\cite{ref_zhang2023_dataintensive} propose a deep reinforcement learning workflow scheduler using an enhanced Deep Q-Network (DQN) with multi-objective reward shaping to optimize data transmission volume, execution time, and cluster load balancing. Wang et~al.~\cite{ref_wang2023_ecofriendly} introduce the Eco-friendly Reinforcement Learning in Federated Cloud (ERLFC) framework, employing an Actor-Critic architecture to dispatch jobs across geographically distributed data centers based on regional carbon emission factors and cooling efficiency.

Furthermore, Subashree et~al.~\cite{ref_subashree2025_dssso} propose Dolphin Swarm Sparrow Search Optimization (DSSSO), balancing global space exploration with localized tuning to optimize makespan, monetary cost, and hardware utilization. To handle large-scale interactive decision variables in cloud DAGs, Li et~al.~\cite{ref_li2023_vcaes} develop the Variable Contribution Adaptive Evolutionary Scheduling (VCAES) algorithm, dynamically allocating evolutionary optimization resources to the most impactful decision variable clusters.

\section{Standardized Tool Protocols and Multi-Provider LLM Routing}
Historically, connecting LLMs to external developer tools required brittle proprietary API bindings, such as OpenAI Function Calling or custom wrappers. In late 2024, Anthropic open-sourced the \textbf{Model Context Protocol (MCP)}~\cite{ref_mcp_spec}, establishing an open JSON-RPC 2.0 standard for connecting AI assistants to local and remote data sources, developer tools, and prompt repositories.

Recent research benchmarks have systematically examined tool orchestration efficiency. Hu et~al.~\cite{ref_toolcua} introduced \textbf{ToolCUA}, demonstrating that hybrid path orchestration between graphical user interfaces (GUIs) and API tool calls yields significantly higher task success rates and reduced latency for Computer Use Agents (CUAs). Furthermore, benchmarks including \textbf{LiveMCPBench}~\cite{ref_livemcpbench} and \textbf{Open-M3-Bench}~\cite{ref_openm3} established standardized evaluation suites for schema validation, tool invocation fidelity, and sandboxed error recovery across multi-tool environments.

As the frontier LLM ecosystem expanded across diverse providers---ranging from proprietary reasoning engines (OpenAI o1, GPT-4o) and safety-aligned models (Claude 3.5 Sonnet) to ultra-fast inference LPUs (Groq Llama 3) and private microservices (NVIDIA NIM)---intelligent runtime model routing has become imperative. RoutingBench (Chen et~al.~\cite{ref_routerbench}) and xRouteBench (Li et~al.~\cite{ref_xroutebench}) demonstrated that no single model dominates across all query categories, latency constraints, and cost boundaries. By deploying lightweight intent classifiers trained on multi-model benchmark arenas (such as LMSYS Chatbot Arena~\cite{ref_lmsys}), developer operating environments can achieve frontier-grade code generation while curbing inference costs by over 70\%.

\section{Advanced Reinforcement Learning and Reward Formulations}
Formulating robust learning objectives in multi-agent and financial environments requires nuanced reward engineering. Cornalba et~al.~\cite{ref_cornalba2024_multiobj} investigate multi-objective reward generalization in deep reinforcement learning, demonstrating that algorithms incorporating generalized reward functions and discount factors during training exhibit superior predictive stability and handle sparse feedback significantly better than single-objective strategies.

In operational scenarios where step returns are predominantly positive or profit-derived, standard discounted RL algorithms fail due to Laurent series expansion dominance by average reward terms. To resolve this, Schneckenreither and Moser~\cite{ref_schneckenreither2025_aral} formulate Average Reward Adjusted Discounted Reinforcement Learning (ARAL), proving that adjusting state value targets by the average reward preserves discriminative policy convergence across complex operations research benchmarks.

When enforcing behavioral constraints, Marzari et~al.~\cite{ref_marzari2026_epsretrain} propose $\varepsilon$-retraining reinforcement learning. By identifying state-space regions where agents violated safety or behavioral preferences and mixing these into restart distributions via an $\varepsilon$-decay mechanism, $\varepsilon$-retrain guarantees monotonic policy improvements without distorting underlying convergence properties. In information retrieval and ranking settings, Zhuang et~al.~\cite{ref_zhuang2022_roltr} develop Reinforcement Online Learning to Rank (ROLTR) with unbiased reward shaping, utilizing inverse propensity scoring on both clicked and unclicked items to eliminate position bias.

\section{Human-in-the-Loop Alignment and Instruction Optimization}
Incorporating human guidance is crucial for constraining autonomous exploration and aligning model policies with complex user expectations. Niu et~al.~\cite{ref_niu2025_hiat} propose Human-in-the-Loop Reinforcement Learning with Auxiliary Task (HIAT) and its adaptive weighting variant (AWHIAT). By employing an auxiliary task that evaluates policy similarity to compensate for early-stage sample imbalance, HIAT significantly elevates mean episode rewards and sample efficiency.

In the domain of language model fine-tuning, Lee~\cite{ref_lee2025_instructpatentgpt} presents InstructPatentGPT, showcasing how three-stage Reinforcement Learning from Human Feedback (RLHF)~\cite{ref_rlhf} can be executed on consumer-grade GPU hardware to steer complex generative tasks (e.g., patent claim drafting) according to implicit human feedback and granular constraints.

While traditional RLHF and Direct Preference Optimization (DPO)~\cite{ref_dpo} require separate reward modeling or reference networks, Hong et~al.~\cite{ref_orpo} introduced \textbf{Odds Ratio Preference Optimization (ORPO)}, penalizing undesirable generation trajectories directly during Supervised Fine-Tuning:
\begin{equation}
    \mathcal{L}_{\mathrm{ORPO}} = \mathcal{L}_{\mathrm{SFT}} + \beta \cdot \mathcal{L}_{\mathrm{OR}}
\end{equation}
When paired with Low-Rank Adaptation (LoRA)~\cite{ref_lora} and curated preference datasets like UltraFeedback~\cite{ref_ultrafeedback} and CMU Agent Trajectories~\cite{ref_agent_trajectories}, ORPO enables rapid, memory-efficient adaptation of specialized agent personas on local workstations.

\section{Responsible AI Governance and Meaningful Human Control}
Deploying autonomous agents with local system execution privileges necessitates stringent ethical governance and safety guarantees. Vyhmeister et~al.~\cite{ref_vyhmeister2023_responsibleai} propose a comprehensive Responsible AI framework structured around pipeline contextualization, treating ethical and trustworthiness considerations as formal engineering hazards across all lifecycle stages.

To prevent responsibility gaps when autonomous agents execute critical workflows, Siebert et~al.~\cite{ref_siebert2023_humancontrol} establish four actionable properties for \textbf{Meaningful Human Control (MHC)}: (1) defining explicit boundaries for morally loaded situations, (2) ensuring mutually compatible representations between human and AI agents, (3) calibrating human authority and capability, and (4) maintaining explicit causal tracing between agent actions and human awareness. These principles directly underpin calibrated safety checkpoints and runtime guardrails, such as WildGuard~\cite{ref_wildguard}, which evaluate prompt harms, execution risks, and adversarial jailbreaks prior to tool invocation.

\section{Local-First Data Architectures and Reactive In-Browser Databases}
The local-first software paradigm (Kleppmann et~al.~\cite{ref_local_first}) prioritizes client-side storage on user hardware, treating cloud connectivity as an opportunistic enhancement. In browser environments, the HTML5 IndexedDB API provides persistent client object storage but lacks native reactivity. The emergence of \textbf{Dexie.js}~\cite{ref_dexie} provides an ACID-compliant abstraction layer over IndexedDB featuring compound B-tree indexing, transactional guarantees, and the \texttt{useLiveQuery} observable hook. Integrating Dexie with modern frontend frameworks enables automatic UI re-renders upon database mutations, ensuring sub-50ms reactive state propagation without server latency. For backend microservices, asynchronous architectures built on FastAPI~\cite{ref_fastapi}, combined with high-performance ML libraries such as XGBoost~\cite{ref_xgboost} and Scikit-learn~\cite{ref_scikit}, deliver low-latency intent classification and agent orchestration.

\section{Summary of Identified Research Gaps}
Table~\ref{tab:lit_comparison} synthesizes the comparative analysis of existing developer environments and agent platforms against the contributions of PrismSpace.

\begin{table}[H]
\centering
\begin{singlespace}
\caption{Comparative analysis of existing developer agent platforms and PrismSpace.}
\label{tab:lit_comparison}
\footnotesize
\renewcommand{\arraystretch}{1.1}
\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{2.3cm} >{\centering\arraybackslash}p{1.7cm} >{\centering\arraybackslash}p{1.7cm} >{\centering\arraybackslash}p{1.7cm} >{\centering\arraybackslash}p{1.6cm} >{\raggedright\arraybackslash}X}
\toprule
\textbf{Framework} & \textbf{Tool Protocol} & \textbf{Model Routing} & \textbf{Safety Gate} & \textbf{Local DB} & \textbf{Primary Focus / Limitations} \\
\midrule
AutoGen \cite{ref_autogen} & Custom API & No & Manual Flag & In-Memory & Python agent framework; lacks native UI and local DB. \\
MetaGPT \cite{ref_metagpt} & Custom SOP & No & No & File-Based & High token consumption; rigid waterfall lifecycle. \\
Cursor / Copilot & Proprietary & Limited & Prompt-Level & Cloud Synced & Closed source; single-vendor dependency; opaque execution. \\
ToolCUA \cite{ref_toolcua} & Custom RPC & No & No & None & Research benchmark for GUI/API navigation paths. \\
\textbf{PrismSpace} & \textbf{Open MCP} & \textbf{Yes (5 Tiers)} & \textbf{Yes (Tuned)} & \textbf{Dexie IDB} & \textbf{Unified developer OS, observable swarm, and ML routing.} \\
\bottomrule
\end{tabularx}
\end{singlespace}
\end{table}

"""

# String replacement without regex escape issues
idx1 = main_tex.find('\\chapter{Literature Review}')
idx2 = main_tex.find('\\chapter{System Requirements and Architecture Specification}')

if idx1 == -1 or idx2 == -1:
    raise Exception("Could not find chapter bounds")

main_tex_updated = main_tex[:idx1] + new_chapter_2 + main_tex[idx2:]

# Replace thebibliography
idx_bib1 = main_tex_updated.find('\\begin{thebibliography}{99}')
idx_bib2 = main_tex_updated.find('\\end{thebibliography}') + len('\\end{thebibliography}')

if idx_bib1 == -1 or idx_bib2 == -1:
    raise Exception("Could not find thebibliography bounds")

main_tex_updated = main_tex_updated[:idx_bib1] + all_bibitems + main_tex_updated[idx_bib2:]

with open('main.tex', 'w', encoding='utf-8') as f:
    f.write(main_tex_updated)

print("Updated main.tex successfully via string slicing!")
