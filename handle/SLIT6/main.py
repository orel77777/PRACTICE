import numpy as np
from astropy.io import fits
from scipy import integrate
from scipy.interpolate import interp1d
from sys import exit

# input: file_name
#        x1 		#(include)
#        x2		#(include)
#	 b		#'y' or 'n' substract atmpsphere lines

p0 = np.zeros((2),dtype=int)
p1 = np.zeros((2),dtype=int)

file_name = raw_input()
f = fits.open(file_name)
dd = f[0].data
header = f[0].header
p0[0] = int(raw_input())
p0[1] = 0
p1[0] = (int(raw_input()) + 1)
p1[1] = header['NAXIS2']
b = raw_input()

if (b == 'y'):
	for i in range(header['NAXIS2']):
		dd[i] -= (np.mean(dd[i,0:490]) + np.mean(dd[i,540:header['NAXIS1']]))/2
	out = fits.PrimaryHDU(dd)
	out.writeto(file_name[0:len(file_name)-5] + '_without_atm_lines.fts')

spec = dd[p0[1]:p1[1],p0[0]:p1[0]] #+1

energy_spec = np.zeros((spec.shape[0], 2))

for i in range(spec.shape[0]):
	energy_spec[i,0] = ((header['A_DISP'])+(header['B_DISP']*i)+(header['C_DISP']*i*i)+(header['D_DISP']*i*i*i))*(1e-8)
	energy_spec[i,1] = abs(np.mean(spec[i]))*(p1[0]-p0[0])*(header['NDRS']-1)

energy_spec[0,1] = (energy_spec[0,1]*2.2) / (energy_spec[1,0] - energy_spec[0,0]) #not mean

for i in range(1,spec.shape[0]):
	energy_spec[i,1] = (energy_spec[i,1]*2.2) / (energy_spec[i,0] - energy_spec[i-1,0])

#vega:
#	vegaY = 5.81e-2 erg/(cm^2*c*cm)
#	vegaJ = 3.14e-2 erg/(cm^2*c*cm)
#	vegaH = 1.20e-2 erg/(cm^2*c*cm)
#	vegaK = 0.412e-2 erg/(cm^2*c*cm)

np.savetxt(b+'_'+file_name[0:len(file_name)-5] + '_spectr_abs.txt', energy_spec, delimiter=' ', fmt = '%e')

wave_len, b_rel = np.loadtxt('uka0v.dat', usecols=[0,1], unpack=True)

mat_sgs = np.zeros((wave_len.shape[0],2))
for i in range(wave_len.shape[0]):
	mat_sgs[i,0] = (wave_len[i] * (1e-8))
	mat_sgs[i,1] = (b_rel[i])
list_filtr = ['F040JMKO.txt', 'F047HMKO.txt', 'F049KMKO.txt', 'F041YOS1.txt']
print file_name[9]
if(file_name[9] == 'J'):
	use_filt = list_filtr[0]
	e = 3.14e-2 #vega erg/(c*cm^2) in J; dlamda = 0.166mcm
	k_our = 10**((-5.901)/2.5)  #mJ=5.901
elif(file_name[9] == 'H'):
	use_filt = list_filtr[1]
	e = 1.20e-2 #vega erg/(c*cm^2) in H;dlamda = 0.288mcm
	k_our = 10**((-5.955)/2.5) #mH = 5.955
elif(file_name[9] == 'K'):
	use_filt = list_filtr[2]
	e = 0.412e-2 #vega erg/(c*cm^2) in K;dlamda = 0.314mcm
	k_our = 10**((-5.915)/2.5) #mK = 5.915
elif(file_name[9] == 'Y'):
	use_filt = list_filtr[3]
	e = 5.81e-2 #vega erg/(c*cm^2) in Y;dlamda = 0.200mcm
	k_our = 10**((-5.924)/2.5) #mY =~equal median 
else:
	print 'unknown [9] symbol of file_name(use Y,J,H,K)'
	sys.exit()
wave_len_tr, trans_proc = np.loadtxt(use_filt, usecols=[0,1], unpack=True)

mat_tr_sgs = np.zeros((wave_len_tr.shape[0],2)) #lambda_trans
mat_res = np.zeros((wave_len_tr.shape[0],2)) 

for i in range(wave_len_tr.shape[0]):
	mat_tr_sgs[i,0] = wave_len_tr[i] = (wave_len_tr[i] * (1e-7))
	mat_res[i,0] = mat_tr_sgs[i,0]
	mat_tr_sgs[i,1] = trans_proc[i] = (trans_proc[i]/100)

energ = e*integrate.simps(wave_len_tr, trans_proc)
j=0
for i in range(mat_sgs.shape[0]):
	if ( (j != mat_tr_sgs.shape[0]) and ((mat_sgs[mat_sgs.shape[0]-i-1,0] - mat_tr_sgs[j,0]) <1e-13)):
		mat_res[j,1] = (mat_tr_sgs[j,1]*mat_sgs[mat_sgs.shape[0]-i-1,1])
		j+=1

x = np.zeros(mat_res.shape[0])
y = np.zeros(mat_res.shape[0])

for i in range(x.shape[0]):
	x[i] = mat_res[i,0]
	y[i] = mat_res[i,1]

area = integrate.simps(x,y)
norm = area/energ
print 'sgs:'
print area
print norm

for i in range(mat_sgs.shape[0]):
	mat_sgs[i,1] = ((mat_sgs[i,1]/norm)*k_our*mat_sgs[i,0]*5.0341e15)
	mat_sgs[i,1] = mat_sgs[i,1]*header['ITIME']*49087.385 #*Texp*Stel

for i in range(mat_res.shape[0]):
	mat_res[i,1] = ((mat_res[i,1]/norm)*k_our*mat_res[i,0]*5.0341e15)
	mat_res[i,1] = mat_res[i,1]*header['ITIME']*49087.385 #*Texp*Stel

np.savetxt('our_star_phot.txt',mat_sgs,delimiter=' ',fmt='%e')
np.savetxt('our_star_phot'+file_name[9]+'.txt',mat_res,delimiter=' ',fmt='%e')

x1 = np.zeros(energy_spec.shape[0])
x2 = np.zeros(mat_res.shape[0])
y1 = np.zeros(energy_spec.shape[0])
y2 = np.zeros(mat_res.shape[0])
for i in range(energy_spec.shape[0]):
	x1[i] = energy_spec[i,0]
	y1[i] = energy_spec[i,1]
for i in range(mat_res.shape[0]):
	x2[mat_res.shape[0]-1-i] = mat_res[i,0]
	y2[mat_res.shape[0]-1-i] = mat_res[i,1]

y1 = np.interp(x1, x2, y2)
inter_matr = np.zeros((y1.shape[0],2))

for i in range(x1.shape[0]):
	inter_matr[i,0] = x1[i]
	inter_matr[i,1] = y1[i] = energy_spec[i,1]/y1[i]

np.savetxt('interpolated_teor_to_prac'+file_name[9]+'.txt', inter_matr, delimiter = ' ', fmt='%e')
