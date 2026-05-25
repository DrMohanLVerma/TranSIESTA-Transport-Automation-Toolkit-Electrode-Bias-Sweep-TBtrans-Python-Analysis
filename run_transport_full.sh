#!/bin/bash

echo "=========================================="
echo "  FULL TRANSPORT AUTOMATION WORKFLOW"
echo "=========================================="

NP=12   # number of processors

BASE_DIR=$(pwd)
RESULTS=transport_results

mkdir -p $RESULTS
cd $RESULTS

cp ../Elec/elec.HSX .

> IV.dat
mkdir -p cont

# ==============================
# FUNCTION: RUN SINGLE BIAS
# ==============================

run_bias () {
V=$1
echo "----------------------------------"
echo "Running bias: $V V"
echo "----------------------------------"

mkdir -p scat_$V
cd scat_$V

cp ../../*.psml .
cp ../elec.HSX .
cp ../../scat.fdf .

sed -i "s/TS.Voltage.*/TS.Voltage $V eV/" scat.fdf

cp ../cont/* . 2>/dev/null

mpirun --oversubscribe -np $NP siesta scat.fdf | tee scat.out

# ---- Check convergence ----
if ! grep -q "SCF converged" scat.out; then
    echo "⚠ Not converged → retrying with safer mixing"

    sed -i "s/DM.MixingWeight.*/DM.MixingWeight 0.002/" scat.fdf
    mpirun -np $NP siesta scat.fdf | tee scat_retry.out
fi

# ---- Run TBtrans ----
mpirun --oversubscribe -np $NP tbtrans scat.fdf | tee tbt.out

# ---- Extract current ----
I=$(grep 'Left -> Right, V \[V\] / I \[A\]:' tbt.out | tail -1 | awk '{print $12}')

echo "$V   $I" >> ../IV.dat

# ---- Save continuation ----
mkdir -p ../cont
cp scat.DM ../cont/ 2>/dev/null
cp scat.TSHS ../cont/ 2>/dev/null
cp scat.TSDE ../cont/ 2>/dev/null

cd ..
}

# ==============================
# STEP 1: ZERO BIAS
# ==============================

run_bias 0.0

# ==============================
# STEP 2: POSITIVE BIAS
# ==============================

for V in $(seq 0.1 0.1 1.0)
do
run_bias $V
done

# ==============================
# STEP 3: NEGATIVE BIAS
# ==============================

cp cont/* cont_backup/

for V in $(seq -0.1 -0.1 -1.0)
do
cp cont_backup/* cont/ 2>/dev/null
run_bias $V
done

# ==============================
# STEP 4: POST-PROCESSING
# ==============================

echo "Generating plots..."

python3 <<EOF
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from netCDF4 import Dataset

# -------- Load IV data --------
if not os.path.exists("IV.dat"):
    print("IV.dat not found")
    exit()

data = np.loadtxt("IV.dat")
data = data[data[:,0].argsort()]

V = data[:,0]
I = data[:,1]

# -------- I-V --------
plt.figure(figsize=(6,5))
plt.plot(V,I,'o-',linewidth=2)
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.title("I-V Curve")
plt.grid()
plt.savefig("IV_curve.png",dpi=300)

# -------- dI/dV --------
dIdV = np.gradient(I,V)

plt.figure(figsize=(6,5))
plt.plot(V,dIdV,linewidth=2)
plt.xlabel("Voltage (V)")
plt.ylabel("dI/dV")
plt.title("Differential Conductance")
plt.grid()
plt.savefig("dIdV.png",dpi=300)

# -------- Transmission (0 bias) --------
folders = sorted(glob.glob("scat_*"))

for f in folders:
    tbt_files = glob.glob(f + "/*.TBT.nc")
    if tbt_files:
        nc = Dataset(tbt_files[0])
        E = nc.variables['E'][:]
        T = nc.variables['transmission'][:]

        if T.ndim > 1:
            T = T.sum(axis=0)

        plt.figure(figsize=(6,5))
        plt.plot(E,T)
        plt.xlabel("Energy (eV)")
        plt.ylabel("T(E)")
        plt.title("Transmission: " + f)
        plt.axvline(0, linestyle='--')
        plt.grid()
        plt.savefig(f + "/Transmission.png", dpi=300)

print("All plots generated successfully")
EOF

echo "=========================================="
echo " WORKFLOW COMPLETE "
echo "=========================================="
