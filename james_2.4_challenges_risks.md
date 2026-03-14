2.4 Key Technical Challenges & Risks

The following identifies the major technical challenges and risks facing the ML/computation work stream of IMULAS, along with their assessed probability, impact, and mitigation strategies.

Training data scarcity — publicly available spaceflight urine datasets contain only 4 crew members (OSD-656/571), far below the sample size needed for robust supervised learning. Probability: High. Impact: High. Mitigation: Build the full ML pipeline on small public datasets to validate architecture end-to-end; supplement with non-NASA public urinalysis datasets (e.g., UCI ML Repository, Kaggle, PhysioNet) containing overlapping analytes; generate synthetic urine chemistry samples based on published population distributions from NASA literature.

LSAH dataset access delayed beyond Phase 1 — the controlled-access LSAH dataset (1,517 samples, 581 astronauts) requires IRB approval, formal NASA data request, and advisory board review with an estimated 4–6 month timeline. Probability: Medium. Impact: High. Mitigation: Initiate the LSAH data request as early as possible in Phase 1 through the PI; design the pipeline to be dataset-agnostic so it can ingest LSAH data as a drop-in replacement when access is granted; use OSD-656/571 and supplemental datasets as interim training data.

ML model fails to achieve statistically significant classification performance — the model's health classifications may not outperform random chance due to limited or noisy training data. Probability: Medium. Impact: High. Mitigation: Evaluate each architecture (MLP, CNN, Transformer) against a null hypothesis with statistical significance assessed at p < 0.05; if significance is not achieved, revisit feature engineering, analyte ratio construction, and data augmentation strategies before advancing architectures; retain the option to fall back to simpler rule-based anomaly detection.

Overfitting on small datasets — with limited training samples, models may memorize training data rather than learning generalizable biomarker patterns. Probability: High. Impact: Medium. Mitigation: Apply k-fold cross-validation, L2 regularization, and dropout during training; use data augmentation (synthetic samples, noise injection) to expand effective training set size; monitor validation loss divergence as an early stopping criterion.

Embedded deployment constraints — the final model must run on a resource-constrained onboard processor with limited memory and compute budget. Probability: Low. Impact: Medium. Mitigation: Prioritize lightweight architectures (MLP) as the baseline; apply model compression techniques (quantization, pruning) if CNN or Transformer is selected; benchmark inference latency on target hardware during Phase 3 integration testing.

Note: Hardware-specific risks (e.g., microgravity fluidic behavior, sensor electrode fouling, power budget constraints) are to be completed by the hardware team.
