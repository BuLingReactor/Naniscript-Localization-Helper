import os
import glob
import pickle
import pandas as pd

class FileHandler:
    def __init__(self):
        self.original_folder_path = ''
        self.localization_folder_path = ''
        self.data = {}

    def setOriginalFolderPath(self, path):
        self.original_folder_path = path
        self.data = {}

    def setLocalizationFolderPath(self, path):
        self.localization_folder_path = path

    def getFiles(self):
        if self.original_folder_path and self.localization_folder_path:
            original_files = [os.path.basename(file) for file in glob.glob(os.path.join(self.original_folder_path, '*.nani'))]
            localization_files = [os.path.basename(file) for file in glob.glob(os.path.join(self.localization_folder_path, '*.nani'))]
            return sorted(list(set(original_files) & set(localization_files)))
        else:
            return []

    def saveData(self, filename, df):
        self.data[filename] = df

    def saveProgress(self):
        with open('progress.pkl', 'wb') as f:
            pickle.dump([self.original_folder_path, self.localization_folder_path], f)
 
    def loadProgress(self):
        with open('progress.pkl', 'rb') as f:
            self.original_folder_path, self.localization_folder_path = pickle.load(f)

    def saveAllToFile(self):
        for filename, df in self.data.items():
            output = []
            entered = False
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                cur = 0
                for line in lines:
                    text = line.strip()
                    if text.startswith(";"):
                        if entered == False:
                            output.append(line)
                    elif text.startswith("#"):
                        entered = True
                        if output != []:
                            output.append("")
                        output.append(line.strip())
                        if df.iloc[cur]["Speaker/Command"] == "":
                            output.append("; " + df.iloc[cur]["Original Text"])
                            output.append(df.iloc[cur]["Translated Text"])
                        elif df.iloc[cur]["Speaker/Command"].startswith("@"):
                            output.append("; " + df.iloc[cur]["Speaker/Command"] + " " + df.iloc[cur]["Original Text"])
                            output.append(df.iloc[cur]["Speaker/Command"] + " " + df.iloc[cur]["Translated Text"])
                        else:
                            output.append("; " + df.iloc[cur]["Speaker/Command"] + ": " + df.iloc[cur]["Original Text"])
                            output.append(df.iloc[cur]["Speaker/Command"] + ": " + df.iloc[cur]["Translated Text"])
                        cur += 1
                # df = pd.DataFrame(data, columns=['ID', 'Speaker/Command', 'Original Text', 'Translated Text'])
                # self.data[filename] = df
                # return df
            os.remove(filename)
            with open(filename, 'w', encoding='utf-8') as f:
                for line in output:
                    f.write(line + '\n')
            #df.to_csv(filename, index=False)

    def loadFile(self, filename):
        if filename in self.data:
            return self.data[filename]
        else:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                data = self.processFile(lines)
                df = pd.DataFrame(data, columns=['ID', 'Speaker/Command', 'Original Text', 'Translated Text'])
                self.data[filename] = df
                return df

    def processFile(self, lines):
        data = []
        block_entered = False
        ID = ''
        speaker = ''
        original_text = ''
        translated_text = ''
        for line in lines:
            if line.startswith('# '):
                if block_entered:
                    data.append([ID, speaker, original_text, translated_text])
                else:
                    block_entered = True
                ID = line[2:].strip()
                speaker = ''
                original_text = ''
                translated_text = ''
            elif line.startswith(';'):
                text = line[1:].strip()
                if text.startswith('@'):
                    if text.find(" ") != -1:
                        speaker, original_text = text.split(" ", 1)
                    else:
                        speaker = text
                else:
                    if text.find(":") != -1:
                        speaker, original_text = text.split(":", 1)
                    else:
                        original_text = text
            elif line.strip() != '':
                text = line.strip()
                if text.startswith('@'):
                    if text.find(" ") != -1:
                        speaker, translated_text = text.split(" ", 1)
                    else:
                        speaker = text
                elif text.find(":") != -1:
                    speaker, translated_text = text.split(":", 1)
                else:
                    translated_text = text
            ID = ID.strip()
            speaker = speaker.strip()
            original_text = original_text.strip()
            translated_text = translated_text.strip()

        if block_entered:
            data.append([ID, speaker, original_text, translated_text])
        return data
    
    def copyToClipboardProgress(self, clipboard):
        clipboard.setText("TE")

    def exportAllToSingleCSV(self, filename):
        df = pd.concat(self.data.values())
        df.to_csv(filename, index=False)

    def exportAllToXlsx(self, filename):
        df = pd.concat(self.data.values())
        df.to_excel(filename, index=False)

    def importFromCSV(self, filename):
        df = pd.read_csv(filename)
        df = df[df['Translated Text'].notna()]
        for sheet in self.data.values():
            for index, row in sheet.iterrows():
                row_id = row[0]
                if df[df['ID'] == row_id].empty == False and df[df['ID'] == row_id].values[0][3] != '':
                    row[3] = df[df['ID'] == row_id].values[0][3]