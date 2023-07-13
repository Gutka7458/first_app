from cmath import log, pi
import json

class Heat_Ex:
    def __init__(self, filename):
        with open(filename) as file:
            data = json.load(file)
        
        self.T1 = data["T1"]                   # cold inlet temperature
        self.T2 = data["T2"]                   # cold outlet temperature
        self.T3 = data["T3"]                   # hot inlet temperature
        self.T4 = data["T4"]                   # hot outlet temperature
        self.rho = data["rho"]                 # density of fluid
        self.mu = data["mu"]                   # dynamic viscosity of the fluid
        self.L = data["L"]                     # characteristic linear dimension
        self.Cp = data["Cp"]                   # heat capacity of the fluid
        self.K = data["K"]                     # thermal conductivity of the fluid
        self.dh = data["dh"]                   # hydraulic diameter
        self.mu_bf = data["mu_bf"]             # viscosity at bulk
        self.mu_wf = data["mu_wf"]             # viscosity at feed
        self.F_T = data["F_T"]                 # correction factor
        self.d_o = data["d_o"]                 # outer diameter of the tube
        self.d_i = data["d_i"]                 # inner diameter of the tube
        self.k_w = data["k_w"]                 # resistance value for the tube wall
        self.R_do = data["R_do"]               # shell side dirt factor
        self.R_di = data["R_di"]               # tube side dirt factor
        self.h0 = data["h0"]                   # Shell side heat transfer coefficient
        self.h_i = data["h_i"]                 # Tube side heat transfer coefficient
        self.m = data["m"]                     # mass flow rate on the tube side
        self.N_P = data["N_P"]                 # Number of tube passes

    def overall_heat_trsfr_coeff(self):    # overall_heat_transfer_coefficient
        Ao = (pi * (self.d_o ** 2)) / 4
        Ai = (pi * (self.d_i ** 2)) / 4
        U = 1 / ((1 / self.h0) + self.R_do + ((Ao / Ai) * ((self.d_o - self.d_i) / (2 * self.k_w))) + (Ao / Ai) * (1 / self.h_i) + (Ao / Ai) * self.R_di)
        return U



    def flowtype(self):
        self.Re = (self.rho * self.Fluid_Velocity() * self.L) / self.mu
        self.Pr = (self.Cp * self.mu) / self.K
        if self.Re < 1100:
            flow = "Laminar Flow"
        elif 1100 <= self.Re <= 2200:
            flow = "Transient Flow"
        else:
            flow = "Turbulent Flow"
        return flow

    def Fluid_Velocity(self):
        V_T = (4 * self.m * self.N_P) / (self.num_of_tubes() * pi * self.rho * (self.d_i ** 2))
        return V_T

    def num_of_tubes(self):
        N_T = self.A_overall() / (self.d_o * pi * self.L)
        return N_T

    def A_overall(self):
        LMTD = ((self.T3 - self.T1) - (self.T4 - self.T2)) / ((log((self.T3 - self.T1) / (self.T4 - self.T2))).real)
        A_o = self.heat_transfer() / (self.overall_heat_trsfr_coeff() * LMTD)
        return A_o

    def heat_transfer(self):
        Q = self.m * self.Cp * (self.T2 - self.T1)
        return Q

def main():
    calc = Heat_Ex("input.json")
    flow_type = calc.flowtype()
    U = calc.overall_heat_trsfr_coeff()
    A = calc.A_overall()

    print("Overall Heat Transfer Coefficient (U):", U)
    print("Overall Area of Heat Transfer (A):", A)
    print("Reynolds number (Re):",calc.Re)
    print("Prandtl Number (Pr):",calc.Pr)
    print("Flow Type:", flow_type)
    print("Number of tubes :",calc.num_of_tubes())
    print("Totle heat transfer (Q):",calc.heat_transfer())
    print("Fluid Velocity (V_T):",calc.Fluid_Velocity())


if __name__ == "__main__":
    main()
