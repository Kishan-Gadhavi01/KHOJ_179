import os
import sys
import traci
import math
import random
import numpy as np
import time
start_time = time.time()



circle_data = [
    {'lat': 9838.68, 'lon': 36.53, 'radius': 100}, {'lat': 9821.84, 'lon': 43.47, 'radius': 100}, {'lat': 9801.89, 'lon': 42.05, 'radius': 100}, {'lat': 9775.52, 'lon': 32.46, 'radius': 100}, {'lat': 9756.75, 'lon': 37.68, 'radius': 100}, {'lat': 9768.89, 'lon': 57.67, 'radius': 100}, {'lat': 9800.04, 'lon': 66.37, 'radius': 100}, {'lat': 9812.83, 'lon': 73.33, 'radius': 100}, {'lat': 9815.94, 'lon': 81.12, 'radius': 100}, {'lat': 9803.15, 'lon': 91.26, 'radius': 100}, {'lat': 9779.74, 'lon': 91.53, 'radius': 100}, {'lat': 9763.55, 'lon': 81.08, 'radius': 100}, {'lat': 9740.28, 'lon': 83.37, 'radius': 100}, {'lat': 9723.67, 'lon': 110.13, 'radius': 100}, {'lat': 9711.06, 'lon': 112.63, 'radius': 100}, {'lat': 9664.0, 'lon': 121.46, 'radius': 100}, {'lat': 9658.44, 'lon': 138.73, 'radius': 100}, {'lat': 9645.94, 'lon': 134.97, 'radius': 100}, {'lat': 9634.74, 'lon': 120.23, 'radius': 100}, {'lat': 9634.51, 'lon': 100.46, 'radius': 100}, {'lat': 9613.53, 'lon': 99.66, 'radius': 100}, {'lat': 9604.94, 'lon': 99.11, 'radius': 100}, {'lat': 9601.94, 'lon': 75.77, 'radius': 100}, {'lat': 9576.13, 'lon': 78.21, 'radius': 100}, {'lat': 9555.19, 'lon': 98.53, 'radius': 100}, {'lat': 9562.69, 'lon': 117.04, 'radius': 100}, {'lat': 9580.23, 'lon': 136.63, 'radius': 100}, {'lat': 9580.89, 'lon': 144.91, 'radius': 100}, {'lat': 9571.53, 'lon': 145.02, 'radius': 100}, {'lat': 9543.1, 'lon': 157.67, 'radius': 100}, {'lat': 9530.92, 'lon': 191.49, 'radius': 100}, {'lat': 9540.42, 'lon': 208.86, 'radius': 100}, {'lat': 9564.78, 'lon': 218.21, 'radius': 100}, {'lat': 9578.86, 'lon': 215.56, 'radius': 100}, {'lat': 9584.12, 'lon': 221.24, 'radius': 100}, {'lat': 9568.35, 'lon': 261.38, 'radius': 100}, {'lat': 9568.56, 'lon': 278.77, 'radius': 100}, {'lat': 9568.83, 'lon': 301.94, 'radius': 100}, {'lat': 9593.57, 'lon': 306.1, 'radius': 100}, {'lat': 9602.16, 'lon': 291.84, 'radius': 100}, {'lat': 9604.58, 'lon': 264.52, 'radius': 100}, {'lat': 9605.11, 'lon': 246.93, 'radius': 100}, {'lat': 9611.14, 'lon': 247.37, 'radius': 100}, {'lat': 9628.3, 'lon': 259.25, 'radius': 100}, {'lat': 9635.92, 'lon': 276.04, 'radius': 100}, {'lat': 9652.59, 'lon': 265.41, 'radius': 100}, {'lat': 9678.68, 'lon': 264.29, 'radius': 100}, {'lat': 9688.99, 'lon': 272.15, 'radius': 100}, {'lat': 9689.74, 'lon': 278.74, 'radius': 100}, {'lat': 9683.19, 'lon': 300.82, 'radius': 100}, {'lat': 9669.38, 'lon': 332.73, 'radius': 100}, {'lat': 9663.57, 'lon': 355.98, 'radius': 100}, {'lat': 9679.51, 'lon': 364.26, 'radius': 100}, {'lat': 9696.19, 'lon': 352.26, 'radius': 100}, {'lat': 9718.2, 'lon': 335.86, 'radius': 100}, {'lat': 9745.83, 'lon': 333.92, 'radius': 100}, {'lat': 9757.55, 'lon': 343.78, 'radius': 100}, {'lat': 9764.28, 'lon': 358.37, 'radius': 100}, {'lat': 9768.19, 'lon': 385.15, 'radius': 100}, {'lat': 9786.19, 'lon': 407.86, 'radius': 100}, {'lat': 9789.98, 'lon': 428.96, 'radius': 100}, {'lat': 9808.16, 'lon': 451.24, 'radius': 100}, {'lat': 9827.27, 'lon': 459.52, 'radius': 100}, {'lat': 9838.78, 'lon': 460.33, 'radius': 100}, {'lat': 9859.99, 'lon': 458.32, 'radius': 100}, {'lat': 9865.94, 'lon': 458.75, 'radius': 100}, {'lat': 9860.85, 'lon': 475.33, 'radius': 100}, {'lat': 9869.9, 'lon': 492.81, 'radius': 100}, {'lat': 9889.39, 'lon': 512.64, 'radius': 100}, {'lat': 9904.02, 'lon': 521.36, 'radius': 100}, {'lat': 9933.07, 'lon': 484.13, 'radius': 100}, {'lat': 9944.87, 'lon': 464.86, 'radius': 100}, {'lat': 9949.82, 'lon': 466.03, 'radius': 100}, {'lat': 9946.71, 'lon': 483.41, 'radius': 100}, {'lat': 9966.79, 'lon': 498.28, 'radius': 100}, {'lat': 9993.3, 'lon': 533.1, 'radius': 100}, {'lat': 9989.5, 'lon': 546.52, 'radius': 100}, {'lat': 9983.98, 'lon': 570.66, 'radius': 100}, {'lat': 9998.06, 'lon': 583.41, 'radius': 100}, {'lat': 10007.13, 'lon': 629.95, 'radius': 100}, {'lat': 10002.71, 'lon': 658.39, 'radius': 100}, {'lat': 10040.88, 'lon': 675.92, 'radius': 100}, {'lat': 10046.71, 'lon': 703.23, 'radius': 100}, {'lat': 10070.2, 'lon': 703.82, 'radius': 100}, {'lat': 10070.98, 'lon': 714.18, 'radius': 100}, {'lat': 10068.06, 'lon': 726.39, 'radius': 100}, {'lat': 10054.47, 'lon': 735.05, 'radius': 100}, {'lat': 10040.45, 'lon': 759.61, 'radius': 100}, {'lat': 10055.88, 'lon': 772.45, 'radius': 100}, {'lat': 10086.06, 'lon': 778.85, 'radius': 100}, {'lat': 10110.89, 'lon': 754.48, 'radius': 100}, {'lat': 10116.64, 'lon': 754.41, 'radius': 100}, {'lat': 10125.05, 'lon': 764.81, 'radius': 100}, {'lat': 10135.63, 'lon': 796.81, 'radius': 100}, {'lat': 10132.52, 'lon': 830.88, 'radius': 100}, {'lat': 10135.12, 'lon': 846.83, 'radius': 100}, {'lat': 10126.37, 'lon': 853.69, 'radius': 100}, {'lat': 10114.52, 'lon': 853.14, 'radius': 100}, {'lat': 10103.31, 'lon': 833.94, 'radius': 100}, {'lat': 10081.57, 'lon': 820.21, 'radius': 100}, {'lat': 10045.5, 'lon': 812.21, 'radius': 100}, {'lat': 10076.61, 'lon': 958.84, 'radius': 100}, {'lat': 10085.85, 'lon': 1001.28, 'radius': 100}, {'lat': 10075.17, 'lon': 1098.7, 'radius': 100}, {'lat': 10083.08, 'lon': 1211.2, 'radius': 100}, {'lat': 10081.17, 'lon': 1238.34, 'radius': 100}, {'lat': 10089.22, 'lon': 1279.7, 'radius': 100}, {'lat': 10095.0, 'lon': 1312.66, 'radius': 100}, {'lat': 10112.19, 'lon': 1346.74, 'radius': 100}, {'lat': 10117.72, 'lon': 1383.0, 'radius': 100}, {'lat': 10111.86, 'lon': 1397.64, 'radius': 100}, {'lat': 10109.43, 'lon': 1429.18, 'radius': 100}, {'lat': 10139.87, 'lon': 1482.68, 'radius': 100}, {'lat': 10175.85, 'lon': 1534.14, 'radius': 100}, {'lat': 10242.56, 'lon': 1656.16, 'radius': 100}, {'lat': 10259.36, 'lon': 1698.59, 'radius': 100}, {'lat': 10245.88, 'lon': 1741.39, 'radius': 100}, {'lat': 10286.25, 'lon': 1753.64, 'radius': 100}, {'lat': 10289.86, 'lon': 1775.34, 'radius': 100}, {'lat': 10303.5, 'lon': 1790.47, 'radius': 100}, {'lat': 10341.44, 'lon': 1811.43, 'radius': 100}, {'lat': 10356.86, 'lon': 1819.63, 'radius': 100}, {'lat': 10353.46, 'lon': 1833.06, 'radius': 100}, {'lat': 10341.54, 'lon': 1849.27, 'radius': 100}, {'lat': 10308.45, 'lon': 1858.12, 'radius': 100}, {'lat': 10264.09, 'lon': 1866.76, 'radius': 100}, {'lat': 10242.34, 'lon': 1892.76, 'radius': 100}, {'lat': 10243.61, 'lon': 1917.06, 'radius': 100}, {'lat': 10255.46, 'lon': 1935.23, 'radius': 100}, {'lat': 10288.9, 'lon': 1951.82, 'radius': 100}, {'lat': 10343.82, 'lon': 1995.51, 'radius': 100}, {'lat': 10376.21, 'lon': 2000.63, 'radius': 100}, {'lat': 10495.77, 'lon': 1987.94, 'radius': 100}, {'lat': 10503.48, 'lon': 1998.13, 'radius': 100}, {'lat': 10491.48, 'lon': 2050.96, 'radius': 100}, {'lat': 10467.9, 'lon': 2070.53, 'radius': 100}, {'lat': 10459.79, 'lon': 2099.57, 'radius': 100}, {'lat': 10461.09, 'lon': 2113.24, 'radius': 100}, {'lat': 10499.39, 'lon': 2122.54, 'radius': 100}, {'lat': 10519.21, 'lon': 2112.38, 'radius': 100}, {'lat': 10526.17, 'lon': 2097.33, 'radius': 100}, {'lat': 10542.41, 'lon': 2102.77, 'radius': 100}, {'lat': 10568.71, 'lon': 2088.42, 'radius': 100}, {'lat': 10588.8, 'lon': 2095.96, 'radius': 100}, {'lat': 10603.56, 'lon': 2091.19, 'radius': 100}, {'lat': 10622.29, 'lon': 2090.97, 'radius': 100}, {'lat': 10632.72, 'lon': 2097.97, 'radius': 100}, {'lat': 10648.33, 'lon': 2113.12, 'radius': 100}, {'lat': 10661.67, 'lon': 2117.03, 'radius': 100}, {'lat': 10694.25, 'lon': 2107.86, 'radius': 100}, {'lat': 10705.7, 'lon': 2111.51, 'radius': 100}, {'lat': 10712.99, 'lon': 2119.38, 'radius': 100}, {'lat': 10729.72, 'lon': 2142.43, 'radius': 100}, {'lat': 10754.08, 'lon': 2200.55, 'radius': 100}, {'lat': 10767.1, 'lon': 2243.11, 'radius': 100}, {'lat': 10790.84, 'lon': 2272.12, 'radius': 100}, {'lat': 10788.71, 'lon': 2290.0, 'radius': 100}, {'lat': 10785.32, 'lon': 2307.5, 'radius': 100}, {'lat': 10780.14, 'lon': 2316.01, 'radius': 100}, {'lat': 10770.8, 'lon': 2321.33, 'radius': 100}, {'lat': 10756.77, 'lon': 2325.95, 'radius': 100}, {'lat': 10711.27, 'lon': 2355.9, 'radius': 100}, {'lat': 10699.38, 'lon': 2385.58, 'radius': 100}, {'lat': 10677.05, 'lon': 2394.78, 'radius': 100}, {'lat': 10673.54, 'lon': 2410.42, 'radius': 100}, {'lat': 10656.8, 'lon': 2424.91, 'radius': 100}, {'lat': 10625.87, 'lon': 2455.98, 'radius': 100}, {'lat': 10624.64, 'lon': 2514.7, 'radius': 100}, {'lat': 10622.74, 'lon': 2561.7, 'radius': 100}, {'lat': 10625.75, 'lon': 2589.15, 'radius': 100}, {'lat': 10627.66, 'lon': 2610.58, 'radius': 100}, {'lat': 10618.07, 'lon': 2622.8, 'radius': 100}, {'lat': 10606.21, 'lon': 2637.66, 'radius': 100}, {'lat': 10602.17, 'lon': 2657.85, 'radius': 100}, {'lat': 10621.36, 'lon': 2667.6, 'radius': 100}, {'lat': 10635.84, 'lon': 2676.17, 'radius': 100}, {'lat': 10637.19, 'lon': 2685.91, 'radius': 100}, {'lat': 10600.15, 'lon': 2701.84, 'radius': 100}, {'lat': 10577.82, 'lon': 2799.08, 'radius': 100}, {'lat': 10576.11, 'lon': 2820.51, 'radius': 100}, {'lat': 10591.75, 'lon': 2833.53, 'radius': 100}, {'lat': 10611.03, 'lon': 2824.17, 'radius': 100}, {'lat': 10630.92, 'lon': 2803.92, 'radius': 100}, {'lat': 10649.33, 'lon': 2798.56, 'radius': 100}, {'lat': 10656.45, 'lon': 2812.3, 'radius': 100}, {'lat': 10670.86, 'lon': 2825.38, 'radius': 100}, {'lat': 10711.65, 'lon': 2839.25, 'radius': 100}, {'lat': 10769.26, 'lon': 2854.15, 'radius': 100}, {'lat': 10788.71, 'lon': 2877.13, 'radius': 100}, {'lat': 10793.73, 'lon': 2893.84, 'radius': 100}, {'lat': 10784.51, 'lon': 2925.13, 'radius': 100}, {'lat': 10784.95, 'lon': 2962.06, 'radius': 100}, {'lat': 10801.08, 'lon': 2970.37, 'radius': 100}, {'lat': 10823.37, 'lon': 2968.34, 'radius': 100}, {'lat': 10840.63, 'lon': 2975.12, 'radius': 100}, {'lat': 10847.04, 'lon': 2994.28, 'radius': 100}, {'lat': 10837.34, 'lon': 3019.23, 'radius': 100}, {'lat': 10819.89, 'lon': 3044.65, 'radius': 100}, {'lat': 10776.17, 'lon': 3063.0, 'radius': 100}, {'lat': 10767.0, 'lon': 3093.45, 'radius': 100}, {'lat': 10770.12, 'lon': 3135.2, 'radius': 100}, {'lat': 10754.72, 'lon': 3161.68, 'radius': 100}, {'lat': 10735.21, 'lon': 3171.2, 'radius': 100}, {'lat': 10735.36, 'lon': 3184.32, 'radius': 100}, {'lat': 10748.18, 'lon': 3190.92, 'radius': 100}, {'lat': 10745.27, 'lon': 3203.73, 'radius': 100}, {'lat': 10725.6, 'lon': 3201.42, 'radius': 100}, {'lat': 10701.79, 'lon': 3247.77, 'radius': 100}, {'lat': 10679.13, 'lon': 3291.9, 'radius': 100}, {'lat': 10644.48, 'lon': 3352.02, 'radius': 100}, {'lat': 10638.48, 'lon': 3522.06, 'radius': 100}, {'lat': 10641.48, 'lon': 3557.95, 'radius': 100}, {'lat': 10643.22, 'lon': 3578.73, 'radius': 100}, {'lat': 10647.8, 'lon': 3633.53, 'radius': 100}, {'lat': 10659.24, 'lon': 3661.44, 'radius': 100}, {'lat': 10645.3, 'lon': 3689.09, 'radius': 100}, {'lat': 10652.25, 'lon': 3701.61, 'radius': 100}, {'lat': 10668.18, 'lon': 3780.32, 'radius': 100}, {'lat': 10690.95, 'lon': 3840.62, 'radius': 100}, {'lat': 10695.86, 'lon': 3881.95, 'radius': 100}, {'lat': 10706.08, 'lon': 3906.93, 'radius': 100}, {'lat': 10716.66, 'lon': 3931.53, 'radius': 100}, {'lat': 10713.66, 'lon': 3967.19, 'radius': 100}, {'lat': 10676.94, 'lon': 4072.07, 'radius': 100}, {'lat': 10663.34, 'lon': 4131.76, 'radius': 100}, {'lat': 10663.71, 'lon': 4163.27, 'radius': 100}, {'lat': 10650.36, 'lon': 4205.62, 'radius': 100}, {'lat': 10639.51, 'lon': 4224.09, 'radius': 100}, {'lat': 10644.4, 'lon': 4253.0, 'radius': 100}, {'lat': 10638.9, 'lon': 4315.98, 'radius': 100}, {'lat': 10659.29, 'lon': 4360.63, 'radius': 100}, {'lat': 10671.75, 'lon': 4385.55, 'radius': 100}, {'lat': 10676.38, 'lon': 4415.27, 'radius': 100}, {'lat': 10672.44, 'lon': 4448.94, 'radius': 100}, {'lat': 10663.88, 'lon': 4484.78, 'radius': 100}, {'lat': 10668.8, 'lon': 4508.7, 'radius': 100}, {'lat': 10691.36, 'lon': 4561.23, 'radius': 100}, {'lat': 10692.68, 'lon': 4590.78, 'radius': 100}, {'lat': 10701.67, 'lon': 4620.24, 'radius': 100}, {'lat': 7424.5, 'lon': 8143.52, 'radius': 100}, {'lat': 7448.65, 'lon': 8132.64, 'radius': 100}, {'lat': 7488.49, 'lon': 8110.0, 'radius': 100}, {'lat': 7514.8, 'lon': 8091.21, 'radius': 100}, {'lat': 7612.1, 'lon': 8034.76, 'radius': 100}, {'lat': 7647.61, 'lon': 8016.14, 'radius': 100}, {'lat': 7656.78, 'lon': 8014.39, 'radius': 100}, {'lat': 7669.84, 'lon': 8014.0, 'radius': 100}, {'lat': 7681.22, 'lon': 8002.62, 'radius': 100}, {'lat': 7690.38, 'lon': 7989.1, 'radius': 100}, {'lat': 7702.75, 'lon': 7982.58, 'radius': 100}, {'lat': 7715.9, 'lon': 7972.79, 'radius': 100},
    {'lat': 4863.57, 'lon': 3058.3, 'radius': 100}, {'lat': 4881.58, 'lon': 3063.11, 'radius': 100}, {'lat': 4897.5, 'lon': 3058.28, 'radius': 100}, {'lat': 4940.77, 'lon': 3051.47, 'radius': 100}, {'lat': 4975.73, 'lon': 3044.14, 'radius': 100}, {'lat': 5015.21, 'lon': 3042.72, 'radius': 100}, {'lat': 5055.04, 'lon': 3046.2, 'radius': 100}, {'lat': 5079.01, 'lon': 3070.65, 'radius': 100}, {'lat': 5097.23, 'lon': 3096.66, 'radius': 100}, {'lat': 5124.43, 'lon': 3139.41, 'radius': 100}, {'lat': 5136.84, 'lon': 3182.18, 'radius': 100}, {'lat': 5146.05, 'lon': 3233.62, 'radius': 100}, {'lat': 5169.62, 'lon': 3303.28, 'radius': 100}, {'lat': 5165.42, 'lon': 3345.35, 'radius': 100}, {'lat': 5164.85, 'lon': 3376.98, 'radius': 100}, {'lat': 5167.97, 'lon': 3405.55, 'radius': 100}, {'lat': 5173.05, 'lon': 3451.39, 'radius': 100}, {'lat': 5172.43, 'lon': 3476.61, 'radius': 100}, {'lat': 5164.38, 'lon': 3504.82, 'radius': 100}, {'lat': 5150.65, 'lon': 3537.77, 'radius': 100}, {'lat': 5128.9, 'lon': 3576.2, 'radius': 100}, {'lat': 5105.37, 'lon': 3629.48, 'radius': 100}, {'lat': 5090.45, 'lon': 3664.8, 'radius': 100}, {'lat': 5082.7, 'lon': 3688.32, 'radius': 100}, {'lat': 5076.58, 'lon': 3715.86, 'radius': 100}, {'lat': 5064.24, 'lon': 3852.6, 'radius': 100}, {'lat': 5059.11, 'lon': 3897.88, 'radius': 100}, {'lat': 5050.68, 'lon': 3932.87, 'radius': 100}, {'lat': 5078.65, 'lon': 3983.98, 'radius': 100}, {'lat': 5099.63, 'lon': 3999.4, 'radius': 100}, {'lat': 5134.11, 'lon': 4009.71, 'radius': 100}, {'lat': 5165.82, 'lon': 4010.99, 'radius': 100}, {'lat': 5188.92, 'lon': 3996.5, 'radius': 100}, {'lat': 5219.02, 'lon': 3958.7, 'radius': 100}, {'lat': 5256.37, 'lon': 3947.34, 'radius': 100}, {'lat': 5273.73, 'lon': 3947.73, 'radius': 100}, {'lat': 5284.34, 'lon': 3951.1, 'radius': 100}, {'lat': 5292.59, 'lon': 3956.06, 'radius': 100}, {'lat': 5303.61, 'lon': 3972.35, 'radius': 100}, {'lat': 5313.89, 'lon': 3997.04, 'radius': 100}, {'lat': 5321.74, 'lon': 4021.05, 'radius': 100}, {'lat': 5330.08, 'lon': 4050.82, 'radius': 100}, {'lat': 5338.68, 'lon': 4069.9, 'radius': 100}, {'lat': 5352.46, 'lon': 4100.21, 'radius': 100}, {'lat': 5395.67, 'lon': 4174.05, 'radius': 100}, {'lat': 5419.79, 'lon': 4216.0, 'radius': 100}, {'lat': 5426.83, 'lon': 4240.31, 'radius': 100}, {'lat': 5427.15, 'lon': 4266.33, 'radius': 100}, {'lat': 5426.94, 'lon': 4300.9, 'radius': 100}, {'lat': 5418.77, 'lon': 4318.59, 'radius': 100}, {'lat': 5404.15, 'lon': 4337.69, 'radius': 100}, {'lat': 5400.89, 'lon': 4352.08, 'radius': 100}, {'lat': 5400.45, 'lon': 4369.48, 'radius': 100}, {'lat': 5404.38, 'lon': 4395.06, 'radius': 100}, {'lat': 5420.33, 'lon': 4421.39, 'radius': 100}, {'lat': 5444.66, 'lon': 4486.26, 'radius': 100}, {'lat': 5468.36, 'lon': 4538.52, 'radius': 100}, {'lat': 5505.83, 'lon': 4588.43, 'radius': 100}, {'lat': 5541.92, 'lon': 4626.85, 'radius': 100}, {'lat': 5554.77, 'lon': 4655.21, 'radius': 100}, {'lat': 5556.2, 'lon': 4696.62, 'radius': 100}, {'lat': 5552.88, 'lon': 4738.95, 'radius': 100}, {'lat': 5558.94, 'lon': 4768.48, 'radius': 100}, {'lat': 5554.94, 'lon': 4801.22, 'radius': 100}, {'lat': 5552.57, 'lon': 4844.18, 'radius': 100}, {'lat': 5561.79, 'lon': 4883.99, 'radius': 100}, {'lat': 5594.09, 'lon': 4961.41, 'radius': 100}, {'lat': 5597.51, 'lon': 4989.76, 'radius': 100}, {'lat': 5592.9, 'lon': 5017.43, 'radius': 100}, {'lat': 5572.53, 'lon': 5075.23, 'radius': 100}, {'lat': 5563.67, 'lon': 5091.55, 'radius': 100}, {'lat': 5537.49, 'lon': 5113.2, 'radius': 100}, {'lat': 5504.92, 'lon': 5138.92, 'radius': 100}, {'lat': 5487.09, 'lon': 5169.51, 'radius': 100}, {'lat': 5455.35, 'lon': 5236.52, 'radius': 100}, {'lat': 5431.92, 'lon': 5306.05, 'radius': 100}, {'lat': 5425.59, 'lon': 5339.26, 'radius': 100}, {'lat': 5420.16, 'lon': 5374.59, 'radius': 100}, {'lat': 5433.92, 'lon': 5420.22, 'radius': 100}, {'lat': 5444.57, 'lon': 5466.82, 'radius': 100}, {'lat': 5450.62, 'lon': 5522.37, 'radius': 100}, {'lat': 5456.72, 'lon': 5603.92, 'radius': 100}, {'lat': 5471.74, 'lon': 5641.4, 'radius': 100}, {'lat': 5493.94, 'lon': 5680.52, 'radius': 100}, {'lat': 5520.56, 'lon': 5724.79, 'radius': 100}, {'lat': 5558.54, 'lon': 5784.79, 'radius': 100}, {'lat': 5653.22, 'lon': 5911.66, 'radius': 100}, {'lat': 5688.89, 'lon': 5956.54, 'radius': 100}, {'lat': 5713.18, 'lon': 5997.56, 'radius': 100}, {'lat': 5740.2, 'lon': 6034.01, 'radius': 100}, {'lat': 5766.62, 'lon': 6061.42, 'radius': 100}, {'lat': 5800.98, 'lon': 6083.3, 'radius': 100}, {'lat': 5845.69, 'lon': 6106.62, 'radius': 100}, {'lat': 5925.88, 'lon': 6144.41, 'radius': 100}, {'lat': 6212.63, 'lon': 6265.45, 'radius': 100}, {'lat': 6252.51, 'lon': 6294.61, 'radius': 100}, {'lat': 6292.02, 'lon': 6297.45, 'radius': 100}, {'lat': 6345.2, 'lon': 6299.71, 'radius': 100}, {'lat': 6377.61, 'lon': 6310.3, 'radius': 100}, {'lat': 6398.16, 'lon': 6332.74, 'radius': 100}, {'lat': 6414.16, 'lon': 6365.3, 'radius': 100}, {'lat': 6430.36, 'lon': 6427.73, 'radius': 100}, {'lat': 6441.21, 'lon': 6447.53, 'radius': 100}, {'lat': 6450.48, 'lon': 6467.72, 'radius': 100}, {'lat': 6464.48, 'lon': 6493.03, 'radius': 100}, {'lat': 6500.12, 'lon': 6577.38, 'radius': 100}, {'lat': 6521.87, 'lon': 6650.39, 'radius': 100}, {'lat': 6543.82, 'lon': 6722.77, 'radius': 100}, {'lat': 6550.18, 'lon': 6778.6, 'radius': 100}, {'lat': 6551.41, 'lon': 6825.79, 'radius': 100}, {'lat': 6550.86, 'lon': 6859.09, 'radius': 100}, {'lat': 6554.28, 'lon': 6877.93, 'radius': 100}, {'lat': 6566.35, 'lon': 6896.66, 'radius': 100}, {'lat': 6583.3, 'lon': 6918.61, 'radius': 100}, {'lat': 6628.65, 'lon': 6948.34, 'radius': 100}, {'lat': 6649.3, 'lon': 6960.83, 'radius': 100}, {'lat': 6660.2, 'lon': 6980.3, 'radius': 100}, {'lat': 6661.48, 'lon': 6999.62, 'radius': 100}, {'lat': 6647.15, 'lon': 7069.35, 'radius': 100}, {'lat': 6640.43, 'lon': 7105.87, 'radius': 100}, {'lat': 6641.37, 'lon': 7146.96, 'radius': 100}, {'lat': 6644.46, 'lon': 7180.9, 'radius': 100}, {'lat': 6653.14, 'lon': 7203.98, 'radius': 100}, {'lat': 6671.69, 'lon': 7232.25, 'radius': 100}, {'lat': 6684.59, 'lon': 7246.35, 'radius': 100}, {'lat': 6710.24, 'lon': 7276.58, 'radius': 100}, {'lat': 6761.76, 'lon': 7334.01, 'radius': 100}, {'lat': 6811.84, 'lon': 7383.5, 'radius': 100}, {'lat': 6839.43, 'lon': 7416.62, 'radius': 100}, {'lat': 6878.99, 'lon': 7486.73, 'radius': 100}, {'lat': 6945.03, 'lon': 7597.0, 'radius': 100}, {'lat': 6976.28, 'lon': 7635.34, 'radius': 100}, {'lat': 7005.42, 'lon': 7647.22, 'radius': 100}, {'lat': 7019.91, 'lon': 7669.5, 'radius': 100}, {'lat': 7030.66, 'lon': 7701.18, 'radius': 100}, {'lat': 7038.31, 'lon': 7755.02, 'radius': 100}, {'lat': 7037.48, 'lon': 7831.5, 'radius': 100}, {'lat': 7029.88, 'lon': 7850.65, 'radius': 100}, {'lat': 7023.78, 'lon': 7882.94, 'radius': 100}, {'lat': 7033.45, 'lon': 7903.45, 'radius': 100}, {'lat': 7049.48, 'lon': 7927.2, 'radius': 100}, {'lat': 7079.92, 'lon': 7940.51, 'radius': 100}, {'lat': 7125.37, 'lon': 7954.98, 'radius': 100}, {'lat': 7178.43, 'lon': 7971.85, 'radius': 100}, {'lat': 7205.4, 'lon': 7984.43, 'radius': 100}, {'lat': 7265.08, 'lon': 8033.7, 'radius': 100}, {'lat': 7337.34, 'lon': 8078.61, 'radius': 100}, {'lat': 7383.19, 'lon': 8112.82, 'radius': 100}, {'lat': 7402.51, 'lon': 8139.86, 'radius': 100}, {'lat': 7416.78, 'lon': 8158.14, 'radius': 100}, {'lat': 7425.03, 'lon': 8168.06, 'radius': 100}, {'lat': 7455.95, 'lon': 8227.75, 'radius': 100}, {'lat': 7500.86, 'lon': 8266.0, 'radius': 100}, {'lat': 7555.11, 'lon': 8280.59, 'radius': 100}, {'lat': 7608.12, 'lon': 8286.97, 'radius': 100}, {'lat': 7666.3, 'lon': 8307.21, 'radius': 100}, {'lat': 7724.56, 'lon': 8330.61, 'radius': 100}, {'lat': 7725.64, 'lon': 8331.3, 'radius': 100}, {'lat': 7772.67, 'lon': 8375.25, 'radius': 100}, {'lat': 7823.73, 'lon': 8455.05, 'radius': 100}, {'lat': 7852.41, 'lon': 8508.71, 'radius': 100}, {'lat': 7862.46, 'lon': 8550.06, 'radius': 100}, {'lat': 7863.53, 'lon': 8569.94, 'radius': 100}, {'lat': 7853.85, 'lon': 8590.63, 'radius': 100}, {'lat': 7826.55, 'lon': 8615.83, 'radius': 100}, {'lat': 7812.11, 'lon': 8625.65, 'radius': 100}, {'lat': 7787.35, 'lon': 8621.85, 'radius': 100}, {'lat': 7739.87, 'lon': 8600.69, 'radius': 100}, {'lat': 7673.2, 'lon': 8565.47, 'radius': 100}, {'lat': 7627.34, 'lon': 8542.02, 'radius': 100}, {'lat': 7562.65, 'lon': 8530.33, 'radius': 100}, {'lat': 7503.78, 'lon': 8531.92, 'radius': 100}, {'lat': 7443.98, 'lon': 8538.86, 'radius': 100}, {'lat': 7397.98, 'lon': 8557.43, 'radius': 100}, {'lat': 7380.04, 'lon': 8575.7, 'radius': 100}, {'lat': 7376.55, 'lon': 8603.3, 'radius': 100}, {'lat': 7391.86, 'lon': 8641.88, 'radius': 100}, {'lat': 7427.43, 'lon': 8666.63, 'radius': 100}, {'lat': 7450.22, 'lon': 8684.48, 'radius': 100}, {'lat': 7489.53, 'lon': 8735.61, 'radius': 100}, {'lat': 7551.96, 'lon': 8809.17, 'radius': 100}, {'lat': 7565.17, 'lon': 8847.06, 'radius': 100}, {'lat': 7561.34, 'lon': 8866.49, 'radius': 100}, {'lat': 7550.4, 'lon': 8880.83, 'radius': 100}, {'lat': 7521.96, 'lon': 8887.84, 'radius': 100}, {'lat': 7483.35, 'lon': 8889.18, 'radius': 100}, {'lat': 7432.64, 'lon': 8893.39, 'radius': 100}, {'lat': 7396.3, 'lon': 8924.86, 'radius': 100}, {'lat': 7381.7, 'lon': 8951.0, 'radius': 100}, {'lat': 7382.06, 'lon': 8981.06, 'radius': 100}, {'lat': 7411.41, 'lon': 9027.25, 'radius': 100}, {'lat': 7456.48, 'lon': 9102.23, 'radius': 100}, {'lat': 7475.7, 'lon': 9137.61, 'radius': 100}, {'lat': 7520.41, 'lon': 9179.24, 'radius': 100}, {'lat': 7551.37, 'lon': 9191.99, 'radius': 100}, {'lat': 7569.4, 'lon': 9211.98, 'radius': 100}, {'lat': 7581.56, 'lon': 9233.83, 'radius': 100}, {'lat': 7587.02, 'lon': 9265.69, 'radius': 100}, {'lat': 7569.22, 'lon': 9316.45, 'radius': 100}, {'lat': 7564.42, 'lon': 9366.64, 'radius': 100}, {'lat': 7569.42, 'lon': 9396.13, 'radius': 100}, {'lat': 7593.27, 'lon': 9423.89, 'radius': 100}, {'lat': 7624.58, 'lon': 9430.11, 'radius': 100}, {'lat': 7658.2, 'lon': 9419.46, 'radius': 100}, {'lat': 7678.46, 'lon': 9393.18, 'radius': 100}, {'lat': 7683.7, 'lon': 9373.15, 'radius': 100}, {'lat': 7693.92, 'lon': 9339.58, 'radius': 100}, {'lat': 7700.51, 'lon': 9311.99, 'radius': 100}, {'lat': 7719.49, 'lon': 9287.61, 'radius': 100}, {'lat': 7743.03, 'lon': 9278.41, 'radius': 100}, {'lat': 7771.94, 'lon': 9286.49, 'radius': 100}, {'lat': 7800.67, 'lon': 9297.01, 'radius': 100}, {'lat': 7814.29, 'lon': 9325.73, 'radius': 100}, {'lat': 7816.3, 'lon': 9354.11, 'radius': 100}, {'lat': 7797.71, 'lon': 9398.41, 'radius': 100}, {'lat': 7777.96, 'lon': 9445.2, 'radius': 100}, {'lat': 7764.32, 'lon': 9475.06, 'radius': 100}, {'lat': 7777.8, 'lon': 9499.26, 'radius': 100}, {'lat': 7797.07, 'lon': 9536.45, 'radius': 100}, {'lat': 7829.54, 'lon': 9567.1, 'radius': 100}, {'lat': 7847.03, 'lon': 9588.31, 'radius': 100}, {'lat': 7879.62, 'lon': 9664.06, 'radius': 100}, {'lat': 7963.65, 'lon': 9832.28, 'radius': 100}, {'lat': 7967.55, 'lon': 9866.77, 'radius': 100}, {'lat': 7974.73, 'lon': 9936.95, 'radius': 100}, {'lat': 8011.87, 'lon': 9960.34, 'radius': 100}, {'lat': 8052.93, 'lon': 9984.0, 'radius': 100}, {'lat': 8069.65, 'lon': 10014.6, 'radius': 100}, {'lat': 8096.65, 'lon': 10062.46, 'radius': 100}, {'lat': 8106.22, 'lon': 10086.32, 'radius': 100}, {'lat': 8135.16, 'lon': 10098.91, 'radius': 100}, {'lat': 8181.03, 'lon': 10116.69, 'radius': 100}, {'lat': 8222.22, 'lon': 10145.57, 'radius': 100}, {'lat': 8244.64, 'lon': 10172.36, 'radius': 100}, {'lat': 8248.2, 'lon': 10192.9, 'radius': 100}, {'lat': 8245.95, 'lon': 10215.46, 'radius': 100}, {'lat': 8236.56, 'lon': 10232.03, 'radius': 100}, {'lat': 8231.2, 'lon': 10252.54, 'radius': 100}, {'lat': 8237.12, 'lon': 10298.7, 'radius': 100}, {'lat': 8238.43, 'lon': 10335.08, 'radius': 100}, {'lat': 8231.8, 'lon': 10372.05, 'radius': 100}, {'lat': 8232.26, 'lon': 10410.46, 'radius': 100}, {'lat': 8239.08, 'lon': 10450.04, 'radius': 100}, {'lat': 8269.11, 'lon': 10496.75, 'radius': 100}, {'lat': 8360.48, 'lon': 10673.15, 'radius': 100}, {'lat': 8441.77, 'lon': 10821.53, 'radius': 100}, {'lat': 8486.43, 'lon': 10928.37, 'radius': 100}, {'lat': 8554.19, 'lon': 11034.23, 'radius': 100}, {'lat': 8644.09, 'lon': 11168.37, 'radius': 100}, {'lat': 8701.47, 'lon': 11292.94, 'radius': 100}, {'lat': 8746.54, 'lon': 11333.12, 'radius': 100}, {'lat': 8796.76, 'lon': 11342.48, 'radius': 100}, {'lat': 8857.24, 'lon': 11335.56, 'radius': 100}, {'lat': 8908.06, 'lon': 11332.34, 'radius': 100}, {'lat': 8955.96, 'lon': 11338.68, 'radius': 100}, {'lat': 9005.78, 'lon': 11359.7, 'radius': 100}, {'lat': 9061.28, 'lon': 11402.43, 'radius': 100}, {'lat': 9104.92, 'lon': 11459.46, 'radius': 100}, {'lat': 9132.96, 'lon': 11503.25, 'radius': 100}, {'lat': 9160.08, 'lon': 11531.39, 'radius': 100}
    
]

# Set the SUMO_HOME environment variable if not already done
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

# Define the paths for network and configuration files
script_directory = os.path.dirname(os.path.abspath(__file__))
conf = os.path.abspath(os.path.join(script_directory, "../osm.sumocfg"))



# VehicleManager class to handle vehicle operations like adding vehicles, getting/setting positions and speed


class DynamicCircle:
    def __init__(self, lat, lon, initial_radius, end_step=None):
        self.lat = lat
        self.lon = lon
        self.radius = initial_radius
        self.noise_amplitudes = [random.uniform(-98, 50) for _ in range(36)]  # Larger spikes for sharper edges
        self.spiky_points = self.create_spiky_circle_points()  # Create initial spiky points
        self.end_step = end_step  # Step at which updates will stop
        self.active = True  # Circle starts as active

    def update_radius(self, step):
        """
        Update the radius dynamically for irregular boundary expansion.
        Stops updating after `end_step` is reached.
        """
              
        self.radius += 1  # Expand the circle uniformly
        self.spiky_points = self.create_spiky_circle_points()  # Recalculate spiky points based on the updated radius

    def create_spiky_circle_points(self, num_points=36):
        """
        Generate the points for the circle's perimeter with spiky irregularities.
        :param num_points: Number of points to approximate the circle
        :return: List of (x, y) tuples representing the spiky circle's perimeter
        """
        spiky_points = []
        for angle in range(0, 360, int(360 / num_points)):
            radians = math.radians(angle)
            # Apply sharp noise to the radius for spiky boundary
            spiky_radius = self.radius + self.noise_amplitudes[angle // (360 // num_points)]
            x = self.lat + spiky_radius * math.cos(radians)
            y = self.lon + spiky_radius * math.sin(radians)
            spiky_points.append((x, y))
        return spiky_points


class VehicleManager:
    def __init__(self):
        pass

    # Adds a vehicle to the simulation with the given properties
    def add_vehicle(self, vehicle_id, vehicle_type, depart, from_edge, to_edge, depart_lane="best", speed=0):
        traci.vehicle.add(vehicle_id, routeID="", typeID=vehicle_type, depart=depart, departLane=depart_lane, departSpeed=speed)
        traci.vehicle.changeTarget(vehicle_id, to_edge)
        traci.vehicle.setRoute(vehicle_id, [from_edge, to_edge])

    # Gets the initial position (first edge) of a vehicle
    def get_initial_position(self, vehicle_id):
        return traci.vehicle.getRoute(vehicle_id)[0]

    # Sets the initial position (first edge) of a vehicle
    def set_initial_position(self, vehicle_id, from_edge):
        route = traci.vehicle.getRoute(vehicle_id)
        route[0] = from_edge
        traci.vehicle.setRoute(vehicle_id, route)

    # Gets the terminal position (last edge) of a vehicle
    def get_terminal_position(self, vehicle_id):
        return traci.vehicle.getRoute(vehicle_id)[-1]

    # Sets the terminal position (last edge) of a vehicle
    def set_terminal_position(self, vehicle_id, to_edge):
        route = traci.vehicle.getRoute(vehicle_id)
        route[-1] = to_edge
        traci.vehicle.setRoute(vehicle_id, route)

    # Gets the current speed of the vehicle
    def get_speed(self, vehicle_id):
        return traci.vehicle.getSpeed(vehicle_id)

    # Sets the speed of the vehicle
    def set_speed(self, vehicle_id, speed):
        traci.vehicle.setSpeed(vehicle_id, speed)



class DynamicFilledZone:
    def __init__(self, lat, lon, initial_radius, poly_id="zone", color=(255, 0, 0, 127), size_change=False, size_change_rate=0, start_step=0, end_step=None, max_radius=None):
        """
        Initializes the DynamicFilledZone.

        :param lat: Latitude of the center of the zone.
        :param lon: Longitude of the center of the zone.
        :param initial_radius: Initial radius of the zone.
        :param poly_id: ID of the polygon.
        :param color: Color of the polygon.
        :param size_change: Boolean indicating if the size should change over time.
        :param size_change_rate: Rate at which the size changes per step.
        :param start_step: Simulation step at which the zone appears.
        :param end_step: Simulation step at which the zone disappears (optional).
        :param max_radius: Maximum radius the zone can reach (optional).
        """
        self.lat = lat
        self.lon = lon
        self.initial_radius = initial_radius
        self.poly_id = poly_id
        self.color = color
        self.size_change = size_change
        self.size_change_rate = size_change_rate
        self.start_step = start_step
        self.end_step = end_step
        self.max_radius = max_radius
        self.x, self.y = traci.simulation.convertGeo(lon, lat, fromGeo=True)

    def update_zone(self, step):
        if step < self.start_step:
            return
        if self.end_step is not None and step > self.end_step:
            if self.poly_id in traci.polygon.getIDList():
                traci.polygon.remove(self.poly_id)
            return

        current_radius = self.initial_radius
        if self.size_change:
            current_radius += self.size_change_rate * (step - self.start_step)
            if self.max_radius is not None:
                current_radius = min(current_radius, self.max_radius)

        num_points = 72
        circle_points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            point_x = self.x + current_radius * math.cos(angle)
            point_y = self.y + current_radius * math.sin(angle)
            circle_points.append((point_x, point_y))

        if self.poly_id in traci.polygon.getIDList():
            traci.polygon.remove(self.poly_id)

        traci.polygon.add(
            polygonID=self.poly_id,
            shape=circle_points,
            color=self.color,
            fill=True,
            layer=1
        )

class WaterLoggingZone:
    def __init__(self, lat, lon, initial_radius, poly_id="water_zone", color=(0, 0, 255, 127), size_change=False, size_change_rate=0, start_step=0, end_step=None, max_radius=None):
        """
        Initializes the WaterLoggingZone.
        """
        self.lat = lat
        self.lon = lon
        self.initial_radius = initial_radius
        self.poly_id = poly_id
        self.color = color
        self.size_change = size_change
        self.size_change_rate = size_change_rate
        self.start_step = start_step
        self.end_step = end_step
        self.max_radius = max_radius
        self.x, self.y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
        self.perlin_offsets = [random.uniform(0, 100) for _ in range(360)]  # Perlin noise offsets for each angle

    def _perlin_noise(self, angle_index):
        """Generate smooth radius variation using Perlin noise."""
        return (np.sin(self.perlin_offsets[angle_index] + angle_index * 0.1) + 1) / 2  # Normalize to [0, 1]

    def update_zone(self, step):
        """Updates the zone and its size."""
        if step < self.start_step:
            return
        if self.end_step is not None and step > self.end_step:
            if self.poly_id in traci.polygon.getIDList():
                traci.polygon.remove(self.poly_id)
            return

        # Calculate current radius
        current_radius = self.initial_radius
        if self.size_change:
            current_radius += self.size_change_rate * (step - self.start_step)
            if self.max_radius is not None:
                current_radius = min(current_radius, self.max_radius)

        num_points = 52  # More points for a smoother circle
        polygon_points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            radius_variation = current_radius * (0.9 + 0.2 * self._perlin_noise(i))  # Controlled radius variation
            point_x = self.x + radius_variation * math.cos(angle)
            point_y = self.y + radius_variation * math.sin(angle)
            polygon_points.append((point_x, point_y))

        # Update or create the polygon
        if self.poly_id in traci.polygon.getIDList():
            traci.polygon.remove(self.poly_id)

        traci.polygon.add(
            polygonID=self.poly_id,
            shape=polygon_points,
            color=self.color,
            fill=True,
            layer=10
        )

# Function to create a filled red zone (for restricted areas) using geographic coordinates and a radius
def create_filled_red_zone(lat, lon, radius, poly_id="red_zone"):
    x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)

    # Generate points for the circle approximation
    num_points = 72  # Higher values create a smoother circle
    circle_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        point_x = x + radius * math.cos(angle)
        point_y = y + radius * math.sin(angle)
        circle_points.append((point_x, point_y))

    # Add the polygon to SUMO with a semi-transparent red fill
    traci.polygon.add(
        polygonID=poly_id,
        shape=circle_points,
        color=(255, 0, 0, 127),  # RGBA color (red)
        layer=1
    )
    print(f"Filled red zone created with center at ({lat}, {lon}) and radius {radius}.")

# Function to create a filled zone (can be used for safe zones or other designated areas)
def create_filled_zone(lat, lon, radius, poly_id="zone", color=(255, 0, 0, 127)):
    x, y = traci.simulation.convertGeo(lon, lat, fromGeo=True)

    # Generate points for the circle approximation
    num_points = 72  # Higher values create a smoother circle
    circle_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        point_x = x + radius * math.cos(angle)
        point_y = y + radius * math.sin(angle)
        circle_points.append((point_x, point_y))

    # Add the polygon to SUMO
    traci.polygon.add(
        polygonID=poly_id,
        shape=circle_points,
        color=color,  # Color can be customized
        fill=True,
        layer=1
    )
    print(f"Filled zone created with center at ({lat}, {lon}) and radius {radius}.")

# Dictionary to store the path (trail) of each vehicle
vehicle_trails = {}

# Function to update the trail of a single vehicle as a polygon
def update_vehicle_trail(veh_id, path, color):
    polygon_id = f"trail_{veh_id}"

    # Remove existing polygon if exists
    if polygon_id in traci.polygon.getIDList():
        traci.polygon.remove(polygon_id)

    # Add the new trail polygon
    traci.polygon.add(
        polygonID=polygon_id,
        shape=path,
        color=color,
        layer=10,  # High layer to ensure it's visible on top
        fill=False
    )

# Function to update the trails of all vehicles dynamically
def update_vehicle_trails():
    """
    Tracks and visualizes the vehicle trail (route) dynamically as polygons.
    """
    for veh_id in traci.vehicle.getIDList():
        position = traci.vehicle.getPosition(veh_id)  # Get current position (x, y)

        # Store positions in vehicle_trails dictionary
        if veh_id not in vehicle_trails:
            vehicle_trails[veh_id] = [position]
        else:
            vehicle_trails[veh_id].append(position)

        # Limit the trail length for performance optimization (e.g., 100 points max)
        if len(vehicle_trails[veh_id]) > 100:
            vehicle_trails[veh_id] = vehicle_trails[veh_id][-100:]

        # Add polygon for the trail (removes old one to update)
        polygon_id = f"trail_{veh_id}"
        if polygon_id in traci.polygon.getIDList():
            traci.polygon.remove(polygon_id)  # Remove previous polygon

        # Add the new trail polygon
        traci.polygon.add(
            polygonID=polygon_id,
            shape=vehicle_trails[veh_id],
            color=(0, 255, 0, 100),  # Green color with some transparency
            layer=1,
            fill=False
        )

def get_vehicle_counts_by_edge():
    # Get the list of all vehicles in the simulation
    vehicle_ids = traci.vehicle.getIDList() 
    
    # Create a dictionary to store vehicle counts per edge
    edge_vehicle_count = {}
    
    for vehicle_id in vehicle_ids:
        # Get the edge where the vehicle is currently located
        edge_id = traci.vehicle.getRoadID(vehicle_id)
        
        # Increment the count for that edge
        if edge_id not in edge_vehicle_count:
            edge_vehicle_count[edge_id] = 0
        edge_vehicle_count[edge_id] += 1
    
    return edge_vehicle_count
# Main simulation function
def run_simulation(config_file, duration=1000, red_zone_data=None, safe_zone_data=None, water_logging_data=None, vehicle_data_dict=None, circle_data=circle_data):
    sumoCmd = ["sumo", "-c", config_file]
    traci.start(sumoCmd)

    # circles = [
    #     DynamicCircle(circle['lat'], circle['lon'], circle['radius'], end_step=45)
    #     for i, circle in enumerate(circle_data) 
    #     if (i + 1) % 3 == 0
    # ]
    

    # dynamic_zones = []
    # if red_zone_data:
    #     for i, red_zone in enumerate(red_zone_data):
    #         print(f"Creating red zone {i+1} with parameters: {red_zone}")
    #         dynamic_zone = DynamicFilledZone(
    #             lat=red_zone['lat'],
    #             lon=red_zone['lon'],
    #             initial_radius=red_zone['radius'],
    #             size_change=False,  # enable size change if needed
    #             size_change_rate=1,  # change rate per step
    #             start_step=50,  # example start step
    #             # end_step=800,  # example end step
    #             max_radius=1000,  # example maximum radius
    #             poly_id=f"red_zone_{i+1}",
    #             color=(255, 0, 0, 127)  # Red
    #         )
    #         dynamic_zones.append(dynamic_zone)

    # if safe_zone_data:
    #     for i, ged_zone in enumerate(safe_zone_data):
    #         print(f"Creating ged zone {i+1} with parameters: {ged_zone}")
    #         dynamic_zone = DynamicFilledZone(
    #             lat=ged_zone['lat'],
    #             lon=ged_zone['lon'],
    #             initial_radius=ged_zone['radius'],
    #             size_change=False,  # enable size change if needed
    #             size_change_rate=1,  # change rate per step
    #             start_step=50,  # example start step
    #             # end_step=800,  # example end step
    #             # max_radius=1000,  # example maximum radius
    #             poly_id=f"ged_zone_{i+1}",
    #             color=(0, 255,0 , 200)  # Red
    #         )
    #         dynamic_zones.append(dynamic_zone)

    # for entry in water_logging_data:
    #     water_logging_zone = WaterLoggingZone(
    #         lat=entry['lat'],
    #         lon=entry['lon'],
    #         initial_radius=entry['radius'],
    #         size_change=True,
    #         size_change_rate=1,
    #         start_step=100,
    #         #end_step=800,
    #         max_radius=500,
    #         poly_id=f"water_logging_zone_{entry['id']}",  # Use the defined ID
    #         color=(0, 0, 255, 127)  # Blue
    #     )
    #     dynamic_zones.append(water_logging_zone)
        
    
    for step in range(duration):
        traci.simulationStep()
        

        # # if step==0:
        # #     junction_id = "cluster_319299724_3738686326_8650508223"
        # #     incoming_edges = traci.junction.getIncomingEdges(junction_id)  # Use sumolib or manual mapping
        #     #  slow= ["361899467#1","361899464#0","361899467#0", "757107596#1", "361899472", "921930233#1", "933225158#4", "361899480#3", "361899464#1","1316332627","370138510",]
        #     #  for edge in slow:                            
        #     #     traci.edge.setMaxSpeed(edge,1)
        # # if step==260:
        # #     for edge in incoming_edges:                              
        # #         traci.edge.setMaxSpeed(edge,50)  
        # if step < 50:
        #     for i, circle in enumerate(circles):
            
        #         circle.update_radius(step=step)

        #     # Get the updated spiky points after radius change
        #         circle_points = circle.spiky_points

        #         # Remove and re-add the polygon to update it (this is needed to simulate the radius change)
        #         polygon_id = f"circle_polygon_{i+1}"
        #         if polygon_id in traci.polygon.getIDList():
        #             traci.polygon.remove(polygon_id)  # Remove existing polygon

        #         # Add the updated polygon with spiky boundaries
        #         traci.polygon.add(
        #             polygon_id,
        #             circle_points,
        #             color=(0, 0, 255, 128),  # Blue color with transparency
        #             layer=1,
        #             fill=True
        #         )     
        # for dynamic_zone in dynamic_zones:
        #     dynamic_zone.update_zone(step)
            #update_vehicle_trails()
            #   update_vehicle_trails()
        if (step + 1) % 100 == 0:
                print(f"Simulation step: {step}")
                edge_vehicle_count = get_vehicle_counts_by_edge()
                
                #Print vehicle counts for each edge at the specified step
                print(f"Step {step + 1}")
                for edge_id, count in edge_vehicle_count.items():
                    print(f"  Edge {edge_id} has {count} vehicles")
                print(f"Simulation step: {step}")    
       

    

    traci.close()


def calculate_evacuation_time_in_seconds(first_departure_step, last_arrival_step, step_length):
    if first_departure_step > last_arrival_step:
        raise ValueError("Departure step cannot be greater than arrival step.")

    steps = last_arrival_step - first_departure_step
    evacuation_time_seconds = steps / step_length

    return evacuation_time_seconds



if __name__ == "__main__":
    # Define the red zone parameters (restricted areas)
    red_zones = [
        { # siddharth bungalows , sama
            'lat': 22.33779597622535,
            'lon': 73.20539458409085,
            'radius': 500  # Adjust the radius as needed
        },
        { # Sayaji Baug 
            'lat':22.309013089338773,
            'lon': 73.18794929300843,
            'radius': 500
        },
         { # Mangal Pandey Bridge
            'lat':22.327122462926578,
            'lon': 73.19733245781374,
            'radius': 500
        }

    
    ]

    # Define safe zone parameters (areas where vehicles are allowed to go freely)
    green_zone = [
        { 
            'lat':  22.3221852671073,
            'lon':  73.20951029691204,
            'radius': 400  # Adjust the radius as needed
        },
        { 
            'lat':22.333033258815544,
            'lon': 73.16366701437853,
            'radius': 400
        },
            
     { 
            'lat':22.314236, 
            'lon': 73.162264,
            'radius': 400
        }
            
    ]
    
    water_logging_data = [
    {
        'id': 1,  # Add unique ID
        'lat': 22.33779597622535,
        'lon': 73.19607730306171,
        'radius': 50
}
    ]  

    # Run the simulation with the defined red and safe zones
    run_simulation(conf, duration=2500, red_zone_data=red_zones, safe_zone_data=green_zone, circle_data=circle_data)
    evac_time = calculate_evacuation_time_in_seconds(0, 2422, 60)

    end_time = time.time()

    # Calculate and display the total runtime
    total_runtime = end_time - start_time
    print(f"Total runtime: {total_runtime:.2f} seconds. \n evacuation time {end_time} ")