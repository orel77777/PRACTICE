import numpy as np
from scipy import integrate

wave_len, b_rel = np.loadtxt('uka0v.dat', usecols=[0,1], unpack=True)

mat_sgs = np.zeros((wave_len.shape[0],2))
for i in range(wave_len.shape[0]):
	mat_sgs[i,0] = (wave_len[i] * (10**(-8)))
	mat_sgs[i,1] = (b_rel[i])

wave_len_tr, trans_proc = np.loadtxt('F040JMKO.txt', usecols=[0,1], unpack=True)

mat_tr_sgs = np.zeros((wave_len_tr.shape[0],2)) #lambda_trans
mat_res = np.zeros((wave_len_tr.shape[0],2)) #shape == (301,2)

for i in range(wave_len_tr.shape[0]):
	mat_tr_sgs[i,0] = (wave_len_tr[i] * (10**(-7)))
	mat_res[i,0] = mat_tr_sgs[i,0]
	mat_tr_sgs[i,1] = (trans_proc[i]/100)
j=0
for i in range(mat_sgs.shape[0]):
	if ( (j != mat_tr_sgs.shape[0]) and ((mat_sgs[mat_sgs.shape[0]-i-1,0] - mat_tr_sgs[j,0]) < 0.000000001)):
		mat_res[j,1] = (mat_tr_sgs[j,1]*mat_sgs[mat_sgs.shape[0]-i-1,1])
		j+=1

x = np.zeros(mat_res.shape[0])
y = np.zeros(mat_res.shape[0])

for i in range(x.shape[0]):
	x[i] = mat_res[i,0]
	y[i] = mat_res[i,1]

area = integrate.simps(x,y)
energ = 5.21*10**(-7) ##vega erg/(c*cm^2) in J
norm = area/energ
print 'sgs:'
print area
print norm

for i in range(mat_sgs.shape[0]):
	mat_sgs[i,1] = mat_sgs[i,1]/norm

