import numpy as np
import matplotlib.pyplot as plt
import os

# =====================================================
# Physical constants
# =====================================================

e = 1.602176634e-19
h = 6.62607015e-34

G0 = 2*e**2/h

print("\n================================")
print("Conductance Quantum")
print("G0 =",G0," S")
print("================================\n")

# =====================================================
# Bias folders
# =====================================================

selected_bias=[
    "scat_0.3",
    "scat_0.5",
    "scat_0.7"
]

# =====================================================
# Helper function
# =====================================================

def load_transport_file(fname):

    try:

        data=np.loadtxt(
            fname,
            comments="#"
        )

        return data

    except Exception as e:

        print(
            "Error:",
            fname
        )

        print(e)

        return None


# =====================================================
# Transmission comparison
# =====================================================

plt.figure(figsize=(8,6))

for folder in selected_bias:

    file=f"{folder}/scat.TBT.AVTRANS_Left-Right"

    if not os.path.exists(file):
        continue

    data=load_transport_file(file)

    if data is None:
        continue

    E=data[:,0]
    T=data[:,1]

    bias=folder.replace(
        "scat_",
        ""
    )

    plt.plot(
        E,
        T,
        linewidth=2,
        label=f"{bias} V"
    )

plt.axvline(
    0,
    linestyle='--',
    linewidth=2,
    label='EF'
)

plt.xlabel(
    "Energy (eV)",
    fontsize=13
)

plt.ylabel(
    "Transmission T(E)",
    fontsize=13
)

plt.title(
    "Transmission Spectrum",
    fontsize=14
)

plt.legend()

plt.grid()

plt.tight_layout()

plt.savefig(
    "Transmission_comparison.png",
    dpi=600
)

plt.close()

print(
    "Saved: Transmission_comparison.png"
)

# =====================================================
# Conductance G/G0
# =====================================================

plt.figure(figsize=(8,6))

for folder in selected_bias:

    file=f"{folder}/scat.TBT.AVTRANS_Left-Right"

    if not os.path.exists(file):
        continue

    data=load_transport_file(file)

    if data is None:
        continue

    E=data[:,0]
    T=data[:,1]

    G=G0*T

    Gnorm=G/G0

    bias=folder.replace(
        "scat_",
        ""
    )

    plt.plot(
        E,
        Gnorm,
        linewidth=2,
        label=f"{bias} V"
    )

plt.axvline(
    0,
    linestyle='--',
    linewidth=2,
    label='EF'
)

plt.xlabel(
    "Energy (eV)",
    fontsize=13
)

plt.ylabel(
    r"Conductance ($G/G_0$)",
    fontsize=13
)

plt.title(
    "Normalized Conductance",
    fontsize=14
)

plt.legend()

plt.grid()

plt.tight_layout()

plt.savefig(
    "Conductance_normalized.png",
    dpi=600
)

plt.close()

print(
    "Saved: Conductance_normalized.png"
)

# =====================================================
# Conductance in microSiemens
# =====================================================

plt.figure(figsize=(8,6))

for folder in selected_bias:

    file=f"{folder}/scat.TBT.AVTRANS_Left-Right"

    if not os.path.exists(file):
        continue

    data=load_transport_file(file)

    if data is None:
        continue

    E=data[:,0]
    T=data[:,1]

    G=G0*T

    Gmicro=G*1e6

    bias=folder.replace(
        "scat_",
        ""
    )

    plt.plot(
        E,
        Gmicro,
        linewidth=2,
        label=f"{bias} V"
    )

plt.axvline(
    0,
    linestyle='--',
    linewidth=2,
    label='EF'
)

plt.xlabel(
    "Energy (eV)",
    fontsize=13
)

plt.ylabel(
    r"Conductance ($\mu S$)",
    fontsize=13
)

plt.title(
    "Conductance Spectrum",
    fontsize=14
)

plt.legend()

plt.grid()

plt.tight_layout()

plt.savefig(
    "Conductance_microS.png",
    dpi=600
)

plt.close()

print(
    "Saved: Conductance_microS.png"
)

# =====================================================
# Eigenchannels
# =====================================================

for folder in selected_bias:

    file=f"{folder}/scat.TBT.AVTEIG_Left-Right"

    if not os.path.exists(file):
        continue

    data=load_transport_file(file)

    if data is None:
        continue

    E=data[:,0]

    plt.figure(figsize=(8,6))

    max_channels=min(
        5,
        data.shape[1]-1
    )

    for i in range(
        1,
        max_channels+1
    ):

        plt.plot(
            E,
            data[:,i],
            linewidth=2,
            label=f"Channel {i}"
        )

    plt.axvline(
        0,
        linestyle='--'
    )

    bias=folder.replace(
        "scat_",
        ""
    )

    plt.xlabel(
        "Energy (eV)"
    )

    plt.ylabel(
        "Eigenchannel T"
    )

    plt.title(
        f"Eigenchannels ({bias} V)"
    )

    plt.legend()

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        f"{folder}/Eigenchannels.png",
        dpi=600
    )

    plt.close()

# =====================================================
# IV and dI/dV
# =====================================================

ivfile=None

if os.path.exists(
    "IV.dat"
):
    ivfile="IV.dat"

elif os.path.exists(
    "IV.csv"
):
    ivfile="IV.csv"

if ivfile:

    try:

        data=np.loadtxt(
            ivfile,
            comments="#",
            delimiter=","
        )

    except:

        data=np.loadtxt(
            ivfile
        )

    V=data[:,0]
    I=data[:,1]

    idx=np.argsort(V)

    V=V[idx]
    I=I[idx]

    # Current in microamp

    I_micro=I*1e6

    plt.figure(figsize=(8,6))

    plt.plot(
        V,
        I_micro,
        'o-',
        linewidth=2
    )

    plt.xlabel(
        "Bias Voltage (V)"
    )

    plt.ylabel(
        r"Current ($\mu A$)"
    )

    plt.title(
        "I-V Characteristics"
    )

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "IV_curve.png",
        dpi=600
    )

    plt.close()

    print(
        "Saved: IV_curve.png"
    )

    # dI/dV

    dIdV=np.gradient(
        I_micro,
        V
    )

    plt.figure(figsize=(8,6))

    plt.plot(
        V,
        dIdV,
        linewidth=2
    )

    plt.axhline(
        0,
        linestyle='--'
    )

    plt.xlabel(
        "Bias Voltage (V)"
    )

    plt.ylabel(
        r"dI/dV ($\mu A/V$)"
    )

    plt.title(
        "Differential Conductance"
    )

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "dIdV.png",
        dpi=600
    )

    plt.close()

    print(
        "Saved: dIdV.png"
    )

print("\n================================")
print("All plots generated successfully")
print("================================")
