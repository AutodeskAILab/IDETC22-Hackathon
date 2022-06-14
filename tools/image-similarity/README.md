# image-similarity

- **High-level Description:** This tool extracts numerical embeddings (fingerprints) that expressively represents the 2D features of thumbnail images, and save them into a spreadsheet file. This tool is adapted based on [this repository](https://github.com/zegami/image-similarity-clustering), under the MIT license. You may consider using the extracted fingerprints as a way to evaluate the similarity and difference between 2D thumbnail images. For more visual-oriented tools of image similarity evaluation, please refer to `image-clustering`.

- **Usage:**
```
python fingerprint-generator.py features [dir of images] [result CSV file]

# (e.g.) python fingerprint-generator.py features ./images ./fingerprints.csv
```
