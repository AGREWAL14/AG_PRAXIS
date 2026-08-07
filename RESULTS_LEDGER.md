# AG_PRAXIS — Results Ledger

Append only. Every run that is a result is entered here, including the runs that made
things worse. A correction is a new entry, never an edit to an old one.

### NB05 — baseline models (2026-08-04)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| run date | 2026-08-04 |
| git sha | 15b46f4 |
| seed | 42 |
| pass reported | full |
| runs | 7, of which 1 were read back from an earlier session |
| runtime | fast 0.0 min, full 303.0 min |
| features | 44, after dropping Drate |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05 |
| status | reference run |

| run | model | task | split | accuracy | weighted F1 | macro F1 | gap |
|---|---|---|---|---|---|---|---|
| ours_cnn_19class | mohammadi_cnn | 19-class | two_tier | 0.9852 | 0.9831 | 0.7356 | 0.2474 |
| published_cnn_19class | mohammadi_cnn | 19-class | shipped | 0.9863 | 0.9840 | 0.7110 | 0.2730 |
| forest_19class | random_forest | 19-class | two_tier | 0.9923 | 0.9906 | 0.8418 | 0.1488 |
| ours_cnn_6class | mohammadi_cnn | 6-class | two_tier | 0.9945 | 0.9947 | 0.9006 | 0.0941 |
| published_cnn_6class | mohammadi_cnn | 6-class | shipped | 0.9929 | 0.9931 | 0.8786 | 0.1145 |
| forest_6class | random_forest | 6-class | two_tier | 0.9980 | 0.9980 | 0.9681 | 0.0299 |
| published_cnn_2class | mohammadi_cnn | 2-class | shipped | 0.9968 | 0.9968 | 0.9651 | 0.0317 |

### NB05 — ours_cnn_19class (2026-08-04)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| git sha | 15b46f4 |
| seed | 42 |
| written | 1 of 7 |
| model | mohammadi_cnn |
| task | 19-class, 19 classes |
| split | two_tier |
| parent | published_cnn_19class |
| the one change | split |
| training rows | 6,228,288 |
| test rows | 1,229,711 |
| accuracy | 0.9852 (chance 0.0526, largest class 0.1591) |
| weighted P / R / F1 | 0.9877 / 0.9852 / 0.9831 |
| macro P / R / F1 | 0.8384 / 0.7497 / 0.7356 |
| weighted F1 minus macro F1 | 0.2474 |
| cross-validation | none |
| classes at F1 0.00 | none |
| four weakest classes | Recon-VulScan 0.01, Recon-OS_Scan 0.05, MQTT-DDoS-Publish_Flood 0.09, MQTT-Malformed_Data 0.40 |
| train seconds | 3,890.4 |
| inference seconds | 3.8 (322,794 rows/s) |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/ours_cnn_19class |
| status | reference run |


### NB05 — published_cnn_19class (2026-08-04)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| git sha | 15b46f4 |
| seed | 42 |
| written | 2 of 7 |
| model | mohammadi_cnn |
| task | 19-class, 19 classes |
| split | shipped |
| parent | none, this is where the chain starts |
| the one change | none, root configuration |
| training rows | 7,160,831 |
| test rows | 1,614,182 |
| accuracy | 0.9863 (chance 0.0526, largest class 0.2243) |
| weighted P / R / F1 | 0.9887 / 0.9863 / 0.9840 |
| macro P / R / F1 | 0.8615 / 0.7252 / 0.7110 |
| weighted F1 minus macro F1 | 0.2730 |
| cross-validation | none |
| classes at F1 0.00 | Recon-VulScan |
| four weakest classes | Recon-VulScan 0.00, Recon-Ping_Sweep 0.01, Recon-OS_Scan 0.03, MQTT-DDoS-Publish_Flood 0.19 |
| train seconds | 4,391.7 |
| inference seconds | 5.3 (304,930 rows/s) |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/published_cnn_19class |
| status | reference run |


### NB05 — forest_19class (2026-08-04)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| git sha | 15b46f4 |
| seed | 42 |
| written | 3 of 7 |
| model | random_forest |
| task | 19-class, 19 classes |
| split | two_tier |
| parent | none, this is where the chain starts |
| the one change | none, root configuration |
| training rows | 999,998 |
| test rows | 1,229,711 |
| accuracy | 0.9923 (chance 0.0526, largest class 0.1591) |
| weighted P / R / F1 | 0.9937 / 0.9923 / 0.9906 |
| macro P / R / F1 | 0.9603 / 0.8225 / 0.8418 |
| weighted F1 minus macro F1 | 0.1488 |
| cross-validation | 5-fold on training, macro-F1 0.8958 +/- 0.0049 |
| classes at F1 0.00 | none |
| four weakest classes | MQTT-DDoS-Publish_Flood 0.12, Recon-VulScan 0.25, MQTT-Malformed_Data 0.68, Recon-Ping_Sweep 0.69 |
| train seconds | 21.2 |
| inference seconds | 12.3 (99,905 rows/s) |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/forest_19class |
| status | reference run |


### NB05 — ours_cnn_6class (2026-08-04)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| git sha | 15b46f4 |
| seed | 42 |
| written | 4 of 7 |
| model | mohammadi_cnn |
| task | 6-class, 6 classes |
| split | two_tier |
| parent | ours_cnn_19class |
| the one change | task |
| training rows | 6,228,288 |
| test rows | 1,229,711 |
| accuracy | 0.9945 (chance 0.1667, largest class 0.5750) |
| weighted P / R / F1 | 0.9950 / 0.9945 / 0.9947 |
| macro P / R / F1 | 0.8942 / 0.9116 / 0.9006 |
| weighted F1 minus macro F1 | 0.0941 |
| cross-validation | none |
| classes at F1 0.00 | none |
| four weakest classes | Spoofing 0.54, Benign 0.93, Recon 0.94, MQTT 0.99 |
| train seconds | 3,857.8 |
| inference seconds | 2.4 (505,255 rows/s) |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/ours_cnn_6class |
| status | reference run |


### NB05 — published_cnn_6class (2026-08-04)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| git sha | 15b46f4 |
| seed | 42 |
| written | 5 of 7 |
| model | mohammadi_cnn |
| task | 6-class, 6 classes |
| split | shipped |
| parent | published_cnn_19class |
| the one change | task |
| training rows | 7,160,831 |
| test rows | 1,614,182 |
| accuracy | 0.9929 (chance 0.1667, largest class 0.6609) |
| weighted P / R / F1 | 0.9934 / 0.9929 / 0.9931 |
| macro P / R / F1 | 0.8704 / 0.8933 / 0.8786 |
| weighted F1 minus macro F1 | 0.1145 |
| cross-validation | none |
| classes at F1 0.00 | none |
| four weakest classes | Spoofing 0.41, Benign 0.93, Recon 0.95, MQTT 0.99 |
| train seconds | 4,748.2 |
| inference seconds | 2.4 (678,054 rows/s) |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/published_cnn_6class |
| status | reference run |


### NB05 — forest_6class (2026-08-04)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| git sha | 15b46f4 |
| seed | 42 |
| written | 6 of 7 |
| model | random_forest |
| task | 6-class, 6 classes |
| split | two_tier |
| parent | forest_19class |
| the one change | task |
| training rows | 999,998 |
| test rows | 1,229,711 |
| accuracy | 0.9980 (chance 0.1667, largest class 0.5750) |
| weighted P / R / F1 | 0.9980 / 0.9980 / 0.9980 |
| macro P / R / F1 | 0.9783 / 0.9594 / 0.9681 |
| weighted F1 minus macro F1 | 0.0299 |
| cross-validation | 5-fold on training, macro-F1 0.9559 +/- 0.0012 |
| classes at F1 0.00 | none |
| four weakest classes | Spoofing 0.86, Recon 0.98, Benign 0.98, MQTT 0.99 |
| train seconds | 24.7 |
| inference seconds | 7.1 (172,653 rows/s) |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/forest_6class |
| status | reference run |


### NB05 — published_cnn_2class (2026-08-04)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| git sha | 15b46f4 |
| seed | 42 |
| written | 7 of 7 |
| model | mohammadi_cnn |
| task | 2-class, 2 classes |
| split | shipped |
| parent | published_cnn_19class |
| the one change | task |
| training rows | 7,160,831 |
| test rows | 1,614,182 |
| accuracy | 0.9968 (chance 0.5000, largest class 0.9767) |
| weighted P / R / F1 | 0.9968 / 0.9968 / 0.9968 |
| macro P / R / F1 | 0.9623 / 0.9681 / 0.9651 |
| weighted F1 minus macro F1 | 0.0317 |
| cross-validation | none |
| classes at F1 0.00 | none |
| four weakest classes | Benign 0.93, Attack 1.00 |
| train seconds | 4,697.1 |
| inference seconds | 2.3 (694,744 rows/s) |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/published_cnn_2class |
| status | reference run |


### NB04 — preprocessing and splits (2026-08-06)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB04_preprocessing_splits.ipynb |
| run date | 2026-08-06 |
| git sha | bc71318 |
| seed | 42 |
| pass reported | full, every row of every file read once |
| fast/full agreement | all 19 compared values agree |
| split checks | all 10 passed |
| row-order check | passed, 143 of 216 file-and-column combinations above z of 3 (66.2%), rule stated before the run at 50%, none unscorable. Per column: Rate 98.6%, Header_Length 100%, IAT 0%. IAT's median observed lag-1 is -0.2593 against a null of -0.0001, so IAT departs from randomness strongly in the negative direction and the one-sided rule scores it as failure. Row order is not random and the sequence premise holds |
| status | reference run |
| runtime | fast 12s, full 215s |
| files read | 72, 8,775,013 rows |
| features | 44, after dropping Drate |
| timing-excluded slice | defined in the manifest, not written: drop Duration, Rate, Srate, IAT, 40 features remain |
| split protocol | two-tier, 70%/15%/15%, whole recordings held out for 8 classes, contiguous blocks for 11 |
| rows per partition | train 6,228,288 (71.0%), val 1,317,014 (15.0%), test 1,229,711 (14.0%) |
| recordings per partition | train 46, val 28, test 20 |
| window, stride | 50 records, 25 records, never crossing a file boundary |
| sequences | train 249,061, val 52,637, test 49,159 |
| smallest class in sequences | Recon-Ping_Sweep, 2 in its smallest partition |
| scaler | StandardScaler, fitted on 6,228,288 training rows from 46 blocks, no validation or test row read |
| shipped split | saved as file lists and row ranges only, train 7,160,831 rows, test 1,614,182; NB05 reads those CSVs itself and fits its own scaler, so the baseline is reproduced as published |
| artefacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB04, 9 files, 4.4 GB: records_train.npz, sequences_train.npz, records_val.npz, sequences_val.npz, records_test.npz, sequences_test.npz, splits.json, scaler.joblib, NB04_manifest.json. Individual sizes are not recorded for this run |

Stated limitation: 11 of 19 classes have one recording each. Their training, validation and test rows are consecutive stretches of that single recording, so anything a model learns about the session helps it on all three sides. Their scores are not evidence of generalisation to a new recording. Those classes are 8.05% of the rows and 8.61% of the test partition. Two Tier B classes have partitions that cross their file boundary. Recon-VulScan trains on the whole of its train file plus rows 0 to 71 of its test file, and Spoofing tests on rows 15,122 to 16,047 of its train file plus the whole of its test file. Both follow the concatenate-and-cut rule fixed in PREREGISTRATION.md Amendment 4, and both classes are in the H2 class set.

### NB04 row-order check — reading of the IAT result (2026-08-06)

The rule counts z above +3 only. Read two-sided, all 216 of 216 file-and-column combinations depart from randomness, not 143.

Per-file z for IAT across all 72 files: minimum -4,008,331, median -129.3, maximum -10.5. All 72 are below -3. Observed lag-1 ranges from -1.000 to -0.210 with a median of -0.259.

IAT is therefore the most strongly ordered of the three columns measured, not the least. It is negatively autocorrelated: adjacent records alternate rather than resemble each other, which in inter-arrival timing is consistent with paired or bursty traffic. The one-sided rule scores this as failure.

The rule stands as stated before the run and the reported verdict is unchanged at 66.2%. This reading is recorded as a further finding, not as a revision of the rule.

A window of 50 consecutive records carries this alternating structure and a single record cannot. Recorded before NB06 was run.

### NB06 — sequence_cnn_lstm_19class (2026-08-07)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB06_sequence_model.ipynb |
| run date | 2026-08-07 |
| git sha | 20d4709 |
| seed | 42 |
| pass reported | full |
| runtime | fast 0.4 min, full 41.0 min |
| model | mohammadi_cnn_lstm, the published encoder per record and one LSTM of 128 across the window |
| parameters | 214,227 |
| task | 19-class, 19 classes |
| split | two_tier |
| input | 50 records at stride 25, 44 features, no column excluded |
| parent | ours_cnn_19class |
| the one change | model |
| training sequences | 249,061 |
| test sequences | 49,159 |
| accuracy | 0.8197 (chance 0.0526, largest class 0.1592) |
| weighted P / R / F1 | 0.8087 / 0.8197 / 0.8064 |
| macro P / R / F1 | 0.7813 / 0.7093 / 0.7138 |
| weighted F1 minus macro F1 | 0.0926 |
| macro F1 against published_cnn_19class | 0.7138 against 0.7110, +0.0028 |
| the five compared classes, F1 | MQTT-Malformed_Data 0.4883 to 0.8421, Spoofing 0.3438 to 0.7653, Recon-OS_Scan 0.0343 to 0.6061, Recon-VulScan 0.0000 to 0.5385, MQTT-DDoS-Publish_Flood 0.1858 to 0.0796 |
| detected at F1 0.50 | 4 of 5 here, 0 of 5 there, newly: MQTT-Malformed_Data, Recon-OS_Scan, Recon-VulScan, Spoofing |
| classes at F1 0.00 | Recon-Ping_Sweep |
| four weakest classes | Recon-Ping_Sweep 0.00, MQTT-DDoS-Publish_Flood 0.08, DoS-ICMP 0.32, DoS-TCP 0.52 |
| too few sequences to interpret | Recon-Ping_Sweep (4 test, 2 validation); Recon-VulScan (18 test, 18 validation); MQTT-Malformed_Data (40 test, 38 validation) |
| gate | 10 checks, all passed |
| train seconds | 2,427.7 |
| inference seconds | 7.0 (6,985 sequences/s) |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB06/sequence_cnn_lstm_19class |
| status | reference run |

| class | F1 | test sequences | thin |
|---|---|---|---|
| Recon-Ping_Sweep | 0.0000 | 4 | yes |
| MQTT-DDoS-Publish_Flood | 0.0796 | 215 |  |
| DoS-ICMP | 0.3178 | 3,936 |  |
| DoS-TCP | 0.5161 | 3,282 |  |
| Recon-VulScan | 0.5385 | 18 | yes |
| Recon-OS_Scan | 0.6061 | 123 |  |
| MQTT-DoS-Publish_Flood | 0.7551 | 316 |  |
| Spoofing | 0.7653 | 104 |  |
| DDoS-ICMP | 0.7721 | 7,826 |  |
| DoS-SYN | 0.8023 | 3,942 |  |
| DDoS-TCP | 0.8137 | 7,302 |  |
| MQTT-Malformed_Data | 0.8421 | 40 | yes |
| DDoS-SYN | 0.8926 | 6,894 |  |
| Recon-Port_Scan | 0.9301 | 638 |  |
| MQTT-DoS-Connect_Flood | 0.9741 | 94 |  |
| Benign | 0.9808 | 1,381 |  |
| DoS-UDP | 0.9880 | 5,501 |  |
| DDoS-UDP | 0.9881 | 6,255 |  |
| MQTT-DDoS-Connect_Flood | 0.9996 | 1,288 |  |

### NB06 — full 19-class comparison against published_cnn_19class (2026-08-07)

Source: data/processed/NB06/metrics.json against results/NB05/published_cnn_19class/metrics.json,
full precision.

- 9 classes gained F1, sum +2.0566. 10 classes lost F1, sum -2.0033. Net +0.0533 over
  19 classes (+0.0028 per class), matching the macro-F1 delta already in the ledger
  entry above.
- One class crossed below the 0.50 detection threshold: DoS-ICMP, 0.9960 to 0.3178,
  a loss of -0.6782, larger in magnitude than any single class's gain among the five
  H2 classes.
- The five largest losses are all volumetric classes: DoS-ICMP, DoS-TCP, DDoS-ICMP,
  DoS-SYN, DDoS-TCP, summing -1.7662, which is 88% of the total negative movement.
- Four classes crossed above the 0.50 threshold: MQTT-Malformed_Data, Spoofing,
  Recon-VulScan, Recon-OS_Scan.
- MQTT-DDoS-Publish_Flood, the fifth H2 class, did not cross: 0.1858 to 0.0796, a
  further loss.

Full 19-class table, sorted by difference ascending:

| class | published F1 | NB06 F1 | difference |
|---|---|---|---|
| DoS-ICMP | 0.996018 | 0.317827 | -0.678191 |
| DoS-TCP | 0.997981 | 0.516140 | -0.481841 |
| DDoS-ICMP | 0.999140 | 0.772083 | -0.227057 |
| DoS-SYN | 0.997886 | 0.802349 | -0.195537 |
| DDoS-TCP | 0.997247 | 0.813724 | -0.183524 |
| MQTT-DDoS-Publish_Flood | 0.185792 | 0.079646 | -0.106146 |
| DDoS-SYN | 0.995929 | 0.892643 | -0.103286 |
| Recon-Ping_Sweep | 0.010695 | 0.000000 | -0.010695 |
| DDoS-UDP | 0.998491 | 0.988061 | -0.010431 |
| DoS-UDP | 0.994557 | 0.987960 | -0.006596 |
| MQTT-DDoS-Connect_Flood | 0.997059 | 0.999612 | +0.002553 |
| MQTT-DoS-Connect_Flood | 0.967774 | 0.974093 | +0.006320 |
| Recon-Port_Scan | 0.900620 | 0.930091 | +0.029471 |
| MQTT-DoS-Publish_Flood | 0.693707 | 0.755078 | +0.061370 |
| Benign | 0.909429 | 0.980810 | +0.071381 |
| MQTT-Malformed_Data | 0.488332 | 0.842105 | +0.353773 |
| Spoofing | 0.343826 | 0.765306 | +0.421480 |
| Recon-VulScan | 0.000000 | 0.538462 | +0.538462 |
| Recon-OS_Scan | 0.034306 | 0.606061 | +0.571754 |
