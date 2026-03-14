### NASA Urinalysis / Spaceflight Health Monitoring Data Resources

| Resource / Dataset                                        | Source Organization                                 | Type of Data                    | What It Contains                                                                                                                                                                  | Availability        | Why It Matters for the Project                                                         |
| --------------------------------------------------------- | --------------------------------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| OSD-656 – Inspiration4 Urine Inflammation Panel           | NASA Open Science Data Repository (OSDR)            | Urine biomarker dataset         | Multiplex inflammation / immune markers measured in urine samples from Inspiration4 crew; metadata and processed tables                                                           | Public              | Most feasible dataset for a first ML prototype because it is fully open and structured |
| OSD-343 – Astronaut Metabolomics Study                    | NASA OSDR                                           | Metabolomics (urine + blood)    | Metabolic biomarkers associated with spaceflight physiology; includes Twins Study related work                                                                                    | Public              | Useful for modeling physiological adaptation to spaceflight                            |
| OS-571 – Bed Rest Analog Study                            | NASA OSDR                                           | Urinary biomarker data          | Urine calcium and hydroxyproline changes in microgravity analog bed-rest studies                                                                                                  | Public              | Helps simulate microgravity physiology for early model training                        |
| OS-586 – Bed Rest Analog Study                            | NASA OSDR                                           | Urinary metabolic markers       | Additional analog experiment measuring urinary changes under long-term bed rest                                                                                                   | Public              | Useful for training models on spaceflight-like physiological changes                   |
| LSAH Astronaut Urine Chemistry Dataset (Request ID 10658) | NASA Life Sciences Data Archive (LSAH)              | Clinical urine chemistry        | 1,517 urine samples from 581 astronauts; chemistry variables include calcium, oxalate, citrate, magnesium, uric acid, sulfate, phosphate, sodium, potassium, urine volume, and pH | Controlled access   | Closest dataset to real astronaut urinalysis monitoring                                |
| Spaceflight Standard Measures Dataset                     | NASA Life Sciences Portal (NLSP)                    | Clinical monitoring data        | Blood and urine chemistry collected before and after space missions; currently includes ~31 ISS crewmembers                                                                       | Controlled access   | Represents NASA’s operational astronaut health monitoring framework                    |
| NASA OCHMO-STD-100.1A Medical Standard                    | NASA Office of the Chief Health and Medical Officer | Medical standards documentation | Defines routine astronaut urinalysis parameters such as specific gravity, glucose, protein, pH, ketones, blood, microscopic exam                                                  | Public              | Provides the clinical schema for what urine analysis should monitor                    |
| MR089S Annual Astronaut Medical Exams                     | NASA Life Sciences Archive                          | Medical workflow documentation  | Explains how astronaut lab results are processed through CLIMS and stored in EMR systems                                                                                          | Public              | Shows how a monitoring system should report and store results                          |
| NASA Twins Study Publications                             | NASA / academic collaborations                      | Multi-omics biological data     | Includes urine and blood biomarkers measuring long-term physiological changes during spaceflight                                                                                  | Public (aggregated) | Provides physiological context for astronaut health models                             |
| NASA Open Science Data Repository (OSDR) API              | NASA OSDR                                           | Data infrastructure             | Programmatic access to datasets, metadata, and experiment records                                                                                                                 | Public              | Enables automated ingestion pipelines for ML experiments                               |

---

### Data Accessibility Assessment (March 2026)

After researching each dataset, the following practical notes should guide the ML team's planning:

**Public and downloadable now:**
- **OSD-656** and **OSD-571** (Inspiration4): Available at osdr.nasa.gov. However, these contain data from only **4 crew members** across 9 timepoints. Useful for building and testing the pipeline end-to-end, but too small (n=4) for meaningful supervised model training or accuracy claims.

**Access unclear or restricted:**
- **OSD-343**: Returned a 403 (forbidden) error when accessed via OSDR. May be restricted or not yet publicly released. Needs manual verification with NASA OSDR support.
- **OSD-586**: Could not be located in public OSDR listings or related publications. May not exist publicly or may be under a different identifier.

**Controlled access (formal application required):**
- **LSAH (Request ID 10658)**: The only dataset with sufficient sample size for ML (1,517 samples, 581 astronauts) and the exact urine chemistry variables we need. Access requires: (1) university IRB approval, (2) formal NASA data request via nlsp.nasa.gov, (3) review by an LSAH Epidemiologist, and potentially (4) LSAH Advisory Board approval. Estimated timeline: **4–6 months**. The PI should initiate this request as early as possible in Phase 1.

**Action items for the ML team:**
1. **Immediately**: Begin LSAH data request process through PI (Jai) — this is the critical-path item for the ML work stream.
2. **Phase 1 fallback**: Build the full ML pipeline using OSD-656/571 data (n=4) to prove the architecture works end-to-end.
3. **Supplemental data**: Investigate non-NASA public urinalysis/kidney stone datasets (e.g., UCI ML Repository, Kaggle, PhysioNet) that may contain hundreds of samples with overlapping analytes (calcium, creatinine, pH, etc.) to bridge the gap if LSAH access is delayed.
4. **Synthetic data option**: Generate synthetic urine chemistry samples based on published population distributions from NASA literature as a training data augmentation strategy.

---

### Recap of What These Resources Represent

The resources above fall into **three categories**, which helps clarify the technical strategy for the project.

The first category is **fully public datasets**. These include the OSDR datasets such as **OSD-656**, **OSD-343**, and the bed-rest analog experiments. These are the most practical starting points for building the first prototype because they can be downloaded immediately and already contain structured biological measurements. While they do not always resemble standard clinical urinalysis panels, they contain urine-derived biomarkers that still reflect physiological changes caused by spaceflight or simulated microgravity.

The second category is **controlled astronaut health datasets**. The most relevant example is the **LSAH astronaut urine chemistry dataset**, which contains thousands of astronaut urine samples with clinically meaningful chemistry markers such as calcium, citrate, and oxalate. This dataset is highly valuable because it directly reflects the kinds of measurements used to monitor astronaut kidney stone risk and fluid balance. However, because these data involve identifiable astronaut health records, they are usually accessed through formal requests rather than open downloads.

The third category is **medical standards and operational workflow documents**. These include NASA’s medical standards such as **OCHMO-STD-100.1A** and the **MR089S astronaut medical exam documentation**. These resources do not provide datasets themselves but define how urinalysis is interpreted and integrated into NASA’s health monitoring infrastructure. For example, they specify the clinical variables typically measured in astronaut urine samples and describe how laboratory results move from the clinical laboratory system into the astronaut electronic medical record.

Understanding these three categories is important because they correspond to the **three major components of the machine learning system** that the team might eventually build. Public datasets allow the team to train early models and explore features. Controlled datasets provide the opportunity to validate models against real astronaut clinical data. Medical standards determine how the model’s outputs should be structured so that the system integrates into an operational monitoring workflow.

From a project planning perspective, the **most feasible first step** is to begin with the public OSDR datasets. These datasets will allow the team to build the full machine learning pipeline: data ingestion, preprocessing, feature engineering, model training, anomaly detection, and structured reporting. Once that pipeline exists, it can later be adapted to more clinically meaningful datasets if access becomes available.

Another key insight from reviewing these resources is that astronaut urinalysis monitoring is rarely a single measurement problem. Instead, it is a **longitudinal monitoring problem**. Astronauts are often evaluated across multiple phases of a mission: pre-flight baseline, in-flight physiological adaptation, and post-flight recovery. This means the most natural machine learning framing may not be simple classification but rather **change detection relative to baseline physiology**.

In practical terms, the system we are envisioning would likely follow a pipeline similar to the following: urine biomarker measurements are collected and stored in a dataset; the machine learning model analyzes patterns and deviations relative to expected ranges or individual baselines; the model then produces an interpretable output such as an anomaly score, risk indicator, or health monitoring summary. That output would ideally be formatted in a way that resembles the reporting logic used in NASA’s health monitoring systems.

From a strategic standpoint, the most realistic path for the next nine months is to build a prototype that demonstrates the entire workflow—from raw urine measurements to health-monitoring insights—using publicly available data first. Once the pipeline exists, more sophisticated datasets can be integrated without redesigning the architecture.

Two important planning questions remain that will influence the entire design of the project:

First, should the prototype emphasize **physiological interpretation** (for example detecting kidney stone risk or hydration imbalance), or should it emphasize **general anomaly detection** in astronaut biomarker profiles?

Second, should the final prototype aim to be **a predictive ML model**, or should it function more like **an intelligent monitoring and reporting system** that assists human medical reviewers?

The answers to those questions will determine whether the project emphasizes biomedical modeling, clinical risk prediction, or health monitoring infrastructure.
