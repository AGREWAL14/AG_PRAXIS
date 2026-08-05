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

