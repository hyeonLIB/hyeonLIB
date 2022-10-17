import matplotlib.pyplot as plt

def plt_performance(history, path='./', filename=''):
    epoch = list(range(0,len(history.history['loss'])))
    
    fig, (his_accuracy, his_loss) = plt.subplots(nrows=2,ncols=1,figsize=(10,8),sharex=True)
    his_loss.plot(epoch, history.history['loss'], label='Training loss')
    his_loss.plot(epoch, history.history['val_loss'], label='Validation loss')
    his_loss.set_xlabel("Epochs", fontsize=14)
    his_loss.set_ylabel("Loss", fontsize=14)
    his_loss.set_title("Loss", fontsize=14)
    his_loss.legend(loc='best')
    
    his_accuracy.plot(epoch, history.history['acc'], label='Training accuracy')
    his_accuracy.plot(epoch, history.history['val_acc'], label='Validation accuracy')
    his_accuracy.set_xlabel("Epochs", fontsize=14)
    his_accuracy.set_ylabel("Accuracy", fontsize=14)
    his_accuracy.set_title("Accuracy", fontsize=14)
    his_accuracy.legend(loc='best')
    
    fig.tight_layout()
    if filename == '':
        plt.savefig(f'{path}/performance.png', bbox_inches='tight')
    else:
        plt.savefig(f'{path}/{filename}.png', bbox_inches='tight')
        
        
def segmenting_1_second(PPG_data):
    """ PPG_data = Whole PPG data (40 participants) """
    
    import neurokit2.ppg.ppg_findpeaks as findpeaks
    
    result, peaks, diff_sig_2 = get_peaks(preprocessed[0])
    
    result = findpeaks(preprocessed[0], sampling_rate=128, show=True)
    print(result)

    segmented = []
    index = 0
    cal= 0

    for i in range(0,22):
        for PPG in preprocessed:

            tmp = []
            result = findpeaks(PPG, sampling_rate=128)
            a = result['PPG_Peaks']
            for idx in a:
                a = idx
                if a > 70:
                    seg = PPG[a-70:a+70]
                    times = list(range(0,len(seg)))
                else:
                    seg = PPG[0:a+70]
                    times = list(range(0,len(seg)))
                if len(seg) == 140:
                    cal+=1
                    tmp.append(seg)

            segmented.append(tmp)
            index += 1