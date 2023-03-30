import pandas as pd

# load the dataframe
Dataframe = pd.read_csv("test_full.csv")


# if var < 100 label it as immobility
# if var <10000 and var < 1000 label it as nonlocomotion
# if var > 10000 label it as locomotion


# replace '--' with 0 
Dataframe["var"] = Dataframe["var"].replace("--", 0)
Dataframe["var"] = Dataframe["var"].astype(float)
# label the dataframe
Dataframe["cluster"] = Dataframe["var"].apply(lambda x: "immobility" if x < 100 else ("nonlocomotion" if x < 10000 else "locomotion"))


# map the cluster labels to the videos
import cv2
cap = cv2.VideoCapture("C:\\Users\\chang\\DeepLabCut\\main\\JUPYTER\\DLC_Data\\videos\\2022-10-07 12-15-51DLC_resnet50_mainDec6shuffle1_120000_labeled.mp4")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
font = cv2.FONT_HERSHEY_SIMPLEX
text_color = (0, 0, 0)
text_size = 1
text_thickness = 2

# save the editted video 
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = cap.get(cv2.CAP_PROP_FPS)
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))


frame_number = 0
while frame_number < len(Dataframe):
    ret, frame = cap.read()
    if ret:
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        print(frame_number)
        cv2.putText(frame, 'cluster: {}, var {}'.format(Dataframe['cluster'][frame_number-1], round(Dataframe['var'][frame_number-1]), 2), (10, 50), font, text_size, text_color, text_thickness)
        cv2.imshow('frame', frame)
        output_video.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break


cap.release()
output_video.release()
cv2.destroyAllWindows()

