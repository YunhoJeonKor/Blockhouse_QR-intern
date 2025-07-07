This is Yunho Jeon (yj3258@nyu.edu), currently studying Mathematics in Finance at NYU.

I have constructed the required Order Flow Imbalance (OFI) features based on the given dataset.
All computations are performed with a time interval of 10 seconds, and the resulting features are provided in the file ofi_features_output.csv.

⸻

 Constructed Features

1. Best-Level OFI
	•	This feature captures the order flow imbalance at the best bid and ask levels (level 0).
	•	It is computed at each 10-second timestamp and is saved under the column best_level_ofi.

2. Multi-Level OFI
	•	This feature accounts for OFI values across deeper levels of the order book.
	•	For levels 0 through 9, the columns deep_ofi_0 to deep_ofi_9 are created, each representing OFI at that specific level.

3. Integrated OFI
	•	Following the methodology described in the paper, this feature aggregates the multi-level OFIs into a single measure.
	•	It is provided under the column integrated_ofi and reflects a more comprehensive imbalance by integrating depth information.

⸻

💬 Remarks

The original paper also discusses cross-asset OFI as an extension. However, the dataset I was given only includes order book data for Apple stock.
Therefore, implementing cross-asset OFI was not feasible in this case. Despite that, I closely followed the feature construction methodology as outlined in the paper to ensure consistency and validity.


<p align="center">
  <img width="400" alt="OFI screenshot from paper" src="https://github.com/user-attachments/assets/cc9eb8b7-76ca-4d69-93da-d46055682182" />
</p>

Moreover, as shown in the paper through the included screenshot, the next step is to calculate OFI-based beta values and test their predictive power using techniques such as Lasso regression and other regularization methods.
This lays the groundwork for further empirical analysis and robust model building.
