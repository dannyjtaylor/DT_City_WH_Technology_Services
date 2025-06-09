import pandas as pd
import os


jostleYesPhotoList = []
# iterate through jostle yes photos folder (to separate people in jostle that have photos, with those that have either WH logo or no photo at all)    
for file in os.listdir("C:\\Users\\dtaylor\\Documents\\Jostle Pictures Project\\Jostle (Yes Photos)"):
    if file.endswith(".jpg"):
        jostleYesPhotoList.append(str(file)[:-4])
        print(file)

# iterate through work email column in the jostle list CSV
df = pd.read_csv("C:\\Users\\dtaylor\\Documents\\Jostle Pictures Project\\jostleUsers.csv")
newdf = df[~df['WorkEmail'].isin(jostleYesPhotoList)][['WorkEmail', 'FirstName', 'LastName']].reset_index(drop=True)

print(newdf)
# save the new dataframe to a CSV file
newdf.to_csv("C:\\Users\\dtaylor\\Documents\\Jostle Pictures Project\\jostleNoPhotoV2.csv", index=False)



