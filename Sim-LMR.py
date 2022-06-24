from numpy import *
import matplotlib.pyplot as plt


class LMR(object):
    def __init__(self):
        # Attributes:
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

        self.FOM_TM, self.FOM_TE = [], []  # Lists with the FOM in TM and TE  polarizations
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
                        t = "\nKretschmann configuration\n"
                    else:
                        t = "\nConfiguration using fiber optics\n"
                    print(t)
                    break
            except ValueError:
                print("- {!} - \nPlease select some option...\n")

        # Method that selects a interrogation mode : Angular ou Wavelength.
        while True:
            try:
                self.mod_int = int(
                    input("Select an interrogation mode:\n1 - Angular (AIM)\n2 - Wavelength (WIM)\n-> "))
                if self.mod_int < 1 or self.mod_int > 2:
                    print("Invalid option selected")
                else:
                    t = "\nAngular Interrogation Mode\n" if self.mod_int == 1 else "\nWavelength Interrogation Mode\n "
                    print(t)
                    break
            except ValueError:
                print("- {!} - \nPlease select some option...\n")

        self.setLayers()  # Method that asks the user for the characteristics of the layers

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

        # Method that asks the user for the number of interactions and the change in the refractive index of the analyte
        self.sensibility()

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

            # Method that calculates sensitivity and other quality indicators
            self.calculation(self.inter)

            # Método que exibe os gráficos:
            # (1) Curva de ressonancia,
            # (2) Deslocamentos da curva de ressonancia em função da variação do indice de refração
            # (3) Curva de Sesibilidade e (4) Curva dos pontos de ressonancia
            self.plot(self.inter, self.index_ref_ana)

        # Wavelength interrogation mode
        else:
            # Comprimento de onda inicial
            while True:
                try:
                    self.a1 = float(input("Comprimento de Onda Inicial (nm):\n-> ")) * 1e-9
                    if 0 < self.a1:
                        break
                    else:
                        print("Valor Inválido!")
                except ValueError:
                    print("- {!} - \nInsira um valor válido\n")

            # Comprimento de onda final
            while True:
                try:
                    self.a2 = float(input("Comprimento de Onda Inicial (nm):\n-> ")) * 1e-9
                    if self.a1 < self.a2:
                        break
                    else:
                        print("Valor Inválido!")
                except ValueError:
                    print("- {!} - \nInsira um valor válido\n")

            # Passo do Comprimento de onda
            while True:
                try:
                    self.step_var = float(input("Passo de varredura (nm):\n-> ")) * 1e-9
                    if 0 < self.step_var < (self.a2 - self.a1):
                        break
                    else:
                        print("Valor Inválido!")
                except ValueError:
                    print("- {!} - \nInsira um valor válido\n")

            # Ângulo do feixe incidente
            while True:
                try:
                    self.theta_i = float(input("Ângulo do feixe incidende (°):\n-> ")) * (pi / 180)
                    if 0 < self.theta_i <= (pi / 2):
                        break
                    else:
                        print("Valor Inválido")
                except ValueError:
                    print("- {!} - \nInsira um valor válido\n")

            self.lambda_i = arange(self.a1, self.a2, self.step_var)  # Array com os comprimentos de onda incidentes

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
                    if self.mod_int == 1 or material == 9:
                        self.indexRef.append(self.set_index_Angular())  # Assignment of refractive index
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
                              f"\n13 - Gold   14 - Silver     15 - Copper    16 - Water "
                              f"\n17 - Air    18 - LiF        19 - ZnO       20 - Other")
                        material = (int(input(f"\nMaterial -> ")))
                        if material > 0:
                            self.material.append(material)  # Assignment of materials
                            if self.mod_int == 1 or material == 9:
                                self.indexRef.append(self.set_index_Angular())  # Assignment of refractive index
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
            else:
                break

        self.nLayers = len(self.indexRef)
        print(
            f"\n-------------------- Structure with {self.nLayers}-layers was successfully built --------------------\n"
            "----------------------------------------------------------------------------------------")

    @staticmethod
    def set_index(material, wi):
        B1, B2, B3, C1, C2, C3, X, n, k_index = 0, 0, 0, 0, 0, 0, [], [], []  # Inicialização dos parametros
        Lambda_i = wi * 1e6  # Comprimento de onda de incidência em micrômetros
        j = 0 + 1j
        # Materiais que compõem os prismas modelados pela equação de Sellmeier
        if 0 < material <= 8:
            if material == 1:  # BK7
                B1, B2, B3, C1, C2, C3 = 1.03961212, 2.31792344E-1, 1.01046945, 6.00069867E-3, 2.00179144E-2, 103.560653

            elif material == 2:  # Silica
                B1, B2, B3, C1, C2, C3 = 0.6961663, 0.4079426, 0.8974794, 4.6791E-3, 1.35121E-2, 97.934003

            elif material == 3:  # N-F2
                B1, B2, B3, C1, C2, C3 = 1.39757037, 1.59201403E-1, 1.2686543, 9.95906143E-3, 5.46931752E-2, 119.2483460

            elif material == 4:  # Safira sintética(Al2O3)
                B1, B2, B3, C1, C2, C3 = 1.4313493, 0.65054713, 5.3414021, 0.00527993, 0.0142383, 325.01783

            elif material == 5:  # SF2
                B1, B2, B3, C1, C2, C3 = 1.78922056, 3.28427448E-1, 2.01639441, 1.35163537E-2, 6.22729599E-2, 168.014713

            elif material == 6:  # FK51A
                B1, B2, B3, C1, C2, C3 = 0.971247817, 0.216901417, 0.904651666, 0.00472301995, 0.0153575612, 168.68133

            elif material == 7:  # N-SF14
                B1, B2, B3, C1, C2, C3 = 1.69022361, 0.288870052, 1.704518700, 0.01305121130, 0.0613691880, 149.5176890

            elif material == 8:  # Acrilico SUVT
                B1, B2, B3, C1, C2, C3 = 0.59411, 0.59423, 0, 0.010837, 0.0099968, 0

            # Equação de Sellmeier
            n = sqrt(1 + ((B1 * Lambda_i ** 2) / (Lambda_i ** 2 - C1)) + ((B2 * Lambda_i ** 2) / (Lambda_i ** 2 - C2))
                     + ((B3 * Lambda_i ** 2) / (Lambda_i ** 2 - C3)))

        # Glicerol e PVA
        elif 8 < material <= 10:
            if material == 9:  # PVA
                B1, B2, B3, C1, C2, C3 = 1.460, 0.00665, 0, 0, 0, 0
            elif material == 10:  # Glicerina/glicerol
                B1, B2, B3, C1, C2, C3 = 1.45797, 0.00598, -0.00036, 0, 0, 0
            # Equação que modela o index de refração em função do comprimento e onda
            n = B1 + (B2 / Lambda_i ** 2) + (B3 / Lambda_i ** 4)

        # Quartzo
        elif 10 < material <= 11:
            B1, B2, B3, C1, C2, C3 = 2.356764950, -1.139969240E-2, 1.087416560E-2, 3.320669140E-5, 1.086093460E-5, 0
            n = sqrt(B1 + (B2 * Lambda_i ** 2) + (B3 / Lambda_i ** 2) + (C1 / Lambda_i ** 4) + (C2 / Lambda_i ** 6))

        # Metais
        elif 11 < material <= 15:
            """
            X - Define os comprimentos de onda em micrometros,
            n - parte real do index de refração e k_index - parte imaginária
            tomando como base Johnson and Christy, 1972
            """
            if material == 12:  # Aluminio com base no modelo de Drude
                LambdaP, LambdaC = 1.0657E-7, 2.4511E-5
                n = sqrt(1 - (((wi ** 2) * LambdaC) / ((LambdaC + (j * wi)) * (LambdaP ** 2))))
            elif material == 13:  # Ouro
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

            elif material == 14:  # Prata
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

            elif material == 15:  # Cobre
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

            # Método que calcula os indices de refração dos metais atrevés de interpolação linear
            # baseado nos pontos contidos em X, n e k_index descritos anteriormente
            n_interp = interp(Lambda_i, X, n)
            k_interp = interp(Lambda_i, X, k_index)
            n = complex(n_interp, k_interp)

        # Indice de refração da água
        elif material == 16:
            n = 1.333

        # Indice de refração do Ar
        elif material == 17:
            n = 1.0000

        # Indice de refração do LiF (Fluoreto de Lítio)
        elif material == 18:
            B1, B2, B3, C1, C2, C3 = 0.92549, 6.96747, 0, 5.4405376E-3, 1075.1841, 0
            n = sqrt(1 + ((B1 * Lambda_i ** 2) / (Lambda_i ** 2 - C1)) + ((B2 * Lambda_i ** 2) / (Lambda_i ** 2 - C2))
                     + ((B3 * Lambda_i ** 2) / (Lambda_i ** 2 - C3)))

        n0 = round(real(n), 5)  # Faz o arredondamento para 5 casas decimais
        k0 = round(imag(n), 5)  # Faz o arredondamento para 5 casas decimais

        return n0 + k0 * j  # Retorna o index de refração complexo do metal com 5 casas decimais

    @staticmethod
    def set_index_Angular():
        while True:
            try:
                id_real = float(input(f"Refractive index:\n    * Real part: -> "))
                id_imag = float(input(f"    * Imaginary part: -> "))
                break
            except ValueError:
                print("- {!} - \nInvalid Value!\nPlease enter a valid value...\n")
        return complex(id_real, id_imag)

    def sensibility(self):
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
        # O método calculos() recebe o numero (i) de variações do index de refração do analito,
        # calcula (1) a curva de reflectancia, (2) o ponto de ressonancia, (3) a sensibilidade para cada interação
        # e exibe os resultados pelo método - exibir_resultados()
        # delta_X -> Variação do angulo ou comprimento de onda de ressonacia dado a variação no analito
        delta_X_TM, delta_X_TE = 0, 0
        s = None

        for s in range(i):
            if self.mod_int == 1:
                # Atualização do index de refração da camada sensoriada para analise da sensibilidade
                if s == 0:
                    self.analyte_index_0 = self.indexRef[self.layer_A]
                self.indexRef[self.layer_A] = complex(round(self.analyte_index_0.real + (self.step_shift * s), 4), 0)
                # Faz o calculo do ângulo crítico de reflexão interna para o mode de interrogação angular
                self.critical_point.append(abs(arcsin(self.analyte_index_0 / self.indexRef[0]) * (180 / pi)))

            self.theta_i = arange(self.a1, self.a2, self.step_var)  # List with angles of incidence

            # Variável local que armazena temporariamente os valores de reflectance para cada uma das 's' interações
            r_tm, r_te = self.ReflectanceAux(self.mod_int, s)

            # Preenchimento do array com os indices de refração do analito para plotagem dos graficos
            self.index_ref_ana.append(self.indexRef[self.layer_A])

            # Ponto de ressonância pelo valores fornecidos a partir do grafico em graus ou nanometros
            self.Resonance_Point_TM.append(self.Point_LMR(r_tm, self.mod_int, s))
            self.Resonance_Point_TE.append(self.Point_LMR(r_te, self.mod_int, s))

            # Armazena os arrays com as curvas de reflectancia para cada uma das 's' interações
            self.R_TM.append(r_tm)
            self.R_TE.append(r_te)

            # Calcula a sensibilidade pelo valores obtidos a partir do grafico
            # Variação do ponto de ressonâcia
            delta_X_TM = self.Resonance_Point_TM[s] - self.Resonance_Point_TM[0]
            delta_X_TE = self.Resonance_Point_TE[s] - self.Resonance_Point_TE[0]

            # Variação do index de refração
            delta_indice = self.indexRef[self.layer_A].real - self.analyte_index_0.real

            # Calcula a Sensibilidade como (Variação do ponto de ressonâcia )/(Variação do index de refração)
            if s == 0:
                # Inicializa-se em zero a primeira interação pois a razão ficaria 0/0
                self.S_TM.append(0)
                self.S_TE.append(0)

            else:
                # Apenas a partir da segunda interação a sensibilidade é considerada
                self.S_TM.append(delta_X_TM / delta_indice)
                self.S_TE.append(delta_X_TE / delta_indice)

                self.S_TM[0] = self.S_TM[1]
                self.S_TE[0] = self.S_TE[1]

            # Calcula o FWHM
            Rmed = self.set_R_med(r_tm)
            self.Fwhm_TM.append(self.fwhm(Rmed, r_tm))
            Rmed = self.set_R_med(r_te)
            self.Fwhm_TE.append(self.fwhm(Rmed, r_te))

            # Reinicializa os arrays com os ângulos ou comprimentos de onda de incidencia para plotagem dos gráficos
            if self.mod_int == 1:
                self.theta_i = arange(self.a1, self.a2, self.step_var)
            else:
                self.lambda_i = arange(self.a1, self.a2, self.step_var)

        # Calculo da FOM nas polarizações TM and TE
        for s in range(i):
            self.FOM_TM.append((self.S_TM[s] / self.Fwhm_TM[s]))
            self.FOM_TE.append((self.S_TE[s] / self.Fwhm_TE[s]))

        # Method that displays results
        self.display_results(s, delta_X_TM, delta_X_TE)

    def Reflectance(self, index, theta_i, wavelenght, mode):
        """ Modelagem para o cálculo da reflectância baseada na forma matricial das equações de Fresnel descritas em:
            * PALIWAL, N.; JOHN, J. Lossy mode resonance based fiber optic sensors. In: Fiber Optic Sensors.
            [S_TM.l.]: Springer, 2017. p. 31–50. DOI : 10.1007/978-3-319-42625-9_2."""

        j = complex(0, 1)  # Simplificação do numero complexo "j"
        k0 = (2 * pi) / wavelenght  # Número de onda

        b = []  # b_j -> Deslocamento de fase em cada camada
        q_TM = []  # q_TM_j -> Admitância de cada camada polarização TM
        q_TE = []  # q_TE_j -> Admitância de cada camada polarização TE

        M_TM = []  # M_TM_j -> Matriz de transferência entre cada camada polarização TM
        M_TE = []  # M_TE_j -> Matriz de transferência entre cada camada polarização TE
        for layer in range(self.nLayers):
            y = sqrt((index[layer] ** 2) - ((index[0] * sin(theta_i)) ** 2))

            b.append(k0 * self.d[layer] * y)
            q_TM.append(y / index[layer] ** 2)
            q_TE.append(y)

            # Calculo da matriz de transferencia entre as N camadas( N-1 interfaces)
            if layer < (self.nLayers - 1):
                M_TM.append(array([[cos(b[layer]), (-j / q_TM[layer]) * sin(b[layer])],
                                   [-j * q_TM[layer] * sin(b[layer]), cos(b[layer])]]))
                M_TE.append(array([[cos(b[layer]), (-j / q_TE[layer]) * sin(b[layer])],
                                   [-j * q_TE[layer] * sin(b[layer]), cos(b[layer])]]))

        Mt_TM = M_TM[0]  # Mt_TM -> Matriz de transferência total do sistema polarização TM
        Mt_TE = M_TE[0]  # Mt_TE -> Matriz de transferência total do sistema polarização TE
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

        r_TM = num_TM / den_TM  # 'r_TM'-> Coeficiente de reflexção de Fresnel para polarização TM
        r_TE = num_TE / den_TE  # 'r_TE'-> Coeficiente de reflexção de Fresnel para polarização TE

        if mode == 0:
            return abs(r_TM) ** 2  # Retorna a reflectância polarização TM
        elif mode == 1:
            return abs(r_TE) ** 2  # Retorna a reflectância polarização TE
        else:
            return (abs(r_TE) ** 2 + abs(r_TM) ** 2) / 2  # Retorna a reflectância polarização TE + TM

    def ReflectanceAux(self, mod_int, s):
        # Método auxiliar para calcular as curvas de reflectancia em cada polarização
        # Se mod_int (mode de interrogação) == 1 -> calcula-se a reflectancia em função do ângulo de incidencia
        # Se mod_int (mode de interrogação) == 2 -> calcula-se a reflectancia em função do comprimento de onda
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

        else:
            for t in range(len(self.lambda_i)):
                self.indexRef = []  # Indice de refração reinicializado para cada comprimento de onda

                for m in range(self.nLayers):  # Cálculo do novo index de refração para cada material
                    self.indexRef.append(self.set_index(self.material[m], self.lambda_i[t]))

                # Atualização do index de refração da camada sensoriada para analise da sensibilidade
                self.analyte_index_0 = self.indexRef[self.layer_A]
                self.indexRef[self.layer_A] = complex(round(self.analyte_index_0.real + (self.step_shift * s), 4), 0)

                for mod_p in range(3):
                    if mod_p == 0:
                        self.R_TM_i.append(self.Reflectance(self.indexRef, self.theta_i, self.lambda_i[t], mod_p))
                    elif mod_p == 1:
                        self.R_TE_i.append(self.Reflectance(self.indexRef, self.theta_i, self.lambda_i[t], mod_p))

            return self.R_TM_i, self.R_TE_i

    def Point_LMR(self, reflectance, mode, s):
        # O método Ponto_LMR retorna o ponto de ressonância da curva, seja angulo de ressonancia em graus
        # ou comprimento do onda de ressonancia em nanômetros
        try:
            idm = reflectance.index(min(reflectance))  # Recebe a posição do ponto mínimo da curva
            if mode == 1:
                a = self.theta_i[idm] * (180 / pi)
                b = self.critical_point[s]
                if a > b:
                    c = a
                else:
                    lst = asarray(self.theta_i)
                    idx = (abs(lst - (b * pi / 180))).argmin()

                    reflect_right_critical_point = reflectance[idx:-1]
                    idm = reflectance.index(min(reflect_right_critical_point))
                    c = self.theta_i[idm] * (180 / pi)

                return c  # Returns the angle in degrees
            else:
                return self.lambda_i[idm] * 1E9  # Returns the wavelength in nanometers
        except ValueError:
            print("---------------------- {!} ---------------------- "
                  "\nThere is no resonance in the specified range."
                  "\nGenerated value does not match the actual value\n"
                  "------------------------------------------------- ")
            if mode == 1:
                return self.theta_i[0] * (180 / pi)  # Returns the angle in degrees
            else:
                return self.lambda_i[0] * 1E9  # Returns the wavelength in nanometers

    @staticmethod
    def set_R_med(curve):
        tam = len(curve)
        y1 = list(curve)  # Lista com os valores da reflectancia
        c = y1.index(min(curve))  # Recebe a posição do ponto mínimo da curva
        y_left = curve[0:(c + 1)]  # Parte esquerda da curva
        y_right = curve[c:(tam + 1)]  # Parte direita da curva

        max_left = max(y_left)  # Máximo da parte esquerda
        min_left = min(y_left)  # Mínimo da parte esquerda
        max_right = max(y_right)  # Máximo da parte direita
        min_right = min(y_right)  # Mínimo da parte direita

        y_med1 = (max_left + min_left) / 2  # Ponto médio da parte esquerda
        y_med2 = (max_right + min_right) / 2  # Ponto médio da parte direita

        return abs(y_med1 + y_med2) / 2  # Return half height entre o ponto médio a esquerda e o ponto médio a direita

    def fwhm(self, med_y, curve):
        # O método fwhm recebe o valor da meia altura(med_y) calcula a largura total a meia altura da curva (f)
        try:
            # Lista do eixo x em graus ou comprimento de onda
            xList = self.theta_i if self.mod_int == 1 else self.lambda_i

            yList = curve  # Lista dos valores de reflectancia calculados

            # Cálculo para descobrir os pontos (x1 e x2) que estão à meia altura
            signs = sign(add(yList, -med_y))

            zero_crossings = (signs[0:-2] != signs[1:-1])
            zero_crossings_i = where(zero_crossings)[0]

            # Usa-se uma método de interpolação ( lin_interp() ) para encontrar x1 e x2
            x1 = self.lin_interp(xList, yList, zero_crossings_i[-2], med_y)  # Ponto x1 da meia altura
            x2 = self.lin_interp(xList, yList, zero_crossings_i[-1], med_y)  # Ponto x2 da meia altura
            f = abs((x1 * 180 / pi) - (x2 * 180 / pi)) if self.mod_int == 1 else abs(x2 - x1) * 1E9
        except IndexError:
            print("---------------------- {!} ---------------------- "
                  "\nFailed to calculate FWHM due to curve shape."
                  "\nGenerated value does not match the actual value\n"
                  "------------------------------------------------- ")
            f = 1

        return f  # Retorna a diferença |X2 - X1| em graus ou nanômetros

    @staticmethod
    def lin_interp(x, y, i, h):
        # Linear interpolation to calculate abscissa values
        return x[i] + (x[i + 1] - x[i]) * ((h - y[i]) / (y[i + 1] - y[i]))

    def display_results(self, s, delta_X_TM, delta_X_TE):
        # O método exibir_resultados mostra no terminal de comando os resultados obtidos após as 's' interações
        # de variação do analito. Os reusltados fornecidos são:
        # (1) Ponto de ressonância na primeira interação (s=0), (2) Reflectancia mínima na primeira interação (s=0)
        # (3) Sensibilidade, (4) FWHM da primeira curva (s=0)
        # (5) Variação do ângulo ou comprimento de onda de ressonância após as 's' interações
        # (6) Detecção de acurácia (DA) e (7) Fator de qualidade (QF), todos em suas respectivas unidades

        c = 'Degrees' if self.mod_int == 1 else 'nm'  # Correspondência entre graus ou nanometros
        z = 'Theta' if self.mod_int == 1 else 'Lambda'  # Correspondência entre mode AIM ou WIM

        parameters = dict(zip([f"LMR Resonance Point - TM ({c})", f"LMR Resonance Point - TE ({c})",
                               f"Sensibility - TM ({c}/RIU)", f"Sensibility - TE ({c}/RIU)",
                               f"FWHM - TM ({c})", f"FWHM - TE ({c})", f"Delta_{z}_LMR - TM ({c})",
                               f"Delta_{z}_LMR - TE ({c})", "QF - TM (RIU-1)", f"QF - TE (RIU-1)"],
                              [self.Resonance_Point_TM, self.Resonance_Point_TE,
                               self.S_TM, self.S_TE, self.Fwhm_TM, self.Fwhm_TE,
                               delta_X_TM, delta_X_TE, self.FOM_TM, self.FOM_TE]))

        print(f"\nAfter {s + 1} iterations:\n")
        for item in parameters.keys():
            print(f'{item} \n{parameters[item]}\n')

    def plot(self, s, ind_ana):
        # O método plot() recebe o numero de interações 's' na variação do analito e o vetor ind_ana com o
        # indice de refração do analito e então apresenta os gráficos:
        # (1) Curva de ressonancia,
        # (2) Deslocamentos da curva de ressonancia em função da variação do indice de refração
        # (3) Curva de Sensibility e (4) Curva dos pontos de ressonancia

        # adjust modes AIM ou WIM
        y = 'Ângulo' if self.mod_int == 1 else 'Comprimento de Onda'
        c = 'graus' if self.mod_int == 1 else 'nm'
        n = chr(952) if self.mod_int == 1 else chr(955)
        ax_x = self.theta_i * (180 / pi) if self.mod_int == 1 else self.lambda_i * 1E9
        z = 180 / pi if self.mod_int == 1 else 1E9

        legend_i = []  # Array que armazena os rótulos da legenda

        font = dict(size=10, family='Times New Roman')  # Definição da fonte e tamanho
        plt.rc('font', **font)
        plt.style.use("seaborn-paper")
        dpi = 500
        fontsize = 8
        font_leg = 6
        # Gráfico da curva de reflectância com detalhe para caixa de anotações informando os pontos de ressonância
        # TM-Polarization plot
        fig0, ax_TM = plt.subplots(dpi=dpi)
        ax_TM.plot(ax_x, (self.R_TM[0]))
        ax_TM.set_title("Polarização TM", fontsize=fontsize, loc='center', pad='6')
        ax_TM.set(xlabel=f'{y} de Incidência ({c})', ylabel='Reflectância')
        if self.mod_int == 1:  # AIM
            text = f"{n}$_C$ = {self.critical_point[0]:.4f} °" \
                   f"\n{n}$_L$$_M$$_R$ = {self.Resonance_Point_TM[0]:.4f} °"
        else:  # WIM
            text = f"{n}$_L$$_M$$_R$ = {self.Resonance_Point_TM[0]:.4f}nm"

        ax_TM.annotate(text, (self.Resonance_Point_TM[0], min(self.R_TM[0])), xytext=((self.a1 * z), 0.1),
                       bbox={'facecolor': 'white', 'edgecolor': 'gray', 'alpha': 0.7}, fontsize=font_leg)
        plt.yticks(arange(0, 1.20, 0.20))
        ax_TM.grid()

        # TE-Polarization plot
        fig_TE, ax_TE = plt.subplots(dpi=dpi)
        ax_TE.plot(ax_x, (self.R_TE[0]))
        ax_TE.set_title("Polarização TE", fontsize=fontsize, loc='center', pad='6')
        ax_TE.set(xlabel=f'{y} de Incidência ({c})', ylabel='Reflectância')
        if self.mod_int == 1:  # Mode AIM
            text = f"{n}$_C$ = {self.critical_point[0]:.4f} °" \
                   f"\n{n}$_L$$_M$$_R$ = {self.Resonance_Point_TE[0]:.4f} °"
        else:  # WIM
            text = f"{n}$_L$$_M$$_R$ = {self.Resonance_Point_TE[0]:.4f}nm"

        ax_TE.annotate(text, (self.Resonance_Point_TE[0], min(self.R_TE[0])), xytext=((self.a1 * z), 0.1),
                       bbox={'facecolor': 'white', 'edgecolor': 'gray', 'alpha': 0.7}, fontsize=font_leg)
        plt.yticks(arange(0, 1.20, 0.20))
        ax_TE.grid()

        # Gráfico do deslocamento da curva de reflectância dado a variação do indice de refração do analito

        # TM-Polarization plot
        fig, ax1_TM = plt.subplots(dpi=dpi)
        l2 = []  # Armazena os valores no eixo x nos graficos da sensibilidade e ponto de ressonancia
        for i in range(s):
            ax1_TM.plot(ax_x, self.R_TM[i])
            legend_i.append(fr"{ind_ana[i].real:.4f}")
            l2.append(f"{ind_ana[i].real:.3f}")
        ax1_TM.set_title("Polarização TM", fontsize=fontsize, loc='center', pad='6')
        ax1_TM.set(xlabel=f'{y} de Incidência ({c})', ylabel='Reflectância')
        ax1_TM.grid(alpha=0.25)
        ax1_TM.legend(legend_i, fontsize=font_leg)
        plt.yticks(arange(0, 1.20, 0.20))

        # TE-Polarization plot
        fig2_te, ax1_TE = plt.subplots(dpi=dpi)
        l2 = []  # Armazena os valores no eixo x nos graficos da sensibilidade e ponto de ressonancia
        for i in range(s):
            ax1_TE.plot(ax_x, self.R_TE[i])
            legend_i.append(fr"{ind_ana[i].real:.4f}")
            l2.append(f"{ind_ana[i].real:.3f}")
        ax1_TE.set_title("Polarização TE", fontsize=fontsize, loc='center', pad='6')
        ax1_TE.set(xlabel=f'{y} de Incidência ({c})', ylabel='Reflectância')
        ax1_TE.grid(alpha=0.25)
        ax1_TE.legend(legend_i, fontsize=font_leg)
        plt.yticks(arange(0, 1.20, 0.20))

        # Gráfico da Sensibilidade

        # TM-Polarization plot
        fig3, ax2_TM = plt.subplots(dpi=dpi)
        ax2_TM.plot(real(ind_ana), self.S_TM, '-s', linewidth=0.8, markersize=3, c='b')
        ax2_TM.grid()
        ax2_TM.set_title("Sensibilidade Polarização TM", fontsize=fontsize, loc='center', color='b', pad='6')
        ax2_TM.set_xticks(real(ind_ana))
        ax2_TM.set_xticklabels(l2, rotation=45)
        ax2_TM.set_yticks(self.S_TM)

        # TE-Polarization plot
        fig3_te, ax2_TE = plt.subplots(dpi=dpi)
        ax2_TE.plot(real(ind_ana), self.S_TE, '-s', linewidth=0.8, markersize=3, c='b')
        ax2_TE.grid()
        ax2_TE.set_title("Sensibilidade Polarização TE", fontsize=fontsize, loc='center', color='b', pad='6')
        ax2_TE.set_xticks(real(ind_ana))
        ax2_TE.set_xticklabels(l2, rotation=45)
        ax2_TE.set_yticks(self.S_TE)

        # Resonance Angle vs. Analyte Refractive index

        # TM-Polarization plot
        figs, axs_TM = plt.subplots(dpi=dpi)
        axs_TM.plot(real(ind_ana), self.Resonance_Point_TM, '-s', linewidth=0.8, markersize=3, c='r')
        axs_TM.grid()
        axs_TM.set_title("Resonance Angle vs. Analyte Refractive index TM", fontsize=fontsize, loc='center',
                         color='b', pad='6')
        axs_TM.set_xticks(real(ind_ana))
        axs_TM.set_xticklabels(l2, rotation=45)
        axs_TM.set_yticks(self.Resonance_Point_TM)

        # TE-Polarization plot
        figsTE, axs_TE = plt.subplots(dpi=dpi)
        axs_TE.plot(real(ind_ana), self.Resonance_Point_TE, '-s', linewidth=0.8, markersize=3, c='r')
        axs_TE.grid()
        axs_TE.set_title("Resonance Angle vs. Analyte Refractive index TE", fontsize=fontsize,
                         loc='center', color='b', pad='6')

        axs_TE.set_xticks(real(ind_ana))
        axs_TE.set_xticklabels(l2, rotation=45)
        axs_TE.set_yticks(self.Resonance_Point_TE)

        # Gráfico da FOM

        # TM-Polarization plot
        fig3_FOM_TM, ax2_fom_TM = plt.subplots(dpi=dpi)
        ax2_fom_TM.plot(real(ind_ana), self.FOM_TM, '-o', linewidth=0.8, markersize=3, c='b')
        ax2_fom_TM.grid()
        ax2_fom_TM.set_title("FOM Polarização TM", fontsize=fontsize, loc='center', color='b', pad='6')
        ax2_fom_TM.set_xticks(real(ind_ana))
        ax2_fom_TM.set_xticklabels(l2, rotation=45)
        ax2_fom_TM.set_yticks(self.FOM_TM)

        # TE-Polarization plot
        fig3_FOM_TE, ax2_fom_TE = plt.subplots(dpi=dpi)
        ax2_fom_TE.plot(real(ind_ana), self.FOM_TE, '-o', linewidth=0.8, markersize=3, c='b')
        ax2_fom_TE.grid()
        ax2_fom_TE.set_title("FOM polarização TE", fontsize=fontsize, loc='center', color='b', pad='6')
        ax2_fom_TE.set_xticks(real(ind_ana))
        ax2_fom_TE.set_xticklabels(l2, rotation=45)
        ax2_fom_TE.set_yticks(self.FOM_TE)

        # Gráfico da FWHM

        # TM-Polarization plot
        fig_Fwhm_TM, ax2_fwhm_TM = plt.subplots(dpi=dpi)
        ax2_fwhm_TM.plot(real(ind_ana), self.Fwhm_TM, '-o', linewidth=0.8, markersize=3, c='b')
        ax2_fwhm_TM.grid()
        ax2_fwhm_TM.set_title("FWHM Polarização TM", fontsize=fontsize, loc='center', color='b', pad='6')
        ax2_fwhm_TM.set_xticks(real(ind_ana))
        ax2_fwhm_TM.set_xticklabels(l2, rotation=45)
        ax2_fwhm_TM.set_yticks(self.Fwhm_TM)

        # TE-Polarization plot
        fig_Fwhm_TE, ax2_fwhm_TE = plt.subplots(dpi=dpi)
        ax2_fwhm_TE.plot(real(ind_ana), self.Fwhm_TE, '-o', linewidth=0.8, markersize=3, c='b')
        ax2_fwhm_TE.grid()
        ax2_fwhm_TE.set_title("FWHM Polarização TE", fontsize=fontsize, loc='center', color='b', pad='6')
        ax2_fwhm_TE.set_xticks(real(ind_ana))
        ax2_fwhm_TE.set_xticklabels(l2, rotation=45)
        ax2_fwhm_TE.set_yticks(self.Fwhm_TE)

        plt.show()


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
