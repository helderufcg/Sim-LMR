# Sim- LMR 
## Description:
**_Sim-LMR_** is an **open source simulator** in development implemented in **Python** for the **study**, **analysis** and **design** of biosensors based on **Lossy Mode Resonance (LMR)**.

## Characteristics:
  * Open source;
  * Python language;
  * Supports N layers;
  * Kretschmann-Raether configuration;
  * Angular Interrogation Mode;

## Flowchart:

```mermaid
flowchart TD;

    start([Start])-->input1[/Select Kretschmann configuration/];
    input1[/Select Kretschmann configuration/]-->input2[/Select Angular Interrogation Mode/];
    input2-->input3[/"#149; Type of material: <p>#149; Layer thickness: <p>#149; Refractive Index:"/];
    input3-->input4{"Insert new layer?"};
    input4-->|Yes|input3[/"#149; Type of material: <p>#149; Layer thickness: <p>#149; Refractive Index:"/];
    input4-->|No|connection((A))
    connection2((A))-->input5[/"#149;Indicate the analyte layer<p>#149;Indicate the increment of the refractive<p>  index of the analyte (#Delta;ns)"/];
    input5-->input6[/"#149; Angular range (0#deg; - 90#deg;): <p>#149; Incident wavelength(#lambda;i): <p>#149; Shift angle(#Delta;#theta;):"/];
    input6-->input7["Calculation:<p> #149; Reflectance<p> #149; Sensibility<p> #149; Full Width at Half Maximum (FWHM)<p> #149; Quality Factor (QF)<p>"];
    input7-->display{{"Graphic and numerical results"}};
    display-->theend([End]);
    
    style start fill:	#4F4F4F,stroke:	#000000, stroke-width:2px,color:#FFFFFF
    style input1 fill:	#FFFFFF,stroke:	#000000, stroke-width:2px
    style input2 fill:	#FFFFFF,stroke:	#000000, stroke-width:2px
    style input3 fill:	#FFFFFF,stroke:	#000000, stroke-width:2px
    style input4 fill:	#FFFFFF,stroke:	#000000, stroke-width:2px
    style input5 fill:	#FFFFFF,stroke:	#000000, stroke-width:2px
    style input6 fill:	#FFFFFF,stroke:	#000000, stroke-width:2px
    style input7 fill:	#FFFFFF,stroke:	#000000, stroke-width:2px
    style display fill:	#FFFFFF,stroke:	#000000, stroke-width:2px
    style theend fill:	#4F4F4F,stroke:	#000000, stroke-width:2px,color:#FFFFFF
    
```

## Author
* **Adeilson de Sousa Leal** - Electrical Engineering Department - Federal University of Campina Grande - UFCG
* **LinkedIn**: https://www.linkedin.com/in/adeilson-de-sousa-leal-8a04271a1/
* **Contact**: adeilson.leal@ee.ufcg.edu.br
