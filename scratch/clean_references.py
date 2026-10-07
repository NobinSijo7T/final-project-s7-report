import re

# Read extracted bibitems
with open('references/extracted_bibitems.tex', 'r', encoding='utf-8') as f:
    extracted_bibs = f.read().strip()

# Read main.tex
with open('main.tex', 'r', encoding='utf-8') as f:
    tex = f.read()

# 1. Update thebibliography in main.tex to ONLY include the 25 extracted bibitems
new_bib = f"""\\begin{{thebibliography}}{{99}}

{extracted_bibs}

\\end{{thebibliography}}"""

idx_bib1 = tex.find('\\begin{thebibliography}{99}')
idx_bib2 = tex.find('\\end{thebibliography}') + len('\\end{thebibliography}')
if idx_bib1 == -1 or idx_bib2 == -1:
    raise Exception("Could not find thebibliography bounds in main.tex")

tex = tex[:idx_bib1] + new_bib + tex[idx_bib2:]

# 2. In Chapter 2, remove non-extracted cites:
# ref_react, ref_autogen, ref_metagpt
tex = tex.replace(r"established by Yao et~al.~\cite{ref_react} with the \textbf{ReAct} (Reasoning and Acting) framework",
                  r"established through the \textbf{ReAct} (Reasoning and Acting) framework")
tex = tex.replace(r"frameworks such as AutoGen (Wu et~al.~\cite{ref_autogen}) and MetaGPT (Hong et~al.~\cite{ref_metagpt})",
                  r"frameworks such as AutoGen and MetaGPT")

# ref_mcp_spec, ref_toolcua, ref_livemcpbench, ref_openm3
tex = tex.replace(r"\textbf{Model Context Protocol (MCP)}~\cite{ref_mcp_spec}",
                  r"\textbf{Model Context Protocol (MCP)}")
tex = tex.replace(r"Hu et~al.~\cite{ref_toolcua} introduced \textbf{ToolCUA}",
                  r"benchmarks such as \textbf{ToolCUA}")
tex = tex.replace(r"benchmarks including \textbf{LiveMCPBench}~\cite{ref_livemcpbench} and \textbf{Open-M3-Bench}~\cite{ref_openm3}",
                  r"benchmarks including \textbf{LiveMCPBench} and \textbf{Open-M3-Bench}")

# ref_routerbench, ref_xroutebench, ref_lmsys
tex = tex.replace(r"RoutingBench (Chen et~al.~\cite{ref_routerbench}) and xRouteBench (Li et~al.~\cite{ref_xroutebench})",
                  r"Empirical benchmarks such as RoutingBench and xRouteBench")
tex = tex.replace(r"arenas (such as LMSYS Chatbot Arena~\cite{ref_lmsys})",
                  r"arenas (such as LMSYS Chatbot Arena)")

# ref_rlhf, ref_dpo, ref_orpo, ref_lora, ref_ultrafeedback, ref_agent_trajectories
tex = tex.replace(r"Feedback (RLHF)~\cite{ref_rlhf}",
                  r"Feedback (RLHF)")
tex = tex.replace(r"Direct Preference Optimization (DPO)~\cite{ref_dpo} require separate reward modeling or reference networks, Hong et~al.~\cite{ref_orpo} introduced",
                  r"Direct Preference Optimization (DPO) require separate reward modeling or reference networks, Odds Ratio Preference Optimization (ORPO) was introduced,")
tex = tex.replace(r"Low-Rank Adaptation (LoRA)~\cite{ref_lora} and curated preference datasets like UltraFeedback~\cite{ref_ultrafeedback} and CMU Agent Trajectories~\cite{ref_agent_trajectories}",
                  r"Low-Rank Adaptation (LoRA) and curated preference datasets like UltraFeedback and CMU Agent Trajectories")

# ref_wildguard
tex = tex.replace(r"such as WildGuard~\cite{ref_wildguard}, which evaluate",
                  r"which evaluate")

# ref_local_first, ref_dexie, ref_fastapi, ref_xgboost, ref_scikit
tex = tex.replace(r"(Kleppmann et~al.~\cite{ref_local_first})",
                  r"(such as local-first software principles)")
tex = tex.replace(r"\textbf{Dexie.js}~\cite{ref_dexie}",
                  r"\textbf{Dexie.js}")
tex = tex.replace(r"FastAPI~\cite{ref_fastapi}, combined with high-performance ML libraries such as XGBoost~\cite{ref_xgboost} and Scikit-learn~\cite{ref_scikit}",
                  r"FastAPI, combined with high-performance ML libraries such as XGBoost and Scikit-learn")

# Table 2.1
tex = tex.replace(r"AutoGen \cite{ref_autogen} &", r"AutoGen &")
tex = tex.replace(r"MetaGPT \cite{ref_metagpt} &", r"MetaGPT &")
tex = tex.replace(r"ToolCUA \cite{ref_toolcua} &", r"ToolCUA &")

# Line 400
tex = tex.replace(r"(LMSYS Chatbot Arena \cite{ref_lmsys}, RouterBench \cite{ref_routerbench}, WildGuardMix \cite{ref_wildguard}, UltraFeedback \cite{ref_ultrafeedback}, and CMU Agent Trajectories \cite{ref_agent_trajectories})",
                  r"(LMSYS Chatbot Arena, RouterBench, WildGuardMix, UltraFeedback, and CMU Agent Trajectories)")

# Lines 687-691
tex = tex.replace(r"\item \textbf{LMSYS Chatbot Arena Conversations \cite{ref_lmsys}:}",
                  r"\item \textbf{LMSYS Chatbot Arena Conversations:}")
tex = tex.replace(r"\item \textbf{RouterBench \cite{ref_routerbench}:}",
                  r"\item \textbf{RouterBench:}")
tex = tex.replace(r"\item \textbf{WildGuardMix \cite{ref_wildguard}:}",
                  r"\item \textbf{WildGuardMix:}")
tex = tex.replace(r"\item \textbf{UltraFeedback Binarized \cite{ref_ultrafeedback}:}",
                  r"\item \textbf{UltraFeedback Binarized:}")
tex = tex.replace(r"\item \textbf{CMU Agent Trajectories \cite{ref_agent_trajectories}:}",
                  r"\item \textbf{CMU Agent Trajectories:}")

# Save updated main.tex
with open('main.tex', 'w', encoding='utf-8') as f:
    f.write(tex)

print("Cleaned all non-extracted citations from main.tex!")
