"""
Founding Engineer Academy — Two learning tracks:
1. AI Academy: AI/ML/LLM mastery (15 sections, 155 topics)
2. Founder Academy: Leadership, Business, Product, Communication, Edviron (5 sections, 67+ topics)

Each topic has prerequisites — system recommends topics whose prereqs are satisfied.
"""

import random

# ══════════════════════════════════════════════════════════════════════
# TRACK 1: AI / ML / LLM ACADEMY
# ══════════════════════════════════════════════════════════════════════

AI_SECTIONS = {

    # ── SECTION 1: ML FOUNDATIONS ────────────────────────────────────
    "ml_foundations": {
        "name": "Core ML Foundations",
        "emoji": "📐",
        "order": 1,
        "goal": "You can debug models mathematically.",
        "topics": [
            {"id": "ml_linalg", "title": "Linear Algebra for ML — Vectors, Matrices, Eigenvalues, SVD", "prereqs": [], "tags": ["math", "foundations"]},
            {"id": "ml_prob_stats", "title": "Probability & Statistics — Bayes, Distributions, MLE, MAP", "prereqs": [], "tags": ["math", "foundations"]},
            {"id": "ml_information_theory", "title": "Information Theory — Entropy, KL Divergence, Cross-Entropy Loss", "prereqs": ["ml_prob_stats"], "tags": ["math", "foundations"]},
            {"id": "ml_optimization", "title": "Optimization — SGD, Adam, Learning Rate Schedules, Convergence", "prereqs": ["ml_linalg"], "tags": ["math", "training"]},
            {"id": "ml_bias_variance", "title": "Bias–Variance Tradeoff & Model Complexity", "prereqs": ["ml_prob_stats"], "tags": ["theory"]},
            {"id": "ml_overfitting", "title": "Overfitting, Regularization (L1/L2/Dropout) & Generalization", "prereqs": ["ml_bias_variance"], "tags": ["theory"]},
            {"id": "ml_linear_logistic", "title": "Linear & Logistic Regression — Derivation to Production", "prereqs": ["ml_linalg", "ml_optimization"], "tags": ["classical"]},
            {"id": "ml_trees", "title": "Decision Trees, Random Forest, XGBoost & Gradient Boosting", "prereqs": ["ml_bias_variance"], "tags": ["classical"]},
            {"id": "ml_svm", "title": "Support Vector Machines & Kernel Methods", "prereqs": ["ml_linalg", "ml_optimization"], "tags": ["classical"]},
            {"id": "ml_clustering", "title": "Clustering — K-Means, DBSCAN, Hierarchical & When to Use What", "prereqs": ["ml_linalg"], "tags": ["unsupervised"]},
            {"id": "ml_dim_reduction", "title": "Dimensionality Reduction — PCA, t-SNE, UMAP", "prereqs": ["ml_linalg", "ml_prob_stats"], "tags": ["unsupervised"]},
            {"id": "ml_eval_metrics", "title": "Evaluation Metrics — Precision, Recall, F1, AUC, RMSE & When Each Matters", "prereqs": ["ml_linear_logistic"], "tags": ["evaluation"]},
            {"id": "ml_feature_eng", "title": "Feature Engineering, Selection & Importance in Production", "prereqs": ["ml_eval_metrics"], "tags": ["practical"]},
            {"id": "ml_experiment", "title": "ML Experiment Design — A/B Testing, Cross-Validation, Hyperparameter Tuning", "prereqs": ["ml_eval_metrics"], "tags": ["practical"]},
        ],
    },

    # ── SECTION 2: DEEP LEARNING ─────────────────────────────────────
    "deep_learning": {
        "name": "Deep Learning Fundamentals",
        "emoji": "🧠",
        "order": 2,
        "goal": "You can implement a transformer from scratch.",
        "topics": [
            {"id": "dl_nn_basics", "title": "Neural Networks — Perceptrons, MLPs, Universal Approximation", "prereqs": ["ml_linalg", "ml_optimization"], "tags": ["foundations"]},
            {"id": "dl_backprop", "title": "Backpropagation — Full Derivation, Computational Graphs, Autograd", "prereqs": ["dl_nn_basics"], "tags": ["math", "training"]},
            {"id": "dl_activation_loss", "title": "Activation Functions & Loss Functions — Complete Guide", "prereqs": ["dl_backprop"], "tags": ["foundations"]},
            {"id": "dl_cnn", "title": "CNNs — Convolutions, Pooling, ResNet, Architecture Evolution", "prereqs": ["dl_backprop"], "tags": ["architecture"]},
            {"id": "dl_rnn_lstm", "title": "RNNs, LSTMs & GRUs — Sequential Modeling & Vanishing Gradients", "prereqs": ["dl_backprop"], "tags": ["architecture"]},
            {"id": "dl_attention", "title": "Attention Mechanism — Bahdanau to Multi-Head, From Scratch", "prereqs": ["dl_rnn_lstm"], "tags": ["architecture", "critical"]},
            {"id": "dl_transformer", "title": "Transformer Architecture — Complete Deep Dive (Vaswani et al.)", "prereqs": ["dl_attention"], "tags": ["architecture", "critical"]},
            {"id": "dl_positional_enc", "title": "Positional Encoding — Sinusoidal, Learned, Rotary", "prereqs": ["dl_transformer"], "tags": ["architecture"]},
            {"id": "dl_layernorm_batchnorm", "title": "Normalization — BatchNorm, LayerNorm, RMSNorm, GroupNorm", "prereqs": ["dl_backprop"], "tags": ["training"]},
            {"id": "dl_dropout_init", "title": "Dropout, Weight Initialization & Gradient Clipping", "prereqs": ["dl_backprop"], "tags": ["training"]},
            {"id": "dl_training_tricks", "title": "Training at Scale — Mixed Precision, Warmup, Cosine Annealing", "prereqs": ["dl_dropout_init", "dl_layernorm_batchnorm"], "tags": ["training", "practical"]},
            {"id": "dl_transfer_learning", "title": "Transfer Learning & Pretraining Paradigm", "prereqs": ["dl_transformer"], "tags": ["practical", "critical"]},
        ],
    },

    # ── SECTION 3: LLM INTERNALS ─────────────────────────────────────
    "llm_internals": {
        "name": "Modern LLM Internals",
        "emoji": "🔥",
        "order": 3,
        "goal": "You understand how GPT-4, Claude, Llama are built.",
        "topics": [
            {"id": "llm_pretraining", "title": "Pretraining — Next Token Prediction, Causal vs Masked LMs", "prereqs": ["dl_transformer"], "tags": ["pretraining", "critical"]},
            {"id": "llm_tokenization", "title": "Tokenization Deep Dive — BPE, SentencePiece, Tiktoken", "prereqs": ["dl_transformer"], "tags": ["pretraining"]},
            {"id": "llm_scaling_laws", "title": "Scaling Laws — Chinchilla, Compute-Optimal Training, Emergent Abilities", "prereqs": ["llm_pretraining"], "tags": ["pretraining", "theory"]},
            {"id": "llm_data_mixtures", "title": "Data Curation — Web Crawls, Filtering, Dedup, Data Quality", "prereqs": ["llm_pretraining"], "tags": ["pretraining"]},
            {"id": "llm_architecture_variants", "title": "LLM Architectures — GPT, LLaMA, Mistral, Gemma Differences", "prereqs": ["llm_pretraining"], "tags": ["architecture", "critical"]},
            {"id": "llm_sft", "title": "Supervised Fine-Tuning (SFT) — Data, Methods, Pitfalls", "prereqs": ["llm_pretraining"], "tags": ["post-training", "critical"]},
            {"id": "llm_rlhf", "title": "RLHF — Reward Models, PPO, Why Alignment Is Hard", "prereqs": ["llm_sft"], "tags": ["post-training", "critical"]},
            {"id": "llm_dpo", "title": "DPO & ORPO — Simpler Alignment Without RL", "prereqs": ["llm_rlhf"], "tags": ["post-training"]},
            {"id": "llm_constitutional", "title": "Constitutional AI, RLAIF & Self-Alignment", "prereqs": ["llm_rlhf"], "tags": ["alignment"]},
            {"id": "llm_kv_cache", "title": "KV Cache — Memory, PagedAttention, Flash Attention", "prereqs": ["dl_transformer", "dl_attention"], "tags": ["architecture", "critical"]},
            {"id": "llm_rope_alibi", "title": "RoPE, ALiBi & Long Context — YaRN, NTK-Aware Scaling", "prereqs": ["dl_positional_enc", "llm_kv_cache"], "tags": ["architecture"]},
            {"id": "llm_moe", "title": "Mixture of Experts (MoE) — Mixtral, Switch Transformer, Routing", "prereqs": ["llm_pretraining"], "tags": ["architecture"]},
            {"id": "llm_speculative", "title": "Speculative Decoding & Parallel Inference", "prereqs": ["llm_kv_cache"], "tags": ["inference"]},
            {"id": "llm_reasoning", "title": "Reasoning in LLMs — Chain of Thought, o1-style, Test-Time Compute", "prereqs": ["llm_pretraining"], "tags": ["critical", "frontier"]},
        ],
    },

    # ── SECTION 4: PROMPT ENGINEERING ────────────────────────────────
    "prompt_engineering": {
        "name": "Expert Prompt Engineering",
        "emoji": "🧩",
        "order": 4,
        "goal": "You can reliably control LLM behavior in production.",
        "topics": [
            {"id": "pe_zeroshot_fewshot", "title": "Zero-Shot, Few-Shot & In-Context Learning", "prereqs": ["llm_pretraining"], "tags": ["fundamentals"]},
            {"id": "pe_cot", "title": "Chain of Thought & Step-by-Step Reasoning", "prereqs": ["pe_zeroshot_fewshot"], "tags": ["technique"]},
            {"id": "pe_self_consistency", "title": "Self-Consistency, Tree of Thought & Majority Voting", "prereqs": ["pe_cot"], "tags": ["technique"]},
            {"id": "pe_react", "title": "ReAct Prompting — Reasoning + Acting Pattern", "prereqs": ["pe_cot"], "tags": ["technique", "critical"]},
            {"id": "pe_tool_prompting", "title": "Tool Use & Function Calling — OpenAI, Claude, Gemini APIs", "prereqs": ["pe_react"], "tags": ["technique", "critical"]},
            {"id": "pe_structured", "title": "Structured Outputs — JSON Mode, Pydantic, Grammar Constraints", "prereqs": ["pe_zeroshot_fewshot"], "tags": ["practical"]},
            {"id": "pe_system_prompts", "title": "System Prompt Design — Personas, Rules, Production Patterns", "prereqs": ["pe_zeroshot_fewshot"], "tags": ["practical"]},
            {"id": "pe_injection", "title": "Prompt Injection Attacks — Direct, Indirect & Defense", "prereqs": ["pe_system_prompts"], "tags": ["security"]},
            {"id": "pe_guardrails", "title": "Guardrails — Input/Output Validation, Content Filters", "prereqs": ["pe_injection"], "tags": ["security", "practical"]},
            {"id": "pe_eval", "title": "Prompt Evaluation — Automated Testing, LLM-as-Judge", "prereqs": ["pe_zeroshot_fewshot"], "tags": ["evaluation"]},
        ],
    },

    # ── SECTION 5: RAG SYSTEMS ───────────────────────────────────────
    "rag_systems": {
        "name": "RAG Systems",
        "emoji": "📚",
        "order": 5,
        "goal": "You can build production RAG that actually works at scale.",
        "topics": [
            {"id": "rag_embeddings", "title": "Embeddings Deep Dive — Word2Vec to Modern Embedding Models", "prereqs": ["dl_transformer"], "tags": ["retrieval", "critical"]},
            {"id": "rag_vectordb", "title": "Vector Database Internals — Pinecone, Weaviate, Qdrant, pgvector", "prereqs": ["rag_embeddings"], "tags": ["retrieval"]},
            {"id": "rag_ann", "title": "ANN Algorithms — HNSW, IVF, PQ, ScaNN Explained", "prereqs": ["rag_vectordb"], "tags": ["retrieval"]},
            {"id": "rag_hybrid", "title": "Hybrid Search — BM25 + Vector + Reranking (Cohere, ColBERT)", "prereqs": ["rag_ann"], "tags": ["retrieval", "critical"]},
            {"id": "rag_chunking", "title": "Chunking Strategies — Semantic, Recursive, Parent-Child", "prereqs": ["rag_embeddings"], "tags": ["retrieval", "practical"]},
            {"id": "rag_basic_pipeline", "title": "Building a Production RAG Pipeline End to End", "prereqs": ["rag_hybrid", "rag_chunking", "pe_zeroshot_fewshot"], "tags": ["pipeline", "practical"]},
            {"id": "rag_multihop", "title": "Multi-Hop RAG — Complex Questions Across Multiple Docs", "prereqs": ["rag_basic_pipeline"], "tags": ["advanced"]},
            {"id": "rag_graph", "title": "Graph RAG — Knowledge Graphs + Retrieval (Microsoft's Approach)", "prereqs": ["rag_basic_pipeline"], "tags": ["advanced"]},
            {"id": "rag_agentic", "title": "Agentic RAG — Self-Correcting, Query Routing, Adaptive Retrieval", "prereqs": ["rag_basic_pipeline", "pe_react"], "tags": ["advanced", "critical"]},
            {"id": "rag_evaluation", "title": "RAG Evaluation — RAGAS, Faithfulness, Context Relevance", "prereqs": ["rag_basic_pipeline"], "tags": ["evaluation"]},
            {"id": "rag_multimodal", "title": "Multimodal RAG — Images, Tables, PDFs in Retrieval", "prereqs": ["rag_basic_pipeline"], "tags": ["advanced"]},
        ],
    },

    # ── SECTION 6: AI AGENTS ─────────────────────────────────────────
    "ai_agents": {
        "name": "AI Agents",
        "emoji": "🤖",
        "order": 6,
        "goal": "You can design reliable agents for production (not toy demos).",
        "topics": [
            {"id": "agent_react", "title": "ReAct Pattern — The Foundation of Modern Agents", "prereqs": ["pe_react", "pe_tool_prompting"], "tags": ["pattern", "critical"]},
            {"id": "agent_tool_use", "title": "Tool Use & Function Calling — Building Reliable Tool Agents", "prereqs": ["agent_react"], "tags": ["pattern"]},
            {"id": "agent_planning", "title": "Planning — Task Decomposition, Plan-and-Execute, LATS", "prereqs": ["agent_react"], "tags": ["architecture"]},
            {"id": "agent_memory", "title": "Agent Memory — Short/Long-term, Vector Memory, Summarization", "prereqs": ["agent_react", "rag_embeddings"], "tags": ["architecture", "critical"]},
            {"id": "agent_multi", "title": "Multi-Agent Systems — Orchestration, Debate, Specialization", "prereqs": ["agent_planning", "agent_memory"], "tags": ["advanced"]},
            {"id": "agent_failures", "title": "Agent Failure Modes — Loops, Hallucination, Error Recovery", "prereqs": ["agent_react"], "tags": ["reliability"]},
            {"id": "agent_deterministic", "title": "Deterministic vs Autonomous Agents — When to Use What", "prereqs": ["agent_planning"], "tags": ["architecture"]},
            {"id": "agent_frameworks", "title": "Frameworks Deep Dive — LangGraph, LlamaIndex, AutoGen, CrewAI", "prereqs": ["agent_tool_use"], "tags": ["practical"]},
            {"id": "agent_code", "title": "Code Agents — Writing, Testing & Deploying Code via Agents", "prereqs": ["agent_tool_use"], "tags": ["practical", "critical"]},
            {"id": "agent_eval", "title": "Agent Evaluation — Benchmarks, Traces, Reliability Metrics", "prereqs": ["agent_failures"], "tags": ["evaluation"]},
        ],
    },

    # ── SECTION 7: LLMOPS / PRODUCTION ───────────────────────────────
    "llmops": {
        "name": "LLMOps / Production AI",
        "emoji": "⚙️",
        "order": 7,
        "goal": "You can run LLMs cheaply at massive scale.",
        "topics": [
            {"id": "ops_serving", "title": "LLM Serving — vLLM, TGI, TensorRT-LLM, Continuous Batching", "prereqs": ["llm_kv_cache"], "tags": ["serving", "critical"]},
            {"id": "ops_quantization", "title": "Quantization — GPTQ, AWQ, GGUF, INT4/INT8 Tradeoffs", "prereqs": ["dl_transformer"], "tags": ["optimization"]},
            {"id": "ops_lora", "title": "LoRA & QLoRA — Parameter-Efficient Fine-Tuning at Scale", "prereqs": ["llm_sft", "ops_quantization"], "tags": ["fine-tuning", "critical"]},
            {"id": "ops_gpu_cpu", "title": "GPU Architecture for AI — CUDA Cores, Tensor Cores, HBM, NVLink", "prereqs": ["ops_serving"], "tags": ["infra"]},
            {"id": "ops_throughput_latency", "title": "Throughput vs Latency — Batching, Prefill/Decode Split", "prereqs": ["ops_serving"], "tags": ["infra"]},
            {"id": "ops_cost", "title": "Cost Optimization — Prompt Caching, Model Cascade, Distillation", "prereqs": ["ops_throughput_latency"], "tags": ["business", "critical"]},
            {"id": "ops_streaming", "title": "Streaming & Real-Time — SSE, WebSockets, Token-by-Token", "prereqs": ["ops_serving"], "tags": ["practical"]},
            {"id": "ops_logging", "title": "Observability — Prompt Logging, Traces, LangSmith, Langfuse", "prereqs": ["ops_serving"], "tags": ["monitoring"]},
            {"id": "ops_hallucination", "title": "Hallucination Detection & Grounding in Production", "prereqs": ["ops_logging", "rag_evaluation"], "tags": ["monitoring", "critical"]},
            {"id": "ops_eval_pipeline", "title": "Evaluation Pipelines — CI/CD for LLMs, Regression Testing", "prereqs": ["ops_logging"], "tags": ["evaluation"]},
            {"id": "ops_drift", "title": "Drift Monitoring — Prompt Drift, Data Drift, Model Decay", "prereqs": ["ops_eval_pipeline"], "tags": ["monitoring"]},
            {"id": "ops_gateway", "title": "AI Gateway — Rate Limiting, Load Balancing, API Management", "prereqs": ["ops_serving"], "tags": ["infra", "practical"]},
        ],
    },

    # ── SECTION 8: AI SYSTEM DESIGN ──────────────────────────────────
    "ai_system_design": {
        "name": "AI System Design",
        "emoji": "🏗️",
        "order": 8,
        "goal": "You think like an AI architect.",
        "topics": [
            {"id": "aisd_chatgpt", "title": "Design: ChatGPT-like System End to End", "prereqs": ["ops_serving", "agent_memory"], "tags": ["design", "critical"]},
            {"id": "aisd_rag_scale", "title": "Design: RAG Pipeline at Scale (1M+ docs, 1000 QPS)", "prereqs": ["rag_basic_pipeline", "ops_throughput_latency"], "tags": ["design", "critical"]},
            {"id": "aisd_multitenant", "title": "Design: Multi-Tenant AI SaaS Platform", "prereqs": ["aisd_chatgpt"], "tags": ["design"]},
            {"id": "aisd_realtime", "title": "Design: Real-Time AI Inference System (< 100ms)", "prereqs": ["ops_throughput_latency", "ops_streaming"], "tags": ["design"]},
            {"id": "aisd_caching", "title": "AI Caching — Semantic Cache, KV Cache Sharing, Prompt Cache", "prereqs": ["ops_cost", "rag_embeddings"], "tags": ["optimization"]},
            {"id": "aisd_routing", "title": "Model Routing — Cost-Aware, Quality-Aware, Fallback Chains", "prereqs": ["ops_cost"], "tags": ["architecture"]},
            {"id": "aisd_guardrails_arch", "title": "Guardrails Architecture — Input/Output Safety at Scale", "prereqs": ["pe_guardrails", "aisd_chatgpt"], "tags": ["architecture", "safety"]},
            {"id": "aisd_feedback", "title": "Feedback Loops — RLHF from Production, Flywheel Effects", "prereqs": ["ops_eval_pipeline"], "tags": ["architecture"]},
            {"id": "aisd_search", "title": "Design: AI-Powered Search Engine (Perplexity-like)", "prereqs": ["rag_agentic", "ops_serving"], "tags": ["design", "critical"]},
            {"id": "aisd_copilot", "title": "Design: AI Code Copilot (Cursor/GitHub Copilot-like)", "prereqs": ["agent_code", "ops_serving"], "tags": ["design"]},
        ],
    },

    # ── SECTION 9: AI SAFETY & RELIABILITY ───────────────────────────
    "ai_safety": {
        "name": "AI Safety & Reliability",
        "emoji": "🔐",
        "order": 9,
        "goal": "You build safe, reliable AI systems in production.",
        "topics": [
            {"id": "safe_hallucinations", "title": "Hallucinations — Root Causes, Detection & Mitigation", "prereqs": ["llm_pretraining"], "tags": ["safety"]},
            {"id": "safe_injection", "title": "Prompt Injection — Direct, Indirect & Multi-Layer Defense", "prereqs": ["pe_injection"], "tags": ["security", "critical"]},
            {"id": "safe_jailbreak", "title": "Jailbreak Attacks — DAN, PAIR, Multi-Turn & Defense", "prereqs": ["safe_injection"], "tags": ["security"]},
            {"id": "safe_data_leakage", "title": "Data Leakage, PII & Privacy in LLM Systems", "prereqs": ["safe_hallucinations"], "tags": ["privacy"]},
            {"id": "safe_misuse", "title": "Model Misuse, Deepfakes & Responsible AI Deployment", "prereqs": ["safe_hallucinations"], "tags": ["ethics"]},
            {"id": "safe_redteam", "title": "Red-Teaming LLMs — Systematic Methods & Frameworks", "prereqs": ["safe_jailbreak", "safe_injection"], "tags": ["evaluation", "critical"]},
            {"id": "safe_compliance", "title": "AI Compliance — EU AI Act, NIST AI RMF, SOC2 for AI", "prereqs": ["safe_data_leakage"], "tags": ["regulatory"]},
        ],
    },

    # ── SECTION 10: ADVANCED TOPICS ──────────────────────────────────
    "advanced_ai": {
        "name": "Advanced & Frontier Topics",
        "emoji": "🧮",
        "order": 10,
        "goal": "Cutting-edge skills that separate you from everyone else.",
        "topics": [
            {"id": "adv_finetune", "title": "Fine-Tuning Open Models End to End — Llama, Mistral, Gemma", "prereqs": ["ops_lora", "llm_sft"], "tags": ["practical", "critical"]},
            {"id": "adv_distillation", "title": "Model Distillation — Knowledge Transfer, Smaller Faster Models", "prereqs": ["llm_pretraining", "ops_quantization"], "tags": ["optimization"]},
            {"id": "adv_synthetic", "title": "Synthetic Data Generation — Self-Instruct, Evol-Instruct, UltraChat", "prereqs": ["llm_sft"], "tags": ["data"]},
            {"id": "adv_multimodal", "title": "Multimodal Models — Vision-Language, LLaVA, GPT-4V Architecture", "prereqs": ["dl_cnn", "dl_transformer"], "tags": ["architecture"]},
            {"id": "adv_speech", "title": "Speech Models — Whisper, TTS, Voice Agents, Real-Time Voice", "prereqs": ["dl_transformer"], "tags": ["architecture"]},
            {"id": "adv_diffusion", "title": "Diffusion Models — DDPM, Stable Diffusion, Video Gen", "prereqs": ["dl_backprop", "ml_prob_stats"], "tags": ["architecture"]},
            {"id": "adv_graph_llm", "title": "Graph Neural Networks + LLMs — Knowledge Reasoning at Scale", "prereqs": ["rag_graph"], "tags": ["architecture"]},
            {"id": "adv_mcp", "title": "MCP (Model Context Protocol) — The New Tool Standard", "prereqs": ["agent_tool_use", "pe_tool_prompting"], "tags": ["protocol", "critical"]},
            {"id": "adv_world_models", "title": "World Models & Video Generation — Sora, Gen-3", "prereqs": ["adv_diffusion"], "tags": ["frontier"]},
            {"id": "adv_test_time", "title": "Test-Time Compute — o1, Reasoning Tokens, Search at Inference", "prereqs": ["llm_reasoning"], "tags": ["frontier", "critical"]},
        ],
    },

    # ══════════════════════════════════════════════════════════════════
    # NEW: INDUSTRY & REAL-WORLD SECTIONS
    # ══════════════════════════════════════════════════════════════════

    # ── SECTION 11: HOW INDUSTRY USES AI ─────────────────────────────
    "industry_ai": {
        "name": "How Industry Leverages AI",
        "emoji": "🏢",
        "order": 11,
        "goal": "You understand how real companies build & ship AI products.",
        "topics": [
            {"id": "ind_openai_arch", "title": "How OpenAI Built ChatGPT — Architecture, Infra & Scale", "prereqs": ["llm_pretraining", "ops_serving"], "tags": ["industry", "critical"]},
            {"id": "ind_google_search", "title": "How Google Uses AI in Search — BERT, MUM, SGE, Gemini", "prereqs": ["dl_transformer", "rag_embeddings"], "tags": ["industry"]},
            {"id": "ind_stripe_fraud", "title": "How Stripe Uses ML for Fraud Detection at Scale", "prereqs": ["ml_trees", "ml_eval_metrics"], "tags": ["industry", "fintech"]},
            {"id": "ind_netflix_recsys", "title": "Netflix & Spotify Recommendation Systems — Deep Dive", "prereqs": ["rag_embeddings", "ml_eval_metrics"], "tags": ["industry"]},
            {"id": "ind_tesla_autopilot", "title": "Tesla Autopilot & Waymo — Real-Time Vision AI at Scale", "prereqs": ["dl_cnn", "dl_transformer"], "tags": ["industry"]},
            {"id": "ind_copilot", "title": "GitHub Copilot & Cursor — How AI Code Assistants Work", "prereqs": ["llm_pretraining", "rag_basic_pipeline"], "tags": ["industry", "critical"]},
            {"id": "ind_midjourney", "title": "Midjourney & DALL-E — Text-to-Image in Production", "prereqs": ["adv_diffusion"], "tags": ["industry"]},
            {"id": "ind_anthropic", "title": "Anthropic's Approach — Constitutional AI, Claude, Safety-First", "prereqs": ["llm_constitutional", "safe_redteam"], "tags": ["industry"]},
            {"id": "ind_fintech_ai", "title": "AI in Fintech — Credit Scoring, KYC, Risk, Payment Fraud", "prereqs": ["ml_trees", "ml_eval_metrics"], "tags": ["industry", "fintech", "critical"]},
            {"id": "ind_healthcare_ai", "title": "AI in Healthcare — Diagnostics, Drug Discovery, Clinical NLP", "prereqs": ["dl_transformer", "ml_eval_metrics"], "tags": ["industry"]},
            {"id": "ind_ai_startups", "title": "AI Startup Playbook — What Works, What Fails, Moats", "prereqs": ["ind_openai_arch"], "tags": ["industry", "strategy"]},
        ],
    },

    # ── SECTION 12: AI PRODUCT & STRATEGY ────────────────────────────
    "ai_product": {
        "name": "AI Product & Strategy",
        "emoji": "🎯",
        "order": 12,
        "goal": "You can decide what to build, buy, or fine-tune — like a CTO.",
        "topics": [
            {"id": "prod_build_vs_buy", "title": "Build vs Buy vs Fine-Tune — Decision Framework for AI", "prereqs": ["ops_cost", "llm_sft"], "tags": ["strategy", "critical"]},
            {"id": "prod_moats", "title": "AI Moats — Data, Distribution, Workflow, Switching Costs", "prereqs": ["ind_ai_startups"], "tags": ["strategy"]},
            {"id": "prod_pricing", "title": "AI Product Pricing — Per-Token, Per-Seat, Value-Based, Usage", "prereqs": ["ops_cost"], "tags": ["business"]},
            {"id": "prod_eval_driven", "title": "Eval-Driven Development — Ship AI with Confidence", "prereqs": ["ops_eval_pipeline", "pe_eval"], "tags": ["methodology", "critical"]},
            {"id": "prod_user_feedback", "title": "User Feedback Loops — Thumbs Up/Down to Model Improvement", "prereqs": ["aisd_feedback"], "tags": ["product"]},
            {"id": "prod_ai_ux", "title": "AI UX Patterns — Chat, Copilot, Autocomplete, Suggestions", "prereqs": ["pe_structured"], "tags": ["product"]},
            {"id": "prod_launch", "title": "Launching AI Features — Canary, Shadow Mode, Feature Flags", "prereqs": ["ops_eval_pipeline"], "tags": ["methodology"]},
            {"id": "prod_compliance_gdpr", "title": "AI & Data Privacy — GDPR, CCPA, Data Processing for ML", "prereqs": ["safe_data_leakage"], "tags": ["regulatory"]},
            {"id": "prod_roi", "title": "Measuring AI ROI — Cost per Query, Value Generated, Automation Rate", "prereqs": ["prod_pricing"], "tags": ["business", "critical"]},
        ],
    },

    # ── SECTION 13: AI INFRA & CLOUD ─────────────────────────────────
    "ai_infra": {
        "name": "AI Infrastructure & Cloud",
        "emoji": "☁️",
        "order": 13,
        "goal": "You can architect and deploy AI at any scale.",
        "topics": [
            {"id": "infra_gpu_landscape", "title": "GPU Landscape — A100, H100, H200, AMD MI300, TPU Comparison", "prereqs": ["ops_gpu_cpu"], "tags": ["hardware"]},
            {"id": "infra_distributed_training", "title": "Distributed Training — DDP, FSDP, DeepSpeed, Megatron-LM", "prereqs": ["dl_training_tricks", "ops_gpu_cpu"], "tags": ["training", "critical"]},
            {"id": "infra_cloud_ai", "title": "Cloud AI Services — AWS Bedrock, Azure OpenAI, GCP Vertex", "prereqs": ["ops_serving"], "tags": ["cloud"]},
            {"id": "infra_kubernetes_ai", "title": "Kubernetes for AI — GPU Scheduling, KServe, Ray Serve", "prereqs": ["ops_serving"], "tags": ["infra"]},
            {"id": "infra_vector_at_scale", "title": "Vector Search at Scale — Billion-Vector Infrastructure", "prereqs": ["rag_ann", "infra_cloud_ai"], "tags": ["infra"]},
            {"id": "infra_data_pipeline", "title": "ML Data Pipelines — Feature Stores, ETL, Data Versioning", "prereqs": ["ml_feature_eng"], "tags": ["data", "practical"]},
            {"id": "infra_model_registry", "title": "Model Registry & MLflow — Versioning, Deployment, Rollback", "prereqs": ["ops_eval_pipeline"], "tags": ["mlops"]},
            {"id": "infra_edge_ai", "title": "Edge AI & On-Device Models — ONNX, CoreML, TFLite", "prereqs": ["ops_quantization"], "tags": ["deployment"]},
        ],
    },

    # ── SECTION 14: REAL-WORLD AI ENGINEERING ────────────────────────
    "ai_engineering": {
        "name": "Real-World AI Engineering",
        "emoji": "🔧",
        "order": 14,
        "goal": "You can solve the messy, real problems that textbooks don't cover.",
        "topics": [
            {"id": "eng_debugging_llm", "title": "Debugging LLM Applications — Traces, Evals, Root Cause Analysis", "prereqs": ["ops_logging", "pe_eval"], "tags": ["practical", "critical"]},
            {"id": "eng_latency_budget", "title": "Latency Budgeting — Where Time Goes in an AI Request", "prereqs": ["ops_throughput_latency"], "tags": ["practical"]},
            {"id": "eng_context_window", "title": "Context Window Management — What to Include, What to Summarize", "prereqs": ["rag_chunking", "pe_system_prompts"], "tags": ["practical"]},
            {"id": "eng_structured_extraction", "title": "Structured Data Extraction — Parsing PDFs, Invoices, Tables with AI", "prereqs": ["pe_structured", "rag_basic_pipeline"], "tags": ["practical", "critical"]},
            {"id": "eng_ai_testing", "title": "Testing AI Systems — Unit Tests, Integration Tests, Fuzzing", "prereqs": ["ops_eval_pipeline"], "tags": ["testing"]},
            {"id": "eng_migration", "title": "Migrating Between LLM Providers — OpenAI → Anthropic → OSS", "prereqs": ["ops_serving", "pe_system_prompts"], "tags": ["practical"]},
            {"id": "eng_cost_war_stories", "title": "AI Cost War Stories — How Teams Cut 90% of LLM Costs", "prereqs": ["ops_cost"], "tags": ["business", "critical"]},
            {"id": "eng_oncall_ai", "title": "On-Call for AI Systems — Incidents, Degradation, Runbooks", "prereqs": ["ops_drift", "ops_hallucination"], "tags": ["operations"]},
            {"id": "eng_ai_tech_debt", "title": "AI Technical Debt — Hidden Costs, Anti-Patterns, Refactoring", "prereqs": ["eng_debugging_llm"], "tags": ["architecture"]},
        ],
    },

    # ── SECTION 15: AI FOR FOUNDING ENGINEERS ────────────────────────
    "ai_founder": {
        "name": "AI for Founding Engineers",
        "emoji": "🚀",
        "order": 15,
        "goal": "You can lead AI strategy at a startup — from prototype to production to PMF.",
        "topics": [
            {"id": "founder_ai_strategy", "title": "AI Strategy for Startups — Where AI Creates Real Value", "prereqs": ["prod_build_vs_buy", "ind_ai_startups"], "tags": ["strategy", "critical"]},
            {"id": "founder_mvp_ai", "title": "Building AI MVPs — Fastest Path to Product-Market Fit", "prereqs": ["rag_basic_pipeline", "pe_system_prompts"], "tags": ["product", "critical"]},
            {"id": "founder_hiring_ai", "title": "Hiring for AI — What to Look For, Interview Questions, Team Structure", "prereqs": ["founder_ai_strategy"], "tags": ["leadership"]},
            {"id": "founder_ai_pitch", "title": "Pitching AI to Investors — What VCs Actually Care About", "prereqs": ["prod_moats", "prod_roi"], "tags": ["business"]},
            {"id": "founder_build_data_moat", "title": "Building a Data Moat — Flywheel, Network Effects, Proprietary Data", "prereqs": ["prod_moats", "prod_user_feedback"], "tags": ["strategy"]},
            {"id": "founder_ai_edviron", "title": "AI Opportunities at Edviron — Payment Intelligence, School Analytics, Smart Routing", "prereqs": ["ind_fintech_ai", "founder_ai_strategy"], "tags": ["edviron", "critical"]},
            {"id": "founder_compete", "title": "Competing in the AI Era — Defensibility When Everyone Has GPT-4", "prereqs": ["prod_moats", "founder_ai_strategy"], "tags": ["strategy"]},
            {"id": "founder_responsible", "title": "Responsible AI as a Founding Engineer — Ethics, Bias, Fairness", "prereqs": ["safe_misuse", "safe_compliance"], "tags": ["ethics"]},
        ],
    },

}

# ══════════════════════════════════════════════════════════════════════
# TRACK 2: FOUNDER ACADEMY — Leadership, Business, Product, Comm, Edviron
# ══════════════════════════════════════════════════════════════════════

FOUNDER_SECTIONS = {

    # ── SECTION 1: LEADERSHIP & MANAGEMENT ──────────────────────────
    "leadership": {
        "name": "Leadership & Management",
        "emoji": "👑",
        "order": 1,
        "goal": "You can build, lead, and scale an engineering team from 0 → 50.",
        "topics": [
            {"id": "lead_self_awareness", "title": "Self-Awareness & Leadership Style — Know Your Strengths & Blind Spots", "prereqs": [], "tags": ["foundations", "critical"]},
            {"id": "lead_one_on_ones", "title": "Running Effective 1-on-1s — Templates, Cadence, Difficult Conversations", "prereqs": ["lead_self_awareness"], "tags": ["management", "critical"]},
            {"id": "lead_feedback", "title": "Giving & Receiving Feedback — Radical Candor, SBI Framework, Growth Mindset", "prereqs": ["lead_one_on_ones"], "tags": ["management", "critical"]},
            {"id": "lead_hiring", "title": "Hiring Engineers — Job Descriptions, Interviews, Scorecards, Closing", "prereqs": ["lead_self_awareness"], "tags": ["hiring", "critical"]},
            {"id": "lead_interview_design", "title": "Designing Technical Interviews — System Design, Coding, Culture Fit", "prereqs": ["lead_hiring"], "tags": ["hiring"]},
            {"id": "lead_onboarding", "title": "Onboarding Engineers — 30-60-90 Plans, Buddy System, First PR in 48h", "prereqs": ["lead_hiring"], "tags": ["management"]},
            {"id": "lead_delegation", "title": "Delegation — What to Delegate, How, When to Step In, Manager vs Maker", "prereqs": ["lead_one_on_ones"], "tags": ["management", "critical"]},
            {"id": "lead_performance", "title": "Performance Management — Reviews, PIPs, Promotions, Calibration", "prereqs": ["lead_feedback"], "tags": ["management"]},
            {"id": "lead_conflict", "title": "Conflict Resolution — Disagreements, Difficult People, Healthy Debate", "prereqs": ["lead_feedback"], "tags": ["management"]},
            {"id": "lead_tech_vision", "title": "Setting Technical Vision — Architecture Principles, Tech Radar, ADRs", "prereqs": ["lead_self_awareness"], "tags": ["technical-leadership", "critical"]},
            {"id": "lead_without_authority", "title": "Leading Without Authority — Influence, Persuasion, Building Consensus", "prereqs": ["lead_tech_vision"], "tags": ["technical-leadership"]},
            {"id": "lead_team_culture", "title": "Building Engineering Culture — Blameless Postmortems, Psychological Safety", "prereqs": ["lead_conflict"], "tags": ["culture"]},
            {"id": "lead_team_scaling", "title": "Scaling Teams — 3 → 10 → 30 Engineers, Reorgs, Communication Patterns", "prereqs": ["lead_delegation", "lead_team_culture"], "tags": ["scaling", "critical"]},
            {"id": "lead_maker_manager", "title": "Maker vs Manager Schedule — Time Management for Tech Leaders", "prereqs": ["lead_delegation"], "tags": ["productivity"]},
            {"id": "lead_mentoring", "title": "Mentoring & Coaching Engineers — Growing Senior Engineers, Career Paths", "prereqs": ["lead_feedback", "lead_performance"], "tags": ["growth"]},
            {"id": "lead_exec_presence", "title": "Executive Presence — Board Meetings, C-Suite Communication, Gravitas", "prereqs": ["lead_without_authority"], "tags": ["communication", "critical"]},
            {"id": "lead_remote", "title": "Leading Remote & Hybrid Teams — Async Communication, Trust Building", "prereqs": ["lead_team_culture"], "tags": ["management"]},
            {"id": "lead_burnout", "title": "Managing Burnout — Yours & Your Team's, Sustainable Pace, Recovery", "prereqs": ["lead_self_awareness"], "tags": ["wellbeing"]},
            {"id": "lead_crisis", "title": "Crisis Leadership — When Things Go Wrong, Communication, Decision-Making", "prereqs": ["lead_exec_presence"], "tags": ["critical"]},
            {"id": "lead_founder_cto", "title": "Founder-CTO Playbook — What Changes at Each Stage (Seed → Series C)", "prereqs": ["lead_team_scaling", "lead_exec_presence"], "tags": ["strategy", "critical"]},
        ],
    },

    # ── SECTION 2: BUSINESS & STRATEGY ──────────────────────────────
    "business": {
        "name": "Business & Strategy",
        "emoji": "💼",
        "order": 2,
        "goal": "You understand how money works, how companies grow, and how to connect tech to business outcomes.",
        "topics": [
            {"id": "biz_unit_economics", "title": "Unit Economics — CAC, LTV, Payback, Contribution Margin", "prereqs": [], "tags": ["fundamentals", "critical"]},
            {"id": "biz_pnl", "title": "Reading a P&L — Revenue, COGS, Gross Margin, Burn Rate, Runway", "prereqs": ["biz_unit_economics"], "tags": ["fundamentals", "critical"]},
            {"id": "biz_financial_model", "title": "Building Financial Models — Revenue Forecasting, Scenario Analysis", "prereqs": ["biz_pnl"], "tags": ["practical"]},
            {"id": "biz_pricing", "title": "Pricing Strategy — Value-Based, Cost-Plus, Freemium, Per-Transaction", "prereqs": ["biz_unit_economics"], "tags": ["strategy", "critical"]},
            {"id": "biz_gtm", "title": "Go-to-Market Strategy — Sales Motions, Channel Strategy, PLG vs Sales-Led", "prereqs": ["biz_pricing"], "tags": ["strategy"]},
            {"id": "biz_fundraising", "title": "Fundraising — Term Sheets, Dilution, Valuation, VC Psychology", "prereqs": ["biz_pnl", "biz_financial_model"], "tags": ["fundraising", "critical"]},
            {"id": "biz_pitch_deck", "title": "Building a Pitch Deck — Story, Metrics, TAM, Competition, Ask", "prereqs": ["biz_fundraising"], "tags": ["fundraising"]},
            {"id": "biz_board_meetings", "title": "Board Meetings — Preparation, Presentation, Managing Board Dynamics", "prereqs": ["biz_fundraising"], "tags": ["governance"]},
            {"id": "biz_competitive", "title": "Competitive Analysis — Porter's Five Forces, SWOT, Moats, Defensibility", "prereqs": ["biz_gtm"], "tags": ["strategy"]},
            {"id": "biz_partnerships", "title": "Strategic Partnerships — BD, APIs as Distribution, Win-Win Deals", "prereqs": ["biz_competitive"], "tags": ["growth"]},
            {"id": "biz_marketplace", "title": "Marketplace & Platform Economics — Network Effects, Chicken-Egg, Take Rate", "prereqs": ["biz_unit_economics"], "tags": ["strategy"]},
            {"id": "biz_india_startup", "title": "Indian Startup Ecosystem — Regulations, Funding, Market Dynamics", "prereqs": ["biz_fundraising"], "tags": ["india"]},
            {"id": "biz_metrics_dashboard", "title": "Building a Metrics Dashboard — North Star, Leading vs Lagging, Dashboards", "prereqs": ["biz_unit_economics"], "tags": ["practical"]},
            {"id": "biz_negotiation", "title": "Negotiation — Vendor Deals, Partnerships, Salary, Term Sheets", "prereqs": [], "tags": ["skill"]},
            {"id": "biz_legal_basics", "title": "Legal Basics for Founders — Incorporation, ESOP, Contracts, IP", "prereqs": [], "tags": ["legal"]},
        ],
    },

    # ── SECTION 3: PRODUCT THINKING & UX ────────────────────────────
    "product": {
        "name": "Product Thinking & UX",
        "emoji": "🎨",
        "order": 3,
        "goal": "You can think like a PM, design features users love, and measure impact.",
        "topics": [
            {"id": "prod_think_frameworks", "title": "Product Thinking Frameworks — Jobs-to-be-Done, Kano Model, RICE", "prereqs": [], "tags": ["fundamentals", "critical"]},
            {"id": "prod_user_research", "title": "User Research — Customer Interviews, Surveys, Observation, Empathy Maps", "prereqs": ["prod_think_frameworks"], "tags": ["research", "critical"]},
            {"id": "prod_pmf", "title": "Product-Market Fit — How to Measure, How to Achieve, Sean Ellis Test", "prereqs": ["prod_user_research"], "tags": ["strategy", "critical"]},
            {"id": "prod_roadmap", "title": "Product Roadmap — Prioritization, Now/Next/Later, Stakeholder Alignment", "prereqs": ["prod_think_frameworks"], "tags": ["planning"]},
            {"id": "prod_user_stories", "title": "User Stories & Requirements — Writing Specs Engineers Love", "prereqs": ["prod_roadmap"], "tags": ["practical"]},
            {"id": "prod_ab_testing", "title": "A/B Testing — Hypothesis, Sample Size, Statistical Significance, Common Mistakes", "prereqs": ["prod_user_research"], "tags": ["measurement", "critical"]},
            {"id": "prod_metrics", "title": "Product Metrics — Funnels, Cohorts, Retention Curves, Activation", "prereqs": ["prod_ab_testing"], "tags": ["measurement"]},
            {"id": "prod_growth", "title": "Growth Engineering — Loops, Referrals, Activation Optimization, Viral Coefficients", "prereqs": ["prod_metrics"], "tags": ["growth"]},
            {"id": "prod_ux_principles", "title": "UX Principles for Engineers — Heuristics, Accessibility, Mobile-First", "prereqs": [], "tags": ["design"]},
            {"id": "prod_feature_flags", "title": "Feature Flags & Progressive Rollouts — Canary, Shadow Mode, Kill Switches", "prereqs": ["prod_roadmap"], "tags": ["practical", "critical"]},
            {"id": "fdr_prod_launch", "title": "Launching Features — GTM for Features, Rollout Plans, Rollback Strategy", "prereqs": ["prod_feature_flags"], "tags": ["practical"]},
            {"id": "prod_analytics_setup", "title": "Setting Up Analytics — Mixpanel, Amplitude, Custom Events, Data Pipelines", "prereqs": ["prod_metrics"], "tags": ["practical"]},
        ],
    },

    # ── SECTION 4: COMMUNICATION & WRITING ──────────────────────────
    "communication": {
        "name": "Communication & Writing",
        "emoji": "📝",
        "order": 4,
        "goal": "Your ideas get adopted because you communicate them brilliantly.",
        "topics": [
            {"id": "comm_rfc", "title": "Writing RFCs & Technical Proposals — Structure, Persuasion, Examples", "prereqs": [], "tags": ["writing", "critical"]},
            {"id": "comm_documentation", "title": "Writing Great Documentation — ADRs, Runbooks, API Docs, READMEs", "prereqs": ["comm_rfc"], "tags": ["writing"]},
            {"id": "comm_stakeholder", "title": "Communicating with Non-Technical Stakeholders — Translating Tech to Business", "prereqs": [], "tags": ["verbal", "critical"]},
            {"id": "comm_presentations", "title": "Technical Presentations — Demo Days, Tech Talks, Conference Talks", "prereqs": ["comm_stakeholder"], "tags": ["verbal"]},
            {"id": "comm_async", "title": "Async Communication Mastery — Slack, Email, PRs, Decision Docs", "prereqs": [], "tags": ["writing"]},
            {"id": "comm_status_updates", "title": "Status Updates & Reports — Weekly Updates, Incident Reports, Metrics", "prereqs": ["comm_async"], "tags": ["writing"]},
            {"id": "comm_storytelling", "title": "Storytelling for Engineers — Making Your Work Visible & Compelling", "prereqs": ["comm_presentations"], "tags": ["verbal", "critical"]},
            {"id": "comm_code_review", "title": "Code Review Communication — Giving Constructive Feedback on PRs", "prereqs": [], "tags": ["writing"]},
            {"id": "comm_investor_update", "title": "Writing Investor Updates — Monthly Updates That Build Confidence", "prereqs": ["comm_status_updates"], "tags": ["writing"]},
            {"id": "comm_personal_brand", "title": "Personal Brand for Engineers — Twitter, Blog, GitHub, LinkedIn", "prereqs": ["comm_storytelling"], "tags": ["growth"]},
        ],
    },

    # ── SECTION 5: EDVIRON MASTERY ──────────────────────────────────
    "edviron_mastery": {
        "name": "Edviron Deep Dive",
        "emoji": "🏫",
        "order": 5,
        "goal": "You understand Edviron's business, tech, and strategy better than anyone in the company.",
        "topics": [
            {"id": "edv_business_model", "title": "Edviron Business Model — Revenue Streams, Take Rate, Unit Economics", "prereqs": ["biz_unit_economics"], "tags": ["business", "critical"]},
            {"id": "edv_payment_flow", "title": "Edviron Payment Architecture — Every Service, Every Call, Every State", "prereqs": [], "tags": ["technical", "critical"]},
            {"id": "edv_competitive", "title": "Edviron Competitive Landscape — Who Competes, How We Win, Moats", "prereqs": ["biz_competitive"], "tags": ["strategy"]},
            {"id": "edv_regulatory", "title": "Edviron Regulatory Landscape — RBI PA License, PCI DSS, DPDP Act", "prereqs": [], "tags": ["compliance", "critical"]},
            {"id": "edv_school_economics", "title": "School Fee Collection Economics — Parent Behavior, Seasonal Patterns, Payment Methods", "prereqs": ["edv_business_model"], "tags": ["domain"]},
            {"id": "edv_trustee_model", "title": "Trustee Model Deep Dive — Commission Tiers, Settlement Flows, Conflicts", "prereqs": ["edv_business_model"], "tags": ["domain"]},
            {"id": "edv_growth_strategy", "title": "Edviron Growth Strategy — School Acquisition, Trustee Partnerships, Geographic Expansion", "prereqs": ["edv_competitive", "biz_gtm"], "tags": ["strategy", "critical"]},
            {"id": "edv_tech_roadmap", "title": "Edviron Technical Roadmap — What to Build Next, Architecture Evolution", "prereqs": ["edv_payment_flow"], "tags": ["technical"]},
            {"id": "edv_scaling_plan", "title": "Scaling Edviron 10x — Infrastructure, Team, Processes, Costs", "prereqs": ["edv_tech_roadmap", "lead_team_scaling"], "tags": ["scaling", "critical"]},
            {"id": "edv_crisis_scenarios", "title": "Edviron Crisis Scenarios — Payment Outage, Data Breach, Regulatory Action, Churn", "prereqs": ["edv_payment_flow", "lead_crisis"], "tags": ["risk"]},
            {"id": "edv_payment_infra", "title": "Building Payment Infrastructure — From Aggregator to Platform, White-Label PG, API-First Design", "prereqs": ["edv_payment_flow", "edv_tech_roadmap"], "tags": ["technical", "strategy", "critical"]},
            {"id": "edv_insurance_fees", "title": "Fee Insurance Product — Insuring School Fee Payments, Underwriting, Risk Models, Distribution", "prereqs": ["edv_business_model", "edv_school_economics"], "tags": ["business", "strategy", "critical"]},
            {"id": "edv_data_monetization", "title": "Data Monetization — Payment Data Analytics, Credit Scoring Schools, Risk Assessment", "prereqs": ["edv_payment_infra", "edv_insurance_fees"], "tags": ["strategy"]},
            {"id": "edv_embedded_finance", "title": "Embedded Finance Strategy — BNPL for Fees, Lending, Credit Lines for Schools", "prereqs": ["edv_insurance_fees", "edv_regulatory"], "tags": ["strategy", "critical"]},
            {"id": "edv_platform_play", "title": "Platform Play — From Payments to Ecosystem, Marketplace Dynamics, Network Effects", "prereqs": ["edv_data_monetization", "edv_embedded_finance"], "tags": ["strategy"]},
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════
# ALL SECTIONS COMBINED (for cross-track prereq lookups)
# ══════════════════════════════════════════════════════════════════════
ALL_SECTIONS = {**AI_SECTIONS, **FOUNDER_SECTIONS}

# ══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS — accept `sections` to work with either track
# ══════════════════════════════════════════════════════════════════════

def get_all_topics(sections: dict = None) -> list:
    """Return flat list of all topics with section info attached."""
    if sections is None:
        sections = ALL_SECTIONS
    all_topics = []
    for sec_key, sec in sorted(sections.items(), key=lambda x: x[1]["order"]):
        for t in sec["topics"]:
            all_topics.append({
                **t,
                "section_key": sec_key,
                "section_name": sec["name"],
                "section_emoji": sec["emoji"],
            })
    return all_topics


def get_all_topic_ids(sections: dict = None) -> set:
    """Return set of all topic IDs."""
    if sections is None:
        sections = ALL_SECTIONS
    return {t["id"] for sec in sections.values() for t in sec["topics"]}


def get_available_topics(studied: set, sections: dict = None) -> list:
    """Return topics whose prereqs are all satisfied but not yet studied."""
    # Prereqs can be cross-track, so always check against ALL studied topics
    available = []
    for t in get_all_topics(sections):
        if t["id"] in studied:
            continue
        if all(p in studied for p in t["prereqs"]):
            available.append(t)
    return available


def get_next_recommended(studied: set, recent_topics: list = None, sections: dict = None) -> list:
    """Smart recommendation: prioritize by section order, avoid recent, prefer critical tags."""
    if sections is None:
        sections = ALL_SECTIONS
    available = get_available_topics(studied, sections)
    if not available:
        return []

    recent_set = set(recent_topics or [])

    def score(t):
        s = 0
        sec = sections.get(t["section_key"], ALL_SECTIONS.get(t["section_key"], {"order": 99}))
        s -= sec["order"] * 10
        if "critical" in t.get("tags", []):
            s += 50
        if t["id"] in recent_set:
            s -= 100
        if "industry" in t.get("tags", []):
            s += 20
        if "practical" in t.get("tags", []):
            s += 15
        s += random.randint(0, 8)
        return s

    return sorted(available, key=score, reverse=True)


def get_section_progress(studied: set, sections: dict = None) -> list:
    """Return progress for each section."""
    if sections is None:
        sections = ALL_SECTIONS
    progress = []
    for sec_key, sec in sorted(sections.items(), key=lambda x: x[1]["order"]):
        total = len(sec["topics"])
        done = sum(1 for t in sec["topics"] if t["id"] in studied)
        progress.append({
            "key": sec_key,
            "name": sec["name"],
            "emoji": sec["emoji"],
            "goal": sec["goal"],
            "total": total,
            "done": done,
            "pct": (done / total * 100) if total > 0 else 0,
        })
    return progress


def get_topic_by_id(topic_id: str):
    """Look up a topic by ID — searches ALL sections (both tracks)."""
    for t in get_all_topics(ALL_SECTIONS):
        if t["id"] == topic_id:
            return t
    return None


def build_lesson_prompt(topic: dict, studied: set) -> str:
    """Build a mastery-level prompt — generates exhaustive, industry-grade lessons."""
    sec = ALL_SECTIONS[topic["section_key"]]

    prereq_titles = []
    for pid in topic["prereqs"]:
        pt = get_topic_by_id(pid)
        if pt:
            prereq_titles.append(pt["title"])

    studied_titles = []
    for sid in list(studied)[:25]:
        st_topic = get_topic_by_id(sid)
        if st_topic:
            studied_titles.append(st_topic["title"])

    tags = topic.get("tags", [])
    section_key = topic["section_key"]
    is_industry = "industry" in tags
    is_design = "design" in tags
    is_strategy = "strategy" in tags
    is_practical = "practical" in tags
    is_leadership = section_key == "leadership" or "management" in tags or "leadership" in tags
    is_communication = section_key == "communication" or "writing" in tags or "verbal" in tags
    is_edviron = section_key == "edviron_mastery" or "edviron" in tags
    is_product = section_key == "product" or "measurement" in tags
    is_business = section_key == "business" and not is_strategy
    is_hiring = "hiring" in tags

    # Determine lesson style based on section and tags
    if is_edviron:
        style_instruction = """
## LESSON STYLE: EDVIRON DEEP DIVE
This is an Edviron-specific lesson. You have full context about Edviron's architecture, business model, and codebase. Cover:
- **Current State** — What exists now in the codebase, how it works today (reference actual files, schemas, services)
- **Business Context** — Why this matters for Edviron specifically (school fee collection, trustee model, payment gateways)
- **Problems & Gaps** — What's broken, missing, or risky RIGHT NOW in the existing system
- **Ideal State** — What a well-architected version looks like
- **Competitive Context** — How competitors (PaySchool, FeePayy, InstaSmart) handle this
- **Regulatory Implications** — RBI PA License, PCI DSS, DPDP Act impacts
- **Action Plan** — Step-by-step plan a founding engineer would execute
- **Metrics to Track** — How to measure success
- **Case Study** — A real story from Indian fintech/edtech that's relevant

Be VERY specific to Edviron. Reference actual service names, schemas, and architecture decisions.
"""
    elif is_leadership:
        style_instruction = """
## LESSON STYLE: LEADERSHIP DEEP DIVE
This is a leadership/management lesson for a founding engineer building their first team. Cover:
- **Why This Matters NOW** — Connect to the founding engineer journey (going from 0 to 50 engineers)
- **Framework/Model** — The mental model (with clear diagrams in ASCII)
- **Step-by-Step Playbook** — Exact steps, scripts, templates you'd actually use
- **Real Conversations** — Example dialogues (what to say, what NOT to say)
- **Common Mistakes** — What first-time engineering leaders get wrong
- **Case Studies** — 3-4 real examples from tech companies (name CTOs, situations, outcomes)
- **Templates** — Actual templates (1-on-1 doc, review template, hiring scorecard, etc.)
- **Scaling Considerations** — How this changes at 5, 15, 50, 200 people
- **Self-Assessment** — Questions for the reader to evaluate themselves
- **Reading List** — 3-5 must-read books/articles on this topic

Include real scripts and templates. This should be IMMEDIATELY actionable.
"""
    elif is_communication:
        style_instruction = """
## LESSON STYLE: COMMUNICATION MASTERY
This is a communication/writing lesson. A founding engineer's effectiveness is 50% communication. Cover:
- **Why This Skill Matters** — How poor communication kills startups
- **Framework** — The structure/template for this type of communication
- **Full Example** — A complete, polished example (not a fragment — the FULL document/email/presentation)
- **Anti-Patterns** — Bad examples and why they fail
- **Before vs After** — Transform a bad version into a great one
- **Audience Analysis** — How to tailor for different audiences (board, engineers, customers)
- **Common Mistakes** — What engineers typically get wrong
- **Practice Exercise** — A scenario for the reader to practice
- **Templates** — Copy-pasteable templates they can use immediately
- **Pro Tips** — 5-7 tips from great communicators in tech

Include FULL examples, not fragments. The reader should be able to copy and adapt.
"""
    elif is_product:
        style_instruction = """
## LESSON STYLE: PRODUCT THINKING
This is a product thinking lesson. Founding engineers must think like PMs. Cover:
- **Product Context** — Why this skill is essential for founding engineers (not just PMs)
- **Framework** — The mental model or methodology (with visual diagrams)
- **Real-World Application** — Apply this to a real product (preferably a payments/edtech product)
- **Data-Driven Approach** — How to use data to make this decision (metrics, cohorts, funnels)
- **Tools & Platforms** — What tools the industry uses (with setup guides)
- **Case Studies** — 3-4 real examples from successful products
- **Common Mistakes** — What engineers-turned-PMs get wrong
- **Practical Exercise** — A scenario to practice this skill
- **Edviron Application** — How to apply this at Edviron specifically
- **Reading List** — Essential product thinking resources

Make this PRACTICAL. The reader should be able to apply this tomorrow.
"""
    elif is_business:
        style_instruction = """
## LESSON STYLE: BUSINESS ACUMEN
This is a business/finance lesson for a technical founder. Cover:
- **Why Engineers Must Know This** — Connect to founding engineer responsibilities
- **Core Concepts** — Explain from scratch (assume smart but no MBA)
- **Math & Formulas** — Every formula with worked examples using realistic numbers
- **Spreadsheet Walkthrough** — Step-by-step financial modeling (show the calculations)
- **Indian Startup Context** — How this works specifically in India (taxation, regulations, funding landscape)
- **Case Studies** — 3-4 real Indian/global startups (name companies, actual numbers)
- **Red Flags** — Warning signs that indicate problems in these metrics
- **Conversation Scripts** — How to discuss this with VCs, co-founders, board
- **Templates** — Financial model templates, pitch deck sections
- **Action Items** — What to do this week to improve your business acumen

Use REAL numbers from Indian startups. Reference actual funding rounds, revenue figures, and growth rates.
"""
    elif is_industry:
        style_instruction = """
## LESSON STYLE: INDUSTRY DEEP DIVE
This is an industry analysis lesson. Cover:
- **Company/Product Overview** — What they built, scale, users
- **Technical Architecture** — Actual system design, components, infra
- **AI/ML Stack** — Models used, training data, serving infrastructure
- **Key Engineering Decisions** — Why they chose this approach over alternatives
- **Numbers That Matter** — Latency, throughput, cost per request, accuracy, scale
- **Challenges They Faced** — What went wrong, how they fixed it
- **Lessons for a Founding Engineer** — What you'd steal for your own startup
- **How This Evolves** — Where this space is heading in 2025-2026

Reference real blog posts, papers, and talks. Name specific engineers and teams.
Mention actual model names, hardware, and cloud services used.
"""
    elif is_design:
        style_instruction = """
## LESSON STYLE: SYSTEM DESIGN
This is an AI system design lesson. Structure as:
- **Requirements** — Functional, non-functional, scale targets
- **High-Level Architecture** — Components, data flow (draw with ASCII art)
- **Deep Dive into Each Component** — Detailed design with tradeoffs
- **Model Selection** — Which models, why, fallback strategy
- **Data Pipeline** — How data flows from ingestion to serving
- **Latency & Cost Analysis** — P99 latency budget, cost per 1M requests
- **Failure Modes** — What breaks, monitoring, recovery
- **Scaling Strategy** — How to go from 100 to 100M users
- **Production Checklist** — What you need before going live

Include real numbers. Show calculations. Draw ASCII architecture diagrams.
"""
    elif is_strategy:
        style_instruction = """
## LESSON STYLE: STRATEGIC THINKING
This is a strategy/business lesson. Cover:
- **Market Context** — Current landscape, trends, players
- **Core Framework** — The mental model for thinking about this
- **Decision Framework** — How to actually make this decision in practice
- **Case Studies** — 3-4 real examples (name companies, outcomes, numbers)
- **Anti-Patterns** — What most startups get wrong
- **Founding Engineer Perspective** — How this affects your daily decisions
- **Action Items** — Concrete things to do in the next 30 days

Ground everything in real examples. No abstract theory without cases.
"""
    elif is_practical:
        style_instruction = """
## LESSON STYLE: HANDS-ON ENGINEERING
This is a practical engineering lesson. Emphasize:
- **Real Code** — Production-quality Python code, not toy examples
- **Step-by-Step Implementation** — Build it from scratch
- **Common Bugs** — Things that will bite you, with fixes
- **Production Considerations** — Error handling, logging, monitoring
- **Performance Benchmarks** — Actual numbers on real hardware
- **Tools & Libraries** — What the industry actually uses (with version numbers)
- **War Story** — A real production incident related to this topic

Every code snippet should be copy-pasteable and runnable.
"""
    else:
        style_instruction = """
## LESSON STYLE: DEEP TECHNICAL
This is a core technical lesson. Cover exhaustively:
- **Mathematical Foundation** — Full derivations, notation, proofs where needed
- **Intuition** — Analogies that make the math click
- **Implementation** — Python code from scratch, not just library calls
- **Visual Explanation** — ASCII diagrams, step-by-step examples with numbers
- **Historical Context** — Who invented this, why, what problem they solved
- **Modern Variants** — How this has evolved, latest improvements
- **Common Misconceptions** — Things people get wrong
- **Interview Angle** — How this shows up in ML/system design interviews
"""

    prompt = f"""Write an EXHAUSTIVE, mastery-level lesson article on:

# {topic['title']}

Section: {sec['emoji']} {sec['name']}
Section Goal: {sec['goal']}
Tags: {', '.join(topic.get('tags', []))}

{style_instruction}

## UNIVERSAL REQUIREMENTS (EVERY LESSON MUST HAVE):

1. **WHY THIS MATTERS** — Start with a compelling hook. Why should a founding engineer at a payments/edtech startup care about this? Connect to real business impact.

2. **COMPLETE CONCEPT COVERAGE** — Cover EVERY sub-concept exhaustively. Don't skip anything. If there are 5 approaches, cover all 5. If there's math, derive it fully. If there are variants, compare them all.

3. **REAL CODE** — Include production-quality Python code. Not pseudocode. Not toy examples. Real, runnable code that demonstrates the concept.

4. **REAL NUMBERS** — Include actual benchmarks, latency numbers, costs, accuracy figures. "Fast" and "good" are not numbers.

5. **INDUSTRY CONTEXT** — How does the industry actually use this RIGHT NOW (2025-2026)? Name companies. Name products. Name models.

6. **TRADEOFFS TABLE** — For any decision point, show a comparison table:
   | Approach | Pros | Cons | When to Use |
   |----------|------|------|-------------|

7. **REALISTIC USE CASE** — End with a detailed, realistic scenario:
   - Specific company/product (can be fictional but realistic)
   - Architecture decisions with justifications
   - Numbers: users, QPS, latency, cost
   - What went wrong and how they fixed it

8. **KEY TAKEAWAYS** — 7-10 crisp bullet points — things to REMEMBER

9. **WHAT TO STUDY NEXT** — Connect to the next topics in the curriculum

## STUDENT CONTEXT:
Prerequisites completed: {', '.join(prereq_titles) if prereq_titles else 'Foundational topic — explain from scratch'}
Other topics studied: {', '.join(studied_titles[:15]) if studied_titles else 'Just beginning'}

## QUALITY BAR:
- This should feel like reading a SENIOR STAFF ENGINEER'S personal notes — dense, opinionated, practical
- Length: 2000-3000 words minimum. Don't hold back.
- If something is "well-known", still explain it — the student should learn EVERYTHING from this single lesson
- Bold **key terms** on first use
- Use headers (##, ###) to organize
- Code blocks with language tags
- Tables for comparisons
- This lesson should make the reader feel like they DEEPLY understand the topic — not just "aware of" it"""

    return prompt


# Total counts for display
AI_TOTAL_TOPICS = sum(len(s["topics"]) for s in AI_SECTIONS.values())
AI_TOTAL_SECTIONS = len(AI_SECTIONS)
FOUNDER_TOTAL_TOPICS = sum(len(s["topics"]) for s in FOUNDER_SECTIONS.values())
FOUNDER_TOTAL_SECTIONS = len(FOUNDER_SECTIONS)
TOTAL_TOPICS = AI_TOTAL_TOPICS + FOUNDER_TOTAL_TOPICS
TOTAL_SECTIONS = AI_TOTAL_SECTIONS + FOUNDER_TOTAL_SECTIONS
