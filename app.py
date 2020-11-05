import time
import edgeiq
import numpy
from sign_monitor import SignMonitor
"""
Simultaneously use object detection to detect human faces and classification to classify
the detected faces in terms of age groups, and output results to
shared output stream.

To change the computer vision models, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""


def main():

    # First make a detector to detect facial objects
    hand_detector = edgeiq.ObjectDetection(
            "alwaysai/hand_detection")
    hand_detector.load(engine=edgeiq.Engine.DNN)

    # Then make a detector to detect the sign of the hand
    sign_detector = edgeiq.ObjectDetection("alwaysai/mobilenet_ssd")
    sign_detector.load(engine=edgeiq.Engine.DNN)


    # Descriptions printed to console
    print("Engine: {}".format(hand_detector.engine))
    print("Accelerator: {}\n".format(hand_detector.accelerator))
    print("Model:\n{}\n".format(hand_detector.model_id))
    print("Labels:\n{}\n".format(hand_detector.labels))

    print("Engine: {}".format(sign_detector.engine))
    print("Accelerator: {}\n".format(sign_detector.accelerator))
    print("Model:\n{}\n".format(sign_detector.model_id))
    print("Labels:\n{}\n".format(sign_detector.labels))

    fps = edgeiq.FPS()

    # Variables to limit inference
    counter = 0
    DETECT_RATE = 10
    sign_monitor = SignMonitor()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:

            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # Loop detection
            while True:
                counter += 1  
                if counter % DETECT_RATE == 0:  

                    # Read in the video stream
                    frame = video_stream.read()

                    # Detect human faces
                    results = hand_detector.detect_objects(
                            frame, confidence_level=.5)

                    # Alter the original frame mark up to just show labels
                    frame = edgeiq.markup_image(
                            frame, results.predictions, show_labels=True, show_confidences=False)

                    # Generate labels to display the face detections on the streamer
                    text = ["Model: {}".format(hand_detector.model_id)]
                    text.append(
                            "Inference time: {:1.3f} s".format(results.duration))
                    
                    text.append("Signs:")

                    # Add a counter for the face detection label
                    sign_label = 1

                    # Append each predication to the text output
                    for prediction in results.predictions:

                        # Append labels for face detection & classification
                        text.append("Sign {} ".format(
                            sign_label))

                        sign_label = sign_label + 1

                        # Cut out the hand and use for the sign detection
                        hand_image = edgeiq.cutout_image(frame, prediction.box)

                        # Attempt to classiidnetify sign object
                        sign_results = sign_detector.detect_objects(
                            hand_image, confidence_level=.9)

                        sign = None

                        # If a sign was detected, append the label
                        if sign_results.predictions:
                            sign = sign_results.predictions[0]
                            text.append("sign: {}, confidence: {:.2f}\n".format(
                                 sign_results.predictions[0].label,
                                 sign_results.predictions[0].confidence))
                    
                        if sign is not None:
                            sign_monitor.update(sign.label)
                        
                    # Send the image frame and the predictions to the output stream
                    streamer.send_data(frame, text)

                    fps.update()

                    if streamer.check_exit():
                        break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
