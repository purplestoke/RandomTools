from PIL import Image
import os
import re


# FUNCTION FOR READING METADATA
def retMetaData(image):
    try:
        with Image.open(image) as img:
            metadata = {
                "format": img.format,
                "info": img.info,
                "size": img.size,
            }
            print(metadata)

            if metadata:
                try:
                    print("Looking for Data")
                    if "DateTimeOriginal" in metadata["info"]:
                        date = metadata["info"]["DateTimeOriginal"]
                        print(date)
                        return 2, date
                    else:
                        raise KeyError("DateTimeOriginal not found in metadata")
                except KeyError as e:
                    print("No location in data")
                    return e, image
            else:
                return 3, image
    except Exception as e:
        return e, image


# FUNCTION WHICH READS THE DATE FROM METADATA AND SORTS ACCORDINGLY
def sortData(_metadata):
    lst = []
    pattern = re.compile(r"\b\d{4}:\d{2}:\d{2}\b")
    date = pattern.search(_metadata)
    if date:
        year, month = date.group(1).split(":")
        lst.append(year)
        lst.append(month)
        return 2, lst


# LOOP WHICH ITERATES OVER FILES IN DIR, READS METADATA & ORGANIZES BY DATE TAKEN YY / MM
def organizeTime(fromDir, toDir):
    messup = []
    # MAKE THE DIRECTORY WE ARE MOVING THE ORGANIZED FILES TO
    if not os.path.exists(toDir):
        os.makedirs(toDir)

    for filename in os.listdir(fromDir):
        filepath = os.path.join(fromDir, filename)

        if os.path.isfile(filepath):
            flag, metadata = retMetaData(filepath)
            if flag == 2:
                sortFlag, sortLst = sortData(metadata)
                if sortFlag == 2:
                    yearTaken = sortLst[0]
                    monthTaken = sortLst[1]
                    year_dir = os.path.join(toDir, yearTaken)
                    month_dir = os.path.join(year_dir, monthTaken)

                    for dir_path in [year_dir, month_dir]:
                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)

                        destination_path = os.path.join(month_dir, filename)
                        os.rename(filepath, destination_path)
                else:
                    messup.append(filepath)
            else:
                messup.append(filepath)
        else:
            messup.append(filepath)

    # ENDING OF FUNCTION
    logging = "SortFilesLogs.txt"
    with open(logging, "w") as fhand:
        for ting in messup:
            fhand.write(f"{ting}\n")

    fhand.close()
    print("Files sorted and any files which were unable to be read have been logged.")
    return
