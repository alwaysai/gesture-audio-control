# Gesture Controlled Home Interaction App
This app is designed to let you use your own custom gesture model to activate voice-activated technology, such as Alexa, Google Home, or Siri, using computer vision. After training your own gesture-detection model, using hand signals of your choice, you can use these signals to play audio files that give commands to smart tech. You'll need an alwaysAI account and to have alwayAI installed:

- [alwaysAI account](https://alwaysai.co/auth?register=true)
- [alwaysAI CLI tools](https://dashboard.alwaysai.co/docs/getting_started/development_computer_setup.html)

## Requirements
This app is intended to work on a model you've trained yourself! Follow the steps below before running your app. The alwaysAI support team is available on Discord to help you if you get stuck: https://discord.gg/rjDdRPT.

### Collect a Dataset
To get you up and running, we've prepared a [dataset](https://www.alwaysai.co/docs/_static/beta/hand_signs3.zip) that includes a few hundred images of an open hand, a hand showing a thumbs up, and a hand showing a peace sign. This app will work best using a model that has been trained on your own hand gestures, so we encourage you to add to this dataset, including images in the same gesture, and adding additional gestures (note that for new gestures, more images will be needed for a balanced dataset; see [this doc](https://alwaysai.co/docs/model_training/data_collection.html#data-capture-guidelines) for data collection tips). For speedy data collection, you can use this [image capture app](https://github.com/alwaysai/expanded-image-capture-dashboard) available on the alwaysAI GitHub. 

### Annotate your Data
Then you can annotate your data, using [this guide](https://alwaysai.co/docs/model_training/data_annotation.html).

### Train your Model
 Then, follow the [training section](https://alwaysai.co/docs/model_training/quickstart.html#step-3-train-your-model) of our quickstart guide to train your own model. You'll find links to tips for data collection and annotation on that page as well.  

### (Optional) Make Audio Files
This step is needed if you want to use your gestures for interacting with 'smart' tech that responds to voice commands instead of gestures. However, you could use your gesture commands to turn on devices that are hooked up to an edge device, like a Raspberry Pi. You could also have it send an alert, by integrating your app with Twilio. You can check out the [alwaysAI blog](https://alwaysai.co/blog) for other tutorials and [Discord](https://discord.gg/rjDdRPT) is a great place to collaborate with users and the alwaysAI team for more ideas. 

To make audio files on a Mac:
Open QuickTime Player, select `File`, then `New Audio Recording`. Record your message and then save it with a name you choose and without altering the default suffix. Then use `ffmpeg` to create a `.wav` file. [Ffmpeg](https://ffmpeg.org) is a popular library for altering media files and we recommend users install it for annotation and other projects. Once you have it installed, open your command line interface tool and navigate to the directory with your audio file. Then execute the command `ffmpeg -i old_file.m4a new_file.wav`, substituting the appropriate name and suffix of your old file and whatever name you choose for your new file (as long as it ends in `.wav`!). You can delete the old file if you'd like. Make sure the name you choose is specified in the `self.actions` dictionary in the `sign_monitor.py` file.

### Set up your Project
Clone this repo into a local directory. Then cd into new folder and run `aai app configure` and make the following selections:
- When prompted to choose a project, use the down arrow and select `Create new project`, choosing any name you like.
- Choose to run either locally or on an edge device.

The `app.py` and `alwaysai.app.json` files should be automatically detected and you should not need to create them.

You can find details on working with projects [here](https://alwaysai.co/docs/getting_started/working_with_projects.html).

You can either publish your model and add it to your project using `aai app models add`, or test out an unpublished version using the `--local-version` flag with this command. See [this documentation](https://alwaysai.co/docs/model_training/using_your_model.html) for full details.

Finally, you'll need to replace the model that is used to create `signal_detector` in `app.py` with the name of your own model! 

## Running

You must make sure each key in the `self.actions` dictionary is a label in your gesture model, and each value is a desired audio file (you could also put method calls here, if you don't want to go the audio file route). Also make sure to set your `initial_audio` variable if using audio sounds! The `skip` value should be reserved for your label that is your `start_signal`.

Run the project as you would any alwaysAI app! See [our docs pages](https://alwaysai.co/blog/building-and-deploying-apps-on-alwaysai) if you need help runnig your program.

#### Example Output

Engine: Engine.DNN
Accelerator: Accelerator.GPU

Model:
alwaysai/hand_detection

Labels:
['???', 'hand']

Engine: Engine.DNN
Accelerator: Accelerator.GPU

Model:
username/modelname

Labels:
['???', 'peace', 'five', 'thumbs_up']

[INFO] Streamer started at http://localhost:5000
[INFO] Client connected: 3d4cf024f42a49179a13ce56f0a33dd0
recieved start signal, listening for action signal
playing initializer
length of labels is 6
most common was thumbs_up with count of 6
playing timer.wav
stopping listening until recieve start signal
recieved start signal, listening for action signal
playing initializer
length of labels is 21
most common was peace with count of 21
playing weather.wav
stopping listening until recieve start signal

## Troubleshooting
Docs: https://dashboard.alwaysai.co/docs/getting_started/introduction.html

Community Discord: https://discord.gg/rjDdRPT

Email: support@alwaysai.co