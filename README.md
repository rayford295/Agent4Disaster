# RAPID: A Reproducible Multi-Agent Pipeline for Interpretable Disaster Damage Assessment from Satellite and Street-View Imagery

<p align="center">
  <a href="https://arxiv.org/abs/XXXX.XXXXX"><img src="https://img.shields.io/badge/arXiv-RAPID-b31b1b.svg" alt="arXiv"/></a>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"/>
  <img src="https://img.shields.io/badge/Python-3.8+-green.svg" alt="Python"/>
  <img src="https://img.shields.io/badge/Zero--Shot-Multi--Agent-orange.svg" alt="Zero-Shot"/>
</p>


---

## Abstract

With the increasing frequency and intensity of extreme climate events, there is a growing demand for intelligent, scalable, and autonomous approaches to disaster damage assessment. Existing methods, largely based on supervised learning and task-specific fine-tuning, struggle to generalize under domain shifts, long-tailed data distributions, and heterogeneous geospatial data sources. This paper introduces **RAPID**, an autonomous multi-agent pipeline for interpretable disaster damage assessment — encompassing the assessment of damage levels, interpretation of damage types and degrees, and generation of actionable suggestions for response, remediation, and recovery.

Unlike conventional approaches that rely on single-task supervised models, RAPID coordinates multiple specialized agents to perform cross-view understanding, image restoration, structured damage recognition, and geographical reasoning across heterogeneous data modalities. Without task-specific fine-tuning, RAPID supports **zero-shot damage assessment** by jointly leveraging complementary information from remote sensing and ground-level perspectives. Experiments show that RAPID achieves an overall accuracy of **0.92** on multi-disaster type classification and up to **0.627** on cross-view damage severity prediction.

**Keywords:** Disaster Assessment · Vision-Language Models · Cross-View Imagery · Zero-Shot Learning · Multi-Agent Pipeline

---

## Overview

<p align="center">
  <img src="https://github.com/rayford295/GeoAgent4Disaster/blob/main/figure/proposed%20framework.drawio.png" width="88%"/>
</p>
<p align="center"><i>Figure 1. RAPID: An Autonomous Multi-Agent Framework for Disaster Damage Intelligence</i></p>

RAPID addresses three core research questions:

- **RQ1** — How can an autonomous multi-agent pipeline achieve multimodal disaster understanding across different geospatial data sources *without* task-specific fine-tuning, while maintaining robustness under domain shifts?
- **RQ2** — How can multiple agents efficiently coordinate perception, data restoration, damage recognition, and reasoning to generate structured, interpretable assessment results?
- **RQ3** — To what extent can such a system automatically produce location-specific and decision-relevant disaster intelligence, and what are its strengths and limitations in supporting real-world disaster assessment?

---

## Pipeline

The framework comprises **four collaborative specialized agents** coordinated through task decomposition:

| Agent | Abbreviation | Core Role | Key Output |
|-------|-------------|-----------|------------|
| **Disaster Perception Agent** | DPA | Zero-shot identification of disaster type, image modality, and structural context; plans the downstream workflow | Disaster label + confidence score + task plan |
| **Image Restoration Agent** | IRA | Diagnoses image quality issues (blur, haze, low-light) in SVI/RSI; applies constrained enhancement strategies to preserve disaster-relevant visual evidence | Restored imagery + quality score (Q) |
| **Damage Recognition Agent** | DRA | Structured damage diagnosis across cross-view and bi-temporal settings; severity classification without task-specific fine-tuning | Severity label · object-level indicators · confidence scores |
| **Disaster Reasoning Agent** | DReA | High-level cognitive synthesis; causal interpretation, recovery recommendations, and structured disaster report generation | Decision-relevant disaster report |

### Agent Details

**Disaster Perception Agent (DPA)** comprises three modules: *ModePerceiver* (zero-shot image mode + disaster type recognition), *DisasterReasoner* (natural-language scene explanation with visual evidence), and *TaskPlanner* (downstream agent orchestration).

**Image Restoration Agent (IRA)** evaluates three restoration branches — heuristic baseline, Gemini-guided planner, and image-only Gemini enhancement — and accepts a branch output only when the composite quality score Q (combining contrast, sharpness, and NIQE-proxy) improves beyond a preset margin over the original.

**Damage Recognition Agent (DRA)** operates through four complementary tasks: (1) cross-view hurricane damage prediction from paired RSI+SVI, (2) bi-temporal visual change analysis from pre/post SVI, (3) wildfire-specific five-level classification, and (4) object-level detection + instance segmentation for spatial damage characterization. Evaluated with both standard metrics and the severity-aware **Normalized Cross-Severity Error (NCSE)**:

$$\text{NCSE} = \frac{1}{N}\sum_{i=1}^{N}\frac{\left|y_i - \hat{y}_i\right|}{K-1}$$

**Disaster Reasoning Agent (DReA)** ingests structured JSON outputs from DRA and applies templated chain-of-thought reasoning to generate causal explanations, secondary risk assessments, and FEMA-guideline-aligned recovery recommendations — evaluated by both LLM-based and human expert scoring across factual consistency, causal plausibility, information completeness, and actionability.

---

## Datasets

RAPID is evaluated across three complementary multimodal disaster dataset categories, covering cross-view, bi-temporal, and multi-hazard scenarios:

| Dataset | Data Type | Images | Disaster | Severity | Source | Agents |
|---------|-----------|--------|----------|----------|--------|--------|
| **A** | SVI + RSI pairs | 300 | Hurricane | 3 levels | CVDisaster (Li et al., 2025) | DPA · IRA · DRA · DReA |
| **B** | Bi-temporal SVI | 300 | Hurricane | 3 levels | BiTemporal (Yang et al., 2025) | DPA · IRA · DRA · DReA |
| **C1** | Post-disaster SVI | 188 | Drought / Earthquake / Flood / Ice Storm / Wildfire | N/A | Incidents Dataset (Weber et al., 2020) | DPA |
| **C2** | Post-disaster SVI | 295 | Wildfire | 5 levels | LA DINS (2025) | DPA · DRA |

Geographic coverage spans California and Florida, USA. Dataset A and B each contain 150 image pairs; Dataset C totals 483 images across diverse hazard types.

| Geolocation Distribution | Dataset Statistics |
|:---:|:---:|
| <img src="https://github.com/rayford295/GeoAgent4Disaster/blob/main/figure/geolocation.png" width="340"/> | <img src="https://github.com/rayford295/GeoAgent4Disaster/blob/main/figure/stastics.png" width="340"/> |

---

## Results

### Disaster Perception Agent — Multi-Disaster Type Classification

| Model | Overall Accuracy |
|-------|-----------------|
| GPT-5-mini | **0.92** |
| GPT-5.1 | 0.88 |
| Gemini-2.5-flash | 0.86 |

### Image Restoration Agent — Visual Quality Enhancement

Restoration consistently improves quality scores across all disaster types and image modalities. Representative results:

| Category | Image Type | Q_original | Q_baseline | Q_planner | Q_gemini |
|----------|-----------|-----------|-----------|----------|---------|
| Dataset A — Hurricane | Satellite | 0.62 | **0.73** | 0.71 | 0.69 |
| Dataset A — Hurricane | SVI | 0.75 | 0.78 | 0.76 | **0.79** |
| Dataset B — Hurricane | SVI | 0.76 | 0.78 | 0.78 | **0.79** |

### Damage Recognition Agent — Severity Prediction

| Model | Dataset A Accuracy | Dataset B Accuracy | Dataset C Accuracy |
|-------|-------------------|-------------------|-------------------|
| Gemini-3-Pro | **0.627** | 0.493 | 0.442 |
| GPT-5.1 | 0.573 | **0.591** | 0.570 |
| GPT-5-mini | 0.387 | 0.503 | **0.573** |

Errors concentrate at adjacent severity levels, validating the role of NCSE as a more sensitive evaluation metric.

### Disaster Reasoning Agent — Report Quality

<p align="center">
  <img src="https://github.com/rayford295/Agent4Disaster/blob/main/figure/reasoning_RESULTs.drawio.png" width="82%"/>
</p>
<p align="center"><i>LLM-based and human evaluation of multimodal disaster reasoning across Gemini-3-Pro, Gemini-2.5-Pro, and GPT-5.1</i></p>

### Example Outputs

| LLM-Based Object Detection | Final Structured Report |
|:---:|:---:|
| <img src="https://github.com/rayford295/GeoAgent4Disaster/blob/main/figure/example-llm-object%20detection.drawio.png" width="340"/> | <img src="https://github.com/rayford295/GeoAgent4Disaster/blob/main/figure/final%20output.png" width="340"/> |

---

## Repository Structure

```
RAPID/
├── Disaster Perception Agent/
│   ├── DisasterPerceptionAgent.py       # ModePerceiver + DisasterReasoner + TaskPlanner
│   └── Prompt--Disaster Perception Agent
├── Image Restoration Agent/
│   ├── test.py                          # IQA diagnosis + 3-branch restoration
│   └── Prompt--Image Restoration Agent
├── Damage Recognition Agent/
│   ├── SVI&RSI.py                       # Cross-view hurricane (Dataset A)
│   ├── SVI-pre&post.py                  # Bi-temporal street-view (Dataset B)
│   ├── SVI-wildfire.py                  # Wildfire severity (Dataset C2)
│   ├── zero_shot_object_detection_Agent3.ipynb
│   └── Prompt--Damage Recognition Agent
├── Disaster Reasoning Agent/
│   ├── Large Language Model-based evaluation.py
│   ├── test.py                          # Report generation + evaluation
│   └── Prompt--Disaster Reasoning Agent
└── figure/
```

---

## Citation


---

## Contact

**Yifan Yang** — Department of Geography, Texas A&M University  
[yyang295@tamu.edu](mailto:yyang295@tamu.edu) · [rayford295.github.io](https://rayford295.github.io)

**Lei Zou** *(Corresponding)* — Department of Geography, Texas A&M University  
[lzou@tamu.edu](mailto:lzou@tamu.edu)
