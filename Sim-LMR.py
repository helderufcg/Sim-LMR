import os
import sys
import time
import matplotlib.pyplot as plt
from numpy import *


class LMR(object):
    def __init__(self):
        # Attributes:
        self.theta_i = []  # List of angles of incidence
        self.d = []  # Thickness
        self.nLayers = 0  # Number of layers
        self.material = []  # List with the materials of each layer
        self.indexRef = []  # List with refractive index of each layer
        self.R_TM_i = []  # TM polarization reflectance
        self.R_TE_i = []  # TE polarization reflectance

        self.R_TM = []  # List with reflectance values for plotting multiple curves in TM polarization
        self.R_TE = []  # List with reflectance values for plotting multiple curves in TE polarization

        self.Resonance_Point_TM = []  # Resonance angle or resonance wavelength  on TM polarization
        self.Resonance_Point_TE = []  # Resonance angle or resonance wavelength  on TE polarization

        self.critical_point = []  # threshold angle for Attenuated Total Reflection
        self.analyte_index_0 = 0  # Initial refractive index of analyte
        self.index_ref_ana = []  # List with analyte refraction indices for graph plotting
        self.S_TM = []  # List with Sensibility values in TM polarization
        self.S_TE = []  # List with Sensibility values in TE polarization

        self.Fwhm_TM = []  # List with FWHM values in TM polarization
        self.Fwhm_TE = []  # List with FWHM values in TM polarization

        self.FOM_TM, self.FOM_TE = [], []  # Lists with the QF in TM and TE  polarizations
        self.inter = 0  # Number of interactions for sensitivity analyses
        self.step_shift = 0  # Variation of the refractive index of the analyte for sensitivity analyses

        # Method that selects sensor configuration: Kretschmann ou Optical Fiber.
        while True:
            try:
                self.config = int(
                    input("Select a configuration:\n1 - Kretschmann\n2 - Optical Fiber\n-> "))
                if self.config < 1 or self.config > 2:
                    print("Invalid option selected")
                else:
                    if self.config == 1:
                        print("\nKretschmann configuration\n")
                    else:
                        print("\nConfiguration using Optical Fiber\n")
                    break
            except ValueError:
                print("- {!} - \nPlease select some option...\n")

        # Kretschmann configuration
        if self.config == 1:
            # Method that selects a interrogation mode: Angular ou Wavelength.
            while True:
                try:
                    self.mod_int = int(
                        input("Select an interrogation mode:\n1 - Angular (AIM)\n2 - Wavelength (WIM)\n-> "))
                    if self.mod_int < 1 or self.mod_int > 2:
                        print("Invalid option selected")
                    else:
                        t = "Angular" if self.mod_int == 1 else "Wavelength"
                        print(f'\n{t} Interrogation Mode\n')
                        break
                except ValueError:
                    print("- {!} - \nPlease select some option...\n")

            # Angular interrogation mode
            if self.mod_int == 1:
                # Initial angle of incidence
                while True:
                    try:
                        self.a1 = float(input("Initial angle (0° - 90°):\n-> ")) * (pi / 180)
                        if 0 <= self.a1 < (pi / 2):
                            break
                        else:
                            print("Value out of range (0° -> 90°)!")
                    except ValueError:
                        print("- {!} - \nEnter an angle\n")

                # Final angle of incidence
                while True:
                    try:
                        self.a2 = float(input("Final angle of incidence (Initial angle -> 90°):\n-> ")) * (pi / 180)
                        if self.a1 < self.a2 <= (pi / 2):
                            break
                        else:
                            print("Value out of range (> Initial angle - 90° <)!")
                    except ValueError:
                        print("- {!} - \nEnter an angle\n")

                # Angle shift step
                while True:
                    try:
                        self.step_var = float(input("Angle shift step (°):\n-> ")) * (pi / 180)
                        if 0 < self.step_var < (self.a2 - self.a1):
                            break
                        else:
                            print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")
                    except ValueError:
                        print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")

                # Incident beam wavelength
                while True:
                    try:
                        self.wavelenght = float(input("Wavelength (nm):\n-> ")) * 1e-9
                        if self.wavelenght <= 0:
                            print("- {!} - \nInvalid Value!\nPlease enter a positive number...\n")
                        else:
                            break
                    except ValueError:
                        print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")

                # Method that asks the user for the characteristics of the layers
                self.setLayers()

                # Analyte layer indication
                while True:
                    try:
                        self.layer_A = (int(input("\nAnalyte layer: ")) - 1)  # Analyte layer
                        if 0 <= self.layer_A < self.nLayers:
                            print(f"\nThe {self.layer_A + 1}th layer is the analyte\n")
                            break
                        else:
                            print(f'\nInvalid Value!\ntry another number between 1 and {self.nLayers};')
                    except ValueError:
                        print("- {!} - \nInvalid Value!\nPlease enter a integer...\n")

                # Method that ask the user for the number of iterations and
                # the change in the index of refraction of the analyte
                self.sensibility()

                print("\n.......................... {!} We are Calculating {!} ..........................\n ")
                time.sleep(1)
                # Method that calculates sensitivity and other quality indicators
                self.calculation(self.inter)

                # Method that shows the graphs:
                # (1) Reflectance vs. Angle of Incidence,
                # (2) Reflectance vs. Angle of Incidence Given the Variation of the Refractive Index of the Analyte
                # (3) Angular Sensibility vs. Refractive Index of the Analyte
                # (4) Resonance Angle vs. Refractive Index of the Analyte
                # (5) Full Width at Half Maximum vs. Refractive Index of the Analyte and"
                # (6) Quality Factor vs. Refractive Index of the Analyte"
                self.plot(self.inter, self.index_ref_ana)

            # Wavelength interrogation mode
            else:
                print("\n========================== {!} Feature Under Development {!} ==========================\n ")

        # Configuration using Optical Fiber
        else:
            print("\n========================== {!} Feature Under Development {!} ==========================\n ")

    def setLayers(self):
        # Defines the characteristics of each layer
        print(
            "\n-------------------------------- Set Layers Characteristics --------------------------------\n"
            "--------------------------------------------------------------------------------------------")
        print("*-- Layer 01 --*")
        self.d.append(1)  # Assigning of Thickness
        # Assigning materials in the first layer
        while True:
            try:
                print(f"\n1 - BK7   2 - Silica   3 - N-F2   4 - Synthetic sapphire(Al2O3)"
                      f"\n5 - SFL6  6 - FK51A    7 - N-SF14 8 - Acrylic SUVT "
                      f"\n9 - Other  ")
                material = (int(input(f"\nMaterial -> ")))
                if material > 0:
                    self.material.append(material)  # Assignment of materials
                    if material == 9:
                        self.indexRef.append(self.set_index_Angular())  # Assignment of refractive index
                    else:
                        self.indexRef.append(self.set_index(material, self.wavelenght))
                    self.nLayers = len(self.indexRef)
                    break
                else:
                    print("- {!} - \nInvalid Value!\nPlease enter a positive number...\n")
            except ValueError:
                print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")

        # Assigning new layers
        while True:
            opt = None
            try:
                opt = int(input("--------------------------------------------------------------------------------------"
                                "------\n1 - New layer with another material \n2 - Replicate the previous layer\n"
                                "3 - Layer assignments are complete\n -> "))
            except ValueError:
                print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")

            # It inserts a new layer
            if opt == 1:
                print(f"\n*-- Layer {(self.nLayers + 1)} --*")
                # Assignment of materials
                while True:
                    try:
                        print(f"\n 1 - BK7     2 - Silica      3 - N-F2       4 - Synthetic sapphire(Al2O3) "
                              f"\n 5 - SFL6    6 - FK51A       7 - N-SF14     8 - Acrylic SUVT"
                              f"\n 9 - PVA    10 - Glycerin   11 - Quartz    12 - Aluminium"
                              f"\n13 - Gold   14 - Silver     15 - Copper    16 - Water (RI = 1.33)"
                              f"\n17 - Air    18 - LiF        19 - Cytop     20 - Other")
                        material = (int(input(f"\nMaterial -> ")))
                        if material > 0:
                            self.material.append(material)  # Assignment of materials
                            if material == 20:
                                self.indexRef.append(self.set_index_Angular())  # Assignment of refractive index
                            else:
                                self.indexRef.append(self.set_index(material, self.wavelenght))
                            self.nLayers = len(self.indexRef)
                            break
                        else:
                            print("- {!} - \nInvalid Value!\nPlease enter a positive number...\n")
                    except ValueError:
                        print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")
                # Assignment of Thickness
                while True:
                    try:
                        d = float(input("Thickness (nm): ")) * 1e-9
                        if d > 0:
                            self.d.append(d)
                            break
                        else:
                            print("- {!} - \nInvalid Value!\nPlease enter a positive number...\n")
                    except ValueError:
                        print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")

            # it replicates the previous layer
            elif opt == 2:
                while True:
                    try:
                        n = int(input("How many times do you want to repeat the previous layer?\n -> "))
                        for i in range(n):
                            print(f"*-- Layer {(self.nLayers + 1)} --*\n -> OK ")
                            self.d.append(self.d[-1])
                            self.indexRef.append(self.indexRef[-1])
                            self.material.append(self.material[-1])
                            self.nLayers = len(self.indexRef)
                        break
                    except ValueError:
                        print("- {!} - \nInvalid Value!\nPlease enter a integer...\n")

            # Layer assignment is complete
            elif opt == 3:
                break
            else:
                print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")

        self.nLayers = len(self.indexRef)
        print(
            f'\n-------------------- Structure with {self.nLayers}-layers was successfully built --------------------\n'
            '----------------------------------------------------------------------------------------')

    @staticmethod
    def set_index(material, wi):
        B1, B2, B3, C1, C2, C3, X, n, k_index = 0, 0, 0, 0, 0, 0, [], [], []  # Initialization of variables
        Lambda_i = wi * 1e6  # Incidence Wavelength in micrometers
        j = 0 + 1j
        # Materials that compose the prisms, modeled by the Sellmeier equation according to the RefractiveIndex.info
        # https://refractiveindex.info/
        if 0 < material <= 8:
            if material == 1:  # BK7
                B1, B2, B3, C1, C2, C3 = 1.03961212, 2.31792344E-1, 1.01046945, 6.00069867E-3, 2.00179144E-2, 103.560653

            elif material == 2:  # Silica
                B1, B2, B3, C1, C2, C3 = 0.6961663, 0.4079426, 0.8974794, 4.6791E-3, 1.35121E-2, 97.934003

            elif material == 3:  # N-F2
                B1, B2, B3, C1, C2, C3 = 1.39757037, 1.59201403E-1, 1.2686543, 9.95906143E-3, 5.46931752E-2, 119.2483460

            elif material == 4:  # Synthetic Sapphire(Al2O3)
                B1, B2, B3, C1, C2, C3 = 1.4313493, 0.65054713, 5.3414021, 0.00527993, 0.0142383, 325.01783

            elif material == 5:  # SF2
                B1, B2, B3, C1, C2, C3 = 1.78922056, 3.28427448E-1, 2.01639441, 1.35163537E-2, 6.22729599E-2, 168.014713

            elif material == 6:  # FK51A
                B1, B2, B3, C1, C2, C3 = 0.971247817, 0.216901417, 0.904651666, 0.00472301995, 0.0153575612, 168.68133

            elif material == 7:  # N-SF14
                B1, B2, B3, C1, C2, C3 = 1.69022361, 0.288870052, 1.704518700, 0.01305121130, 0.0613691880, 149.5176890

            elif material == 8:  # Acrylic SUVT
                B1, B2, B3, C1, C2, C3 = 0.59411, 0.59423, 0, 0.010837, 0.0099968, 0

            # Sellmeier equation
            n = sqrt(1 + ((B1 * Lambda_i ** 2) / (Lambda_i ** 2 - C1)) + ((B2 * Lambda_i ** 2) / (Lambda_i ** 2 - C2))
                     + ((B3 * Lambda_i ** 2) / (Lambda_i ** 2 - C3)))

        # Glycerol e PVA according to the RefractiveIndex.info: https://refractiveindex.info/
        elif 8 < material <= 10:
            if material == 9:  # PVA
                B1, B2, B3, C1, C2, C3 = 1.460, 0.00665, 0, 0, 0, 0
            elif material == 10:  # Glycerin/glycerol
                B1, B2, B3, C1, C2, C3 = 1.45797, 0.00598, -0.00036, 0, 0, 0
            # Equation that models the refractive index as a function of wavelength
            n = B1 + (B2 / Lambda_i ** 2) + (B3 / Lambda_i ** 4)

        # Quartz according to the RefractiveIndex.info: https://refractiveindex.info/
        elif 10 < material <= 11:
            B1, B2, B3, C1, C2, C3 = 2.356764950, -1.139969240E-2, 1.087416560E-2, 3.320669140E-5, 1.086093460E-5, 0
            n = sqrt(B1 + (B2 * Lambda_i ** 2) + (B3 / Lambda_i ** 2) + (C1 / Lambda_i ** 4) + (C2 / Lambda_i ** 6))

        # Metals
        elif 11 < material <= 15:
            """
            X - Wavelength in micrometers,
            n - Real part of the refractive index e k_index - Imaginary part of the refractive index
            according to Johnson and Christy, 1972
            """
            if material == 12:  # Refractive index of Aluminum according to the Drude model
                LambdaP, LambdaC = 1.0657E-7, 2.4511E-5
                n = sqrt(1 - (((wi ** 2) * LambdaC) / ((LambdaC + (j * wi)) * (LambdaP ** 2))))
            elif material == 13:  # Gold
                X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313, 0.2371,
                     0.2426, 0.2490, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107, 0.3204, 0.3315,
                     0.3425, 0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714, 0.4959, 0.5209, 0.5486,
                     0.5821, 0.6168, 0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088, 1.216, 1.393, 1.61, 1.937, 3.5]

                n = [1.28, 1.32, 1.34, 1.33, 1.33, 1.30, 1.30, 1.30, 1.30, 1.31, 1.30, 1.32, 1.32,
                     1.33, 1.33, 1.35, 1.38, 1.43, 1.47, 1.49, 1.53, 1.53, 1.54,
                     1.48, 1.48, 1.50, 1.48, 1.46, 1.47, 1.46, 1.45, 1.38, 1.31, 1.04,
                     0.62, 0.43, 0.29, 0.21, 0.14, 0.13, 0.14, 0.16, 0.17, 0.22, 0.27, 0.35, 0.43, 0.56, 0.92, 1.8]

                k_index = [1.188, 1.203, 1.226, 1.251, 1.277, 1.304, 1.35, 1.387, 1.427, 1.46, 1.497, 1.536, 1.577,
                           1.631,
                           1.688, 1.749, 1.803, 1.847, 1.869, 1.878, 1.889, 1.893, 1.898, 1.883, 1.871, 1.866, 1.895,
                           1.933,
                           1.952, 1.958, 1.948, 1.914, 1.849, 1.833, 2.081, 2.455, 2.863, 3.272, 3.697, 4.103, 4.542,
                           5.083,
                           5.663, 6.35, 7.15, 8.145, 9.519, 11.21, 13.78, 25]

            elif material == 14:  # Silver
                X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313,
                     0.2371, 0.2426, 0.249, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107,
                     0.3204, 0.3315, 0.3425, 0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714,
                     0.4959, 0.5209, 0.5486, 0.5821, 0.6168, 0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088,
                     1.216, 1.393, 1.61, 1.937, 5]

                n = [1.07, 1.1, 1.12, 1.14, 1.15, 1.18, 1.2, 1.22, 1.25, 1.26, 1.28, 1.28, 1.3, 1.31, 1.33, 1.35,
                     1.38, 1.41, 1.41, 1.39, 1.34, 1.13, 0.81, 0.17, 0.14, 0.1, 0.07, 0.05, 0.05, 0.05, 0.04, 0.04,
                     0.05, 0.05, 0.05, 0.06, 0.05, 0.06, 0.05, 0.04, 0.03, 0.04, 0.04, 0.04, 0.04, 0.09, 0.13, 0.15,
                     0.24, 2]

                k_index = [1.212, 1.232, 1.255, 1.277, 1.296, 1.312, 1.325, 1.336, 1.342, 1.344, 1.357, 1.367, 1.378,
                           1.389, 1.393, 1.387, 1.372, 1.331, 1.264, 1.161, 0.964, 0.616, 0.392, 0.829, 1.142, 1.419,
                           1.657, 1.864, 2.07, 2.275, 2.462, 2.657, 2.869, 3.093, 3.324, 3.586, 3.858, 4.152, 4.483,
                           4.838,
                           5.242, 5.727, 6.312, 6.992, 7.795, 8.828, 10.1, 11.85, 14.08, 35]

            elif material == 15:  # Copper
                X = [0.1879, 0.1916, 0.1953, 0.1993, 0.2033, 0.2073, 0.2119, 0.2164, 0.2214, 0.2262, 0.2313, 0.2371,
                     0.2426, 0.249, 0.2551, 0.2616, 0.2689, 0.2761, 0.2844, 0.2924, 0.3009, 0.3107, 0.3204, 0.3315,
                     0.3425,
                     0.3542, 0.3679, 0.3815, 0.3974, 0.4133, 0.4305, 0.4509, 0.4714, 0.4959, 0.5209, 0.5486, 0.5821,
                     0.6168,
                     0.6595, 0.7045, 0.756, 0.8211, 0.892, 0.984, 1.088, 1.216, 1.393, 1.61, 1.937, 5]

                n = [0.94, 0.95, 0.97, 0.98, 0.99, 1.01, 1.04, 1.08, 1.13, 1.18, 1.23, 1.28, 1.34, 1.37, 1.41, 1.41,
                     1.45,
                     1.46, 1.45, 1.42, 1.4, 1.38, 1.38, 1.34, 1.36, 1.37, 1.36, 1.33, 1.32, 1.28, 1.25, 1.24, 1.25,
                     1.22, 1.18,
                     1.02, 0.7, 0.3, 0.22, 0.21, 0.24, 0.26, 0.3, 0.32, 0.36, 0.48, 0.6, 0.76, 1.09, 2.5]

                k_index = [1.337, 1.388, 1.44, 1.493, 1.55, 1.599, 1.651, 1.699, 1.737, 1.768, 1.792, 1.802, 1.799,
                           1.783, 1.741, 1.691,
                           1.668, 1.646, 1.633, 1.633, 1.679, 1.729, 1.783, 1.821, 1.864, 1.916, 1.975, 2.045, 2.116,
                           2.207, 2.305, 2.397,
                           2.483, 2.564, 2.608, 2.577, 2.704, 3.205, 3.747, 4.205, 4.665, 5.18, 5.768, 6.421, 7.217,
                           8.245, 9.439, 11.12, 13.43, 35]

            # Method that calculates the refractive indices of the metals by linear interpolation
            # using the points contained in X, n e k_index previously described
            n_interp = interp(Lambda_i, X, n)
            k_interp = interp(Lambda_i, X, k_index)
            n = complex(n_interp, k_interp)

        # Refractive index of the Water
        elif material == 16:
            n = 1.33

        # Refractive index of the Air
        elif material == 17:
            n = 1.0000

        # Refractive index of the LiF (Lithium Fluoride) according to the RefractiveIndex.info:
        # https://refractiveindex.info/
        elif material == 18:
            B1, B2, B3, C1, C2, C3 = 0.92549, 6.96747, 0, 5.4405376E-3, 1075.1841, 0
            n = sqrt(1 + ((B1 * Lambda_i ** 2) / (Lambda_i ** 2 - C1)) + ((B2 * Lambda_i ** 2) / (Lambda_i ** 2 - C2))
                     + ((B3 * Lambda_i ** 2) / (Lambda_i ** 2 - C3)))

        elif material == 19:  # Cytop
            # According to the AGC chemicals company. Available in:
            # https://www.agc-chemicals.com/jp/en/fluorine/products/cytop/download/index.html
            X = [0.238, 0.245, 0.275, 0.313, 0.365, 0.407, 0.436, 0.546, 0.589, 0.633, 1.3, 1.55]

            n_cy = [1.35764, 1.35637, 1.35393, 1.35132, 1.34840, 1.34566, 1.34404, 1.3402, 1.34, 1.3395, 1.3348, 1.3335]

            # Method that calculates the refractive indices of the metals by linear interpolation
            # using the points contained in X, n e k_index previously described
            n = complex(interp(Lambda_i, X, n_cy))

        n0 = round(real(n), 5)  # Rounded to five decimal places
        k0 = round(imag(n), 5)  # Rounded to five decimal places

        return n0 + k0 * j  # Returns the complex refractive index for each material

    @staticmethod
    def set_index_Angular():
        while True:
            try:
                id_real = float(input(f"Refractive index:\n    * Real part: -> "))
                id_imaginary = float(input(f"    * Imaginary part: -> "))
                break
            except ValueError:
                print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")
        return complex(id_real, id_imaginary)

    def sensibility(self):
        # Method that ask the user for the number of iterations and
        # the change in the index of refraction of the analyte

        while True:
            try:
                self.inter = int(input("Analyze sensitivity in how many interactions?\n-> "))
                if self.inter < 0:
                    print("- {!} - \nInvalid Value!\nPlease enter a positive number...\n")
                else:
                    break
            except ValueError:
                print("- {!} - \nInvalid Value!\nPlease enter a integer...\n")
        while True:
            try:
                self.step_shift = float(input("Refractive index increment (RIU) =  "))
                if self.step_shift < 0:
                    print("- {!} - \nInvalid Value!\nPlease enter a positive number...\n")
                else:
                    break
            except ValueError:
                print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")

    def calculation(self, i):
        # the method self.calculation() receives the number (i) of variations in the refractive index of the analyte,
        # it calculates the resonance angle, sensitivity, full width at half maximum and quality factor
        # and displays the results by the method: self.display_results()
        # delta_X -> variation of the resonance angle given the variation of the refractive index of the analyte
        delta_X_TM, delta_X_TE = 0, 0
        s = None

        for s in range(i):
            if self.mod_int == 1:
                # Update of the analyte refractive index for sensitivity analysis
                if s == 0:
                    self.analyte_index_0 = self.indexRef[self.layer_A]
                self.indexRef[self.layer_A] = complex(round(self.analyte_index_0.real + (self.step_shift * s), 4), 0)

                # It calculates the critical angle of attenuated total reflection
                self.critical_point.append(abs(arcsin(self.analyte_index_0 / self.indexRef[0]) * (180 / pi)))

            self.theta_i = arange(self.a1, self.a2, self.step_var)  # List with angles of incidence

            # Local variable that temporarily stores reflectance values for each of the interactions
            r_tm, r_te = self.ReflectanceAux(self.mod_int)

            # List with the refractive indexes of the analyte to plot the graphs
            self.index_ref_ana.append(self.indexRef[self.layer_A])

            # Resonance angles obtained from the graph
            self.Resonance_Point_TM.append(self.Point_LMR(r_tm, s))
            self.Resonance_Point_TE.append(self.Point_LMR(r_te, s))

            # It stores the lists with the reflectance curves for each of the interactions
            self.R_TM.append(r_tm)
            self.R_TE.append(r_te)

            # Sensibility obtained from the graph

            # Resonance point variation
            delta_X_TM = self.Resonance_Point_TM[s] - self.Resonance_Point_TM[0]
            delta_X_TE = self.Resonance_Point_TE[s] - self.Resonance_Point_TE[0]

            # Refractive index variation
            delta_index = self.indexRef[self.layer_A].real - self.analyte_index_0.real

            # It calculates the angular sensitivity (Resonance point variation)/(Refractive index variation)
            if s == 0:
                # The first interaction is initialized to zero because the ratio would be 0/0
                self.S_TM.append(0)
                self.S_TE.append(0)

            else:
                # Only after the second interaction is sensitivity considered.
                self.S_TM.append(delta_X_TM / delta_index)
                self.S_TE.append(delta_X_TE / delta_index)

                self.S_TM[0] = self.S_TM[1]
                self.S_TE[0] = self.S_TE[1]

            # It calculates the FWHM
            R_med = self.set_R_med(r_tm)
            self.Fwhm_TM.append(self.fwhm(R_med, r_tm))
            R_med = self.set_R_med(r_te)
            self.Fwhm_TE.append(self.fwhm(R_med, r_te))

            # Resets the list with the angles of incidence to plot the graphs
            self.theta_i = arange(self.a1, self.a2, self.step_var)

        # It calculates the QF in TM and TE polarizations
        for s in range(i):
            self.FOM_TM.append((self.S_TM[s] / self.Fwhm_TM[s]))
            self.FOM_TE.append((self.S_TE[s] / self.Fwhm_TE[s]))

        print("\n........................ {!} Completed Calculations {!} ........................\n ")
        time.sleep(3)
        # Method that displays results
        self.display_results(s, delta_X_TM, delta_X_TE)

    def Reflectance(self, index, theta_i, wavelenght, mode):
        """ The numerical model is based on the attenuated total reflection method combined with the transfer matrix
            method for a multilayer system according to:
            * PALIWAL, N.; JOHN, J. Lossy mode resonance based fiber optic sensors. In: Fiber Optic Sensors.
            [S_TM.l.]: Springer, 2017. p. 31–50. DOI : 10.1007/978-3-319-42625-9_2."""

        j = complex(0, 1)  # Simplification for the complex number "j"
        k0 = (2 * pi) / wavelenght  # Wave number

        b = []  # b_j -> Phase shift in each layer
        q_TM = []  # q_TM_j -> Admittance in TM polarization
        q_TE = []  # q_TE_j -> Admittance in TE polarization

        M_TM = []  # M_TM_j -> Transfer matrix between each layer - TM polarization
        M_TE = []  # M_TE_j -> Transfer matrix between each layer - TM polarization
        for layer in range(self.nLayers):
            y = sqrt((index[layer] ** 2) - ((index[0] * sin(theta_i)) ** 2))

            b.append(k0 * self.d[layer] * y)
            q_TM.append(y / index[layer] ** 2)
            q_TE.append(y)

            # Total Transfer Matrix
            if layer < (self.nLayers - 1):
                M_TM.append(array([[cos(b[layer]), (-j / q_TM[layer]) * sin(b[layer])],
                                   [-j * q_TM[layer] * sin(b[layer]), cos(b[layer])]]))
                M_TE.append(array([[cos(b[layer]), (-j / q_TE[layer]) * sin(b[layer])],
                                   [-j * q_TE[layer] * sin(b[layer]), cos(b[layer])]]))

        Mt_TM = M_TM[0]  # Mt_TM -> Total Transfer Matrix - TM polarization
        Mt_TE = M_TE[0]  # Mt_TE -> Total Transfer Matrix - TE polarization
        for k in range(self.nLayers - 2):
            Mt_TM = Mt_TM @ M_TM[k + 1]
            Mt_TE = Mt_TE @ M_TE[k + 1]

        num_TM = (Mt_TM[0][0] + Mt_TM[0][1] * q_TM[self.nLayers - 1]) * q_TM[0] - (
                Mt_TM[1][0] + Mt_TM[1][1] * q_TM[self.nLayers - 1])
        den_TM = (Mt_TM[0][0] + Mt_TM[0][1] * q_TM[self.nLayers - 1]) * q_TM[0] + (
                Mt_TM[1][0] + Mt_TM[1][1] * q_TM[self.nLayers - 1])

        num_TE = (Mt_TE[0][0] + Mt_TE[0][1] * q_TE[self.nLayers - 1]) * q_TE[0] - (
                Mt_TE[1][0] + Mt_TE[1][1] * q_TE[self.nLayers - 1])
        den_TE = (Mt_TE[0][0] + Mt_TE[0][1] * q_TE[self.nLayers - 1]) * q_TE[0] + (
                Mt_TE[1][0] + Mt_TE[1][1] * q_TE[self.nLayers - 1])

        r_TM = num_TM / den_TM  # 'r_TM'-> Fresnel reflection coefficient - TM polarization
        r_TE = num_TE / den_TE  # 'r_TE'-> Fresnel reflection coefficient - TE polarization

        if mode == 0:
            return abs(r_TM) ** 2  # Reflectance - TM polarization
        elif mode == 1:
            return abs(r_TE) ** 2  # Reflectance - TE polarization

    def ReflectanceAux(self, mod_int):
        # Auxiliary method to calculate reflectance curves at each polarization
        # If mod_int (interrogation mode) == 1 -> Reflectance as a function of incidence angle

        self.R_TM_i = []
        self.R_TE_i = []

        if mod_int == 1:
            for t in range(len(self.theta_i)):
                for mod_p in range(3):
                    if mod_p == 0:
                        self.R_TM_i.append(self.Reflectance(self.indexRef, self.theta_i[t], self.wavelenght, mod_p))
                    elif mod_p == 1:
                        self.R_TE_i.append(self.Reflectance(self.indexRef, self.theta_i[t], self.wavelenght, mod_p))

            return self.R_TM_i, self.R_TE_i

    def Point_LMR(self, reflectance, s):
        # The method self.Point_LMR() returns the resonance point of the curve
        try:
            idm = reflectance.index(min(reflectance))  # Position of the minimum point of the curve

            a = self.theta_i[idm] * (180 / pi)
            b = self.critical_point[s]
            # Checks if the minimum is before the critical point
            if a > b:
                c = a
            else:  # It adjusts to be the next minimum after the critical angle
                lst = asarray(self.theta_i)
                idx = (abs(lst - (b * pi / 180))).argmin()

                reflect_right_critical_point = reflectance[idx:-1]
                idm = reflectance.index(min(reflect_right_critical_point))
                c = self.theta_i[idm] * (180 / pi)

            return c  # Returns the angle in degrees

        except ValueError:
            print("---------------------- {!} ---------------------- "
                  "\nThere is no resonance in the specified range."
                  "\nGenerated value does not match the actual value\n"
                  "------------------------------------------------- ")

            return self.theta_i[0] * (180 / pi)  # Returns the angle in degrees

    @staticmethod
    def set_R_med(curve):
        tam = len(curve)
        y1 = list(curve)  # List with reflectance values
        c = y1.index(min(curve))  # Position of the minimum point of the curve
        y_left = curve[0:(c + 1)]  # left part of the curve
        y_right = curve[c:(tam + 1)]  # right part of the curve

        max_left = max(y_left)  # Left maximum
        min_left = min(y_left)  # Left minimum
        max_right = max(y_right)  # Right maximum
        min_right = min(y_right)  # Right minimum

        y_med1 = (max_left + min_left) / 2  # Left Midpoint
        y_med2 = (max_right + min_right) / 2  # Right Midpoint

        return abs(y_med1 + y_med2) / 2  # Returns half height between left midpoint and right midpoint

    def fwhm(self, med_y, curve):
        # The method self.fwhm() receives the value of the half height (med_y) and calculates
        # the full width at the half maximum of the curve (f)
        try:
            # x axis in degrees
            xList = self.theta_i

            yList = curve  # List with reflectance values

            # Calculation to find the points (x1 and x2) that are at half height
            signs = sign(add(yList, -med_y))

            zero_crossings = (signs[0:-2] != signs[1:-1])
            zero_crossings_i = where(zero_crossings)[0]

            # An interpolation method ( lin_interp() ) is used to find x1 and x2
            x1 = self.lin_interp(xList, yList, zero_crossings_i[-2], med_y)  # Half height stitch x1
            x2 = self.lin_interp(xList, yList, zero_crossings_i[-1], med_y)  # Half height stitch x1
            f = abs((x1 * 180 / pi) - (x2 * 180 / pi)) if self.mod_int == 1 else abs(x2 - x1) * 1E9
        except IndexError:
            print("---------------------- {!} ---------------------- "
                  "\nFailed to calculate FWHM due to curve shape."
                  "\nGenerated value does not match the actual value\n"
                  "------------------------------------------------- ")
            f = 1

        return f  # Returns the full width at half maximum |X2 - X1|

    @staticmethod
    def lin_interp(x, y, i, h):
        # Linear interpolation to calculate abscissa values
        return x[i] + (x[i + 1] - x[i]) * ((h - y[i]) / (y[i + 1] - y[i]))

    def display_results(self, s, delta_X_TM, delta_X_TE):
        # The method self.display_results() shows in the command terminal the results obtained after all interactions.
        # The results provided are:
        #   (1) Resonance Angle in TM and TE Polarization
        #   (2) Angular Sensibility in TM and TE Polarization
        #   (3) Full Width at Half Maximum in TM and TE Polarization
        #   (4) Variation of the Resonance Angle and
        #   (5) Quality Factor, all in their respective units

        c = 'Degrees'
        z = 'Theta'

        parameters = dict(zip([f"LMR Resonance Point - TM ({c})", f"LMR Resonance Point - TE ({c})",
                               f"Sensibility - TM ({c}/RIU)", f"Sensibility - TE ({c}/RIU)",
                               f"FWHM - TM ({c})", f"FWHM - TE ({c})", f"Delta_{z}_LMR - TM ({c})",
                               f"Delta_{z}_LMR - TE ({c})", "QF - TM (RIU-1)", f"QF - TE (RIU-1)"],
                              [self.Resonance_Point_TM, self.Resonance_Point_TE,
                               self.S_TM, self.S_TE, self.Fwhm_TM, self.Fwhm_TE,
                               delta_X_TM, delta_X_TE, self.FOM_TM, self.FOM_TE]))

        print(f"\nAfter the {s + 1}th iteration:\n")
        for item in parameters.keys():
            print(f'{item} \n{parameters[item]}\n')

    def plot(self, s, ind_ana):
        # The method self.plot() receives the number of iterations ('s') on the refractive index of analyte and the
        # list (ind_ana) with the refractive index of the analyte and then displays the graphs:
        #   (1) Reflectance vs. Angle of Incidence
        #   (2) Reflectance vs. Angle of Incidence Given the Variation of the Refractive Index of the Analyte "
        #   (3) Angular Sensibility vs. Refractive Index of the Analyte
        #   (4) Resonance Angle vs. Refractive Index of the Analyte"
        #   (5) Full Width at Half Maximum vs. Refractive Index of the Analyte and
        #   (6) Quality Factor vs. Refractive Index of the Analyte

        y = 'Angle'
        c = 'Degrees'
        n = chr(952)
        ax_x = self.theta_i * (180 / pi)
        z = 180 / pi

        legend_i = []  # List of labels for subtitles

        font = dict(size=10, family='Times New Roman')  # Font and size
        plt.rc('font', **font)
        plt.style.use("seaborn-paper")
        dpi = 500
        font_size = 8
        font_leg = 6

        # (1) Reflectance vs. Angle of Incidence with detail for the note box informing the resonance points

        # TM-Polarization plot
        fig0, ax_TM = plt.subplots(dpi=dpi)
        ax_TM.plot(ax_x, (self.R_TM[0]))
        ax_TM.set_title("Reflectance vs. Angle of Incidence - TM", fontsize=font_size, loc='center', pad='6')
        ax_TM.set(xlabel=f'Incidence {y} ({c})', ylabel='Reflectance')
        text = f"{n}$_C$ = {self.critical_point[0]:.4f} ° \n{n}$_L$$_M$$_R$ = {self.Resonance_Point_TM[0]:.4f} °"
        ax_TM.annotate(text, (self.Resonance_Point_TM[0], min(self.R_TM[0])), xytext=((self.a1 * z), 0.1),
                       bbox={'facecolor': 'white', 'edgecolor': 'gray', 'alpha': 0.7}, fontsize=font_leg)
        plt.yticks(arange(0, 1.20, 0.20))
        ax_TM.grid()

        # TE-Polarization plot
        fig_TE, ax_TE = plt.subplots(dpi=dpi)
        ax_TE.plot(ax_x, (self.R_TE[0]))
        ax_TE.set_title("Reflectance vs. Angle of Incidence - TE", fontsize=font_size, loc='center', pad='6')
        ax_TE.set(xlabel=f'Incidence {y} ({c})', ylabel='Reflectance')
        text = f"{n}$_C$ = {self.critical_point[0]:.4f} ° \n{n}$_L$$_M$$_R$ = {self.Resonance_Point_TE[0]:.4f} °"
        ax_TE.annotate(text, (self.Resonance_Point_TE[0], min(self.R_TE[0])), xytext=((self.a1 * z), 0.1),
                       bbox={'facecolor': 'white', 'edgecolor': 'gray', 'alpha': 0.7}, fontsize=font_leg)
        plt.yticks(arange(0, 1.20, 0.20))
        ax_TE.grid()

        # (2) Reflectance vs. Angle of Incidence Given the Variation of the Refractive Index of the Analyte

        # TM-Polarization plot
        fig, ax1_TM = plt.subplots(dpi=dpi)
        l2 = []  # List with the index of refraction of the analyte for plotting the graph
        for i in range(s):
            ax1_TM.plot(ax_x, self.R_TM[i])
            legend_i.append(fr"{ind_ana[i].real:.3f}")
            l2.append(f"{ind_ana[i].real:.3f}")
        ax1_TM.set_title("Reflectance vs. Angle of Incidence - TM", fontsize=font_size, loc='center', pad='6')
        ax1_TM.set(xlabel=f'Incidence {y} ({c})', ylabel='Reflectance')
        ax1_TM.grid(alpha=0.25)
        ax1_TM.legend(legend_i, fontsize=font_leg)
        plt.yticks(arange(0, 1.20, 0.20))

        # TE-Polarization plot
        fig2_te, ax1_TE = plt.subplots(dpi=dpi)
        for i in range(s):
            ax1_TE.plot(ax_x, self.R_TE[i])
        ax1_TE.set_title("Reflectance vs. Angle of Incidence - TE", fontsize=font_size, loc='center', pad='6')
        ax1_TE.set(xlabel=f'Incidence {y} ({c})', ylabel='Reflectance')
        ax1_TE.grid(alpha=0.25)
        ax1_TE.legend(legend_i, fontsize=font_leg)
        plt.yticks(arange(0, 1.20, 0.20))

        # (3) Angular Sensibility vs. Refractive Index of the Analyte

        # TM-Polarization plot
        fig3, ax2_TM = plt.subplots(dpi=dpi)
        ax2_TM.plot(real(ind_ana), self.S_TM, '-s', linewidth=0.8, markersize=3, c='b')
        ax2_TM.grid()
        ax2_TM.set_title("Sensibility - TM", fontsize=font_size, loc='center', pad='6')
        ax2_TM.set_xticks(real(ind_ana))
        ax2_TM.set_xticklabels(l2, rotation=45)
        ax2_TM.set_yticks(self.S_TM)

        # TE-Polarization plot
        fig3_te, ax2_TE = plt.subplots(dpi=dpi)
        ax2_TE.plot(real(ind_ana), self.S_TE, '-s', linewidth=0.8, markersize=3, c='b')
        ax2_TE.grid()
        ax2_TE.set_title("Sensibility - TE", fontsize=font_size, loc='center', pad='6')
        ax2_TE.set_xticks(real(ind_ana))
        ax2_TE.set_xticklabels(l2, rotation=45)
        ax2_TE.set_yticks(self.S_TE)

        # (4) Resonance Angle vs. Analyte Refractive index

        # TM-Polarization plot
        figs, axs_TM = plt.subplots(dpi=dpi)
        axs_TM.plot(real(ind_ana), self.Resonance_Point_TM, '-s', linewidth=0.8, markersize=3, c='r')
        axs_TM.grid()
        axs_TM.set_title("Resonance Angle vs. Analyte Refractive Index - TM", fontsize=font_size, loc='center', pad='6')
        axs_TM.set_xticks(real(ind_ana))
        axs_TM.set_xticklabels(l2, rotation=45)
        axs_TM.set_yticks(self.Resonance_Point_TM)

        # TE-Polarization plot
        figsTE, axs_TE = plt.subplots(dpi=dpi)
        axs_TE.plot(real(ind_ana), self.Resonance_Point_TE, '-s', linewidth=0.8, markersize=3, c='b')
        axs_TE.grid()
        axs_TE.set_title("Resonance Angle vs. Analyte Refractive Index - TE", fontsize=font_size, loc='center', pad='6')
        axs_TE.set_xticks(real(ind_ana))
        axs_TE.set_xticklabels(l2, rotation=45)
        axs_TE.set_yticks(self.Resonance_Point_TE)

        # (5) Full Width at Half Maximum vs. Refractive Index of the Analyte

        # TM-Polarization plot
        fig_Fwhm_TM, ax2_fwhm_TM = plt.subplots(dpi=dpi)
        ax2_fwhm_TM.plot(real(ind_ana), self.Fwhm_TM, '-o', linewidth=0.8, markersize=3, c='b')
        ax2_fwhm_TM.grid()
        ax2_fwhm_TM.set_title("FWHM - TM", fontsize=font_size, loc='center', pad='6')
        ax2_fwhm_TM.set_xticks(real(ind_ana))
        ax2_fwhm_TM.set_xticklabels(l2, rotation=45)
        ax2_fwhm_TM.set_yticks(self.Fwhm_TM)

        # TE-Polarization plot
        fig_Fwhm_TE, ax2_fwhm_TE = plt.subplots(dpi=dpi)
        ax2_fwhm_TE.plot(real(ind_ana), self.Fwhm_TE, '-o', linewidth=0.8, markersize=3, c='b')
        ax2_fwhm_TE.grid()
        ax2_fwhm_TE.set_title("FWHM - TE", fontsize=font_size, loc='center', pad='6')
        ax2_fwhm_TE.set_xticks(real(ind_ana))
        ax2_fwhm_TE.set_xticklabels(l2, rotation=45)
        ax2_fwhm_TE.set_yticks(self.Fwhm_TE)
        # (6) Quality Factor vs. Refractive Index of the Analyte

        # TM-Polarization plot
        fig3_FOM_TM, ax2_fom_TM = plt.subplots(dpi=dpi)
        ax2_fom_TM.plot(real(ind_ana), self.FOM_TM, '-o', linewidth=0.8, markersize=3, c='b')
        ax2_fom_TM.grid()
        ax2_fom_TM.set_title("Quality Factor - TM", fontsize=font_size, loc='center', pad='6')
        ax2_fom_TM.set_xticks(real(ind_ana))
        ax2_fom_TM.set_xticklabels(l2, rotation=45)
        ax2_fom_TM.set_yticks(self.FOM_TM)

        # TE-Polarization plot
        fig3_FOM_TE, ax2_fom_TE = plt.subplots(dpi=dpi)
        ax2_fom_TE.plot(real(ind_ana), self.FOM_TE, '-o', linewidth=0.8, markersize=3, c='b')
        ax2_fom_TE.grid()
        ax2_fom_TE.set_title("Quality Factor - TE", fontsize=font_size, loc='center', pad='6')
        ax2_fom_TE.set_xticks(real(ind_ana))
        ax2_fom_TE.set_xticklabels(l2, rotation=45)
        ax2_fom_TE.set_yticks(self.FOM_TE)

        plt.show()


print(
    "\n---------------------------------------- Welcome to Sim-LMR ------------------------------------------\n"
    "\n------------------------------------------------------------------------------------------------------\n"
    "Sim-LMR is an open source simulator in development implemented in Python for the study, analysis and \n"
    "design of biosensors based on Lossy Mode Resonance (LMR).\n "
    "     The Sim-LMR gives support for to calculate the resonant angle, the sensibility, the full width \n"
    "at half maximum and the quality factor on angular interrogation mode considering Krestchmann config. \n"
    "The numerical model is based on the attenuated total reflection method combined with the transfer \n"
    "matrix method for a multilayer system. \n"
    "\nAt the end of the simulation, the code provides results in terms of: \n"
    "         (1) Resonance Angle in TM and TE Polarization\n"
    "         (2) Angular Sensibility in TM and TE Polarization\n"
    "         (3) Full Width at Half Maximum in TM and TE Polarization\n"
    "         (4) Variation of the Resonance Angle and\n"
    "         (5) Quality Factor\n"

    "And even graphical responses with: \n"
    "         (1) Reflectance vs. Angle of Incidence\n"
    "         (2) Reflectance vs. Angle of Incidence Given the Variation of the Refractive Index of the Analyte \n"
    "         (3) Angular Sensibility vs. Refractive Index of the Analyte \n"
    "         (4) Resonance Angle vs. Refractive Index of the Analyte\n"
    "         (5) Full Width at Half Maximum vs. Refractive Index of the Analyte and\n"
    "         (6) Quality Factor vs. Refractive Index of the Analyte\n"
    "\nThe results obtained were validated using other computational tools available in the literature."

    "\n--------------------------------------------------------------------------------------------------------\n")
op = input("Press enter to continue... \n>>>")
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
while True:
    App_SIM_LMR = LMR()
    while True:
        try:
            op = int(input("\n---------------------------- Simulation done successfully -----------------------------"
                           "\n---------------------------------------------------------------------------------------\n"
                           "\nStart new simulation? \n1 - Yes\n2 - No\n -> "))
            if 0 < op < 3:
                break
            else:
                print("- {!} - \nInvalid Value!\nPlease enter a valid option...\n")
        except ValueError:
            print("- {!} - \nInvalid Value!\nPlease enter a valid option...\n")
    if op == 1:
        print("\n-------------------------------- Simulation Started -----------------------------------"
              "\n---------------------------------------------------------------------------------------\n")
    else:
        break
