import pandas as pd

# load the dataframe
Dataframe = pd.read_csv("test/test.csv")


# if var < 100 label it as immobility
# if var <10000 and var < 1000 label it as nonlocomotion
# if var > 10000 label it as locomotion


# replace '--' with 0 
Dataframe = Dataframe.replace("--", 0)
Dataframe = Dataframe.astype(float)


# label the dataframe
Dataframe["cluster"] = Dataframe["var"].apply(lambda x: "immobility" if x < 100 else ("nonlocomotion" if x < 10000 else "locomotion"))
for i in range(len(Dataframe)):
     if Dataframe["var"][i] == 'nonlocomotion' & Dataframe['var_priority'][i] > 0.7:
         Dataframe["cluster"][i] = "grouping"
# save the dataframe
Dataframe.to_csv("test/test_clustered.csv", index=False)
# map the cluster labels to the videos
import cv2
cap = cv2.VideoCapture("test/test_labeled.mp4")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
font = cv2.FONT_HERSHEY_SIMPLEX
text_color = (0, 0, 0)
text_size = 1
text_thickness = 2

# save the editted video 
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = cap.get(cv2.CAP_PROP_FPS)
output_video = cv2.VideoWriter('test/out.mp4', fourcc, fps, (width, height))


frame_number = 0
while frame_number < len(Dataframe):
    ret, frame = cap.read()
    if ret:
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        print(frame_number)
        cv2.putText(frame, 'cluster: {}, var {}, var_ratio').format(
             Dataframe['cluster'][frame_number-1], round(Dataframe['var'][frame_number-1], 2),
            round((Dataframe['var_priority']), 2), (10, 50), font, text_size, text_color, text_thickness)
        
        cv2.imshow('frame', frame)
        output_video.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break


cap.release()
output_video.release()
cv2.destroyAllWindows()

