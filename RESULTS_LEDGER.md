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

---

### NB07 — class balancing (2026-08-08)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB07_class_balancing.ipynb |
| run date | 2026-08-08 |
| git sha | 45f376d |
| seed | 42 |
| pass reported | full |
| runs | 5, one intervention each, of which 0 were read back from an earlier session |
| runtime | fast 1.6 min, full 212.3 min |
| parent | sequence_cnn_lstm_19class, macro F1 0.7138 |
| input | 50 records at stride 25, 44 features, two-tier split |
| role | reported result, per-class benefit and cost. Not a hypothesis test, no significance computed |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB07, copied to results/NB07/ |
| status | reference run |

| run | Recon-VulScan | Recon-OS_Scan | MQTT-DDoS-Publish_Flood | Spoofing | MQTT-Malformed_Data | volumetric mean | macro F1 |
|---|---|---|---|---|---|---|---|
| sequence_cnn_lstm_19class (parent) | 0.5385 | 0.6061 | 0.0796 | 0.7653 | 0.8421 | 0.7613 | 0.7138 |
| class_weighted_loss | 0.3729 | 0.6667 | 0.0717 | 0.4295 | 0.6000 | 0.6614 | 0.6481 |
| focal_loss | 0.3333 | 0.3377 | 0.0631 | 0.6667 | 0.9500 | 0.7524 | 0.6838 |
| logit_adjustment | 0.4746 | 0.5730 | 0.0631 | 0.7442 | 0.8706 | 0.7720 | 0.7238 |
| threshold_tuning | 0.3902 | 0.8193 | 0.0804 | 0.8406 | 0.8732 | 0.7643 | 0.7320 |
| window_resampling | 0.3768 | 0.8142 | 0.0541 | 0.8547 | 0.9756 | 0.7788 | 0.7699 |

### NB07 — class_weighted_loss (2026-08-08)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB07_class_balancing.ipynb |
| git sha | 45f376d |
| seed | 42 |
| written | 1 of 5 |
| intervention | class_weighted_loss, changes what the model learns |
| parent | sequence_cnn_lstm_19class |
| the one change | class_weight = inverse frequency, N / (K * n), normalised to mean 1 |
| training windows | 249,061 |
| test windows | 49,159 |
| accuracy | 0.7056 |
| weighted P / R / F1 | 0.7632 / 0.7056 / 0.6965 |
| macro P / R / F1 | 0.6887 / 0.7461 / 0.6481 |
| macro F1 against the parent | 0.6481 against 0.7138, -0.0657 |
| the five classes, F1 | Recon-VulScan 0.3729 (-0.1656), Recon-OS_Scan 0.6667 (+0.0606), MQTT-DDoS-Publish_Flood 0.0717 (-0.0079), Spoofing 0.4295 (-0.3358), MQTT-Malformed_Data 0.6000 (-0.2421) |
| of the five, detected at 0.50 | 2 of 5, parent 4 of 5 |
| the eight volumetric classes, mean F1 | 0.6614 against 0.7613, -0.1000 |
| of the eight, detected at 0.50 | 5 of 8, parent 7 of 8 |
| four weakest classes | MQTT-DDoS-Publish_Flood 0.07, DoS-ICMP 0.35, Recon-VulScan 0.37, Recon-Ping_Sweep 0.38 |
| too few windows to interpret | Recon-Ping_Sweep (4 test); Recon-VulScan (18 test); MQTT-Malformed_Data (40 test) |
| gate | 9 checks, all passed |
| train seconds | 2,425.7 |
| inference seconds | 6.9 |
| artifacts | results/NB07/class_weighted_loss |
| status | reference run |

### NB07 — focal_loss (2026-08-08)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB07_class_balancing.ipynb |
| git sha | 45f376d |
| seed | 42 |
| written | 2 of 5 |
| intervention | focal_loss, changes what the model learns |
| parent | sequence_cnn_lstm_19class |
| the one change | loss = categorical_focal_crossentropy, gamma 2.0, alpha 0.25 |
| training windows | 249,061 |
| test windows | 49,159 |
| accuracy | 0.8213 |
| weighted P / R / F1 | 0.8196 / 0.8213 / 0.7989 |
| macro P / R / F1 | 0.7910 / 0.6866 / 0.6838 |
| macro F1 against the parent | 0.6838 against 0.7138, -0.0300 |
| the five classes, F1 | Recon-VulScan 0.3333 (-0.2051), Recon-OS_Scan 0.3377 (-0.2684), MQTT-DDoS-Publish_Flood 0.0631 (-0.0166), Spoofing 0.6667 (-0.0986), MQTT-Malformed_Data 0.9500 (+0.1079) |
| of the five, detected at 0.50 | 2 of 5, parent 4 of 5 |
| the eight volumetric classes, mean F1 | 0.7524 against 0.7613, -0.0090 |
| of the eight, detected at 0.50 | 7 of 8, parent 7 of 8 |
| four weakest classes | Recon-Ping_Sweep 0.00, MQTT-DDoS-Publish_Flood 0.06, DoS-ICMP 0.16, Recon-VulScan 0.33 |
| too few windows to interpret | Recon-Ping_Sweep (4 test); Recon-VulScan (18 test); MQTT-Malformed_Data (40 test) |
| gate | 9 checks, all passed |
| train seconds | 2,466.0 |
| inference seconds | 6.8 |
| artifacts | results/NB07/focal_loss |
| status | reference run |

### NB07 — logit_adjustment (2026-08-08)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB07_class_balancing.ipynb |
| git sha | 45f376d |
| seed | 42 |
| written | 3 of 5 |
| intervention | logit_adjustment, changes how a trained model decides |
| parent | sequence_cnn_lstm_19class |
| the one change | decision_rule = logit adjustment, tau 1.0, priors counted on the training windows |
| training windows | 249,061 |
| test windows | 49,159 |
| accuracy | 0.8150 |
| weighted P / R / F1 | 0.8148 / 0.8150 / 0.8095 |
| macro P / R / F1 | 0.7516 / 0.8000 / 0.7238 |
| macro F1 against the parent | 0.7238 against 0.7138, +0.0100 |
| the five classes, F1 | Recon-VulScan 0.4746 (-0.0639), Recon-OS_Scan 0.5730 (-0.0330), MQTT-DDoS-Publish_Flood 0.0631 (-0.0166), Spoofing 0.7442 (-0.0211), MQTT-Malformed_Data 0.8706 (+0.0285) |
| of the five, detected at 0.50 | 3 of 5, parent 4 of 5 |
| the eight volumetric classes, mean F1 | 0.7720 against 0.7613, +0.0106 |
| of the eight, detected at 0.50 | 7 of 8, parent 7 of 8 |
| four weakest classes | MQTT-DDoS-Publish_Flood 0.06, DoS-ICMP 0.38, Recon-Ping_Sweep 0.47, Recon-VulScan 0.47 |
| too few windows to interpret | Recon-Ping_Sweep (4 test); Recon-VulScan (18 test); MQTT-Malformed_Data (40 test) |
| gate | 9 checks, all passed |
| train seconds | 2,433.3 |
| inference seconds | 6.8 |
| artifacts | results/NB07/logit_adjustment |
| status | reference run |

### NB07 — threshold_tuning (2026-08-08)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB07_class_balancing.ipynb |
| git sha | 45f376d |
| seed | 42 |
| written | 4 of 5 |
| intervention | threshold_tuning, changes how a trained model decides |
| parent | sequence_cnn_lstm_19class |
| the one change | decision_rule = one threshold per class, tuned on validation, largest divided score wins |
| training windows | 249,061 |
| test windows | 49,159 |
| accuracy | 0.8168 |
| weighted P / R / F1 | 0.8271 / 0.8168 / 0.8071 |
| macro P / R / F1 | 0.7797 / 0.7830 / 0.7320 |
| macro F1 against the parent | 0.7320 against 0.7138, +0.0182 |
| the five classes, F1 | Recon-VulScan 0.3902 (-0.1482), Recon-OS_Scan 0.8193 (+0.2132), MQTT-DDoS-Publish_Flood 0.0804 (+0.0007), Spoofing 0.8406 (+0.0753), MQTT-Malformed_Data 0.8732 (+0.0311) |
| of the five, detected at 0.50 | 3 of 5, parent 4 of 5 |
| the eight volumetric classes, mean F1 | 0.7643 against 0.7613, +0.0030 |
| of the eight, detected at 0.50 | 6 of 8, parent 7 of 8 |
| four weakest classes | MQTT-DDoS-Publish_Flood 0.08, Recon-VulScan 0.39, DoS-TCP 0.45, DoS-ICMP 0.46 |
| too few windows to interpret | Recon-Ping_Sweep (4 test); Recon-VulScan (18 test); MQTT-Malformed_Data (40 test) |
| gate | 9 checks, all passed |
| train seconds | 2,446.5 |
| inference seconds | 1.7 |
| artifacts | results/NB07/threshold_tuning |
| status | reference run |

### NB07 — window_resampling (2026-08-08)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB07_class_balancing.ipynb |
| git sha | 45f376d |
| seed | 42 |
| written | 5 of 5 |
| intervention | window_resampling, changes what the model learns |
| parent | sequence_cnn_lstm_19class |
| the one change | resampling = window-level oversampling to the median class size, with replacement |
| training windows | 295,925 |
| test windows | 49,159 |
| accuracy | 0.8393 |
| weighted P / R / F1 | 0.8298 / 0.8393 / 0.8229 |
| macro P / R / F1 | 0.8044 / 0.8074 / 0.7699 |
| macro F1 against the parent | 0.7699 against 0.7138, +0.0561 |
| the five classes, F1 | Recon-VulScan 0.3768 (-0.1616), Recon-OS_Scan 0.8142 (+0.2081), MQTT-DDoS-Publish_Flood 0.0541 (-0.0256), Spoofing 0.8547 (+0.0894), MQTT-Malformed_Data 0.9756 (+0.1335) |
| of the five, detected at 0.50 | 3 of 5, parent 4 of 5 |
| the eight volumetric classes, mean F1 | 0.7788 against 0.7613, +0.0174 |
| of the eight, detected at 0.50 | 7 of 8, parent 7 of 8 |
| four weakest classes | MQTT-DDoS-Publish_Flood 0.05, DoS-ICMP 0.30, Recon-VulScan 0.38, DoS-TCP 0.50 |
| too few windows to interpret | Recon-Ping_Sweep (4 test); Recon-VulScan (18 test); MQTT-Malformed_Data (40 test) |
| gate | 9 checks, all passed |
| train seconds | 2,894.7 |
| inference seconds | 6.8 |
| artifacts | results/NB07/window_resampling |
| status | reference run |

### NB07 — follow-up note (2026-08-08)

Figures re-read from `results/NB07/*/metrics.json` after the artifacts were copied into
the repository. The five macro-F1 values on disk match the run output to four decimals.

All five runs are one key from `sequence_cnn_lstm_19class` and none was read back from an
earlier session, so the five are directly comparable to each other and to the parent. All
six rows are scored on the same 49,159 test windows, which is what makes the per-class
columns above a paired comparison rather than six runs' own scores. No significance test
was computed here; that is NB08's.

**Window resampling gives the largest gain, and three of the five raise macro-F1 and the
volumetric mean together.** Window resampling reaches 0.7699 macro against the parent's
0.7138 and 0.7788 volumetric mean against 0.7613, the largest movement on both of any
intervention. Logit adjustment (+0.0100 macro, +0.0106 volumetric) and threshold tuning
(+0.0182 macro, +0.0030 volumetric) also move both upward by smaller amounts. Window
resampling is the highest macro-F1 any sequence model has reached in this project, and it
remains below `forest_19class` at 0.8418 on single records.

**Recon-VulScan falls under every intervention.** 0.5385 at the parent, and between 0.3333
and 0.4746 across the five. It is the class NB06 lifted across the 0.50 threshold, and all
five balancing methods push it back under. This is why no run improves on the parent's 4 of
5 detected: the count is 3 of 5 or 2 of 5 everywhere. The class rests on 18 test sequences
and carries the Amendment 4 caveat, so a single misclassified window moves its F1
substantially. The direction is consistent across five runs; the magnitude is not
interpretable.

**MQTT-DDoS-Publish_Flood does not respond to any intervention.** 0.0541 to 0.0804 across
all five, against a parent of 0.0796, with no run reaching a tenth of the 0.50 threshold.
Five different treatments of class imbalance produce no movement. `PREREGISTRATION.md`
Objective 2 fixed the reading of this outcome in advance: evidence that the failure is not
caused by imbalance, directing attention to feature separability instead. NB02 is
consistent with that, placing the class in two of the eleven pairs below AUC 0.90,
against MQTT-Malformed_Data at 0.8753 and Spoofing at 0.8930.

**DoS-ICMP under each intervention**, against the parent's 0.3178: focal_loss 0.1594,
window_resampling 0.2995, class_weighted_loss 0.3516, logit_adjustment 0.3769,
threshold_tuning 0.4590. No intervention returns it above 0.50 and two leave it lower than
the parent. What these five figures measure is whether balancing recovers the class, not
what caused the regression. The interventions were not designed to diagnose it and this run
does not diagnose it.

**Cost to the eight volumetric classes.** Two interventions lower the volumetric mean,
class_weighted_loss by -0.1000 and focal_loss by -0.0090; three raise it, threshold_tuning
by +0.0030, logit_adjustment by +0.0106 and window_resampling by +0.0174. No H2 clause
sets a limit on this quantity — `PREREGISTRATION.md` Amendment 10 records that the cost
clause of Amendment 2 did not survive the Amendment 5 replacement — so these figures are
reported without a pass mark.

### NB05 — forest_19class_dadkhah_leaf1 (2026-08-08)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB05_baseline_models.ipynb |
| git sha | 407d5a7 |
| seed | 42 |
| model | random_forest |
| task | 19-class, 19 classes |
| split | two_tier |
| parent | forest_19class |
| the one change | min_samples_leaf 20 to 1, the value in Dadkhah et al. (2024) Table 8 |
| hyperparameters from | Dadkhah et al. (2024), Table 8: 100 trees, max_features sqrt, min_samples_leaf 1 |
| training rows | 999,998 |
| test rows | 1,229,711 |
| accuracy | 0.9928 (chance 0.0526, largest class 0.1591) |
| weighted P / R / F1 | 0.9943 / 0.9928 / 0.9916 |
| macro P / R / F1 | 0.9441 / 0.8526 / 0.8680 |
| macro F1 against the parent | 0.8680 against 0.8418, +0.0262 |
| weighted F1 minus macro F1 | 0.1236 |
| cross-validation | 5-fold on training, macro-F1 0.9427 +/- 0.0046 |
| classes at F1 0.00 | none |
| four weakest classes | MQTT-DDoS-Publish_Flood 0.19, Recon-VulScan 0.49, Recon-Ping_Sweep 0.71, Recon-OS_Scan 0.75 |
| train seconds | 172.4 |
| inference seconds | 15.5 (79,402 rows/s) |
| not controlled | the feature set (39 listed, 45 shipped, 44 used here) and their averaging method, which the paper does not state |
| artifacts | results/NB05/forest_19class_dadkhah_leaf1, config.json and metrics.json only; y_true.npy and y_pred.npy are on Drive at /content/drive/MyDrive/AG_PRAXIS_artifacts/NB05/forest_19class_dadkhah_leaf1 |
| status | ablation, reported result, not a hypothesis test |

Removing the leaf constraint trades precision for recall. Macro precision falls from the
parent's 0.9603 to 0.9441 and macro recall rises from 0.8225 to 0.8526, and the net is
+0.0262 macro-F1. Per class the movement is concentrated in the small classes: Recon-VulScan
0.4886 against 0.2536, MQTT-Malformed_Data 0.8272 against 0.6752, MQTT-DDoS-Publish_Flood
0.1858 against 0.1186. Spoofing is the one that falls, 0.8399 against 0.8605.

This run is reported for what it says about evaluation protocol, not as a comparison
between two models. Dadkhah et al.'s published random forest reads F1 0.551 at nineteen
classes on their file-level split; the same configuration on the capture-disjoint split
reads 0.8680 here, and the leaf setting itself accounts for 0.0262 of the 0.3170 between
them. The feature set and the averaging method are not controlled by this run. H2's
comparator is unchanged.

### NB08 — evaluation and significance (2026-08-10)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB08_evaluation_and_significance.ipynb |
| git sha | d193464 |
| seeds | 42, 43, 44, 45, 46 |
| parent | sequence_cnn_lstm_19class, unchanged and not retrained |
| runs trained here | 7: sequence_budget_05, sequence_budget_10, sequence_budget_25, sequence_seed_43, sequence_seed_44, sequence_seed_45, sequence_seed_46 |
| budgets | k in 5, 10, 25, 50 records, taken as prefixes of the NB04 windows at window 50 stride 25 |
| test items | 49,159 windows, identical across every run, asserted |
| parameters | 214,227 in every run, unchanged by the budget |
| macro F1 by budget | k5 0.6295, k10 0.6837, k25 0.7323, k50 0.7138 |
| classes at F1 0.80 by budget | k5 9, k10 9, k25 11, k50 10 |
| censored at k=50 | 8 of 19 classes, reported as "> 50" and never as 50 |
| records-to-threshold median, low-rate | not reached within 50 (3 of 5 censored) |
| records-to-threshold median, volumetric | 5 (3 of 8 censored) |
| records-to-threshold twofold comparison | not evaluated, at least one median is not determinate; direction reported instead |
| saturation, additional analysis | epsilon 0.02, classes stopping at k=5: 7 of 19 |
| cross-seed macro F1 | 0.7373 plus or minus 0.0233 over 5 seeds at k=50 |
| DoS-ICMP across seeds | 0.3178, 0.3099, 0.3450, 0.2690, 0.2938 |
| McNemar | 11 paired tests, Holm-Bonferroni at alpha 0.05: 5 of 6 budget pairs and 3 of 5 intervention pairs significant within their family |
| not computed | McNemar against published_cnn_19class. Different units and different splits, so no item-level pairing exists. No substitute test was computed |
| label encoding | int16 codes into label_map.json, written beside the runs |
| artifacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB08 |
| status | records-to-threshold measurement and cross-seed variation; the saturation analysis is additional and carries no threshold |

| records-to-threshold, low-rate | Recon-Port_Scan 5, MQTT-Malformed_Data 25, Recon-OS_Scan > 50, Recon-VulScan > 50, Spoofing > 50 |
| records-to-threshold, volumetric | DDoS-SYN 5, DDoS-TCP 5, DDoS-UDP 5, DoS-SYN 5, DoS-UDP 5, DDoS-ICMP > 50, DoS-ICMP > 50, DoS-TCP > 50 |
| saturation budget, per class | low-rate: Spoofing 10, MQTT-Malformed_Data 25, Recon-OS_Scan 25, Recon-Port_Scan 50, Recon-VulScan 50. volumetric: DDoS-ICMP 5, DDoS-SYN 5, DDoS-TCP 5, DoS-SYN 5, DDoS-UDP 25, DoS-UDP 25, DoS-ICMP 50, DoS-TCP 50 |
| saturation below the reliability threshold | 6 classes saturate at F1 below 0.80, including DDoS-ICMP at 0.7998 at k=5 and DoS-ICMP at 0.3178 at k=50 |

### NB08 — correction to the count of classes saturating below F1 0.80 (2026-08-10)

The NB08 entry above gives the count as 6. It is 8.

Read from `data/processed/NB08/tables/saturation.csv`, the classes whose F1 at their own
saturation budget is below 0.80 are DDoS-ICMP 0.7998 at k=5, MQTT-DoS-Publish_Flood
0.7488 at k=5, MQTT-DDoS-Publish_Flood 0.0889 at k=10, Spoofing 0.7941 at k=10,
Recon-OS_Scan 0.6105 at k=25, DoS-ICMP 0.3178 at k=50, DoS-TCP 0.5161 at k=50 and
Recon-VulScan 0.5385 at k=50. That is eight of nineteen.

The two classes the earlier line names are both correct and are among the eight. What is
wrong is the count.

`src/nb08_tables.py` carries this count as one of the checks it runs against
`PROJECT_RECORD.md` Section 5. Section 5 states eight, the script derives eight from the
artifacts, and the check passes at 24 of 24, so the earlier line is the only place the
figure reads 6.

The line is left as written, since this file is append-only. Nothing else in the NB08
entry depends on the count: no per-class saturation budget, no group median, no
records-to-threshold figure and no significance result moves.

### NB03b — timing feature ablation (2026-08-10)

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB03b_timing_ablation.ipynb |
| run date | 2026-08-10 |
| git sha | 8beebb7, working tree clean |
| seed | 42 |
| pass reported | full, 8,000 rows drawn from each recording |
| registered under | PREREGISTRATION.md Amendment 13 |
| column removed | Duration, the TTL header field |
| protocol | NB03's, unchanged: RandomForest, 50 trees, min leaf 100, 30% held out, target the recording |
| recordings | 50, from the 8 classes recorded more than once |
| rows used | 400,000, 8,000 from every recording |
| NB03 figures read from | data/processed/NB03_verdict.json, run 2026-08-04 at 1229f85 |
| runs written | 11: timing_minus_duration, all_minus_duration, duration_only, and within_<class>_minus_duration for the 8 classes |
| timing family without Duration, 3 features (chance 0.0200) | 0.8935 accuracy, 0.8932 macro-F1, against NB03's 0.9301 for the family with it, difference -0.0366 |
| all features without Duration, 43 features (chance 0.0200) | 0.7495 accuracy, 0.7457 macro-F1, against NB03's 0.8010 for all 44, difference -0.0515 |
| all features without Duration, attack class held fixed | 0.8504 mean accuracy over the 8 classes, chance 0.1750, against NB03's 0.8280, difference +0.0225 |
| Duration alone (chance 0.0200) | 0.0299 accuracy, 0.0164 macro-F1. No NB03 counterpart, so no difference is computed |
| reproduction check | run 1 reproduces NB03's capture_timing_three exactly: 0.893475 here against 0.893475, difference 0.000000, inside the 0.0001 allowed |
| per-class direction, attack held fixed | up on five of the eight classes, down on three, one of them by 0.0001 |
| per-class aggregate, attack held fixed | the five increases sum to +0.2173 and the three decreases to -0.0376 |
| seed replicates | none. Every figure above is a single run at seed 42 |
| artifacts, repository | data/processed/NB03b/duration_ablation.json, and config.json and metrics.json for each of the 11 runs under results/NB03b/ |
| artifacts, Drive | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB03b, which also holds y_true.npy, y_pred.npy and model.joblib per run |
| status | reported result, not a hypothesis test |

Per class, attack held fixed, without Duration against NB03 with it: DDoS-ICMP 0.8702 (0.8532) ·
DDoS-SYN 0.8783 (0.8784) · DDoS-TCP 0.8856 (0.8232) · DDoS-UDP 0.7158 (0.6869) · DoS-ICMP
0.8339 (0.7863) · DoS-SYN 0.9106 (0.9178) · DoS-TCP 0.8904 (0.8291) · DoS-UDP 0.8186 (0.8489)

Duration stays in the timing family and in the 44 features for every run already executed.
This notebook measures the column's contribution to the NB03 figures and does not change the
feature set.

### NB09a — SHAP attributions on timing-excluded models (2026-08-12), partial

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB09a_shap_attributions.ipynb |
| run date | 2026-08-12 |
| status | **partial**: the five sequence seeds and the forest fit completed; the forest's TreeExplainer pass was interrupted and did not finish |
| registered under | PREREGISTRATION.md Amendments 18 and 19 |
| environment | tensorflow 2.20.0, keras 3.13.2, shap 0.52.0, scipy 1.16.3, backend tensorflow, accelerator NVIDIA A100-SXM4-40GB |
| features | 40, after dropping Duration, Rate, Srate, IAT |
| sequence models | 5, seeds 42 to 46, parent sequence_cnn_lstm_19class, one change: n_features |
| sequence parameters | 206,035 at 40 features against the parent's 214,227 at 44 |
| macro F1 by seed | 42 0.6747, 43 0.6714, 44 0.6947, 45 0.6805, 46 0.7292 |
| macro F1, five seeds | 0.6901 plus or minus 0.0236, on 49,159 windows |
| sequence training | 2,294, 2,254, 2,253, 2,248 and 2,263 seconds |
| explainer pass, per seed | 444 to 447 seconds each on the A100; each wrote its attributions file as it finished |
| forest fit | complete. forest_timing_excluded, parent forest_19class, one change: n_features. 100 trees, min leaf 20, sqrt, cap 1,000,000 rows, fitted in 107.8s on 999,998 records, cross-validated over 5 folds |
| forest macro F1 | 0.5910 on 1,229,711 records |
| forest attributions | **not produced**. TreeExplainer ran for over an hour against 33,653 records and was interrupted |
| the same four columns, two models | the forest falls from 0.8418 at 44 features to 0.5910 at 40, a fall of 0.2508. The sequence model falls from 0.7138 to a five-seed mean of 0.6901, a fall of 0.0237 |
| units | 49,159 windows for the sequence models and 1,229,711 records for the forest; the same split, not the same partition |
| artefacts present | attributions_seed_42.npz through _46.npz, each (19, 40) at nsamples 50 and background 200; six run directories each holding its five files |
| artefacts absent | attributions_forest.npz, and attributions.json, which is written once after the forest cell and so was not reached |
| outstanding | the TreeExplainer pass and attributions.json, both to be completed by a resume run on a CPU runtime |
| artefacts | /content/drive/MyDrive/AG_PRAXIS_artifacts/NB09a |

H3 is not evaluated by this run. The mapping, the agreement count, Kendall's tau and the
MAUDE search are NB09b's, and NB09b cannot run until attributions.json exists.

### NB09a — SHAP attributions on timing-excluded models (2026-08-13), complete

Supersedes the partial entry of 2026-08-12, which recorded the forest's attribution pass
as outstanding. That entry stands as written; this one records the completed run.

| field | value |
|---|---|
| notebook | AG_PRAXIS_NB09a_shap_attributions.ipynb |
| status | complete. Five sequence seeds, the forest fit and both attribution passes |
| registered under | PREREGISTRATION.md Amendments 18 and 19 |
| environment, sequence arm | 2026-08-12, NVIDIA A100-SXM4-40GB, tensorflow 2.20.0, keras 3.13.2, shap 0.52.0, scipy 1.16.3 |
| environment, forest arm | 2026-08-13, cpu, tensorflow 2.20.0, keras 3.13.2, shap 0.52.0, scipy 1.16.3 |
| where the environment is read from | each run's own `config.json`, which is the authority. `attributions.json` carries one top-level environment field describing the session that wrote it, 2026-08-13 on cpu, not the work it summarises |
| features | 40, after dropping Duration, Rate, Srate, IAT |
| sequence models | 5, seeds 42 to 46, parent sequence_cnn_lstm_19class, one change: n_features |
| sequence parameters | 206,035 against the parent's 214,227 at 44 features |
| macro F1 by seed | 42 0.6747, 43 0.6714, 44 0.6947, 45 0.6805, 46 0.7292 |
| macro F1, five seeds | 0.6901 plus or minus 0.0236, on 49,159 windows |
| sequence training | 2,294, 2,254, 2,253, 2,248 and 2,263 seconds on the A100 |
| sequence explainer | GradientExplainer, 444 to 447 seconds per seed on the A100, each writing its own file as it finished |
| sequence explained | 862 windows, 50 per class or all of them where a class has fewer |
| forest | forest_timing_excluded, parent forest_19class, one change: n_features. 100 trees, min leaf 20, sqrt, cap 1,000,000 rows |
| forest macro F1 | 0.5910269 on 1,229,711 records, fitted in 107.5s, cross-validated over 5 folds in 420.2s |
| forest explainer | TreeExplainer on cpu, exact |
| forest explained | 3,739 records, 200 per class. Reduced from 2,000 per class after two runs at 33,653 records each exceeded an hour without completing, once on the A100 session and once on Colab CPU. Recorded in `DECISIONS.md` under 2026-08-13 |
| the two explained sets are not comparable | 862 windows at 50 per class against 3,739 records at 200 per class. Different units and never a like-for-like sample |
| nsamples | 50, background 200 windows drawn once and held fixed across the five seeds |
| the same four columns, two models | the forest falls from 0.8418 at 44 features to 0.5910 at 40, a fall of 0.2508. The sequence model falls from 0.7138 to a five-seed mean of 0.6901, a fall of 0.0237 |
| units | 49,159 windows for the sequence models and 1,229,711 records for the forest; the same split, not the same partition |
| artefacts | attributions_seed_42.npz through _46.npz, attributions_forest.npz and attributions.json, each attribution table (19, 40); six run directories each holding its five files. There is no attributions.npz: the per-seed design replaced it |
| forest refitted on resume | the resume guard covered the attribution pass and not the fit, so the CPU run refitted the forest and re-ran its five folds. The figures are unaffected. `DECISIONS.md` under 2026-08-13 records it |

H3 is not evaluated by this run. The mapping, the agreement count, Kendall's tau and the
MAUDE search are NB09b's, which has not been run.
