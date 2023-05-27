from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_silence
import os
import wave
import time
import pickle
import pyaudio
import warnings
import numpy as np
from sklearn import preprocessing
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn.mixture import GaussianMixture
import speech_recognition as sr
import math


def calculate_delta(array):
    rows, cols = array.shape
    print(rows)
    print(cols)
    deltas = np.zeros((rows, 20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows-1:
                second = rows-1
            else:
                second = i+j
            index.append((second, first))
            j += 1
        deltas[i] = (array[index[0][0]]-array[index[0][1]] +
                     (2 * (array[index[1][0]]-array[index[1][1]]))) / 10
    return deltas

def extract_features(audio, rate):
    mfcc_feature = mfcc.mfcc(audio, rate, 0.025, 0.01, 20, nfft=1200, appendEnergy=True)
    mfcc_feature = preprocessing.scale(mfcc_feature)
    print(mfcc_feature)
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature, delta))
    return combined

def train_model():

    source = "conversation_analysis/training_set/"
    dest = "conversation_analysis/trained_models/"
    train_file = "conversation_analysis/training_set_addition.txt"
    file_paths = open(train_file, 'r')
    count = 1
    features = np.asarray(())
    for path in file_paths:
        path = path.strip()
        print(path)

        sr, audio = read(source + path)
        print(sr)
        vector = extract_features(audio, sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

        if count == 5:
            gmm = GaussianMixture(
                n_components=6, max_iter=200, covariance_type='diag', n_init=3)
            gmm.fit(features)

            # dumping the trained gaussian model
            picklefile = path.split("-")[0]+".gmm"
            pickle.dump(gmm, open(dest + picklefile, 'wb'))
            print('+ modeling completed for speaker:', picklefile,
                  " with data point = ", features.shape)
            features = np.asarray(())
            count = 0
        count = count + 1

def test_model():

    source = "conversation_analysis/testing_set/"
    modelpath = "conversation_analysis/trained_models/"
    test_file = "conversation_analysis/testing_set_addition.txt"
    file_paths = open(test_file, 'r')
    result=""

    gmm_files = [os.path.join(modelpath, fname) for fname in 
                 os.listdir(modelpath) if fname.endswith('.gmm')]      #### making a list of trained model files paths

    # Load the Gaussian gender Models
    models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]
    speakers = [fname.split("\\")[-1].split(".gmm")[0] for fname
                in gmm_files]

    # Read the test directory and get the list of test audio files
    for path in file_paths:
        path = path.strip() #removes white space in path (in this case path is 'sample.wav' written in testing_set_addition.txt)
        print(path)
        sr, audio = read(source + path) #reading wav file

        vector = extract_features(audio, sr)

        log_likelihood = np.zeros(len(models))

        for i in range(len(models)):
            gmm = models[i]  # checking with each model one by one
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()

        winner = np.argmax(log_likelihood)
        #print(speakers[winner][17:])
        result=speakers[winner][37:]
        time.sleep(1.0)
    return result

def split_audio(myaudio):
    song = AudioSegment.from_wav(myaudio)
    silence_ranges_list=detect_silence(audio_segment=song, min_silence_len=500, silence_thresh=-25, seek_step=1)
    # print(silence_ranges_list)
    # print(len(silence_ranges_list))
    mytalk=[]
    nonsilence_ranges_list=[]
    for i in range(len(silence_ranges_list)-1):
        newAudio = AudioSegment.from_file(myaudio)
        tx=silence_ranges_list[i][1]-500
        ty=silence_ranges_list[i+1][0]+500
        nonsilence_ranges_list.append([tx,ty])
        newAudio = newAudio[tx:ty]
        print(tx,ty)
        newAudio.export('conversation_analysis/testing_set/temp_sample.wav', format="wav")
        mytalk.append(test_model())
        time.sleep(0.1)
    # print(mytalk)
    # print(len(mytalk))
    def create_labelling(labels):
        labelling = []
        start_time = nonsilence_ranges_list[0][0]
        for i in range(len(mytalk)):
            if i>0 and labels[i]!=labels[i-1]:
                    temp = [str(labels[i-1]),start_time,nonsilence_ranges_list[i-1][1]]
                    labelling.append(tuple(temp))
                    start_time = nonsilence_ranges_list[i][0]        
            if i==len(nonsilence_ranges_list)-1:
                    temp = [str(labels[i]),start_time,nonsilence_ranges_list[i][1]]
                    labelling.append(tuple(temp))
        return labelling
    labelling = create_labelling(mytalk)
    print(labelling)
    print(len(labelling))
    return labelling

def speech_to_dialogue(labelling):
    r = sr.Recognizer()
    dialogue_length = len(labelling)
    conversation = ""

    #audio = r.listen('Small Talk2.wav', phrase_time_limit=20)

    for i in range(dialogue_length):
        newAudio = AudioSegment.from_file("conversation_analysis/conversation_audio/conversation00.wav")
        t1=labelling[i][1]
        t2=labelling[i][2]
        newAudio = newAudio[t1:t2]
        newAudio.export('tempAudio.wav', format="wav")
        try:
            clean_support_call = sr.AudioFile('tempAudio.wav')
            with clean_support_call as source:
                clean_support_call_audio = r.record(source)
            mytext = r.recognize_google(clean_support_call_audio, language="en-US")
            #print("You said : {}".format(mytext))
            language = 'en'
            conversation = conversation+labelling[i][0]+":"+mytext+"\n"

        except sr.UnknownValueError:
            print("Sorry, could not recognize what you said or you stopped talking")
      
        # note that there is an error called request error that happens when internet service is poor (in video in links)
        except sr.RequestError:
            print("Request error")
    print(conversation)
    return conversation

def patient_train(audioFilePath):
    audio = AudioSegment.from_file(audioFilePath)
    length_ms = len(audio)
    print(length_ms)
    sub_length=math.floor(length_ms/5)
    for i in range (0,5):
        tx=i*sub_length
        ty=((i+1)*sub_length)
        tempaudio = audio[tx:ty]
        tempaudio.export(f'conversation_analysis/training_set/me-sample{i}.wav', format="wav")
        print(tx, "to", ty)
    train_model()

def speaker_train(audioFilePath):
    audio = AudioSegment.from_file(audioFilePath)
    length_ms = len(audio)
    print(length_ms)
    sub_length=math.floor(length_ms/5)
    for i in range (0,5):
        tx=i*sub_length
        ty=(i+1)*sub_length
        tempaudio = audio[tx:ty]
        tempaudio.export(f'conversation_analysis/training_set/speaker-sample{i}.wav', format="wav")
        # print(i*sub_length, "to", (i+1)*sub_length)
    train_model()

def main_function(audioPatient, audioConversation): # input the patient's audio path and the conversation's audio path, and output the conversation in the form of a dialogue
    patient_train(audioPatient)
    temp_labelling=split_audio(audioConversation)
    conversation = speech_to_dialogue(temp_labelling)
    return conversation

# Patient='./patients_audio/patient00.wav'
# Conversation='./conversation_audio/conversation00.wav'

# print(main_function(Patient,Conversation))