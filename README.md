# Raspberry Pi ML experiments

Repository for ML experiments, specifically for running on a Raspberry Pi

## Requirements

* RPi running Raspbian (tested on Raspbian 9 stretch)

### For /azure-custom-vision
* Python 2.7
* [Sense Hat](https://www.raspberrypi.org/products/sense-hat/)
* [Pi Camera](https://www.raspberrypi.org/products/camera-module-v2/)
* Tensorflow - [Instructions here](https://www.tensorflow.org/install/install_raspbian)

## Azure Custom Vision demo

This demo uses the tensorflow mobile export of a trained
[Azure Custom Vision](https://customvision.ai) model.

### Training the model

You can use the `custom-vision-take-photos.py` script to assist in
taking photos of the correct resolution (227x227).

You can take photos with the Pi Camera using the joystick of the Sense Hat.
Any joystick direction will take a photo and save that image as a numbered file
to an `images` folder, prefixed by the direction of the joystick (for easy grouping).

If you press the middle of the joystick, the program will exit.

Aim for 30+ photos per object you want to detect. The more, the better!

Using [Azure Custom Vision](https://customvision.ai), train a **compact** model
(this is important) with multilabel capabilities using the images you captured.

### Using the trained model

Once trained, you can [export a mobile model](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/export-your-model?WT.mc_id=devops-0000-dabrady).
Use the Tensorflow for Android export type.

From the downloaded zip, place the `model.pb` and `labels.txt` files in the
`azure-custom-vision/model-2` folder, then run `tf-exported-custom-vision.py`.

> Note: The python script is currently set up to look for two labels - `usb` and `coin`.
You'll probably want to modify the script to identify the objects you care about.

To take a picture using the Pi Camera, press the middle of the joystick on the Sense Hat.
The Sense Hat display will show your result, and the console will show the label probabilities.