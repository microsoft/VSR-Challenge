# Grand Challenge on Video Super-Resolution for Video Conferencing - ICME 2025
[[challenge website](https://www.microsoft.com/en-us/research/academic-program/video-super-resolution-challenge-icme-2025/challenge/)]

The Grand Challenge on Video Super-Resolution for Video Conferencing at ICME 2025 is intended to stimulate research in the area of Video Super Resolution in communication systems.

This ICME grand challenge focuses on video super-resolution for video conferencing, where the low-resolution video is encoded using the H.265 codec with fixed Quantization Parameters (QP). The goal is to upscale the input LR videos by a specific factor and provide HR videos with perceptually enhanced quality (including compression artifact removal). We follow the low-delay scenario in the entire challenge, where **no future frames should be used to enhance the current frame**.

There are three tracks specific to video content:

- [**Track 1**: General purpose real-world video content](docs/track1.md), x4 upscaling
- [**Track 2**: Talking Head videos](docs/track2.md), x4 upscaling
- [**Track 3**: Screen sharing videos](docs/track3.md), x3 upscaling

This repository aims to provide the **training set** and **validation set** for each track. The test sets will be provided close to the end of the competition to the registered teams.

For more information about the challenge, timeline, and registration, visit the [ICME 2025 Grand Challenge on Video Super-Resolution for Video Conferencing](https://www.microsoft.com/en-us/research/academic-program/video-super-resolution-challenge-icme-2025/challenge/) web page.

## News
- Feb 3, 2025: Training and validation sets for Track 1 and 2, and validation set for Track 3 are available.

## Download

1. Clone the repository:

```bash
git clone https://github.com/microsoft/VSR-Challenge.git
cd VSR-Challenge
```

2. Install the required libraries:

```bash
cd download
pip install -r requirements.txt
```

3. Download the txt file with the list of URLs from each track's description page ([Track 1](docs/track1.md), [Track 2](docs/track2.md), [Track 3](docs/track3.md)).

4. Change LOCAL_PATH to a path in your file system and run the following command. Replace file_list.txt with the list of files for the training/validation set of the track you are interested in:

```bash
python downloader.py --list-of-files file_list.txt --local-path LOCAL_PATH
```

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Dataset license

This dataset is released under the [Community Data License Agreement – Permissive, Version 2.0 - CDLA](https://cdla.dev/permissive-2-0/). See the [LICENSE-DATA](LICENSE-DATA) file for more details. For information on data sourced from third parties, refer to the [NOTICE](NOTICE) file.


## Code license

MIT License

Copyright (c) Microsoft Corporation.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE


## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
