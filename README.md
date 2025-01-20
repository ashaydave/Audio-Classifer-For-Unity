# Audio Classifer For Unity

YAMnet based audio classification and tagging for audio files in Unity to help you organize your audio assets much faster in Unity!

## Installation
1. In Unity, go to Assets > Import Package > Custom Package
2. Choose the AudioClassifierForUnity.unitypackage file
3. This is how your folder heirarchy should look like:
   
```
Assets/
└── AudioClassifier/
    ├── Editor/
    │   └── AudioClassifierWindow.cs
    ├── Runtime/
    │   └── AudioClassifier.exe
    └── Documentation~/
        ├── README.md
        └── images/
            └── screenshot1.png
            └── screenshot2.png
            └── screenshot3.png
```
## Usage
1. Go to Tools > Audio Classifier in Unity's menu
2. Select the folder containing your audio files
3. Click "Run Classification"
![Image](https://github.com/user-attachments/assets/bcf9bf3b-ce3c-4a18-a24f-24489809047c)
5. Audio files will be automatically organized into categories in a "Classified YAMnet Audio" folder
![Image](https://github.com/user-attachments/assets/845842c7-735e-4ca4-8658-5e0320031477)
![Image](https://github.com/user-attachments/assets/1f21d6d5-474c-45af-a1a4-6c4b3569b06e)

## Supported Audio Formats
- Mono or stereo WAV files

## Requirements
- Unity 2022.3 or later

# YAMnet Information:

- Find more about the model used here: https://github.com/tensorflow/models/tree/master/research/audioset/yamnet
- YAMNet is a pretrained deep net that predicts 521 audio event classes based on the AudioSet-YouTube corpus [https://research.google.com/audioset/], and employing the Mobilenet_v1 [https://arxiv.org/pdf/1704.04861] depthwise-separable convolution architecture

