import mido as md
import numpy as np
import matplotlib.pyplot as plt

mid = md.MidiFile('TeVasMilongaorig.mid')
times =np.array([m.time for m in mid])

offsets = np.cumsum(times)
register=[0]*128
matrix_register=[]

for message,time in zip(mid,offsets):
	if not isinstance(message, md.MetaMessage) and message.type=='note_on':
		note=message.note
		if message.velocity==0:
			beg=register[note][1]
			end=time
			matrix_register.append((note,beg,end))
		else:
			register[note]=(note,time);
windowSize = 4096*4
windowTime = windowSize/48000.0
matrixlen = int(round(matrix_register[-1][2]/windowTime))
chromamatrix = [[0]*12]*matrixlen
chromamatrix = np.array(chromamatrix,dtype=np.dtype('b'))
for el in matrix_register:
	note = el[0]
	octave = (note + 3) % 12
	beg = int(round(el[1]/windowTime))

	end = int(round(el[2]/windowTime))
	if beg==end:
		end = end + 1
	chromamatrix[beg:end,octave]=1
times = np.arange(0,matrixlen)*windowTime
times = times.reshape((matrixlen,1))

csvout= np.hstack((times,chromamatrix))
np.savetxt("out.csv",csvout,delimiter=",",fmt='%.3f')
# print chromamatrix[0]
# plt.yticks(np.arange(0,12))
# plt.imsh
# ow(np.transpose(chromamatrix), cmap='Greys',  interpolation='nearest')
# plt.show()

	#print chromamatrix[beg:end][octave]
	#print note,octave,beg,end
