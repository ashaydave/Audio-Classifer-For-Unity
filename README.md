# Audio Classifer For Unity

YAMnet based audio classification and tagging for audio files in Unity to help you organize your audio assets much faster in Unity!

## Installation
1. In Unity, go to Assets > Import Package > Custom Package
2. Choose the AudioClassifierForUnity.unitypackage file

## Usage
1. Go to Tools > Audio Classifier in Unity's menu
2. Select the folder containing your audio files
3. Click "Run Classification"
4. Audio files will be automatically organized into categories in a "Classified YAMnet Audio" folder

## Supported Audio Formats
- Mono or stereo WAV files

## Requirements
- Windows 10 or later
- Unity 2020.3 or later

# YAMnet Information:

- Find more about the model used here: https://github.com/tensorflow/models/tree/master/research/audioset/yamnet
- YAMNet is a pretrained deep net that predicts 521 audio event classes based on the AudioSet-YouTube corpus [https://research.google.com/audioset/], and employing the Mobilenet_v1 [https://arxiv.org/pdf/1704.04861] depthwise-separable convolution architecture

