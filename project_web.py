import streamlit as st
from cmath import log, pi
import requests

class Heat_Ex:
    def __init__(self):
        pass
        # self.T1 = 0                     # cold inlet temperature
        # self.T2 = 0                      # cold outlet temperature
        # self.T3 = 0                      # hot inlet temperature
        # self.T4 = 0                      # hot outlet temperature
        # self.rho = 0                     # density of fluid
        # self.mu = 0                      # dynamic viscosity of the fluid
        # self.L = 0                       # characteristic linear dimension
        # self.Cp = 0                      # heat capacity of the fluid
        # self.K = 0                       # thermal conductivity of the fluid
        # self.dh = 0                      # hydraulic diameter
        # self.mu_bf = 0                   # viscosity at bulk
        # self.mu_wf = 0                   # viscosity at feed
        # self.F_T = 0                     # correction factor
        # self.d_o = 0                     # outer diameter of the tube
        # self.d_i =0                      # inner diameter of the tube
        # self.k_w =0                      # resistance value for the tube wall
        # self.R_do = 0                    # shell side dirt factor
        # self.R_di = 0                    # tube side dirt factor
        # self.h0 = 0                      # Shell side heat transfer coefficient
        # self.h_i = 0                     # Tube side heat transfer coefficient
        # self.m = 0                       # mass flow rate on the tube side
        # self.N_P = 0                     # Number of tube passes

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
            image_url = "https://4.bp.blogspot.com/-6uia6oDQdAU/W4btj4qGkzI/AAAAAAAAEvg/C7PF3M-ip0w8OPOqjudNsMVDFquaTDjzQCLcBGAs/s1600/1.jpg"  # Replace with your image URL
            response = requests.get(image_url)
            if response.status_code == 200:

                st.image(response.content, caption="Laminar Flow :Laminar flow or streamline flow in pipes (or tubes) occurs when a fluid flows in parallel layers, with no disruption between the layers. At low velocities, the fluid tends to flow without lateral mixing, and adjacent layers slide past one another like playing cards.", use_column_width=True)
            else:
                st.write("Error loading image.")
        elif 1100 <= self.Re <= 2200:
            flow = "Transient Flow"
            image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6ZhIj400s2dMpsmkZo1kvY6pEP3351b_zfQ&usqp=CAU"  # Replace with your image URL
            response = requests.get(image_url)
            if response.status_code == 200:

                st.image(response.content, caption="Transient Flow : Transient flow, is flow where the flow velocity and pressure are changing with time. When changes occur to a fluid systems such as the starting or stopping of a pump, closing or opening a valve, or changes in tank levels, then transient flow conditions exist: otherwise the system is steady state.", use_column_width=True)
            else:
                st.write("Error loading image.")
        else:
            flow = "Turbulent Flow"
            image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmgh74xXky0WRWfD2o1H1VYPSJdxx0Van1_Q&usqp=CAU"  # Replace with your image URL
            response = requests.get(image_url)
            if response.status_code == 200:

                st.image(response.content, caption="Turbulent Flow : turbulent flow, type of fluid (gas or liquid) flow in which the fluid undergoes irregular fluctuations, or mixing, in contrast to laminar flow, in which the fluid moves in smooth paths or layers. In turbulent flow the speed of the fluid at a point is continuously undergoing changes in both magnitude and direction.", use_column_width=True)
            else:
                st.write("Error loading image.")
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
    st.title("Heat Exchanger calculator")
    st.write("Put the values and click calculate for calculation")    

    output=Heat_Ex
    col1, col2, col3 = st.columns(3)
    with col1:
        output.T1 = st.number_input('cold inlet temperature', value=0.0)
        output.T2 = st.number_input('cold outlet temperature', value=0.0)
        output.T3 = st.number_input('Hot inlet temperature', value=0.0)
        output.T4 = st.number_input('hot outlet temperature', value=0.0)
        output.rho = st.number_input('density of fluid', value=0.0)
        output.mu = st.number_input('dynamic viscosity of the fluid', value=0.0)
        output.N_P = st.number_input('Number of tube passes', value=0.0)
        output.m = st.number_input('mass flow rate on the tube side', value=0.0)
    with col2:
        output.L = st.number_input('characteristic linear dimension', value=0.0)
        output.Cp = st.number_input('heat capacity of the fluid', value=0.0)
        output.K = st.number_input('thermal conductivity of the fluid', value=0.0)
        output.dh = st.number_input('hydraulic diameter', value=0.0)
        output.mu_bf = st.number_input('viscosity at bulk', value=0.0)
        output.mu_wf = st.number_input('viscosity at feed', value=0.0)
        output.F_T = st.number_input('correction factor', value=0.0)
    with col3:
        output.d_o = st.number_input('outer diameter of the tube', value=0.0,format="%.5f")
        output.d_i = st.number_input('inner diameter of the tube', value=0.0,format="%.5f")
        output.R_do = st.number_input('shell side dirt factor', value=0.0,format="%.5f")
        output.R_di = st.number_input('tube side dirt factor', value=0.0,format="%.5f")
        output.k_w = st.number_input('resistance value for the tube wall', value=0.0)
        output.h0 = st.number_input('Shell side heat transfer coefficient', value=0.0)
        output.h_i = st.number_input('Tube side heat transfer coefficient', value=0.0)



    if st.button("Calculate"):
        calc=Heat_Ex()
        flow_type = calc.flowtype()
        U = calc.overall_heat_trsfr_coeff()
        A = calc.A_overall()

        st.write("Overall Heat Transfer Coefficient (U):", U)
        st.write("Overall Area of Heat Transfer (A):", A)
        st.write("Reynolds number (Re):",calc.Re)
        st.write("Prandtl Number (Pr):",calc.Pr)
        st.write("Flow Type:", flow_type)
        st.write("Number of tubes :",calc.num_of_tubes())
        st.write("Totle heat transfer (Q):",calc.heat_transfer())
        st.write("Fluid Velocity (V_T):",calc.Fluid_Velocity())
        image_url = "https://www.iqsdirectory.com/articles/heat-exchanger/shell-and-tube-heat-exchangers/shell-and-tube-heat-exchanger-system.jpg"  # Replace with your image URL
        response = requests.get(image_url)

    # Check if the request was successful
        if response.status_code == 200:
            # Display the image
            st.image(response.content, caption="Shell and tube heat exchanger", use_column_width=True)
        else:
            st.write("Error loading image.")


    st.sidebar.header("About")
    st.sidebar.subheader("Shell and tube heat exchanger calculator")
    st.sidebar.write("internship at Orio Shanghai Colours Pvt Ltd. \n\n Project under Mr. Krushan Patel \n\n Thank you for giving me the opportunity")


if __name__ == "__main__":
    main()
